"""Build the deterministic S19 upload packet from canonical attack.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

S19_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S19_ROOT.parent
TOOLS_ROOT = S19_ROOT / "tools"
TESTS_ROOT = S19_ROOT / "tests"
RELEASE_ROOT = S19_ROOT / "RELEASE"
BASE_ATTACK = S14_ROOT / "S18" / "attack.py"
SOURCE_ATTACK = S19_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
BASE_SHA256 = "a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a"
REPLACEMENTS = (
    (
        b"FRAME_RACE_REPS = 2\nFRAME_RACE_TEMPLATES = (TEMPLATE, FRAME_TEMPLATE, VERBOSE_FRAME_TEMPLATE)\n",
        b"FRAME_RACE_REPS = 2\nFRAME_RACE_TEMPLATES = (TEMPLATE, FRAME_TEMPLATE, VERBOSE_FRAME_TEMPLATE)\nOVERPACK_TAIL_N = 64          # S19: bounded winner-frame tail after the S18 cutoff\n",
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
        raise FileNotFoundError("S19 has no Python tests")
    return (
        ("S18/attack.py", BASE_ATTACK),
        ("S19/attack.py", SOURCE_ATTACK),
        ("S19/RELEASE/attack.py", RELEASE_ATTACK),
        ("S19/RELEASE/submission.ipynb", NOTEBOOK),
        *tests,
        ("S19/README.md", S19_ROOT / "README.md"),
        ("S19/EXPERIMENT.md", S19_ROOT / "EXPERIMENT.md"),
        ("S19/S19_PLAN.md", S19_ROOT / "S19_PLAN.md"),
        ("S19/tools/make_notebook.py", TOOLS_ROOT / "make_notebook.py"),
        ("S19/tools/build_release.py", TOOLS_ROOT / "build_release.py"),
        ("S19/tools/check_release.py", TOOLS_ROOT / "check_release.py"),
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
        raise RuntimeError("S18 base attack.py hash changed")
    expected = base_bytes
    for old, new in REPLACEMENTS:
        if expected.count(old) != 1:
            raise RuntimeError(f"S18 base no longer has an expected S19 transform: {old!r}")
        expected = expected.replace(old, new)
    if attack_bytes != expected:
        raise RuntimeError("S19 must equal S18 with only the three pinned tail transforms")
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
        f"S19 release built: attack.py {len(attack_bytes)} bytes, "
        f"sha256 {digest_bytes(attack_bytes)}"
    )
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
