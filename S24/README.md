# S24: Eugene V19 with tail increased from 64 to 256

S24 is a single-lever experiment built from Eugene V19 (92.475). It changes
exactly one thing: `OVERPACK_TAIL_N` from 64 to 256.

## Rationale

V19's 64-candidate tail captured +4.320 over S18 (75% of the theoretical
+5.760 ceiling). This suggests significant unclaimed replay reserve: the
tail didn't saturate the available budget. Increasing the tail to 256
candidates gives 4× the tail capacity to absorb that reserve.

Target arithmetic from 92.475:

| Target | Gain needed | Additional successful singles (total across both rows) |
|---|---:|---:|
| 95 | +2.525 | 56 |
| 100 | +7.525 | 167 |
| 105 | +12.525 | 278 |
| 110 | +17.525 | 389 |

A 256-candidate tail has a theoretical ceiling of `256 * 2 * 0.045 = 23.04`
points (if all 256 candidates fire in both model rows). Realistic capture
is likely 50-75% of that, or roughly 11.5-17.3 points — enough to reach
104-110.

## Identity

- Eugene V19 reference: 26,453 bytes, SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`;
- S24 source SHA-256:
  `f8f240dbfedcd3b10bbfe56d44622e4f836407ed4ff93ea54c92ef13d32439e7`;
- Only change: `OVERPACK_TAIL_N` 64 → 256. All other V19 constants,
  templates, race, selection, fill, and packing are preserved exactly.

## Build and verify

From the repository root:

```sh
PYTHONPATH=sdk ./.venv/bin/python -B S24/tools/build_release.py
PYTHONPATH=sdk ./.venv/bin/python -B S24/tools/check_release.py
PYTHONPATH=sdk ./.venv/bin/python -B -m pytest S24/tests -q
PYTHONPATH=sdk ./.venv/bin/python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam','S24/attack.py']; main()"
```

Upload only `S24/RELEASE/submission.ipynb`. Do not hand-edit `RELEASE/`.
