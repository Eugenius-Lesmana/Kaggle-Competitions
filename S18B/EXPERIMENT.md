# S18B experiment record

## Pre-registration

- **ID:** `S18B_S16_RACE_REPLAY_CUTOFF_TAIL64`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** S16 exact attack source, SHA-256
  `33fb04486b62745a617c3dffe86c47a1a8de0d6102518d3e299fa919c1ec20f2`.
- **Scored anchor:** S16 aggregate 87, user-reported; exact row scores pending.
- **Only intended mechanism:** after `_replay_stop` ends a successful eligible
  race/fill, append at most 64 fresh, untested single-post candidates in the
  selected winning frame.
- **Isolation:** keep S16 `REPLAY_SAFE_FRAC=0.97`, two-repetition three-frame
  race, replay coefficient, probe hops, templates, and fired-only prefix.
- **Safety rule:** no tail on environment exception, all-zero race, cap exit, or
  any other stop; total candidates never exceed the configured or SDK hard cap.
- **Hypothesis:** the replay may preserve the proven S16 prefix and score some
  tail candidates using residual wall time.
- **Risk:** moderate. Tail candidates are not live-validated and may consume
  replay time; this arm is less reliable than S18's conservative capacity change.
- **No-tuning rule:** score these exact bytes once. Any code/parameter change
  receives a new ID.

## Interpretation

- Above S16: evidence that residual replay capacity can score a bounded tail.
- Near S16: tail is neutral or run variance dominates.
- Below S16 or any NULL/zero row: treat tail replay-time pressure as the first
  mechanism-specific suspect, after packaging/runtime checks.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: pending
- Aggregate score: pending
- Per-model public/private rows: pending
- Runtime/replay-timeout notes: pending
- Disposition: pending
