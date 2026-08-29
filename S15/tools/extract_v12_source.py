"""Extract the canonical V12 attack cell without changing one source byte."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

S15_ROOT = Path(__file__).resolve().parents[1]
S14_ROOT = S15_ROOT.parent
DEFAULT_DONOR = S14_ROOT / "ai-agent-security-v12.ipynb"
DEFAULT_OUTPUT = S15_ROOT / "attack.py"

DONOR_SHA256 = "ed3e73cd85f94f9e4a88d82636a8d3ca6cc56efec5714839bd8566477329ad82"
ATTACK_SHA256 = "3867ef52aa19811bd246149596cc8aa2623fee0abc08e93be1eaadaf27a45171"
WRITEFILE_MAGIC = "%%writefile /kaggle/working/attack.py\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract(donor: Path = DEFAULT_DONOR) -> bytes:
    raw = donor.read_bytes()
    actual_donor_sha = sha256(raw)
    if actual_donor_sha != DONOR_SHA256:
        raise ValueError(
            f"unexpected V12 notebook sha256: {actual_donor_sha}; expected {DONOR_SHA256}"
        )

    notebook = json.loads(raw.decode("utf-8"))
    matches: list[str] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        text = "".join(source) if isinstance(source, list) else str(source)
        if text.startswith(WRITEFILE_MAGIC):
            matches.append(text[len(WRITEFILE_MAGIC) :])

    if len(matches) != 1:
        raise ValueError(f"expected exactly one V12 attack cell, found {len(matches)}")

    attack_bytes = matches[0].encode("utf-8")
    actual_attack_sha = sha256(attack_bytes)
    if actual_attack_sha != ATTACK_SHA256:
        raise ValueError(
            f"unexpected extracted attack sha256: {actual_attack_sha}; expected {ATTACK_SHA256}"
        )
    return attack_bytes


def main() -> None:
    donor = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DONOR
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT
    attack_bytes = extract(donor)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(attack_bytes)
    print(f"wrote {output}: {len(attack_bytes)} bytes, sha256 {sha256(attack_bytes)}")


if __name__ == "__main__":
    main()
