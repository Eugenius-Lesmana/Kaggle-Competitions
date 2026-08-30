# S18B S16 Replay-Cutoff Tail

S18B is the optional higher-risk arm. It preserves S16's scored three-frame
race and `REPLAY_SAFE_FRAC=0.97`. Its only experiment is a bounded untested tail:
when the live fill stops specifically at the replay-safe cutoff after a
successful frame race, append up to 64 fresh candidates using the winning frame.

The validated prefix is byte- and order-identical to S16 under the same runtime.
Tail indices were never sent to the live environment. The tail is never added
after warm-up or environment failure, an all-zero race, a configured/hard cap,
or any non-replay stop. Candidate count stays within both `hard_n_cap` and
`HARD_N_CAP=2000`.

This is a moderate-risk, unvalidated capacity experiment. The extra candidates
can score if the replay preserves a successful prefix and has spare wall time;
they can instead consume replay time or reduce reliability. S16's user-reported
aggregate score of 87 is evidence for the unchanged prefix/race, not for the
tail.

## Artifacts

- `attack.py` — canonical S18B source, mechanically pinned to S16 plus three
  exact tail transforms;
- `RELEASE/attack.py` — byte-exact release copy;
- `RELEASE/submission.ipynb` — clean deterministic two-cell upload notebook;
- `tests/` — S16 race/release gates plus cutoff-tail isolation tests;
- `EXPERIMENT.md` — preregistration and hosted-result intake;
- `RELEASE/MANIFEST.sha256` — deterministic provenance hashes.

Upload only `RELEASE/submission.ipynb`. Do not hand-edit `RELEASE/`.

## Build and verify

From `S14`:

```powershell
python -B .\S18B\tools\build_release.py
python -B .\S18B\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S18B\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S18B\attack.py']; main()"
```

Local gates do not validate hosted replay-time headroom or establish a score.
