# S18: S16 Race with 0.99 Replay Packing

S18 is the low-risk follow-up to the user-reported S16 score of **87**, the
highest known graded result. Its executable source is exactly S16 with one
replacement:

```text
REPLAY_SAFE_FRAC = 0.97  ->  0.99
```

The successful S16 three-frame race, two repetitions per frame, fired-only
retention, single-post fill, prompt bytes, probe hop count, replay-cost model,
fallback, and `FILL_BUDGET_FRAC=0.95` are unchanged.

## Rationale and risk

At a 9,000-second replay budget, the change raises the nominal safe window from
8,730 to 8,910 seconds: 2.06% more capacity, before warm-up subtraction and the
existing next-candidate margin. This can add roughly 9–21 candidates at observed
8.5–20.4 second latency, but it reduces nominal reserve from 270 to 90 seconds.
The expected leaderboard effect is approximately 0 to +1.8 points if yield is
stable; hosted runtime variance can make it neutral or negative.

S18 is distinct from:

- S15: fixed eight-probe latency routing;
- S16: direct three-frame race with 0.97 replay packing;
- S17: fixed probe-and-flood routing with 0.99 packing.

## Identity

- base: `../S16/attack.py`, SHA-256
  `33fb04486b62745a617c3dffe86c47a1a8de0d6102518d3e299fa919c1ec20f2`;
- canonical S18 source: `attack.py`, 25,746 bytes, SHA-256
  `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`;
- no `ATTACK_MODE` override is baked into the notebook;
- the server starts only when `KAGGLE_IS_COMPETITION_RERUN` is present.

Upload only `RELEASE/submission.ipynb`. Do not hand-edit `RELEASE/`.

## Build and verify

From `S14`:

```powershell
python -B .\S18\tools\build_release.py
python -B .\S18\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S18\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S18\attack.py']; main()"
.\verify_bundle.ps1 -Mode Check
```

Local gates establish exact lineage, packaging, and deterministic behavior; they
cannot establish the hosted score.
