# S25: Eugene V19 with tail increased from 64 to 96

S25 is a single-lever experiment built from Eugene V19 (92.475). It changes
exactly one thing: `OVERPACK_TAIL_N` from 64 to 96.

## Rationale

V19's 64-candidate tail captured +4.320 over S18 (75% of the theoretical
+5.760 ceiling). S24's tail256 scored 90.540 — a regression from V19's 92.475 —
suggesting that a tail of 256 may overshoot the gateway's replay budget,
causing the scored prefix to be truncated.

A three-point quadratic through tail0 (V18), tail64 (V19), and tail256 (S24)
has an exploratory vertex near tail143 (predicted 94.38). Tail96 is a
conservative step in that direction: 1.5× the V19 tail but well short of the
4× that tail256 attempted.

Target arithmetic from 92.475:

| Target | Gain needed | Additional successful singles (total across both rows) |
|---|---:|---:|
| 94 | +1.525 | 34 |
| 96 | +3.525 | 78 |
| 98 | +5.525 | 123 |
| 100 | +7.525 | 167 |

A 96-candidate tail has a theoretical ceiling of `96 * 2 * 0.045 = 8.64`
points (if all 96 candidates fire in both model rows). Realistic capture
is likely 50-75% of that, or roughly 4.3-6.5 points.

## Identity

- Eugene V19 reference: 26,453 bytes, SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`;
- S25 source SHA-256:
  `4e6d31a580168729a74290befa60656e0df65b37e5cc49341db0f2cd30030671`;
- Only change: `OVERPACK_TAIL_N` 64 → 96. All other V19 constants,
  templates, race, selection, fill, and packing are preserved exactly.

## Build and verify

From the repository root:

```sh
PYTHONPATH=sdk ./.venv/bin/python -B S25/tools/build_release.py
PYTHONPATH=sdk ./.venv/bin/python -B S25/tools/check_release.py
PYTHONPATH=sdk ./.venv/bin/python -B -m pytest S25/tests -q
PYTHONPATH=sdk ./.venv/bin/python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam','S25/attack.py']; main()"
```

Upload only `S25/RELEASE/submission.ipynb`. Do not hand-edit `RELEASE/`.
