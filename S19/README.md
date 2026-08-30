# S19: S18 with a Bounded Replay-Cutoff Tail

S19 preserves the scored S18 attack prefix and adds one mechanism: after the
normal S18 replay-safe stop fires, append at most 64 fresh single-post candidates
in the selected winning frame.

## Identity

- hosted anchor: S18, user-reported score `88.155`;
- base: `../S18/attack.py`, 25,746 bytes, SHA-256
  `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`;
- canonical S19 source: `attack.py`, 26,453 bytes, SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`;
- experiment ID: `S19_S18_R099_REPLAY_CUTOFF_TAIL64`.

S19 keeps S18's three-frame race, two probes per frame, winner selection,
successful-probe retention, fired-only live fill, `REPLAY_SAFE_FRAC=0.99`,
single-post scoring shape, fallback, wrapper, and hosted gate unchanged.
`SLOW_MULTIPOST_N` remains `1`.

## Tail eligibility

The tail is added only when all of these are true:

1. replay-safe sizing is active and `_replay_stop()` ends the fill;
2. the six-probe race completed;
3. the selected frame fired at least once;
4. the validated S18 prefix is non-empty;
5. configured and SDK candidate capacity remains.

No tail is added after warm-up failure, a mid-fill environment exception, an
all-zero race, a hard-cap exit, or the legacy non-replay deadline. The validated
prefix remains byte- and order-identical to S18 under the same runtime.

## Release

Upload only `RELEASE/submission.ipynb`. Do not hand-edit `RELEASE/`.

From `S14`:

```powershell
python -B .\S19\tools\build_release.py
python -B .\S19\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S19\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S19\attack.py']; main()"
.\verify_bundle.ps1 -Mode Check
```

Local gates prove lineage, behavior, and packaging. Only the hosted rerun can
measure residual replay capacity and leaderboard score.
