# S27 calibrated hop-1 experiment record

## Pre-registration

- **ID:** `S27_S19_CALIBRATED_HOP1`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base/comparator:** exact S19/V19, user-reported aggregate `92.475`,
  SHA-256 `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
- **Only mechanism:** one-hop selected-frame live validation with conservative,
  per-session eight-hop replay-cost calibration.
- **Frozen constants:** `PROBE_HOPS=1`, offline `REPLAY_COST_COEF=2.0`,
  `REPLAY_COST_SAFETY_FACTOR=1.25`, and `CALIBRATION_SAMPLES=2`.
- **Evidence used to freeze constants:** the S27 plan records unchanged hop-0
  marker-post success in `12/12` one-hop/eight-hop comparisons across both
  models and approximately `1.5-2x` faster one-hop validation.
- **Held constant:** exact S19 prompt bytes, full-hop warm-up, full-hop six-probe
  interleaved race, winner metric, fired-only retention, candidate order,
  Tail64, replay-safe bounds, caps, deadlines, faults, forced-count mode,
  fallback, notebook wrapper, and competition-rerun gate.
- **Excluded:** S23 Tail128, S26 multipost-4, best-first ordering, frame failover,
  burst, model routing, prompt variants, and portfolio sorting.

## Runtime calibration contract

For each model invocation, reuse the selected frame's two full-hop race latencies,
then collect two successful one-hop fill samples at fresh candidate indices.
Compute:

```text
observed_ratio = max(full_hop_latencies) / max(min(one_hop_latencies), LAT_FLOOR_S)
session_coef = max(2.0, observed_ratio * 1.25)
```

Never cap a large observed ratio downward. Retroactively charge both calibration
candidates with the final coefficient, then charge each later one-hop candidate
as `elapsed * session_coef`. The replay-cost bound uses estimated eight-hop cost;
the fill-wall bound uses actual elapsed time. Any incomplete, invalid, or
fire-mismatched calibration returns to exact S19 full-hop behavior.

## Hypothesis

One-hop validation increases the number of fired candidates that can be checked
during the fill wall without admitting blind candidates or exceeding the
eight-hop replay window. The planning range is approximately `0-1.44` aggregate
points. It may be score-neutral when replay capacity, rather than live-fill time,
already determines the returned prefix.

## Primary risks

1. Replay undercharge can overrun the replay phase and void an entire model row.
2. A high-tail eight-hop latency can exceed the offline floor; per-session
   calibration and the `1.25` safety factor must cover it without a downward cap.
3. Two runtime samples are noisy; invalid or inconsistent calibration must fail
   back to full-hop S19 rather than continue optimistically.
4. Faster validation gives no capacity gain when the replay-cost cap binds first.
5. Hosted variance is material; compare per-model rows and runtime diagnostics,
   not only the aggregate.

## Acceptance gates

- canonical S27 source equals the explicit transforms of the pinned S19 bytes;
- warm-up and all six race calls remain full-hop and byte/order-identical;
- hop-1 and hop-8 marker-post success remains equivalent;
- session coefficient is finite, positive, at least `2.0`, and covers observed
  full-hop cost after the safety factor;
- calibration candidates are retroactively charged and the replay stop fires
  before pessimistic eight-hop cost exceeds its cap;
- calibration failure reproduces full-hop S19 behavior;
- S19 prefix, Tail64, ordering, caps, deadlines, faults, fallback, and uniqueness
  gates pass;
- the clean two-cell notebook reproduces canonical bytes and has no mode override;
- S27 tests, S19 regression tests, SDK validation, release manifest, and root
  bundle verification all pass.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Prepared notebook SHA-256:
  `742c993a4fab66c15f14489f79c619124ca3fa44e8b616fd67b259eae735d493`
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical/release `attack.py` bytes and SHA-256: `31,783` /
  `fff81d3f98b3112562617753418692236c46e71233a5933ec4937f81151e1236`
- Session coefficient and calibration diagnostics per model: pending
- Aggregate score: pending
- GPT-OSS public/private row scores: pending
- Gemma public/private row scores: pending
- Phase-1 candidates received per model: pending
- Phase-2 candidates replayed, validated, and timed-out flags per row: pending
- Exception/runtime notes: pending
- Disposition: pending
