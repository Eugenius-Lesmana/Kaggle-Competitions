# S19 experiment record

## Pre-registration

- **ID:** `S19_S18_R099_REPLAY_CUTOFF_TAIL64`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** exact S18 source, SHA-256
  `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`.
- **Hosted anchor:** S18 aggregate `88.155`, user-reported.
- **Only intended mechanism:** after an eligible S18 `_replay_stop`, append at
  most 64 fresh, untested single-post candidates in the selected winning frame.
- **Held constant:** all S18 prompt bytes, three-frame race, two interleaved
  repetitions, selection metric, fired-probe retention, live-fill order,
  `REPLAY_SAFE_FRAC=0.99`, `FILL_BUDGET_FRAC=0.95`, `PROBE_HOPS=0`,
  `REPLAY_COST_COEF=1.0`, `BURST_K=1`, `SLOW_MULTIPOST_N=1`, fallback,
  notebook wrapper, and competition-rerun gate.
- **Hypothesis:** S18's measured ledger, next-candidate reserve, and 1% replay
  reserve leave some usable Phase-2 time; ordered replay will preserve the exact
  S18 prefix and score a portion of the bounded tail.
- **Primary risk:** an unvalidated tail candidate can fail, raise, or occupy the
  final blocking replay call. A normal inner deadline preserves accumulated
  findings, but a replay exception invalidates that model evaluation.
- **No-tuning rule:** attribute this result only to the cutoff tail. Any change
  to tail length, replay fraction, frame race, message shape, or multipost count
  receives a new experiment ID.

## Operational interpretation

These are decision thresholds, not statistical confidence intervals; hosted
variance remains material.

| Result versus `88.155` | Action |
|---|---|
| `0` / `NULL` / runtime failure | Keep S18; inspect packaging and replay exception first. |
| `<= -0.45` | Keep S18; retire the tail unless logs prove an unrelated failure. |
| `-0.45` to `+0.45` | Inconclusive; do not stack the tail into another unproven lever. |
| `+0.45` to `+0.90` | Capacity signal; preserve S19 and seek confirmation before aggressive expansion. |
| `> +0.90` | Strong operational signal; use S19 as the next mechanism anchor. |
| `>= 95` | Goal reached; freeze and exact-repeat only if a second selectable result is needed. |

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: `26,453` / `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`
- Aggregate score: pending
- GPT-OSS public/private row scores: pending
- Gemma public/private row scores: pending
- Phase-1 candidates received per model: pending
- Phase-2 candidates replayed, validated, and timed-out flags per row: pending
- Exception/runtime notes: pending
- Disposition: pending
