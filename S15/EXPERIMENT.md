# S15 experiment record

## Pre-registration

- **ID:** `S15_V12_ENGINE_CONTROL_COMMON_WRAPPER`
- **Artifact:** `RELEASE/submission.ipynb`
- **Hypothesis:** the lean V12 engine will recover throughput lost by the S14
  tournament and conservative replay-accounting layers.
- **Estimand:** current hosted score of the frozen V12 attack source under the
  common hardened S14 wrapper. This does not reproduce the historical V12
  notebook runtime or prove its remembered score.
- **Primary comparator:** S14B, `77.31`.
- **No-tuning rule:** score this exact notebook once. If a repeat is needed for
  an ambiguous result, repeat the same bytes. Any optimization receives a new ID.

Known hosted reference scores supplied by the user:

| Artifact | Score |
|---|---:|
| S14B | 77.31 |
| S14B-V15 | 75.06 |
| S14C | 72.09 |
| S14D | 44.935 |
| Friend S16 | 50.52 |

Interpretation against S14B:

- `73.44–81.18` (within ±5%): provisional noise-equivalence; stop this branch;
- `81.19–92.77`: promising movement; require per-model rows or an exact-byte repeat;
- `>92.77`: strong movement; preserve S15 and fork optimization under a new ID;
- `<73.44`: investigate packaging/runtime and per-model collapse before judging V12.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Disposition: pending
