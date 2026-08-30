"""Build the deterministic conditional S23 packet from canonical attack.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S23_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = S23_ROOT.parent
TOOLS_ROOT = S23_ROOT / "tools"
TESTS_ROOT = S23_ROOT / "tests"
RELEASE_ROOT = S23_ROOT / "RELEASE"
BASE_ATTACK = PROJECT_ROOT / "S22" / "attack.py"
SOURCE_ATTACK = S23_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
BASE_SHA256 = "c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb"
REPLACEMENTS = (
    (
        b")\n# Hop-saturation burst",
        b")\nOVERPACK_TAIL_N = 64          # S23: bounded winner-frame tail after the replay cutoff\n# Hop-saturation burst",
    ),
    (
        b'        cap = int(self.config.get("hard_n_cap", HARD_N_CAP))',
        b'        cap = min(int(self.config.get("hard_n_cap", HARD_N_CAP)), HARD_N_CAP)',
    ),
    (
        b'''                ):
                    break
            else:
''',
        b'''                ):
                    if (
                        race_on
                        and race_index == len(race_plan)
                        and race_fires[chosen_template] > 0
                        and cands
                    ):
                        tail_n = min(OVERPACK_TAIL_N, cap - len(cands))
                        cands.extend(
                            AttackCandidate.from_messages(
                                (_msg(candidate_index, chosen_template),)
                            )
                            for candidate_index in range(idx, idx + tail_n)
                        )
                    break
            else:
''',
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
        raise FileNotFoundError("S23 has no Python tests")
    return (
        ("S22/attack.py", BASE_ATTACK),
        ("S23/attack.py", SOURCE_ATTACK),
        ("S23/RELEASE/attack.py", RELEASE_ATTACK),
        ("S23/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S23/README.md", S23_ROOT / "README.md"),
        ("S23/EXPERIMENT.md", S23_ROOT / "EXPERIMENT.md"),
        ("S23/CONDITIONAL.md", S23_ROOT / "CONDITIONAL.md"),
        ("S23/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S23/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S23/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
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
        raise RuntimeError("S22 base attack.py hash changed")
    expected = base_bytes
    for old, new in REPLACEMENTS:
        if expected.count(old) != 1:
            raise RuntimeError(f"S22 base no longer has an expected S23 transform: {old!r}")
        expected = expected.replace(old, new)
    if attack_bytes != expected:
        raise RuntimeError("S23 must equal S22 with only the three pinned tail transforms")
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
        f"S23 conditional release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
