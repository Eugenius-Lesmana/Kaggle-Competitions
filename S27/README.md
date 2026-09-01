# S27 / V27: calibrated hop-1 live validation

S27 is exact scored S19 plus one isolated operational mechanism: selected-frame
live-fill candidates run at one hop, while replay accounting conservatively
charges their estimated eight-hop cost.

The immutable base is `../S19/attack.py`, 26,453 bytes, SHA-256
`3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
S27 does not inherit S23 Tail128 or S26 multipost-4.

- canonical/release `attack.py`: 31,783 bytes, SHA-256
  `fff81d3f98b3112562617753418692236c46e71233a5933ec4937f81151e1236`
- upload notebook: `RELEASE/submission.ipynb`, SHA-256
  `742c993a4fab66c15f14489f79c619124ca3fa44e8b616fd67b259eae735d493`

## Frozen mechanism

- `PROBE_HOPS = 1`
- `REPLAY_COST_COEF = 2.0` as the offline minimum
- `REPLAY_COST_SAFETY_FACTOR = 1.25`
- `CALIBRATION_SAMPLES = 2`

The constants are frozen from the planning evidence: hop-0 marker-post success
was unchanged in all 12 paired one-hop/eight-hop observations across both
models, and one-hop validation was approximately `1.5-2x` faster. Each runtime
session still calibrates its selected frame. The warm-up and S19's six
interleaved race probes remain at the grader's full hop cap. The first two
selected-frame fill candidates run at one hop and provide session samples:

```text
observed_ratio = max(full_hop_latencies) / max(min(one_hop_latencies), LAT_FLOOR_S)
session_coef = max(REPLAY_COST_COEF,
                   observed_ratio * REPLAY_COST_SAFETY_FACTOR)
```

The calibration candidates are then retroactively charged at estimated
eight-hop cost. Later successful fill candidates run at one hop and are charged
`elapsed * session_coef`. A missing, failed, non-finite, non-positive, or
fire-mismatched calibration fails back to S19's full-hop fill; it never continues
at one hop with an uncalibrated coefficient.

## Held constant

S19's prompt bytes, three-frame race, two interleaved repetitions, winner metric,
fired-only retention, candidate order, replay-safe dual bounds, Tail64, caps,
deadlines, environment-fault behavior, forced-count mode, fallback, notebook
wrapper, and hosted-rerun gate remain frozen. No best-first ordering, frame
failover, burst, larger tail, multipost, model routing, or new prompt is included.

## Packaging

`tools/build_release.py` pins the S19 base hash, S27 canonical hash, and the exact
S19-to-S27 unified-diff hash, rejecting manual drift. It copies canonical bytes
to `RELEASE/attack.py`, generates the notebook, and writes the release manifest.
Do not hand-edit `RELEASE/`.

The generated notebook contains exactly two clean code cells. Cell 1 decodes the
canonical source byte-exact into `/kaggle/working/attack.py`, verifies its SHA-256,
and ensures a placeholder `submission.csv`. Cell 2 starts
`JEDAttackInferenceServer` only when `KAGGLE_IS_COMPETITION_RERUN` is present.
No `ATTACK_MODE` override is baked in.

## Build and verify

From `S14`:

```powershell
python -B .\S27\tools\build_release.py
python -B .\S27\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S27\tests -q
python -B -m pytest -p no:cacheprovider .\S19\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S27\attack.py']; main()"
.\verify_bundle.ps1 -Mode Check
```

The build and checker print the canonical source hash; `RELEASE/MANIFEST.sha256`
pins the base, canonical source, release copy, notebook, tests, documentation, and
tooling. Upload only `RELEASE/submission.ipynb` after explicit approval.
