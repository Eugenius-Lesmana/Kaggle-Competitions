# S26 Harmony multipost-4 experiment record

## Pre-registration

- **ID:** `S26_S19_SLOW_MULTIPOST4`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base/comparator:** exact S19/V19, user-reported aggregate `92.475`,
  SHA-256 `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
- **Same-day control:** exact-byte S25/V25; score pending.
- **Only source transform:** `SLOW_MULTIPOST_N=1 -> 4`.
- **Held constant:** Tail64, all prompt helpers and bytes, three-frame race,
  two interleaved repetitions, selection metric, fired-only retention,
  candidate order, `REPLAY_SAFE_FRAC=0.99`, `FILL_BUDGET_FRAC=0.95`,
  `PROBE_HOPS=0`, `REPLAY_COST_COEF=1.0`, `BURST_K=1`, fallback, notebook
  wrapper, and competition-rerun gate.
- **Hypothesis:** when `FRAME_TEMPLATE` wins, the validated forged plan yields
  about four scoreable posts for about `3.6x` candidate replay cost, improving
  the slow-row score rate enough to beat the same-day S19 control.
- **No-tuning rule:** any tail, route, frame, prompt, hop, replay fraction,
  endpoint-allocation, or multipost-count change receives a new experiment ID.

## Primary risks

1. `chosen_template == FRAME_TEMPLATE` is not model identity; Gemma can receive
   Harmony-forged messages.
2. Four posts consume most of four full reasoning hops, so a modest theoretical
   rate gain may lose after hosted overhead or fire-rate degradation.
3. Historical multi-message growth has shown nonlinear replay cost.
4. Tail64 remains single-post and can reuse endpoint labels named by the forged
   live prefix, reducing clean score-cell diversity without violating validity.
5. Hosted variance is material; compare against S25 and per-model rows, not only
   the historical S19 aggregate.

## Decision rule

- Runtime failure or a regression versus same-day S25: reject multipost-4.
- A small positive delta inside the documented `4.015`-point identical-code
  spread: inconclusive without supportive per-model rows or a repeat.
- A gain larger than that spread with the expected GPT-OSS concentration and no
  Gemma collapse: promote for confirmation.
- Aggregate `>=97.000`: target reached; freeze the exact artifact.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Prepared notebook SHA-256:
  `16768f7c79c90544b3cd2e202859bcc416762fe6dc37394005879f89f7dc6b32`
- Canonical `attack.py` bytes/SHA-256: `26,453` /
  `4e9a7dd4fd6de178dd96e319a790cc01989f58653e118c978ddf17e11a28d11d`
- Aggregate score: pending
- GPT-OSS public/private row scores: pending
- Gemma public/private row scores: pending
- Phase-1 candidates received per model: pending
- Phase-2 candidates replayed, validated, and timed-out flags per row: pending
- Exception/runtime notes: pending
- Disposition: pending
