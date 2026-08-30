# S23 conditional: S22 plus the bounded tail

S23 is an operationally prepared union, not an approved submission. It keeps
the frozen S22 five-frame race and adds Eugene S19's bounded replay-cutoff tail
as a separate artifact. S22 remains unchanged and attributable.

## Identity

- base S22: 25,901 bytes, SHA-256
  `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`;
- conditional S23: 26,611 bytes, SHA-256
  `32cc018df05c534f747ad171ad7aa17af6f3df887f439caa67bbc927cbee1265`;
- only S22→S23 transforms: define `OVERPACK_TAIL_N=64`, clamp the configured
  cap to 2,000, and append fresh winner-frame messages after an eligible
  replay-safe cutoff;
- the notebook has no `ATTACK_MODE` override and serves only during the hosted
  competition rerun.

Do not upload S23 unless the conditions in `CONDITIONAL.md` are satisfied.

## Build and verify

```sh
PYTHONPATH=sdk ./.venv/bin/python -B S23/tools/build_release.py
PYTHONPATH=sdk ./.venv/bin/python -B S23/tools/check_release.py
UV_CACHE_DIR=/tmp/s22-uv-cache PYTHONPATH=sdk uv run --with pytest --python ./.venv/bin/python python -B -m pytest -p no:cacheprovider S23/tests -q
PYTHONPATH=sdk ./.venv/bin/python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam','S23/attack.py']; main()"
```
