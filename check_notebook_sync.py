"""Verify submission.ipynb still embeds the current attack.py byte-exact.

Run before every submission. Exits non-zero on any mismatch.

Usage:  .venv/bin/python check_notebook_sync.py [submission.ipynb] [attack.py]
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NOTEBOOK_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "submission.ipynb"
ATTACK_PATH = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "attack.py"


def main() -> int:
    problems: list[str] = []

    if not NOTEBOOK_PATH.exists():
        print(f"FAIL: {NOTEBOOK_PATH} does not exist — run make_notebook.py")
        return 1

    nb = json.loads(NOTEBOOK_PATH.read_text())
    cells = nb.get("cells", [])
    if len(cells) < 2:
        problems.append(f"expected >=2 cells, found {len(cells)}")

    cell1 = "".join(cells[0].get("source", [])) if cells else ""
    cell2 = "".join(cells[1].get("source", [])) if len(cells) > 1 else ""

    m = re.search(r'ATTACK_B64 = "([A-Za-z0-9+/=]+)"', cell1)
    if not m:
        problems.append("cell 1 has no ATTACK_B64 literal")
        embedded = b""
    else:
        embedded = base64.b64decode(m.group(1))

    current = ATTACK_PATH.read_bytes()
    if hashlib.sha256(embedded).hexdigest() != hashlib.sha256(current).hexdigest():
        problems.append(
            f"embedded attack.py differs from {ATTACK_PATH} "
            f"(embedded {len(embedded)}B, current {len(current)}B) — re-run make_notebook.py"
        )

    # Load-bearing safety checks on the notebook shape.
    if "/kaggle/working/attack.py" not in cell1:
        problems.append("cell 1 does not write /kaggle/working/attack.py")
    if "submission.csv" not in cell1:
        problems.append("cell 1 does not ensure a placeholder submission.csv")
    if "KAGGLE_IS_COMPETITION_RERUN" not in cell2:
        problems.append("cell 2 is missing the rerun gate (would download 25GB interactively)")
    if "JEDAttackInferenceServer" not in cell2:
        problems.append("cell 2 does not serve JEDAttackInferenceServer")

    if problems:
        for p in problems:
            print("FAIL:", p)
        return 1

    print(f"OK: {NOTEBOOK_PATH.name} embeds attack.py byte-exact "
          f"({len(current)} bytes, sha256 {hashlib.sha256(current).hexdigest()[:16]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
