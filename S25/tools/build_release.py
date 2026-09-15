"""Build the deterministic S25 upload packet from canonical attack.py.

S25 = Eugene V19 (92.475) with OVERPACK_TAIL_N increased from 64 to 96.
All other S18/V19 mechanisms are preserved exactly.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S25_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = S25_ROOT.parent
TOOLS_ROOT = S25_ROOT / "tools"
TESTS_ROOT = S25_ROOT / "tests"
RELEASE_ROOT = S25_ROOT / "RELEASE"
SOURCE_ATTACK = S25_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
V19_SHA256 = "3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32"
S25_SHA256 = "4e6d31a580168729a74290befa60656e0df65b37e5cc49341db0f2cd30030671"
V19_SIZE = 26_453
S25_SIZE = 26_446
REPLACEMENTS = (
    (
        b"OVERPACK_TAIL_N = 96          # S25: conservative tail increase (V19 had 64)\n",
        b"OVERPACK_TAIL_N = 64          # S19: bounded winner-frame tail after the S18 cutoff\n",
    ),
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def manifest_files() -> tuple[tuple[str, Path], ...]:
    tests = tuple(
        (path.relative_to(PROJECT_ROOT).as_posix(), path)
        for path in sorted(TESTS_ROOT.rglob("*.py"))
        if "__pycache__" not in path.parts
    )
    if not tests:
        raise FileNotFoundError("S25 has no Python tests")
    return (
        ("S25/attack.py", SOURCE_ATTACK),
        ("S25/RELEASE/attack.py", RELEASE_ATTACK),
        ("S25/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S25/README.md", S25_ROOT / "README.md"),
        ("S25/EXPERIMENT.md", S25_ROOT / "EXPERIMENT.md"),
        ("S25/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S25/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S25/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
        ("S25/RELEASE/kernel-metadata.json", RELEASE_ROOT / "kernel-metadata.json"),
    )


def manifest_bytes(files: tuple[tuple[str, Path], ...] | None = None) -> bytes:
    records = manifest_files() if files is None else files
    missing = [name for name, path in records if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing release inputs: {missing}")
    return ("".join(f"{digest(path)}  {name}\n" for name, path in records)).encode()


def validate_source(attack_bytes: bytes) -> None:
    if digest_bytes(attack_bytes) != S25_SHA256:
        raise RuntimeError("S25 attack.py hash changed")
    # Reverse the tail constant to recover V19
    control = attack_bytes
    for experimental, frozen in REPLACEMENTS:
        if control.count(experimental) != 1:
            raise RuntimeError(
                f"S25 no longer has the expected tail transform: {experimental!r}"
            )
        control = control.replace(experimental, frozen)
    if len(control) != V19_SIZE or digest_bytes(control) != V19_SHA256:
        raise RuntimeError(
            "S25 must equal frozen Eugene V19 with only the tail constant changed"
        )
    if attack_bytes.startswith(b"\xef\xbb\xbf") or b"\r\n" in attack_bytes:
        raise RuntimeError(
            "canonical attack.py must be UTF-8 without BOM and use LF newlines"
        )
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
    } - {"attack.py", "submission.ipynb", "kernel-metadata.json"}
    if extras:
        raise RuntimeError(f"release directory contains unexpected files: {sorted(extras)}")
    MANIFEST.write_bytes(manifest_bytes(files))
    print(
        f"S25 release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
