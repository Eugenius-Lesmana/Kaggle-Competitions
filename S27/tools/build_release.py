"""Build the deterministic S27 upload packet from canonical attack.py."""

from __future__ import annotations

import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

S27_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S27_ROOT.parent
TOOLS_ROOT = S27_ROOT / "tools"
TESTS_ROOT = S27_ROOT / "tests"
RELEASE_ROOT = S27_ROOT / "RELEASE"
BASE_ATTACK = S14_ROOT / "S19" / "attack.py"
SOURCE_ATTACK = S27_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
BASE_SHA256 = "3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32"
ATTACK_SHA256 = "fff81d3f98b3112562617753418692236c46e71233a5933ec4937f81151e1236"
DIFF_SHA256 = "e5d4128f131be05e9e5d17604f25ca2b95c18b3a6249074af3d6ed784890c9d5"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def source_diff(base_bytes: bytes, attack_bytes: bytes) -> bytes:
    base_lines = base_bytes.decode("utf-8").splitlines(keepends=True)
    attack_lines = attack_bytes.decode("utf-8").splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            base_lines,
            attack_lines,
            fromfile="S19/attack.py",
            tofile="S27/attack.py",
            n=3,
            lineterm="\n",
        )
    ).encode("utf-8")


def manifest_files() -> tuple[tuple[str, Path], ...]:
    tests = tuple(
        (path.relative_to(S14_ROOT).as_posix(), path)
        for path in sorted(TESTS_ROOT.rglob("*.py"))
        if "__pycache__" not in path.parts
    )
    if not tests:
        raise FileNotFoundError("S27 has no Python tests")
    return (
        ("S19/attack.py", BASE_ATTACK),
        ("S27/attack.py", SOURCE_ATTACK),
        ("S27/RELEASE/attack.py", RELEASE_ATTACK),
        ("S27/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S27/README.md", S27_ROOT / "README.md"),
        ("S27/EXPERIMENT.md", S27_ROOT / "EXPERIMENT.md"),
        ("S27/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S27/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S27/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
    )


def manifest_bytes(files: tuple[tuple[str, Path], ...] | None = None) -> bytes:
    records = manifest_files() if files is None else files
    missing = [name for name, path in records if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing release inputs: {missing}")
    return ("".join(f"{digest(path)}  {name}\n" for name, path in records)).encode()


def validate_source(attack_bytes: bytes) -> None:
    base_bytes = BASE_ATTACK.read_bytes()
    if digest_bytes(base_bytes) != BASE_SHA256:
        raise RuntimeError("S19 base attack.py hash changed")
    if digest_bytes(attack_bytes) != ATTACK_SHA256:
        raise RuntimeError("S27 canonical attack.py hash changed")
    if digest_bytes(source_diff(base_bytes, attack_bytes)) != DIFF_SHA256:
        raise RuntimeError("S19-to-S27 source transform changed")
    if attack_bytes.startswith(b"\xef\xbb\xbf") or b"\r\n" in attack_bytes:
        raise RuntimeError("canonical attack.py must be UTF-8 without BOM and use LF newlines")
    compile(attack_bytes, str(SOURCE_ATTACK), "exec")


def main() -> None:
    attack_bytes = SOURCE_ATTACK.read_bytes()
    validate_source(attack_bytes)
    RELEASE_ROOT.mkdir(parents=True, exist_ok=True)
    RELEASE_ATTACK.write_bytes(attack_bytes)
    subprocess.run(
        [sys.executable, str(TOOLS_ROOT / "make_notebook.py"), str(RELEASE_ATTACK), str(NOTEBOOK)],
        check=True,
    )
    if SOURCE_ATTACK.read_bytes() != attack_bytes:
        raise RuntimeError("canonical attack.py changed during build")
    extras = {
        path.relative_to(RELEASE_ROOT).as_posix()
        for path in RELEASE_ROOT.rglob("*")
        if path.is_file() and path != MANIFEST
    } - {"attack.py", "submission.ipynb"}
    if extras:
        raise RuntimeError(f"release directory contains unexpected files: {sorted(extras)}")
    files = manifest_files()
    MANIFEST.write_bytes(manifest_bytes(files))
    print(
        f"S27 release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
