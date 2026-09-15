# Kaggle version and artifact ledger

**Recorded:** 2026-08-31 10:16 WIB  
**Competition:** `ai-agent-security-multi-step-tool-attacks`

This is the durable provenance ledger for the Aug-31 endgame analysis. Scores,
owners, refs, and script-version IDs came from the authenticated Kaggle API.
No score below is inferred from notebook ordering.

## Exact submission map

| Owner | Label | Ref | Script version | Status / score |
|---|---:|---:|---:|---:|
| Eugene | V18 | `55870282` | `345867396` | 88.155 |
| Eugene | V19 | `55883308` | `345982069` | **92.475** |
| Timmy | S22 | `55888268` | `346026772` | 87.390 |
| Eugene | V20 | `55889026` | `346033952` | 79.020 |
| Eugene | V21 | `55892238` | `346063944` | 90.900 |
| Eugene | V22 | `55895453` | `346092100` | pending |

## Artifact identity

| Artifact | Attack SHA-256 | Notebook SHA-256 | Binding status |
|---|---|---|---|
| Eugene S18 repo release | `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a` | `99c7cb257aef7f651b5a262b076dcb888d29001e9cf737d66808a649d40f7a8a` | frozen repo control |
| Eugene V19/S19 repo release | `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32` | `cd65fe8e4b44cf99ad289974b590ccba2fe095b44e0b4e66ef4ffff9ac78c670` | reconstructed V19; scored-upload hash remains open |
| Timmy S22 scored source | `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb` | `689c9634d78fa60e0e8151e5662a9382a13b350f24528670e7b1f8291576a873` | closed byte-for-byte |
| Eugene current/latest pull | `366ff1346b5d89a3545814abad8c4d765b2d8568a714b32bff99a4b00e61c826` | `2f6efbce5f0982c904b83e56e9a9bf7051057c9e16eb48c95d19638fb9a9e228` | presumed V22; version binding not independently closed |

The V19 lineage is protected from Git garbage collection by local branch
`archive/eugene-s19` at commit
`002a03830b66e228bdb65daab2a79565d38f72cb`. The downloaded current notebook
and metadata are in `dev_notes/kaggle_versions/latest/`.

## Source deltas that are actually known

- S18 -> repo V19: add a bounded 64-candidate winner-frame tail only at an
  eligible replay cutoff; clamp configured capacity to the SDK maximum. The
  clamp is inert under the default 2,000 cap.
- S18 -> Timmy S22: expand the three-frame, two-repetition race to five frames;
  everything else is the S18 control. Result: -0.765.
- S18 -> current/latest Eugene pull: retain the runner-up frame and switch once
  after six consecutive post-race misses; stop after six misses on the backup.
  The V19 tail is absent.
- V19 -> V20 and V20 -> V21: source unavailable. The V20 score is a bundle-level
  rejection only; no individual mechanism may be blamed from the score alone.

## Causal score evidence

- V18 -> V19: `92.475 - 88.155 = +4.320`. The 64-per-model tail has a
  theoretical aggregate ceiling of `128 * 0.045 = +5.760`; observed capture is
  75%, equivalent to 96 successful single-row candidates across both models.
- V18 -> Timmy S22: `87.390 - 88.155 = -0.765`; reject the two added frames.
- V19 -> V20: `79.020 - 92.475 = -13.455`; reject the unknown V20 bundle.
- V18 -> V21: `90.900 - 88.155 = +2.745`, but V21 source is unavailable;
  record only an unknown-bundle gain. V21 remains `-1.575` below V19.

## Retrieval limits

- Historical private notebook revision pulls return HTTP 403.
- Historical submission raw-file redirects resolve to deleted objects.
- `ListSubmissionEpisodes` returns zero episodes for all five Aug-30 refs.
- Therefore no per-model public/private rows are available. Aggregate deltas
  must not be presented as symmetric per-model effects.

Update this file append-only when V21/V22 finish or when a historical source is
recovered. Record score, ref, script-version ID, exact source hash, and one-diff
classification before changing the next-submission decision.

## Live refresh — 2026-08-31 10:49 WIB

- V22/ref `55895453` remains pending; no score or new source binding.
- Team rank is 277/4,207 with best 92.475 and 46 submissions.
- Historical V19 pull by script-version ID still returns HTTP 403; V20/V21
  source status remains unavailable.
