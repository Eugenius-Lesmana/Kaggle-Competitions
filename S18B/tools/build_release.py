"""Build the deterministic S18B upload packet from canonical attack.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S18B_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S18B_ROOT.parent
TOOLS_ROOT = S18B_ROOT / "tools"
TESTS_ROOT = S18B_ROOT / "tests"
RELEASE_ROOT = S18B_ROOT / "RELEASE"
BASE_ATTACK = S14_ROOT / "S16" / "attack.py"
SOURCE_ATTACK = S18B_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
BASE_SHA256 = "33fb04486b62745a617c3dffe86c47a1a8de0d6102518d3e299fa919c1ec20f2"
REPLACEMENTS = (
    (
        b"FRAME_RACE_REPS = 2\nFRAME_RACE_TEMPLATES = (TEMPLATE, FRAME_TEMPLATE, VERBOSE_FRAME_TEMPLATE)\n",
        b"FRAME_RACE_REPS = 2\nFRAME_RACE_TEMPLATES = (TEMPLATE, FRAME_TEMPLATE, VERBOSE_FRAME_TEMPLATE)\nOVERPACK_TAIL_N = 64          # untested tail only after a replay-safe cutoff\n",
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
        (path.relative_to(S14_ROOT).as_posix(), path)
        for path in sorted(TESTS_ROOT.rglob("*.py"))
        if "__pycache__" not in path.parts
    )
    if not tests:
        raise FileNotFoundError("S18B has no Python tests")
    return (
        ("S16/attack.py", BASE_ATTACK),
        ("S18B/attack.py", SOURCE_ATTACK),
        ("S18B/RELEASE/attack.py", RELEASE_ATTACK),
        ("S18B/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S18B/README.md", S18B_ROOT / "README.md"),
        ("S18B/EXPERIMENT.md", S18B_ROOT / "EXPERIMENT.md"),
        ("S18B/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S18B/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S18B/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
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
            raise RuntimeError(f"S16 base no longer has an expected S18B transform: {old!r}")
        expected = expected.replace(old, new)
    if attack_bytes != expected:
        raise RuntimeError("S18B must equal S16 with only the three pinned overpack transforms")
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
        f"S18B release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
