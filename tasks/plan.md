# S22 plan — recover causality, then clear 90

**Status:** proposed; implementation requires teammate review.
**Deadline:** 2026-09-01 23:59 UTC.
**Control:** Eugene S18/V18 at commit `002a038`, ref `55870282`, score 88.155.
**Rule:** one scoring mechanism per submission; freeze source/notebook hashes.

**Execution override (2026-08-30 16:48 WIB):** the user directed work to proceed
without waiting for V19 or the real-model battery. S22 is therefore being built
as a logic-based conditional artifact. T1 and T3 remain evidence gaps and must
not be represented as passed; they no longer block deterministic packaging.

## Outcome

First target 90 with a measured single-post throughput gain. Keep 95 as the
conditional combined target. A 100-point attempt proceeds only after evidence
for a higher-density arm; current evidence does not justify one.

## Decision tree

1. Decode V19/ref `55883308` before uploading S22.
2. If V19 >= 90, bank it; run S22 as a frame-only experiment for 95.
3. If V19 is 88.155–89.999, treat the tail as weak-positive; still isolate the
   frame experiment before combining.
4. If V19 < 88.155 or blank, reject the tail; use frame-only S22. Exact S18 is
   the fallback if no frame passes the battery.
5. Never combine an unscored frame change, tail, and multipost change.

## Phase 0 — freeze evidence

### T1. Record V19 decode [XS]

- **Depends on:** Kaggle scoring completion.
- **Files:** `dev_notes/submissions.md`, `dev_notes/S22_investigation.md`.
- **Work:** record ref, score, artifact SHA, delta from S18, and decision band.
- **Accept:** no `PENDING` remains for V19; score maps to exact S19 manifest.
- **Verify:** authenticated submission history plus release SHA manifest.

### T2. Materialize the S18 control on `timmyv2` [M]

- **Depends on:** T1 and human approval.
- **Files:** one attack source, one test file, one generated notebook, manifest.
- **Work:** copy the frozen S18 payload, not S21's multi-mode chassis.
- **Accept:** source and notebook payload hashes match Eugene S18 before any
  experimental edit; exact three-frame race and 0.99 cap are preserved.
- **Verify:** SHA checks, notebook sync, SDK validation, unit suite.

### Checkpoint A

Human verifies V19 decode, S18 provenance, and the one-mechanism rule.

## Phase 1 — S22 frame experiment

### T3. Run a pre-registered real-model frame battery [M]

- **Depends on:** T2.
- **Files:** one battery script, one raw result file, investigation log.
- **Work:** compare S18's three complete frames with at most two terse
  single-post candidates. Use both competition models, seed 123, identical
  URLs/payload bands, and at least 12 repetitions/frame/model.
- **Metrics:** fire rate, median, p90, and `median_latency / fire_rate`.
- **Accept:** a candidate wins on both models or is selected by the existing
  per-model race; fire loss <=1 percentage point, p90 regression <=5%, primary
  metric improvement >=3% versus the S18 winner.
- **Stop:** if no candidate clears all gates, do not build S22-FRAME.

### T4. Add effect-level regression tests first [S]

- **Depends on:** T3 winner.
- **Files:** one test file.
- **Work:** prove warm-up exclusion, retained race hits, winning-frame fill,
  accumulated replay-cost stop, and non-zero exploitation output.
- **Accept:** each test fails against the known S21 defect and passes on the S18
  control/approved frame variant.
- **Verify:** focused tests plus full attack suite.

### T5. Build S22-FRAME as one diff [M]

- **Depends on:** T3 pass, T4.
- **Files:** attack source, test file, generated notebook, manifest.
- **Work:** change only the frame-race set. Keep S18 warm-up, fill, replay
  accounting, 0.99 cap, tail absence, and single-post shape unchanged.
- **Accept:** mechanical diff contains only the approved frame constants and
  corresponding exactness tests; notebook embeds source byte-exact.
- **Verify:** full unit suite, SDK validation, deterministic trace, notebook
  sync, SHA manifest, `git diff --check`.

### Checkpoint B

Human reviews raw battery rows, diff, test trace, and frozen hashes before upload.

### T6. Upload once and decode causally [S]

- **Depends on:** Checkpoint B and available submission slot.
- **Files:** append-only submission and investigation logs.
- **Accept:** Kaggle ref maps to the frozen hash; result is classified:
  - >=90: frame lever accepted.
  - 88.155–89.999: weak-positive/variance; do not overclaim.
  - <88.155: reject and restore S18 control.

## Phase 2 — conditional 95–100 work

### T7. Estimate the V19 tail marginal [S]

- **Depends on:** T1.
- **Work:** compare V19−S18 against the +5.760 theoretical ceiling and run
  simulator traces for how many tail items can enter the replay prefix.
- **Accept:** decision is `tail-positive`, `inconclusive`, or `rejected`, with
  an observed/theoretical capture ratio. No tail-size extrapolation otherwise.

### T8. Combine only two proven positives [M]

- **Depends on:** T6 >=90 and T7 `tail-positive`.
- **Work:** combine the frozen winning frame diff with the unchanged V19 tail.
- **Accept:** combined artifact is the union of exactly two already-scored
  diffs; simulator proves prefix identity and graceful deadline truncation.

### T9. Gate any 100-point density experiment [L, optional]

- **Depends on:** no safe path to 100 from T8 and remaining time/slots.
- **Work:** isolate one k=2 or burst frame in the S18 race; do not pre-route by
  model. Require real-model raw-points/second and p90 replay-cost evidence.
- **Accept:** >=15% modeled aggregate gain, no context overflow, stable exact
  post count, and a downside-approved upload slot. Otherwise stop at the banked
  90–95 artifact.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| V19 remains pending | Prepare battery only; do not upload a confounded build. |
| Public notebook titles imply unverified scores | Use their shapes as leads only. |
| Hosted variance masquerades as improvement | Freeze hashes; require isolated diffs and bands. |
| S21 complexity hides dead paths | Start from 460-line S18 payload; effect tests. |
| 100 target causes reckless stacking | T9 is optional and evidence-gated. |

## Definition of done

- V19 decoded and mapped to exact bytes.
- S22 has one isolated lever, passing effect-level tests and artifact sync.
- Submission result and decision are appended to both durable logs.
- Best-scoring frozen notebook and SHA are named in `HANDOFF.md`.
- Graphify is refreshed only if implementation changes source structure.
