# S24 experiment record

## Pre-registration

- **ID:** `S24_V19_TAIL256`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** Eugene V19 source (92.475), SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
- **Only intended executable change:** `OVERPACK_TAIL_N` 64 → 256.
- **Held constant:** all templates, 3-frame race with 2 reps, selection
  metric, fired-probe retention, single-post fill, `REPLAY_SAFE_SIZING=True`,
  `REPLAY_SAFE_FRAC=0.99`, `FILL_BUDGET_FRAC=0.95`, `PROBE_HOPS=0`,
  `REPLAY_COST_COEF=1.0`, `MARGIN_S=47.0`, fallback, notebook wrapper,
  and hosted gate.
- **Hypothesis:** V19's tail captured only 75% of theoretical ceiling because
  the 64-candidate pool was too small. Increasing to 256 lets more of the
  unclaimed replay reserve be harvested, pushing the score toward 100+.
- **Primary risk:** a larger tail may exceed the gateway's replay budget,
  causing the scored prefix to be truncated. The tail is placed AFTER the
  validated prefix and is bounded by the SDK cap (2,000), so the worst case
  is a smaller-than-expected gain.
- **No-tuning rule:** attribute any score only to the tail size increase.

## Deterministic acceptance

- Source matches V19 with exactly `OVERPACK_TAIL_N` changed from 64 to 256.
- The 3-frame race, 6-probe interleaving, selection metric, and fill loop
  are V19-identical.
- Source, release copy, notebook payload, manifest, SDK validation, and tests
  agree on exact bytes.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: `26,453` /
  `f8f240dbfedcd3b10bbfe56d44622e4f836407ed4ff93ea54c92ef13d32439e7`
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Disposition: ready for upload
