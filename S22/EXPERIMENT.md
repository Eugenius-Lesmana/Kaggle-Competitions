# S22 experiment record

## Pre-registration

- **ID:** `S22_S18_FIVE_FRAME_RACE`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** exact Eugene S18/V18 source; hosted score 88.155.
- **Only intended executable change:** add two terse single-post templates to
  `FRAME_RACE_TEMPLATES`, increasing the interleaved race from 6 to 10 probes.
- **Held constant:** prompt payload, S18's three frames, two probes per frame,
  selection metric, fired-probe retention, single-post fill, 0.99 replay cap,
  `FILL_BUDGET_FRAC=0.95`, `PROBE_HOPS=0`, `REPLAY_COST_COEF=1.0`, fallback,
  tail absence, notebook wrapper, and hosted gate.
- **Hypothesis:** the added terse shapes may let either model select a faster
  successful frame and recover enough replay capacity to improve on 88.155.
- **Evidence limit:** the requested logical-assumption path bypassed the planned
  real-model battery. Public designs are leads, not score evidence.
- **Primary risk:** four extra calibration probes can cost more than a new frame
  saves, or a terse frame can lose fire rate under hosted behavior.
- **No-tuning rule:** attribute any score only to the frame-race expansion. A
  tail, multipost, burst, packing, or fill change requires a separate artifact.

## Deterministic acceptance

- Inverse replacement of exactly three pinned S22 byte blocks reproduces the
  25,746-byte frozen S18 SHA-256.
- The race probes all five frames twice in declared order, retains hits, fills
  with the minimum eligible `median_latency / fire_rate` frame, and preserves
  declared-order tie-breaking.
- Source, release copy, notebook payload, manifest, SDK validation, and tests
  agree on exact bytes.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: `25,901` /
  `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Disposition: conditional; no upload authorized
