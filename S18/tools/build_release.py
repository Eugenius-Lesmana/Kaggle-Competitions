"""Build the deterministic S18 upload packet from canonical attack.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S18_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S18_ROOT.parent
TOOLS_ROOT = S18_ROOT / "tools"
TESTS_ROOT = S18_ROOT / "tests"
RELEASE_ROOT = S18_ROOT / "RELEASE"
BASE_ATTACK = S14_ROOT / "S16" / "attack.py"
SOURCE_ATTACK = S18_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
BASE_SHA256 = "33fb04486b62745a617c3dffe86c47a1a8de0d6102518d3e299fa919c1ec20f2"
REPLACEMENTS = (
    (
        b"REPLAY_SAFE_FRAC = 0.97       # 07-18 replay-safe sizing rung: fill_r097_ea_b",
        b"REPLAY_SAFE_FRAC = 0.99       # S18: S16 frame race with public-proven replay packing",
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
        raise FileNotFoundError("S18 has no Python tests")
    return (
        ("S16/attack.py", BASE_ATTACK),
        ("S18/attack.py", SOURCE_ATTACK),
        ("S18/RELEASE/attack.py", RELEASE_ATTACK),
        ("S18/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S18/README.md", S18_ROOT / "README.md"),
        ("S18/EXPERIMENT.md", S18_ROOT / "EXPERIMENT.md"),
        ("S18/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S18/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S18/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
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
        raise RuntimeError("S16 base attack.py hash changed")
    expected = base_bytes
    for old, new in REPLACEMENTS:
        if expected.count(old) != 1:
            raise RuntimeError(f"S16 base no longer has the expected replay-setting line: {old!r}")
        expected = expected.replace(old, new)
    if attack_bytes != expected:
        raise RuntimeError("S18 must equal S16 with only the pinned replay-fraction replacement")
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
        f"S18 release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
