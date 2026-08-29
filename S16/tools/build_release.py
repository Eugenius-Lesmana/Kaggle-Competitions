"""Build the deterministic S16 upload packet from canonical attack.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S16_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S16_ROOT.parent
TOOLS_ROOT = S16_ROOT / "tools"
TESTS_ROOT = S16_ROOT / "tests"
RELEASE_ROOT = S16_ROOT / "RELEASE"
DONOR = S14_ROOT / "ai-agent-security-v12.ipynb"
SOURCE_ATTACK = S16_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
DONOR_SHA256 = "ed3e73cd85f94f9e4a88d82636a8d3ca6cc56efec5714839bd8566477329ad82"


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
        raise FileNotFoundError("S16 has no Python tests")
    return (
        ("ai-agent-security-v12.ipynb", DONOR),
        ("S16/attack.py", SOURCE_ATTACK),
        ("S16/RELEASE/attack.py", RELEASE_ATTACK),
        ("S16/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S16/README.md", S16_ROOT / "README.md"),
        ("S16/EXPERIMENT.md", S16_ROOT / "EXPERIMENT.md"),
        ("S16/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S16/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S16/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
    )


def manifest_bytes(files: tuple[tuple[str, Path], ...] | None = None) -> bytes:
    records = manifest_files() if files is None else files
    missing = [name for name, path in records if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing release inputs: {missing}")
    return ("".join(f"{digest(path)}  {name}\n" for name, path in records)).encode()


def validate_source(attack_bytes: bytes) -> None:
    if digest(DONOR) != DONOR_SHA256:
        raise RuntimeError("V12 donor notebook hash changed")
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
        f"S16 release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
