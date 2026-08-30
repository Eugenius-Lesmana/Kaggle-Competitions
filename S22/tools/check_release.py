"""Fail closed if the S22 notebook or release packet is stale."""

from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from build_release import (
    MANIFEST,
    NOTEBOOK,
    RELEASE_ATTACK,
    RELEASE_ROOT,
    SOURCE_ATTACK,
    TOOLS_ROOT,
    digest_bytes,
    manifest_bytes,
    manifest_files,
    validate_source,
)

EXPECTED_RELEASE_FILES = {"attack.py", "submission.ipynb"}


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_manifest() -> dict[str, str]:
    records: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            fail(f"malformed manifest line: {line!r}")
        name = match.group(2)
        path = PurePosixPath(name)
        if path.is_absolute() or "\\" in name or ".." in path.parts:
            fail(f"unsafe manifest path: {name!r}")
        if name in records:
            fail(f"duplicate manifest entry: {name}")
        records[name] = match.group(1)
    return records


def check_notebook(attack_bytes: bytes) -> None:
    notebook_bytes = NOTEBOOK.read_bytes()
    notebook = json.loads(notebook_bytes.decode("utf-8"))
    if notebook.get("nbformat") != 4:
        fail("notebook must use nbformat 4")
    cells = notebook.get("cells", [])
    if len(cells) != 2:
        fail(f"expected exactly two notebook cells, found {len(cells)}")
    for index, cell in enumerate(cells, start=1):
        if cell.get("cell_type") != "code":
            fail(f"cell {index} is not code")
        if cell.get("execution_count") is not None or cell.get("outputs") != []:
            fail(f"cell {index} is not clean")
        compile("".join(cell.get("source", [])), f"submission.ipynb:cell-{index}", "exec")

    cell1 = "".join(cells[0].get("source", []))
    cell2 = "".join(cells[1].get("source", []))
    payload_match = re.search(r'ATTACK_B64 = "([A-Za-z0-9+/=]+)"', cell1)
    hash_match = re.search(r'ATTACK_SHA256 = "([0-9a-f]{64})"', cell1)
    if not payload_match or not hash_match:
        fail("cell 1 is missing the embedded attack bytes or hash")
    embedded = base64.b64decode(payload_match.group(1), validate=True)
    if embedded != attack_bytes or hash_match.group(1) != digest_bytes(attack_bytes):
        fail("notebook payload or hash differs from canonical attack.py")
    if "/kaggle/working/attack.py" not in cell1 or "submission.csv" not in cell1:
        fail("cell 1 is missing the attack write or placeholder CSV")
    if "ATTACK_MODE" in notebook_bytes.decode("utf-8"):
        fail("S22 must not bake an ATTACK_MODE override")
    gated_server = '''if os.getenv("KAGGLE_IS_COMPETITION_RERUN") is not None:
    import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv

    srv.JEDAttackInferenceServer().run()
'''
    if gated_server not in cell2:
        fail("cell 2 is missing the hosted-rerun gate or inference server")

    with tempfile.TemporaryDirectory() as temp_dir:
        fresh = Path(temp_dir) / "submission.ipynb"
        subprocess.run(
            [sys.executable, str(TOOLS_ROOT / "make_notebook.py"), str(SOURCE_ATTACK), str(fresh)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        if fresh.read_bytes() != notebook_bytes:
            fail("committed notebook differs from a fresh generator output")


def main() -> None:
    if not MANIFEST.is_file():
        fail("release manifest is missing; run build_release.py")
    canonical = SOURCE_ATTACK.read_bytes()
    validate_source(canonical)
    if RELEASE_ATTACK.read_bytes() != canonical:
        fail("release attack.py differs from canonical S22 attack.py")
    check_notebook(canonical)

    files = manifest_files()
    records = parse_manifest()
    if set(records) != {name for name, _path in files}:
        fail(f"manifest allowlist mismatch: {sorted(records)}")
    if MANIFEST.read_bytes() != manifest_bytes(files):
        fail("manifest is stale or not deterministically ordered")
    actual_files = {
        path.relative_to(RELEASE_ROOT).as_posix()
        for path in RELEASE_ROOT.rglob("*")
        if path.is_file() and path != MANIFEST
    }
    if actual_files != EXPECTED_RELEASE_FILES:
        fail(f"release directory contains unexpected files: {sorted(actual_files)}")

    print(
        f"PASS: S22 release attack.py {len(canonical)} bytes, sha256 {digest_bytes(canonical)}; "
        f"clean two-cell notebook reproducible; {len(records)} provenance records verified"
    )


if __name__ == "__main__":
    main()
