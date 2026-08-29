# S14B-V15 release candidate

The proven S14B release with one isolated seventh arm: the scored V15 notebook's
rendered hybrid prompt, including its final `<|end|>` token. All S14B safety
constants and release repairs remain unchanged.

## Key Features & Safety Repairs
- **7-arm guarded tournament**: Compares 5 public controls + 2 challengers. A challenger is promoted to fill only if it achieves $\ge 10\%$ effective-cost advantage and $\ge 2$ positive samples.
- **Replay phase**: Verified `8750s` phase budget with `REPLAY_SAFE = 0.975` (`8531.25s` cap).
- **Latency repricing**: Every confirmed candidate repriced at the latest observed worst latency for its shape upon packing and latency jumps.
- **Outer step limit**: `max_steps` enforced across warmup, tournament, and fill attempts.

## Artifacts
- `attack.py` — canonical source;
- `submission.ipynb` — generated notebook embedding `attack.py` byte-exact;
- `tests/test_release.py` — deterministic behavioral, promotion, and failure-reproduction test suite;
- `MANIFEST.sha256` — checksum manifest.

## Verification Runbook
From `S14`:
```powershell
python ".\Friend's submission\S15\make_notebook.py" ".\S14B_V15_RELEASE\attack.py" ".\S14B_V15_RELEASE\submission.ipynb" S14B_V15_RELEASE
python ".\Friend's submission\S15\check_notebook_sync.py" ".\S14B_V15_RELEASE\submission.ipynb" ".\S14B_V15_RELEASE\attack.py"
python -B -m pytest -p no:cacheprovider ".\S14B_V15_RELEASE\tests" -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S14B_V15_RELEASE\attack.py']; main()"
```
