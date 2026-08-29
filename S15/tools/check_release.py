"""Fail closed if S15 source, notebook, or release packaging is stale."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from extract_v12_source import ATTACK_SHA256, DEFAULT_DONOR, DONOR_SHA256, extract

S15_ROOT = Path(__file__).resolve().parents[1]
TOOLS_ROOT = S15_ROOT / "tools"
RELEASE_ROOT = S15_ROOT / "RELEASE"
SOURCE_ATTACK = S15_ROOT / "attack.py"
RELEASE_ATTACK = RELEASE_ROOT / "attack.py"
NOTEBOOK = RELEASE_ROOT / "submission.ipynb"
MANIFEST = RELEASE_ROOT / "MANIFEST.sha256"
EXPECTED_RELEASE_FILES = {"attack.py", "submission.ipynb"}
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


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_manifest() -> dict[str, str]:
    records: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            fail(f"malformed manifest line: {line!r}")
        name = match.group(2)
        manifest_path = PurePosixPath(name)
        if manifest_path.is_absolute() or "\\" in name or ".." in manifest_path.parts:
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

    cell1 = "".join(cells[0].get("source", []))
    cell2 = "".join(cells[1].get("source", []))
    match = re.search(r'ATTACK_B64 = "([A-Za-z0-9+/=]+)"', cell1)
    if not match:
        fail("cell 1 has no embedded attack")
    embedded = base64.b64decode(match.group(1), validate=True)
    if embedded != attack_bytes:
        fail("notebook payload differs from canonical attack.py")
    if "/kaggle/working/attack.py" not in cell1 or "submission.csv" not in cell1:
        fail("cell 1 is missing the attack write or placeholder CSV")
    if "ATTACK_MODE" in cell1:
        fail("exact V12 control must not bake an ATTACK_MODE override")
    if "KAGGLE_IS_COMPETITION_RERUN" not in cell2 or "JEDAttackInferenceServer" not in cell2:
        fail("cell 2 is missing the hosted-rerun gate or inference server")

    with tempfile.TemporaryDirectory() as temp_dir:
        fresh = Path(temp_dir) / "submission.ipynb"
        subprocess.run(
            [
                sys.executable,
                str(TOOLS_ROOT / "make_notebook.py"),
                str(SOURCE_ATTACK),
                str(fresh),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        if fresh.read_bytes() != notebook_bytes:
            fail("committed notebook differs from a fresh generator output")


def main() -> None:
    if digest(DEFAULT_DONOR) != DONOR_SHA256:
        fail("V12 donor notebook hash changed")
    expected = extract(DEFAULT_DONOR)
    canonical = SOURCE_ATTACK.read_bytes()
    released = RELEASE_ATTACK.read_bytes()
    if canonical != expected or released != expected:
        fail("canonical or release attack.py is not the exact V12 donor source")
    if digest_bytes(canonical) != ATTACK_SHA256:
        fail("unexpected canonical attack hash")
    if canonical.startswith(b"\xef\xbb\xbf") or b"\r\n" in canonical:
        fail("canonical attack.py encoding/newlines changed")

    check_notebook(canonical)

    records = parse_manifest()
    if set(records) != set(MANIFEST_FILES):
        fail(f"manifest allowlist mismatch: {sorted(records)}")
    actual_files = {
        path.relative_to(RELEASE_ROOT).as_posix()
        for path in RELEASE_ROOT.rglob("*")
        if path.is_file() and path != MANIFEST
    }
    if actual_files != EXPECTED_RELEASE_FILES:
        fail(f"release directory contains unexpected files: {sorted(actual_files)}")
    for name, expected_hash in records.items():
        if digest(MANIFEST_FILES[name]) != expected_hash:
            fail(f"manifest hash mismatch: {name}")

    print(
        "PASS: S15 release is an exact V12 control; "
        f"attack.py {len(canonical)} bytes, sha256 {ATTACK_SHA256}; "
        f"notebook freshly reproducible; {len(records)} provenance records verified"
    )


if __name__ == "__main__":
    main()
