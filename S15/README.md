# S15 V12 Engine Control

S15 is the frozen V12 attack engine repackaged with the same hardened two-cell
wrapper used by the S14 release family. It is a calibration control after the
hosted S14 ladder regressed from S14B (`77.31`) through S14B-V15 (`75.06`), S14C
(`72.09`), and S14D (`44.935`). No S14 tournament, conservative repricing, or
new prompt arm is added.

Identity boundary:

- donor: `../ai-agent-security-v12.ipynb`, SHA-256
  `ed3e73cd85f94f9e4a88d82636a8d3ca6cc56efec5714839bd8566477329ad82`;
- canonical V12 attack source: `attack.py`, 25,995 bytes, SHA-256
  `3867ef52aa19811bd246149596cc8aa2623fee0abc08e93be1eaadaf27a45171`;
- `RELEASE/submission.ipynb` embeds those source bytes exactly and has no
  `ATTACK_MODE` override;
- this is source-exact under the common S14 wrapper, not a byte-exact copy of
  the historical four-cell donor notebook.

## Artifacts

- `attack.py` — canonical source extracted from the frozen donor;
- `RELEASE/attack.py` — upload-packet copy of the same bytes;
- `RELEASE/submission.ipynb` — generated upload notebook;
- `tests/test_release.py` — deterministic identity and behavior gates;
- `EXPERIMENT.md` — pre-registered interpretation and result-intake record;
- `RELEASE/MANIFEST.sha256` — donor, source, output, test, documentation, and
  build-tool hashes.

Upload only `RELEASE/submission.ipynb`. Do not hand-edit generated artifacts.

## Rebuild and verify

From `S14`:

```powershell
python -B .\S15\tools\build_release.py
python -B .\S15\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S15\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S15\attack.py']; main()"
.\verify_bundle.ps1 -Mode Check
```

Local gates do not execute the hosted GPT-OSS/Gemma rerun and do not establish a
leaderboard score. Record any hosted result in `EXPERIMENT.md` without changing
the scored notebook.
