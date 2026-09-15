# V19-anchored endgame plan — beat 92.475 without losing causality

## Final-day override — 2026-09-01 21:17 WIB

The tail192 build plan below is superseded by hosted results and the remaining
quota. Tail128 and Tail256 both lost, Tail96 is already pending, four of five
daily slots are consumed, and the scoring queue exceeds the safe remaining
window. Do not implement new attack behavior.

### Task F0: Bind live state [XS]

**Acceptance criteria:** authenticated status and quota recorded; every pending
ref mapped to owner/script where known; unproven source identities remain marked
unknown.

**Verification:** `kaggle competitions submissions` and `submission-limits`
agree on four pending / one remaining.

**Dependencies:** None. **Status:** complete at 21:12 WIB.

### Task F1: Launch byte-exact V19 [XS, human action]

**Acceptance criteria:** use existing script `345982069` if permitted, otherwise
only the frozen notebook SHA `cd65fe8e...`; embedded attack SHA is
`3169466c...`; no rebuild or source edit; record new ref/script/time/hashes.

**Verification:** uploaded notebook and embedded attack match full hashes in
`dev_notes/final_day_submission_plan.md`; quota becomes 5/5.

**Dependencies:** explicit teammate authorization. **Status:** slot consumed by
ref `55942688`; exact artifact identity still requires verification.

### Checkpoint F: Fifth-slot identity

- [ ] Exact hashes verified after Kaggle normalization.
- [ ] New ref/script/upload time recorded in handoff and score ledger.
- [ ] Original V19/ref `55883308` remains selectable.

### Task F2: Monitor and lock final two [XS, human action]

**Acceptance criteria:** refresh at 22:00, 00:00, 03:00, and 05:00 WIB; keep
V19 as Final #1 unless a completed source-bound run clearly beats it; apply the
Final #2 decision tree; manually lock both by 05:30 WIB.

**Verification:** Kaggle UI shows two intended final selections before the
06:59 WIB deadline.

**Dependencies:** F1 accepted; pending score intake.

### Task F3: Close the durable record [XS]

**Acceptance criteria:** final scores, bindings, selection, and unresolved
provenance recorded; Graphify result saved/refreshed if source docs changed.

**Verification:** handoff, plan, task list, and graph memory agree.

**Dependencies:** F2.

---

## Superseded tail192 plan (historical only)

**Status:** superseded historical plan; do not execute.
**Updated:** 2026-08-31 10:16 WIB.  
**Deadline:** 2026-09-01 23:59 UTC.  
**Bank:** Eugene V19, ref `55883308`, script `345982069`, **92.475**.  
**Operational source control:** repo S19 at `archive/eugene-s19`, attack SHA-256
`3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.

This supersedes the S22 frame plan. S22 scored 87.390 and rejected its only
new mechanism; S23 combined that failed mechanism with the positive V19 tail
and must not be submitted.

## Assumptions and evidence limits

1. Repo S19 is the intended V19 source. Kaggle blocks historical private
   revision pulls, so the scored upload cannot be hash-bound independently.
2. Only aggregate public scores are available. Historical raw CSVs are gone;
   no claim may assign a gain or loss to one model row.
3. Clean replay deadline truncation preserves the ordered prefix in the frozen
   SDK gateway. A notebook wall timeout or replay exception remains a downside.
4. V21 finished at 90.900; V22 remains pending. V22 must be decoded before
   building or choosing the next upload.

## What the score gap requires

One successful unique single-post candidate in one model row contributes 0.045
aggregate leaderboard points.

| Target | Gap from 92.475 | Successful single-row equivalents | Balanced illustration only |
|---:|---:|---:|---:|
| 100 | 7.525 | 168 total | 84/model |
| 110 | 17.525 | 390 total | 195/model |

V19's 64-tail adds at most 128 candidates across both model runs. Its observed
gain, +4.320, equals 96 successful-single equivalents: 75% of the +5.760
ceiling. This does **not** prove symmetric rows or linear scaling.

Changing only the tail from 64 to 192 adds 256 possible candidates across both
runs. Its incremental theoretical ceiling is +11.520, or 103.995 from V19. If
the historical 75% capture repeated, the heuristic score would be 101.115.
Replay saturation makes that heuristic optimistic; a flat result is plausible.
No single-post tail result at this size can reach 110 without a new density or
throughput mechanism.

## Decision tree

1. Record V21/ref `55892238` = 90.900 and refresh V22/ref `55895453`
   immediately before work.
2. If either beats 92.475, bank it and recover its exact source before adopting
   any mechanism. Do not infer source from title or score.
3. If V22 is merely above S18, treat its six-miss failover as a lead, not an
   automatic additive win; it was tested without V19's tail and can interact
   with which frame the tail uses.
4. If neither pending submission beats V19, build `V19_TAIL192`: exact repo V19
   with only `OVERPACK_TAIL_N = 64` changed to `192` plus matching test/manifest
   expectations.
5. Do not upload a frame expansion, S23, the old Stage-E chassis, or an
   unrecovered V20/V21 mechanism.
6. Consider a density experiment only after tail expansion plateaus and only
   with real-model score-per-replay-second evidence. Existing Timmy multipost
   scores are negative evidence, not a reusable path to 110.

## Phase 0 — pending-result intake

### T0. Refresh and bind V21/V22 [XS]

**Current:** V21 is complete at 90.900 with source unavailable; V22 is pending.

- **Depends on:** Kaggle scorer.
- **Work:** record final score/status for refs `55892238` and `55895453`; pull
  the then-current notebook; record source and notebook hashes.
- **Accept:** score/ref/script/owner mapping is exact. A source claim is marked
  `closed`, `current-snapshot`, or `unavailable`; never silently upgraded.
- **Verify:** authenticated API plus notebook-embedded SHA.

### Checkpoint A

Teammates choose the best scored control. If neither pending artifact exceeds
92.475, proceed with repo V19 and keep its upload-hash caveat visible.

## Phase 1 — one-variable tail-capacity test

### T1. Materialize the V19 control [S]

- **Depends on:** Checkpoint A.
- **Work:** copy the frozen V19 attack source into a new experiment directory.
- **Accept:** source hash equals `3169466c…` before editing; three-frame race,
  0.99 packing, replay accounting, single-post shape, and tail64 all match.
- **Verify:** byte hash, inverse transform to S18, deterministic source diff.

### T2. Add tail192 tests before changing source [S]

- **Depends on:** T1.
- **Work:** require exactly 192 fresh winner-frame candidates after only an
  eligible replay cutoff.
- **Accept:** tests fail on V19 tail64 and cover: validated-prefix identity,
  unique indices, SDK cap, no tail after environment fault/all-zero race/cap or
  wall stop, and ordered prefix preservation.
- **Verify:** focused RED run captured in the experiment record.

### T3. Build `V19_TAIL192` as one effective change [M]

- **Depends on:** T2.
- **Work:** change only `OVERPACK_TAIL_N = 64` to `192`; update exactness tests,
  generated notebook, manifest, and experiment record.
- **Accept:** reverse `192 -> 64` recovers exact V19 bytes. No frame, budget,
  replay coefficient, hop, multipost, fallback, or margin value changes.
- **Verify:** full tests, deterministic trace, SDK validation, notebook/source
  byte sync, manifest checker, compile check, and `git diff --check`.

### Checkpoint B

Human reviews the one-line effective diff, prefix trace, frozen hashes, pending
scores, and the unrecoverable V19 upload-hash caveat before authorizing upload.

### T4. Upload once and decode [S]

- **Depends on:** Checkpoint B and an available submission slot.
- **Preregistered interpretation:**
  - `>92.925`: positive capacity evidence; bank if it is the new best.
  - `92.025–92.925`: practical plateau/inconclusive band (±0.450); retire
    simple tail-length expansion.
  - `<92.025`, NULL, or runtime failure: harmful; restore V19.
  - `>=100`: stretch target reached; do not stack another untested mechanism.
- **Caveat:** the ±0.450 band is an operational threshold, not a statistical
  confidence interval; only one hosted draw exists for each control.

## Phase 2 — conditional failover combination

### T5. Decode the six-miss failover [M, conditional]

- **Depends on:** V22 complete and current-snapshot source binding credible.
- **Work:** compare V22 to S18 because V22 omits the V19 tail. Inspect exact
  code before interpreting the score.
- **Gate:** only if V22 beats S18 by more than 0.450 without runtime anomalies,
  build a V19-control experiment whose sole diff is the same failover.
- **Stop:** V22 below 87.705 rejects failover; the middle ±0.450 band is
  inconclusive. Do not combine on an inconclusive result.
- **Interaction test:** prove tail candidates use the final active frame and
  the original validated prefix stays ordered under stable-winner traces.

## Phase 3 — 110 requires density, not more untested singles

### T6. Gate one density/throughput experiment [L, optional]

- **Depends on:** tail192 plateau or positive result below 100, remaining time,
  and real-model access.
- **Candidate class:** one V19-based score-per-replay-second mechanism, selected
  by measurement; no fixed model routing and no multi-mechanism bundle.
- **Required evidence:** both competition models, identical payload/URL bands,
  at least 12 repetitions per arm/model, >=15% better raw-points per estimated
  replay second, <=1 percentage-point fire-rate loss, <=5% p90 regression, and
  a simulator ceiling capable of covering the remaining target gap.
- **Negative prior:** Timmy S17 single 70.895, P2P S18 63.070, and P2P S19
  66.565. Do not upload another multipost variant without contrary measurements.
- **Stop:** no real-model evidence or no clean single-diff build means bank the
  best result. Colab is optional only for this phase; save raw rows locally
  after every batch because the VM is expected to disconnect.

## Definition of done

- Pending V21/V22 results are recorded with honest source-binding status.
- The best frozen scored artifact and its exact known hashes are named in
  `HANDOFF.md` and `dev_notes/kaggle_versions/README.md`.
- Any next artifact is one effective diff from the best understood control,
  passes its source/notebook/test/SDK gates, and has a preregistered decode.
- Every score updates the submission ledger, investigation log, handoff, todo,
  and Graphify before another mechanism is selected.
- No upload or remote push occurs without explicit teammate authorization.
