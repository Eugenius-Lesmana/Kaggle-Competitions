# S25 experiment record

## Pre-registration

- **ID:** `S25_V19_TAIL96`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** Eugene V19 source (92.475), SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
- **Only intended executable change:** `OVERPACK_TAIL_N` 64 → 96.
- **Held constant:** all templates, 3-frame race with 2 reps, selection
  metric, fired-probe retention, single-post fill, `REPLAY_SAFE_SIZING=True`,
  `REPLAY_SAFE_FRAC=0.99`, `FILL_BUDGET_FRAC=0.95`, `PROBE_HOPS=0`,
  `REPLAY_COST_COEF=1.0`, `MARGIN_S=47.0`, fallback, notebook wrapper,
  and hosted gate.
- **Hypothesis:** V19's tail64 captured +4.320 over S18 (75% of the theoretical
  +5.760 ceiling). S24's tail256 scored 90.540, suggesting tail overshoot or
  budget saturation. Tail96 represents a conservative midpoint — enough to
  capture more of the unclaimed reserve without risking the replay-budget
  truncation seen at tail256. A quadratic fit through tail0 (V18), tail64 (V19),
  and tail256 (S24) has a vertex near tail143 (predicted 94.38), so tail96
  should be a safe upward step.
- **Primary risk:** even a 50% increase in tail size may exceed the gateway's
  replay budget, though the risk is lower than tail256.
- **No-tuning rule:** attribute any score only to the tail size increase.

## Deterministic acceptance

- Source matches V19 with exactly `OVERPACK_TAIL_N` changed from 64 to 96.
- The 3-frame race, 6-probe interleaving, selection metric, and fill loop
  are V19-identical.
- Source, release copy, notebook payload, manifest, SDK validation, and tests
  agree on exact bytes.

## Result intake

- Kaggle submission/version ID: ref `55932157`, script `346419345`
- Upload timestamp: `2026-09-01 04:52:38.973 UTC` (`11:52:38.973 WIB`)
- Uploaded notebook SHA-256: `58d76e1b2b38c04b1111c75b62ba4898b560d023c3dd33bce7e6522ac9a2f39c`
  after Kaggle normalization
- Re-downloaded embedded `attack.py` SHA-256:
  `4e6d31a580168729a74290befa60656e0df65b37e5cc49341db0f2cd30030671`
- Canonical `attack.py` bytes/SHA-256: `26,446` /
  `4e6d31a580168729a74290befa60656e0df65b37e5cc49341db0f2cd30030671`
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Disposition: submitted; scoring pending
