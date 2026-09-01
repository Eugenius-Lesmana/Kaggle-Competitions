# S25 / V25: exact V19 technical control

S25 is a byte-identical resubmission of the scored V19/S19 artifact (`92.475`).
It is the same-day control for V23 Tail128 and the friend's V24 Tail256, and a
competitive draw against hosted variance. It introduces no new attack behavior.

## Why this is the technical slot

V19 already contains the public-notebook mechanisms with positive transfer
evidence: fired-only live fill, direct three-frame selection, Harmony framing,
replay-cost sizing, `REPLAY_SAFE_FRAC=0.99`, unique score cells, and Tail64.
Best-first ordering and frame failover regressed in V20 and V22. Larger tails,
shallow probing, burst, and multipost remain experiments. Changing any of them
would make this unusable as today's attribution control.

## Pinned identity

- experiment ID: `S25_V19_EXACT_RESUBMIT_CONTROL`
- scored baseline: V19/S19, user-reported `92.475`
- attack SHA-256: `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`
- notebook SHA-256: `cd65fe8e4b44cf99ad289974b590ccba2fe095b44e0b4e66ef4ffff9ac78c670`
- upload file: `RELEASE/submission.ipynb`

The S25 attack, release attack, and notebook must remain byte-identical to S19.
Do not rebuild, rename notebook cells, or change metadata before upload.

## Verify

From `S14`:

```powershell
python -B .\S25\tools\check_control.py
python -B .\S19\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S19\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S25\attack.py']; main()"
```

## Result intake

Record the hosted score and per-model rows without modifying the submitted
notebook. Compare V23 and V24 against this same-day draw as well as the historical
V19 score. A single delta within the documented `4.015`-point identical-code
spread is not clean feature attribution.
