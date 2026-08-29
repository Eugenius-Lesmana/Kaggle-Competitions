"""Rebuild every S15 derived artifact from the frozen V12 donor."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

from extract_v12_source import ATTACK_SHA256, DEFAULT_DONOR, extract

S15_ROOT = Path(__file__).resolve().parents[1]
TOOLS_ROOT = S15_ROOT / "tools"
RELEASE_ROOT = S15_ROOT / "RELEASE"
SOURCE_ATTACK = S15_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
MANIFEST_FILES = {
    "ai-agent-security-v12.ipynb": DEFAULT_DONOR,
    "S15/attack.py": SOURCE_ATTACK,
    "S15/RELEASE/attack.py": RELEASE_ATTACK,
    "S15/RELEASE/submission.ipynb": NOTEBOOK,
    "S15/tests/test_release.py": S15_ROOT / "tests" / "test_release.py",
    "S15/README.md": S15_ROOT / "README.md",
    "S15/EXPERIMENT.md": S15_ROOT / "EXPERIMENT.md",
    "S15/tools/extract_v12_source.py": TOOLS_ROOT / "extract_v12_source.py",
    "S15/tools/make_notebook.py": TOOLS_ROOT / "make_notebook.py",
    "S15/tools/build_release.py": TOOLS_ROOT / "build_release.py",
    "S15/tools/check_release.py": TOOLS_ROOT / "check_release.py",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    RELEASE_ROOT.mkdir(parents=True, exist_ok=True)
    attack_bytes = extract(DEFAULT_DONOR)
    SOURCE_ATTACK.write_bytes(attack_bytes)
    RELEASE_ATTACK.write_bytes(attack_bytes)

    subprocess.run(
        [sys.executable, str(TOOLS_ROOT / "make_notebook.py"), str(SOURCE_ATTACK), str(NOTEBOOK)],
        check=True,
    )

    missing = [name for name, path in MANIFEST_FILES.items() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing release inputs: {missing}")
    lines = [f"{digest(path)}  {name}" for name, path in MANIFEST_FILES.items()]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    if digest(SOURCE_ATTACK) != ATTACK_SHA256:
        raise RuntimeError("canonical attack changed during build")
    print(f"S15 release built: exact V12 attack sha256 {ATTACK_SHA256}")
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
