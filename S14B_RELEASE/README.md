# S14B release candidate

Risk-adjusted S14B: the five public-control arms plus the guarded
`inj_close_empty` challenger. The Ox Alpha donors remain unchanged.

Release repairs:

- replay phase `8750s` with safety factor `0.975` (`8531.25s` cap);
- every confirmed candidate repriced at the latest worst latency for its shape;
- `max_steps` enforced across warmup, tournament, and fill attempts while
  `max_tool_hops` remains a per-interaction limit.

Artifacts:

- `attack.py` — canonical source;
- `submission.ipynb` — generated notebook embedding `attack.py` byte-exact;
- `tests/test_release.py` — deterministic behavioral and failure-reproduction gates;
- `MANIFEST.sha256` — release inputs and outputs, relative to the `S14` folder.

From `S14`, rebuild and verify with:

```powershell
python ".\Friend's submission\S15\make_notebook.py" ".\S14B_RELEASE\attack.py" ".\S14B_RELEASE\submission.ipynb" S14B_RELEASE
python ".\Friend's submission\S15\check_notebook_sync.py" ".\S14B_RELEASE\submission.ipynb" ".\S14B_RELEASE\attack.py"
python -B -m pytest -p no:cacheprovider ".\S14B_RELEASE\tests" -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S14B_RELEASE\attack.py']; main()"
```

Local deterministic verification does not replace separate GPT-OSS and Gemma
hosted evidence. No upload or hosted run is part of this release build.
