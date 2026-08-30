# S17 experiment record

## Pre-registration

- **ID:** `S17_S15_FIXED_PROBE_FLOOD_R099_VERBOSE_HARMONY`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** S15, hosted score `84.95`, source SHA-256
  `3867ef52aa19811bd246149596cc8aa2623fee0abc08e93be1eaadaf27a45171`.
- **Pinned donor settings:** verbose+Harmony `FRAME_TEMPLATE`,
  `FILL_BUDGET_FRAC = 0.99`, and `REPLAY_SAFE_FRAC = 0.99`.
- **Explicit non-changes:** fixed eight-sample latency split, no S16 frame race,
  no probe-hop, candidate-family, or wrapper change.
- **Hypothesis:** transplanting the public `88.425` fixed probe-and-flood arm's
  defining settings onto the scored S15 chassis improves the hosted result.
- **No-tuning rule:** score these exact bytes once. Repeat exact bytes if the
  result is ambiguous; any other change receives a new ID.

This bundled-arm test cannot attribute a gain to any one of the three settings.
Identical public V12 implementations span `4.015` score points.

## Interpretation

| S17 score | Disposition |
|---:|---|
| `>88.97` | Clear lead beyond the observed same-code spread; repeat exact bytes. |
| `80.94–88.97` | Inconclusive; retain S15 as control and use an exact-byte repeat or per-model rows. |
| `<80.94` | Clear regression; revert to S15 and inspect timeout/runtime rows. |
| `0` / `NULL` | Packaging or runtime failure first, not algorithm evidence. |

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: `26,029` / `66d22b6c528e2c2182b53fefe2f3fbd528c7aacbcec168e3c7187f1450e6cfe1`
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Returned-candidate or timeout notes, if available: pending
- Disposition: pending
