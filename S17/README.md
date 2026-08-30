# S17 S15 Fixed Probe-and-Flood

S17 is the scored S15 chassis with the settings from the public `88.425`
fixed probe-and-flood arm. It retains S15's deterministic eight-sample latency
split and does not inherit S16's unscored frame race.

## Identity

- base: `../S15/attack.py`, 25,995 bytes, SHA-256
  `3867ef52aa19811bd246149596cc8aa2623fee0abc08e93be1eaadaf27a45171`;
- exact source delta: verbose+Harmony `FRAME_TEMPLATE`,
  `FILL_BUDGET_FRAC = 0.99`, and `REPLAY_SAFE_FRAC = 0.99`;
- canonical S17 source: `attack.py`, 26,029 bytes, SHA-256
  `66d22b6c528e2c2182b53fefe2f3fbd528c7aacbcec168e3c7187f1450e6cfe1`;
- public provenance: `probe-and-flood-strategy.ipynb`, SHA-256
  `dad420b418d103a3f2fb3906bb32c1d474960040e33add7d378dec1cfc92c486`,
  reported score `88.425`;
- hosted control supplied by the user: S15 scored `84.95`.

This reproduces the donor's defining settings inside S15's hardened chassis;
it is not a claim that the two full source files are byte-identical. Because
`REPLAY_SAFE_SIZING` is enabled, `FILL_BUDGET_FRAC` is provenance-pinned even
though the replay-safe stop path governs the normal hosted run.

## Artifacts

- `attack.py` — canonical S17 source;
- `RELEASE/attack.py` — byte-exact release copy;
- `RELEASE/submission.ipynb` — generated two-cell upload notebook;
- `tests/test_release.py` — identity, behavior, capacity, and packaging gates;
- `EXPERIMENT.md` — preregistration and hosted-result intake;
- `RELEASE/MANIFEST.sha256` — deterministic provenance hashes.

Upload only `RELEASE/submission.ipynb`. Do not hand-edit `RELEASE/`.

## Build and verify

From `S14`:

```powershell
python -B .\S17\tools\build_release.py
python -B .\S17\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S17\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S17\attack.py']; main()"
.\verify_bundle.ps1 -Mode Check
```

Local gates do not establish a hosted score. Record the result in
`EXPERIMENT.md` without changing the scored notebook.
