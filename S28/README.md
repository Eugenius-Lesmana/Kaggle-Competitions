# S26 / V26: isolated Harmony multipost-4 arm

S26 is exact scored S19 plus one pinned source transform:

```text
SLOW_MULTIPOST_N = 1 -> 4
```

No other attack behavior changes. The S19 Tail64 prefix, replay-safe sizing,
race order, winner metric, fallback, notebook wrapper, and hosted gate remain
frozen.

## Why this branch

- S19/V19 is the best confirmed anchor at `92.475`.
- S20 best-first and S22 frame failover regressed; S23 Tail128 and the friend's
  V24 Tail256 remain capacity experiments.
- The current campaign plan reserves the next isolated technical arm for
  `SLOW_MULTIPOST_N=4`, compared against the exact-byte S25/V25 S19 control.
- Existing real-GGUF probe notes report about `4.0` firing posts per candidate
  for roughly `3.6x` replay cost, a theoretical rate gain near `1.11x`.

## Activation and limits

Multipost activates only after the six-probe race selects `FRAME_TEMPLATE`.
Race probes and other winners remain byte-identical to S19. The gate is a frame
choice, not reliable model identity, so Gemma can be exposed if it selects the
same frame. Replay sizing charges the full measured elapsed time of each forged
candidate.

S19's unprobed Tail64 remains single-post. Its endpoint indices can overlap
indices already named inside earlier four-post candidates; this is retained to
keep S26 a one-transform experiment rather than silently adding an allocation
change.

## Identity

- experiment ID: `S26_S19_SLOW_MULTIPOST4`;
- base: `../S19/attack.py`, 26,453 bytes, SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`;
- canonical S26 source: `attack.py`, 26,453 bytes, SHA-256
  `4e9a7dd4fd6de178dd96e319a790cc01989f58653e118c978ddf17e11a28d11d`;
- generated notebook SHA-256:
  `16768f7c79c90544b3cd2e202859bcc416762fe6dc37394005879f89f7dc6b32`;
- no `ATTACK_MODE` override is baked into the notebook;
- the server starts only when `KAGGLE_IS_COMPETITION_RERUN` is present.

## Build and verify

From `S14`:

```powershell
python -B .\S26\tools\build_release.py
python -B .\S26\tools\check_release.py
python -B -m pytest -p no:cacheprovider .\S26\tests -q
python -X utf8 -B -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam',r'S26\attack.py']; main()"
.\verify_bundle.ps1 -Mode Check
```

Upload only `RELEASE/submission.ipynb` after separate explicit approval.
