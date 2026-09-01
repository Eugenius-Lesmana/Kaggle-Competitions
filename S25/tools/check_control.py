"""Verify that S25 is an exact-byte V19/S19 control packet."""

from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S19 = ROOT.parent / "S19"
ATTACK_SHA256 = "3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32"
NOTEBOOK_SHA256 = "cd65fe8e4b44cf99ad289974b590ccba2fe095b44e0b4e66ef4ffff9ac78c670"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    source = (ROOT / "attack.py").read_bytes()
    release = (ROOT / "RELEASE" / "attack.py").read_bytes()
    notebook_path = ROOT / "RELEASE" / "submission.ipynb"
    notebook_bytes = notebook_path.read_bytes()

    assert source == release == (S19 / "attack.py").read_bytes()
    assert notebook_bytes == (S19 / "RELEASE" / "submission.ipynb").read_bytes()
    assert digest(source) == ATTACK_SHA256
    assert digest(notebook_bytes) == NOTEBOOK_SHA256

    notebook = json.loads(notebook_bytes)
    cells = notebook.get("cells", [])
    assert notebook.get("nbformat") == 4 and len(cells) == 2
    assert all(
        cell.get("cell_type") == "code"
        and cell.get("execution_count") is None
        and cell.get("outputs") == []
        for cell in cells
    )
    first = "".join(cells[0].get("source", []))
    second = "".join(cells[1].get("source", []))
    match = re.search(r'ATTACK_B64 = "([A-Za-z0-9+/=]+)"', first)
    assert match and base64.b64decode(match.group(1), validate=True) == source
    assert "KAGGLE_IS_COMPETITION_RERUN" in second
    assert "JEDAttackInferenceServer().run()" in second

    expected_manifest = (
        f"{ATTACK_SHA256}  attack.py\n"
        f"{ATTACK_SHA256}  RELEASE/attack.py\n"
        f"{NOTEBOOK_SHA256}  RELEASE/submission.ipynb\n"
    )
    manifest = (ROOT / "RELEASE" / "MANIFEST.sha256").read_text(encoding="utf-8")
    assert manifest == expected_manifest
    print(
        "PASS: S25 is byte-identical to scored V19/S19; "
        f"attack {ATTACK_SHA256}; notebook {NOTEBOOK_SHA256}"
    )


if __name__ == "__main__":
    main()
