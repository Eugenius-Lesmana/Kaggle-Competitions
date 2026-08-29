# S16 experiment record

## Pre-registration

- **ID:** `S16_V12_DIRECT_THREE_FRAME_RACE_R2`
- **Artifact:** `RELEASE/submission.ipynb`
- **Base:** frozen V12 source and the common hardened S14/S15 two-cell wrapper.
- **Only intended mechanism change:** replace V12's eight-probe fixed latency
  classifier with two interleaved probes of verbose plain, bare + Harmony, and
  verbose + Harmony.
- **Selection rule:** minimize `median probe latency / observed fire rate`;
  zero-fire frames are ineligible and tuple order breaks exact ties.
- **Post-selection rule:** retain every successful race probe, then use only the
  winning frame for single-post fired-only fill under V12's replay and wall-clock
  ledgers.
- **Hypothesis:** direct measurement will avoid a wrong latency-to-frame mapping
  while adding only six probes, improving replay-valid score rate over V12/S15.
- **Primary comparator:** S15, the source-exact V12 control under the same wrapper.
- **No-tuning rule:** score this exact notebook once. Repeat only the same bytes
  to resolve an ambiguous run; any code or parameter change receives a new ID.

This is an inference-driven synthesis, not a score-proven improvement.

## Interpretation

- S16 above S15: evidence for direct frame selection; confirm with per-model rows
  or one exact-byte repeat before attributing the full delta.
- S16 near S15: the frame race is neutral or run noise dominates; retain S15 as
  the simpler control.
- S16 below S15: inspect per-model fire rate, runtime, replay timeout, and the six
  probe traces before changing margins or frame content.
- Any zero/NULL row: treat as packaging, runtime, or replay failure first, not an
  estimate of attack quality.

## Result intake

- Kaggle submission/version ID: pending
- Upload timestamp: pending
- Uploaded notebook SHA-256: pending
- Re-downloaded notebook SHA-256: pending
- Canonical `attack.py` bytes/SHA-256: `25,738` / `33fb04486b62745a617c3dffe86c47a1a8de0d6102518d3e299fa919c1ec20f2`
- Aggregate score: pending
- GPT-OSS public/private rows: pending
- Gemma public/private rows: pending
- Runtime/image notes: pending
- Six-probe trace notes, if available: pending
- Disposition: pending
