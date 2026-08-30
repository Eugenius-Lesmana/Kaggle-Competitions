# S18 experiment record

## Pre-registration

- **ID:** `S18_S16_RACE_REPLAY_R099`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** exact S16 source, user-reported hosted score 87.
- **Comparator:** S16; S15 scored approximately 84.95; S17 is pending.
- **Only intended executable change:** `REPLAY_SAFE_FRAC=0.97` to `0.99`.
- **Held constant:** all prompt bytes, three race frames, two interleaved probes
  per frame, selection metric, fired-probe retention, single-post fill,
  `FILL_BUDGET_FRAC=0.95`, `PROBE_HOPS=0`, `REPLAY_COST_COEF=1.0`, fallback,
  wrapper, and hosted gate.
- **Hypothesis:** the S16 winner has enough runtime stability to convert 2.06%
  tighter replay packing into more scored candidates.
- **Expected score effect:** approximately 0 to +1.8 points, not guaranteed.
- **Primary risk:** nominal reserve falls from 270 to 90 seconds at a 9,000-second
  row budget; latency-tail drift can erase the gain.
- **No-tuning rule:** attribute this score only to the replay fraction. Any other
  executable change receives a separate variant ID.

## Deterministic acceptance

- S18 source equals SHA-pinned S16 after exactly one pinned byte replacement.
- At a synthetic 1,000-second, 10-second/candidate run, 0.97 returns 95
  candidates and 0.99 returns 97.
- Every S16 race, safety, uniqueness, fallback, notebook, and release gate passes.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: `25,746` / `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Disposition: pending
