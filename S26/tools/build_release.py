"""Build the deterministic S26 upload packet from canonical attack.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S26_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S26_ROOT.parent
TOOLS_ROOT = S26_ROOT / "tools"
TESTS_ROOT = S26_ROOT / "tests"
RELEASE_ROOT = S26_ROOT / "RELEASE"
BASE_ATTACK = S14_ROOT / "S19" / "attack.py"
SOURCE_ATTACK = S26_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
BASE_SHA256 = "3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32"
REPLACEMENTS = (
    (
        b"SLOW_MULTIPOST_N = 1          # http.post endpoints planned per slow-row candidate\n",
        b"SLOW_MULTIPOST_N = 4          # http.post endpoints planned per slow-row candidate\n",
    ),
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def manifest_files() -> tuple[tuple[str, Path], ...]:
    tests = tuple(
        (path.relative_to(S14_ROOT).as_posix(), path)
        for path in sorted(TESTS_ROOT.rglob("*.py"))
        if "__pycache__" not in path.parts
    )
    if not tests:
        raise FileNotFoundError("S26 has no Python tests")
    return (
        ("S19/attack.py", BASE_ATTACK),
        ("S26/attack.py", SOURCE_ATTACK),
        ("S26/RELEASE/attack.py", RELEASE_ATTACK),
        ("S26/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S26/README.md", S26_ROOT / "README.md"),
        ("S26/EXPERIMENT.md", S26_ROOT / "EXPERIMENT.md"),
        ("S26/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S26/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S26/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
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
    expected = base_bytes
    for old, new in REPLACEMENTS:
        if expected.count(old) != 1:
            raise RuntimeError(f"S19 base no longer has the expected S26 transform: {old!r}")
        expected = expected.replace(old, new)
    if attack_bytes != expected:
        raise RuntimeError("S26 must equal S19 with only the pinned SLOW_MULTIPOST_N=4 transform")
    if attack_bytes.startswith(b"\xef\xbb\xbf") or b"\r\n" in attack_bytes:
        raise RuntimeError("canonical attack.py must be UTF-8 without BOM and use LF newlines")
    compile(attack_bytes, str(SOURCE_ATTACK), "exec")


def main() -> None:
    files = manifest_files()
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
    MANIFEST.write_bytes(manifest_bytes(files))
    print(
        f"S26 release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
