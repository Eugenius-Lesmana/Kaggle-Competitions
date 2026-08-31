# HANDOFF — AI Agent Security competition (timmyv2 branch, next agent session)

<!-- BEGIN 2026-08-31 S24 TAIL256 SUBMITTED — recorded 2026-08-31 11:32 WIB -->
## 2026-08-31 S24 tail256 submission checkpoint (newest session-state authority)

- **Causal gap analysis complete:** The full V19(92.475) − S22(87.390) = 5.085
  gap is explained by two isolated deltas: tail64 (+4.320) vs 2 extra frames
  (-0.765). Eugene's winning formula is the compact S18/V19 chassis: untimed
  warm-up, 6-probe 3-frame race, retain calibration hits, select by
  median(latency)/fire_rate, fill immediately, measured replay-cost packing at
  0.99, and a guarded tail.
- **S24 built and submitted:** Eugene V19 with `OVERPACK_TAIL_N` increased from
  64 to 256. Only change is the tail constant. All V19 mechanisms preserved.
- **Gates passed:** 16/16 tests, SDK validation, gateway test (deterministic
  public 338.36), release checker, manifest.
- **Notebook pushed to Kaggle:** `timsurreal/s24-tail256-submission` — go to
  that kernel page and click "Submit to Competition" for it to score.
- **Prediction:** V19 captured 75% of theoretical tail64 ceiling (+4.320). A
  256-tail has 4x capacity → theoretical ceiling +23.04, realistic capture
  ~+11-17 → projected **103-110**.
- **V22 still pending** at ref 55895453. Monitor before next submission.
- **Next levers** if S24 underperforms: (1) PROBE_HOPS=1 with REPLAY_COST_COEF
  scaling for 1.5-2x faster fill; (2) MARGIN_S 47→37 for tighter deadline;
  (3) S23 frame+tail union if frame race shows positive.

Full detail: `S24/EXPERIMENT.md`, `S24/README.md`.
<!-- END 2026-08-31 S24 TAIL256 SUBMITTED -->

<!-- BEGIN 2026-08-31 RECOVERY CHECKPOINT 4 — recorded 2026-08-31 10:56 WIB -->
## 2026-08-31 recovery checkpoint 4 (newest session-state authority)

- Recovered Iterations 1–17, the exact submission/ref map, the dirty worktree,
  the V19-anchored plan, and the existing Graphify outputs after another cutoff.
- Preserved `timmyv2`; inspect `Eugene` and `archive/eugene-s19` with read-only
  Git commands only. No worktree checkout, upload, push, or attack-source edit.
- Causal authority is unchanged: V19 tail64 **+4.320** from S18; S22's two
  extra race frames **-0.765** from S18; V20/V21 remain source-unavailable
  bundles; V22 was pending at the last authenticated refresh.
- Active task: refresh V22, finish the evidence/confounder table, then select
  one V19-based experiment with offline invariants and a preregistered decode.

Full detail: `dev_notes/S22_investigation.md` Iteration 18.
<!-- END 2026-08-31 RECOVERY CHECKPOINT 4 -->

**Read this first.** Rewritten 2026-08-29. Sections in this file are current
as of that date; anything contradicting them elsewhere is stale.

<!-- BEGIN 2026-08-31 CAUSAL CHECKPOINT 3 — recorded 2026-08-31 10:52 WIB -->
## 2026-08-31 causal checkpoint 3 (newest strategy authority)

- S18 is the exact shared control for the decisive comparison:
  - Eugene V19 = S18 plus guarded tail64: **+4.320**;
  - Timmy S22 = S18 plus two extra race frames: **-0.765**.
- Their difference is `4.320 - (-0.765) = 5.085`, exactly
  `92.475 - 87.390`. The whole observed V19-over-S22 gap is therefore
  accounted for by the two isolated deltas, subject to single-run variance and
  the open V19 scored-upload hash caveat.
- S21→S22 gained 10.410, but that comparison changes the entire chassis. The
  causal read is that transplanting Eugene S18 recovered the score; Timmy's
  own five-frame expansion slightly hurt it.
- Eugene's repeatable advantage is the compact active path: untimed warm-up,
  six-probe complete-frame race, retain calibration hits, fill the winner
  immediately, keep only fired singles, account returned-prefix replay cost,
  and append capacity experiments after the ordered validated prefix.
- Timmy's S21 path spent complexity on discarded screen hits and an unreachable
  Stage E; S22 then added unmeasured choices to a two-sample-per-frame selector.
  Do not return to either design.

No implementation or upload occurred. Next decision: size the V19 tail follow-up
for the 100–110 target while preserving the V19 prefix and clean replay cutoff.
<!-- END 2026-08-31 CAUSAL CHECKPOINT 3 -->

<!-- BEGIN 2026-08-31 LIVE REFRESH CHECKPOINT 2 — recorded 2026-08-31 10:49 WIB -->
## 2026-08-31 live refresh checkpoint 2 (newest score authority)

- Authenticated Kaggle history at 10:49 WIB still shows V22/ref `55895453`,
  script `346092100`, pending. V21 remains complete at **90.900**; V19 remains
  the team best at **92.475**.
- The current leaderboard has 4,207 teams. `TimmyTurner` is rank **277**, with
  46 submissions and members `timsurreal,zombiespecz`. There are 108 teams at
  100+ and 55 at 110+; the leader is 147.530. The 100–110 target is therefore
  competitive but demonstrably reachable.
- An authenticated historical V19 pull by script-version ID again returned
  HTTP 403. V20/V21 historical code remains unavailable. Their aggregate
  scores must stay classified as unknown-bundle evidence.
- The latest downloadable Eugene notebook remains the presumed V22 snapshot:
  S18 plus a one-time runner-up-frame switch after six consecutive misses, no
  V19 tail. Do not bind this code to V20 or V21.

No attack source, upload, push, or branch switch occurred.
<!-- END 2026-08-31 LIVE REFRESH CHECKPOINT 2 -->

<!-- BEGIN 2026-08-31 RESUME CHECKPOINT 1 — recorded 2026-08-31 10:40 WIB -->
## 2026-08-31 resume checkpoint 1 (newest session-state authority)

- Recovered the existing dirty `timmyv2` worktree, all prior score/provenance
  notes, the V19-anchored plan, archived Kaggle artifacts, and the existing
  Graphify graph before analysis. No branch checkout was needed; Eugene sources
  remain available through git objects and archived files.
- Current banked evidence remains Eugene V19 **92.475**, Timmy S22 **87.390**,
  Eugene V20 **79.020**, Eugene V21 **90.900**, and Eugene V22 pending at the
  last authenticated refresh. V19's bounded tail is the only positive isolated
  hosted delta; S22's frame expansion is a negative isolated delta.
- Queried the existing graph for the V19–V22/S22 comparison. It identifies the
  relevant seams—replay cutoff/tail capacity, frame selection, candidate
  packing, model arms, and score accounting—but does not close missing V20–V22
  historical source provenance.
- Adopted an evidence-first iterative plan: refresh hosted facts, compare exact
  recoverable source, separate causal deltas from unknown bundles, then design
  one V19-based next submission. No attack source, upload, push, or active-branch
  switch occurred in this iteration.

New work from this resumed session is recorded in
`dev_notes/S22_investigation.md` Iteration 15 onward.
<!-- END 2026-08-31 RESUME CHECKPOINT 1 -->

<!-- BEGIN 2026-08-31 RESUME CHECKPOINT 0 — recorded 2026-08-31 10:23 WIB -->
## 2026-08-31 resume checkpoint 0 (newest session-state authority)

- Resumed on `timmyv2`, eight commits ahead of `origin/timmyv2`, preserving all
  pre-existing dirty and untracked work. No submission source was changed.
- Graphify lessons were current and the existing graph query completed. Its
  evidence route remains: Eugene score ladder -> S18/V18 control -> V19 tail64
  versus Timmy S22 frame expansion -> replay cutoff/tail tests.
- Graphify package `0.9.46` warned that the installed skill text is `0.9.17`;
  traversal still completed normally. Treat this as tooling provenance, not a
  competition finding.
- Active unknowns remain V22's final score and historical V20/V21/V22 source
  recovery. No Colab, Kaggle upload, remote push, or branch checkout occurred.

This block is new work from the resumed session; older checkpoints below are
prior-session evidence.
<!-- END 2026-08-31 RESUME CHECKPOINT 0 -->

<!-- BEGIN 2026-08-31 V21 SCORE CHECKPOINT — recorded 2026-08-31 10:16 WIB -->
## 2026-08-31 V21 score checkpoint (newest score authority)

- Authenticated team history now shows Eugene V21/ref `55892238`, script
  `346063944`, complete at **90.900**.
- V21 is **+2.745** versus Eugene V18 but **-1.575** versus V19. V19 remains
  the banked control at **92.475**.
- V21's historical source is unavailable, so its aggregate score rejects or
  accepts only the unknown bundle; it does not identify a reusable mechanism.
- Eugene V22/ref `55895453`, script `346092100`, remains pending. The current
  pulled source is only a presumed V22 snapshot until that binding is closed.
- No next artifact is authorized until V22 finishes and Checkpoint A is reviewed.

No Kaggle upload, push, or working-tree branch checkout occurred.
<!-- END 2026-08-31 V21 SCORE CHECKPOINT -->

<!-- BEGIN 2026-08-31 PROVENANCE CHECKPOINT — recorded 2026-08-31 10:00 WIB -->
## 2026-08-31 provenance and source checkpoint (newest authority)

- Authenticated `GetSubmission` metadata closes the version/ref ownership map:
  Eugene V19 `345982069`/`55883308` = **92.475**; Timmy S22
  `346026772`/`55888268` = **87.390**; Eugene V20
  `346033952`/`55889026` = **79.020**; Eugene V21
  `346063944`/`55892238` and V22 `346092100`/`55895453` remain pending.
- Timmy's scored S22 payload is closed byte-for-byte at attack SHA-256
  `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`.
  Relative to exact S18 it only adds two frame candidates, so its **-0.765**
  result rejects that lever.
- Eugene's reconstructed V19 release source is
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`:
  exact S18 plus the bounded 64-candidate post-cutoff tail and an inert default
  cap clamp. Historical private-revision download returns 403, so the scored
  upload's byte identity remains the one open provenance edge; do not describe
  it as cryptographically closed.
- The current pulled Eugene notebook has attack SHA-256
  `366ff1346b5d89a3545814abad8c4d765b2d8568a714b32bff99a4b00e61c826`.
  It is S18 plus a six-consecutive-miss switch to the race runner-up, with no
  V19 tail. It is the current/latest snapshot and presumed V22; historical V20
  and V21 sources are still unavailable, so V20's large loss cannot be assigned
  to a mechanism.
- Kaggle no longer serves the historical raw submission CSVs, and its episode
  API returns zero rows for these refs. Per-model effects are therefore unknown.
- The otherwise dangling Eugene S17-S19 commit is protected locally by branch
  `archive/eugene-s19`; no remote was changed.
- Operational decision: bank V19, retire S22/S23, wait for V21/V22 decode, and
  run any next upload as one change from V19. The revised gates live in
  `tasks/plan.md`; durable artifact metadata lives in
  `dev_notes/kaggle_versions/README.md`.

No Kaggle upload, push, or working-tree branch checkout occurred.
<!-- END 2026-08-31 PROVENANCE CHECKPOINT -->

<!-- BEGIN 2026-08-31 SCORE INTAKE CHECKPOINT — recorded 2026-08-31 09:42 WIB -->
## 2026-08-31 score intake checkpoint (newest score authority)

- Authenticated Kaggle history now shows Eugene V19/ref `55883308` complete at
  **92.475**. Against frozen S18/ref `55870282` = **88.155**, the isolated
  64-tail gain is **+4.320**, exactly **75%** of its +5.760 theoretical ceiling.
  T1 and T7 therefore pass; classify the bounded tail `tail-positive`.
- Timmy S22 is **87.390** (chronological ref `55888268`, exact notebook/ref
  metadata cross-check still in progress): **-0.765** versus S18. Reject the
  two added frames as a hosted scoring lever; deterministic packaging remains
  valid but does not imply superiority.
- Eugene V20 is **79.020** (chronological ref `55889026`, provenance
  cross-check in progress): **-13.455** versus V19. Do not inherit its new
  mechanism until the exact V19→V20 diff is isolated.
- The two newest refs, `55892238` and `55895453`, remain pending and are the
  likely V21/V22 slots. Exact version/ref mapping is still being verified.
- S23 stays blocked: its tail dependency passed, but its S22-frame dependency
  failed. The next artifact must start from scored V19, not S22/S23.

Full evidence is being appended as `dev_notes/S22_investigation.md`
Iteration 12. No upload, push, or branch checkout occurred in this intake.
<!-- END 2026-08-31 SCORE INTAKE CHECKPOINT -->

<!-- BEGIN LOCAL COMMIT CHECKPOINT — recorded 2026-08-30 17:14 WIB -->
## Local commit checkpoint (newest authority)

- The isolated S22/S23 source, release packets, tests, plan, checklist, and
  durable notes are committed atomically on `timmyv2`.
- Unrelated dirty S21-era files and generated `graphify-out/` content were not
  staged. No remote push and no Kaggle upload occurred.
- S22 is ready for human evidence review, not automatically recommended: its
  waived real-model battery remains the main uncertainty.
- S23 remains non-uploadable until both conditions in `S23/CONDITIONAL.md` pass.

Full evidence: `dev_notes/S22_investigation.md` Iteration 11.
<!-- END LOCAL COMMIT CHECKPOINT -->

<!-- BEGIN GRAPHIFY COMPLETION CHECKPOINT — recorded 2026-08-30 17:12 WIB -->
## Graphify completion checkpoint (newest local-state authority)

- Incremental graph refresh completed after the S22/S23 source and docs work:
  2,508 nodes, 4,953 edges, 145 communities; +288 nodes/+454 edges and
  -39 replaced nodes/-46 replaced edges versus the prior graph.
- Health gate: zero dangling endpoints, missing endpoints, self-loops, or
  collapsed endpoint pairs. The prior 742-dangling warning no longer applies
  to this rebuilt graph.
- Updated query traversal reaches S22/S23 lineage, prefix, tail, release-tool,
  manifest, notebook, and conditional-evidence nodes at their current paths.
- Benchmark reports about 27.9x fewer tokens per query. Graphify's cost file
  records zero tokens because Gemini rejected the configured key and the
  successful host-agent fallback exposed no usage metadata; zero is an
  undercount, not a claim that semantic extraction was free.
- `graphify-out/` remains a pre-existing generated/untracked tree and is not
  part of the isolated S22/S23 commit.

Full evidence: `dev_notes/S22_investigation.md` Iteration 10.
<!-- END GRAPHIFY COMPLETION CHECKPOINT -->

<!-- BEGIN FINAL S22/S23 GATE CHECKPOINT — recorded 2026-08-30 17:01 WIB -->
## Final S22/S23 gate checkpoint (newest authority)

- Joint pytest collection initially exposed a duplicate module name because
  both suites were named `test_release.py`. S23's suite is now uniquely named
  `test_s23_release.py`; the regenerated packet verifies its new manifest path.
- Final joint suite: `29 passed in 0.43s`.
- S22 and S23 independent release checkers pass; both SDK red-team validators
  pass; all 12 Python files compile in memory; `git diff --check` passes.
- S22 remains the only next experimental upload candidate, still conditional
  because its real-model battery was waived. S23 remains blocked behind two
  positive hosted dependencies. No upload or push occurred.
- Graphify refresh and explicit-path atomic commit are the only remaining local
  tasks at this checkpoint.

Full evidence: `dev_notes/S22_investigation.md` Iteration 9.
<!-- END FINAL S22/S23 GATE CHECKPOINT -->

<!-- BEGIN S23 RELEASE CHECKPOINT — recorded 2026-08-30 16:55 WIB -->
## S23 conditional release checkpoint (newest authority)

- The separate S23 packet is fully built but remains blocked from upload.
- Canonical/release source: 26,611 bytes,
  `32cc018df05c534f747ad171ad7aa17af6f3df887f439caa67bbc927cbee1265`.
- Notebook: 37,588 bytes,
  `612e6366b5e4bd7e160b8e570f82a4c6799ff69791b893e6af4215884ed1c8a2`.
- Gates: full S23 suite `16 passed`; release checker passed 11 provenance
  records; SDK red-team validation passed.
- One inherited S22 count assertion correctly failed before adaptation: S23
  totals are S22's unchanged 95/97 prefixes plus exactly 64 tail candidates,
  producing 159/161 under the deterministic trace.
- Activation remains strictly conditional on a positive isolated S22 frame
  result and a `tail-positive` V19/S19 classification. No upload is authorized.

Full evidence: `dev_notes/S22_investigation.md` Iteration 8.
<!-- END S23 RELEASE CHECKPOINT -->

<!-- BEGIN S23 CONDITIONAL CHECKPOINT — recorded 2026-08-30 16:52 WIB -->
## S23 conditional checkpoint (newest follow-up authority)

- `S22/` remains byte-frozen and independently attributable.
- A separate non-uploadable `S23/attack.py` now combines the exact S22 frame
  delta with Eugene S19's three bounded-tail transforms.
- S23 source: 26,611 bytes, SHA-256
  `32cc018df05c534f747ad171ad7aa17af6f3df887f439caa67bbc927cbee1265`.
- Focused tail tests were RED in four expected places on the S22 copy, then
  GREEN (`5 passed`) after only: `OVERPACK_TAIL_N=64`, SDK cap clamping, and
  eligible-cutoff tail append.
- Tests reverse S23 exactly to S22 (`c94487…`) and then S18 (`a09ac2…`). They
  also prove the live calls and validated prefix equal S22 under the same trace.
- S23 is preparation only. Do not upload or recommend it unless S22's frame
  result is positive and V19/S19's tail is `tail-positive` under T7.

Full evidence: `dev_notes/S22_investigation.md` Iteration 7.
<!-- END S23 CONDITIONAL CHECKPOINT -->

<!-- BEGIN S22 RELEASE CHECKPOINT — recorded 2026-08-30 16:48 WIB -->
## S22 release checkpoint (newest build authority)

- The deterministic S22 release packet now exists under `S22/RELEASE/`.
- Canonical and release `attack.py`: 25,901 bytes, SHA-256
  `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`.
- Upload notebook: 36,640 bytes, SHA-256
  `689c9634d78fa60e0e8151e5662a9382a13b350f24528670e7b1f8291576a873`.
- The independent release checker passed: exact source copy, reproducible clean
  two-cell notebook, hosted-rerun gate, and nine manifest records.
- Full S22 pytest gate passed: `13 passed in 0.35s`.
- The planned real-model battery remains unrun. This is a user-directed,
  logic-based conditional artifact, not evidence that the two new frames beat
  S18. No Kaggle upload is authorized.
- Remaining work: SDK validation, conditional-next-artifact decision, Graphify
  update, final diff/release review, and an explicit-path local commit.

Full evidence: `dev_notes/S22_investigation.md` Iteration 6.
<!-- END S22 RELEASE CHECKPOINT -->

<!-- BEGIN S22 BUILD CHECKPOINT — recorded 2026-08-30 16:36 WIB -->
## S22 build checkpoint (newest implementation state)

- Work continues without waiting for V19; no Kaggle upload is authorized.
- `S22/attack.py` began byte-identical to Eugene S18
  (`a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`).
- The conditional S22 source now adds only two public-design single-post race
  frames: `{payload} to {url}` and plain `http.post ... now.`. Its current hash
  is `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`.
- Five-frame effect/lineage tests failed on S18, then passed after the pinned
  change (`5 passed`). Inverse transforms recover the exact S18 hash.
- Real-model superiority is unproven. Treat S22 as a conditional experiment,
  not an upload recommendation, until full release gates and evidence review.
- Next incomplete work: deterministic notebook/manifest, full suite, SDK
  validation, durable release hash, Graphify refresh, isolated local commit.

Full evidence: `dev_notes/S22_investigation.md` Iteration 5.
<!-- END S22 BUILD CHECKPOINT -->

<!-- BEGIN S22 INVESTIGATION ADDENDUM — recorded 2026-08-30 16:08 WIB -->
## S22 investigation addendum (newest authority)

### Score truth

- Team `TimmyTurner` is rank **911/4,189** in the downloaded public snapshot,
  with 42 submissions and a banked best of **88.155**.
- Timmy S21/ref `55871920` = **76.980**. Timmy S20/ref `55856909` = **73.740**.
- Eugene V18/S18/ref `55870282` = **88.155**. V19/S19/ref `55883308` remains
  pending as of 2026-08-30 16:08 WIB.
- The 86.670 score at ref `55857006` is Eugene S16, not Timmy S21.
  `dev_notes/S21_analysis.md` is corrected and otherwise historical.

### Proven explanation

- S21's new Stage E did not create the claimed fill. Stage D has no convergence
  stop and consumes `n_target` or the shared budget first. A deterministic
  always-fire trace with cap 40 returned Stage B=0, Stage C=2, Stage D=38,
  Stage E=0. Existing tests never asserted Stage E reachability.
- Stage B screen hits are also discarded by `_compose()`. S21 nevertheless
  returns hundreds through Stage D; the old claim that it shipped only 35–45
  candidates is false.
- Eugene S18 is a causal, compact ladder: untimed warm-up; six probes across
  three complete replay frames; retain hits; immediately fill the winner; stop
  by accumulated measured replay cost. S18 differs from S16 by exactly one
  tested line: `REPLAY_SAFE_FRAC = 0.97 -> 0.99`, worth +1.485 LB in that run.
- S19 differs from S18 only by a guarded 64-candidate tail after the estimated
  replay cutoff. Its theoretical ceiling over S18 is +5.760, so it can cross
  90 but cannot reach 100 alone.

### S22 decision

Do not patch the 2,433-line multi-mode S21 pipeline. Wait for V19, then use
Eugene S18 as the frozen control chassis. The default S22 experiment changes
one mechanism only: the small single-post frame race, after a real-model battery
proves a candidate at least 3% better on `median_latency / fire_rate` without a
p90 or fire-rate regression. Keep 0.99 packing and omit the V19 tail so the
result remains attributable. If no frame clears the gate, submit no frame
variant; use exact S18 only as a recovery/control artifact.

Targets from S18: 90 needs about 21 additional perfect singles/model; 95 needs
76/model; 100 needs 132/model. Thus 90 is plausible, 95 is conditional, and
100 requires a separately validated score-density or large throughput gain.

Execution plan: `tasks/plan.md`. Checklist: `tasks/todo.md`. Evidence and
iteration log: `dev_notes/S22_investigation.md`. Refreshed navigation graph:
`graphify-out/graph.html` and `graphify-out/GRAPH_REPORT.md`.

This addendum is the only current strategy in this file. Sections below it are
preserved historical context unless this addendum explicitly repeats them.
<!-- END S22 INVESTIGATION ADDENDUM -->

## Reading order (follow exactly; avoids outdated context)

1. **THIS ADDENDUM** — current status and S22 decision. Lower sections are
   historical unless the addendum explicitly repeats them.
2. **`dev_notes/submissions.md`** — the per-submission experiment log.
   Read BACKWARD from the end: § S21_FILL → § S20_K2PURE → § S19B_SINGLEFULL →
   § S19_P2PFULL → § S18_P2P → § AUG-27/28 DECODE SWEEP →
   § S17_HYBRIDULTRA → § S16_ULTRA → § S15_SINGLEPURE → § S14_SINGLEFILE.
   STOP at S13 — everything S6–S13 is history (the 43–51 plateau era);
   its decode shortcuts and decision trees are OBSOLETE.
3. **`dev_notes/S22_investigation.md`** — current evidence and S22 decisions.
   Read this before `dev_notes/S21_analysis.md`; the older file contains a
   misattributed S21 score and is not authoritative for the next build.
4. **`PRD_TIMMYV2.md` § 1** — verified mechanics (scoring formula, budgets,
   n_ctx, refresh rules). Still true. § 3 (S7 pivot design) is historical.
5. **`dev_notes/colab/SETUP.md`** — Colab real-model VM workflow (accurate,
   includes all VM gotchas). Battery scripts live beside it
   (`probe_s18.py`, `probe_s18b.py` = newest; older `probe_*.py` kept for
   reference).
6. **`dev_notes/colab/s18/`** — the 2026-08-28 battery data behind S18
   (results + per-hop logs). This is the evidence for the ladder design.

### DO NOT TRUST (stale / superseded — historical only)

- **`glm52findings/`, `qwen38maxfindings/`** — S16-era agent analyses.
  Both contain arithmetic errors (submissions.md § S17 corrects them) and
  their central predictions were FALSIFIED (S16 decoded 50.52, not their
  90–126; the "180 LB" ceiling was never arithmetic — see the model below).
- **Older sections of any doc describing k=2 as "the one untested lever"** —
  the s18 battery measured the whole k-ladder locally; S18's hosted decode
  (63.070) confirmed the p-ladder is dead hosted — fourth datapoint after
  S11 plateau, S16 50.52, teammate D-v2 44.935. Multi-post per candidate
  is a throughput trap under this evaluator. Never ship p≥2 arms again.
- **S7/S8-era decode shortcuts and the "strategy in one paragraph"**
  (sibling floor, overpack, wording axes) — superseded by the S16/S17/S18
  chassis: keep-only-fired, VERIFY_REPS=1, density ranking, no siblings,
  no lottery tail.
- **`dev_notes/colab_battery_2026-08-24.md`** first-battery conclusions —
  partially revised by later rounds (e.g. "deep short drips = traps" was
  re-measured and softened in round 5).
- Auto-memory `kaggle-ai-agent-security.md` — v1 era; this file supersedes.

## Historical status (2026-08-29) — SUPERSEDED BY S22 ADDENDUM

- **TEAM BEST: 77.310** (teammate A/zombiespecz, ref 55810506). Our banked
  best: **72.095** (S15_SINGLEPURE, ref 55794899).
- **S21 second opinion complete** — see `dev_notes/S21_analysis.md`. Key
  findings: (1) teammate's accumulated-cost budget tracking is more precise
  than our wall-clock approach; (2) untimed warm-up prevents premature fill
  stop; (3) frame race could replace UCB exploration. Recommended S22 build
  order: warm-up → accumulated-cost tracking → tighter margin → frame race.
- **S20_K2PURE = ~73** (scored ~73k on the leaderboard). The k=2 hedge
  (fx2_ultra) and teammate_plain template did NOT move the needle vs S15/S17.
  Reason: keep-only-fired path ships only ~35-45 verified probes, not the
  ~889 the rival/teammate achieve with a fill loop.
- **S19_P2PFULL PENDING** — S18 arms + full budget utilization.
- **S19B_SINGLEFULL PENDING** — predicted ~80.
- **S21_FILL IS THE CORRECT BUILD** (`submission_S21_FILL.ipynb`
  153,340 B; attack.py sha256 `7254d222862ad047…`): S20 arms (fx2_ultra/
  fx1_ultra on gpt, teammate_plain/rival_plain on gemma) + pure exploitation
  fill loop after stage D. The core insight from the S20 decode: our gap vs
  the rival/teammate is NOT templates or forge — it's the fill loop. They
  fire the best template until budget exhausts (~889 candidates/row). Our
  keep-only-fired path ships only ~35-45 verified probes. S21 adds a fill
  loop after UCB converges: fires the best-density family until n_target or
  budget exhausts. Predicted: ~85-100 LB. **Upload this one next slot.**
- Deadline **Sep 1 23:59 UTC**; ~5 uploads/day.

## Historical score model (2026-08-28 — superseded where contradictory)

1 EXFIL post = 16 + 2 (unique cell) = 18 raw. row_norm = raw/200.
LB = (raw_gpt + raw_gemma)/400.

**Hosted per-candidate replay cost is ADDITIVE in posts**: c(p) ≈ 6.6s +
1.1s·post (calibrated on teammate-A 77.31 @ p=1, S15 72.095, and the
rival's ~80 fill-loop). Consequences:

- **Singles wall ≈ 81 LB**: 8750s/9.7s ≈ 902 fired/row max at p=1. The
  whole 72–80 cluster (us, teammate, rival) is pinned there.
- **The top island (92.5–147.5, nobody between 57.1 and 92.5) = p≥2
  posts/candidate.** p=2 ≈ 119 ceiling, p=4 ≈ 137, #1's 147.5 fits p≈2 at
  high efficiency. Deep multi-post (8+) hits the hosted quadratic
  (re-prefill) → the 43–51 plateau where four of our configs and
  teammate's D-v2 died.
- **S16's 50.52 was a LATENCY death**: f1_ultra (bare un-framed line)
  fires 100% but lets gpt_oss's analysis channel generate 169–237 tok
  (vs 51 with the harmony forge) → 2–7s/hop variance → generation probes
  and replay both starve. The forge's real function = reasoning suppressor.
  Never ship un-framed bare lines on the gpt arm.

## Historical FILL LOOP hypothesis (2026-08-29 — falsified by control-flow trace)

Comparing our S20 (~73 LB) vs teammate A's S14B (77.31) and the rival (~80):

| Metric | Our S20 (keep-only-fired) | Teammate/rival (fill loop) |
|---|---|---|
| Ship strategy | ~35-45 verified probes from stages C+D | Continuous fill loop until budget exhaust |
| Candidates/row | ~35-45 (keep-only, no sibling fill) | ~889 (every probe that fires, kept) |
| Fill mechanism | Stage D UCB explores all families | Fire best family until budget runs out |
| Budget utilization | 87.9% (gate-idled) | 99.3% (60s margin) |
| LB score | ~73 | 77-80 |

The gap is **pure fill volume**, not templates, forge, or k-values. S21 adds
a stage-E fill loop that fires the best-density family repeatedly until
n_target or budget exhausts — matching the rival's fill strategy.

## Repo map (timmyv2)

| File | Role |
|---|---|
| `attack.py` | THE submission source. `ATTACK_MODE` env selects config; hosted default comes from the notebook's baked cell. |
| `make_notebook.py` | `make_notebook.py attack.py <out>.ipynb <MODE>` — BAKES the mode into notebook cell 1. Always build variants this way. |
| `submission_S21_FILL.ipynb` | Current ready build (S20 arms + fill loop). Frozen scoring bytes: `submission_S11_TOPTIER.ipynb`, `submission_S15_SINGLEPURE.ipynb` — NEVER rebuild those two. |
| `check_notebook_sync.py` | `check_notebook_sync.py <notebook> attack.py` — byte-exact embed check. Run before EVERY upload. |
| `tests/test_attack_units.py` | 22 suites; MUST pass under the active mode + S17/S16 regression (see gate ritual). |
| `local_check.py --budget 600` | Stub-agent e2e vs public+permissive guardrails (NOT hosted-predictive — shape ratios only). |
| `gateway_local_test.py 90` | Real relay e2e. |
| `sdk/` | Competition SDK (read-only; the source-audited truth for mechanics). |
| `dev_notes/submissions.md` | Experiment ledger — ALWAYS update on every score. |
| `dev_notes/colab/` | VM workflow + all battery scripts/results. |
| `PRD_TIMMYV2.md` | Strategy constitution (§1 mechanics current; rest historical). |

## Verified mechanics (do not re-derive; SDK-audited)

- n_ctx=8192 GGUF both models; overflow kills whole rerun → `_ctx_*` guard
  stays FOREVER. max_new_tokens=1024; greedy (temp 0); seed 123; fresh env
  per candidate; one hop = one inference = one tool call; DENY/text-reply
  breaks the hop loop.
- Budgets: generation 8750s + replay 8750s × {public,private} per model.
  MAX_REPLAY_FINDINGS=2000 candidates; ≤32 msgs/cand; ≤2000 chars/msg.
- Public guardrail = OptimalGuardrail hardcoded. Only reachable predicate:
  EXFILTRATION (+16) via clean-URL `http.post(data="SECRET_MARKER")`;
  predicate stacking PROVEN impossible (UTA window 2 ⊂ deny window 5).
- Aug-6 refresh: replay timeout keeps partial score (attack.py-phase
  timeout still fatal) → overpacking safe, best-first ordering matters.
- Session order fixed: `_STATE["n_sessions"]` → 1=gpt_oss, 2=gemma.
- Candidate validation (whole-run death on violation): mirror-validate,
  never raise, hygiene layer. Rerun log unobservable; LB = only feedback.
- Kaggle CLI (`kaggle competitions submissions -c
  ai-agent-security-multi-step-tool-attacks`) works from this machine;
  `kaggle auth login` periodically needed.

## Gate ritual before ANY upload (current)

```
for m in S21_FILL S20_K2PURE S19B_SINGLEFULL S18_P2P S17_HYBRIDULTRA S16_ULTRA:
    ATTACK_MODE=$m ./.venv/bin/python tests/test_attack_units.py
PYTHONPATH=sdk ./.venv/bin/python -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam','attack.py']; main()"
ATTACK_MODE=<MODE> ./.venv/bin/python local_check.py --budget 600
./.venv/bin/python gateway_local_test.py 90        # when probe/budget/fill logic changed
./.venv/bin/python make_notebook.py attack.py submission_<NAME>.ipynb <MODE>
./.venv/bin/python check_notebook_sync.py submission_<NAME>.ipynb attack.py
```

New mode checklist (follow S18_P2P as the template): arms tuple +
`_session_families` branch + `_ship_ceiling` list + `_family_metric` list +
stage-A skip list + fallback plan + forge/bare route sets + keep-only-fired
list + density-order list + unit-test branch (incl. band disjointness ×400).

## Colab real-model testing (USE THIS FIRST for pool questions)

Proven workflow for measuring hosted-equivalent behavior (real GGUFs +
OptimalGuardrail + SandboxEnv seed 123) on a free Colab T4 in minutes
instead of burning a submission. Guide: `dev_notes/colab/SETUP.md` (SSH/
ngrok, VM gotchas, llama-cpp wheel + LD_LIBRARY_PATH fixes, gemma Q3_K_XL
full-offload requirement, resume support). Standing rule: **any new
family/shape hypothesis gets a battery BEFORE a submission slot** — VMs die
hourly, so scp results to `dev_notes/colab/` immediately (the s18 round
survived two tunnel deaths with zero data loss this way). Caveat that
still holds: T4 ratios and post-counts transfer (greedy, same weights);
absolute latencies do NOT.

## Dead branches (consolidated — never revisit)

Pre-2026-08-28 (proven by LB): wording/persuasion searches · bare-only
pools (S8C/S9A/S9B) · multi-message momentum ladders at depth 8+ ·
sibling fill + overpack WITHOUT keep-only-fired · raw/second
self-selection (rate metric) · taint predicates publicly ·
DESTRUCTIVE_WRITE publicly · identical-candidate cache spam · URL-length
tuning as a lever (S10) · per-model shape micro-tuning for its own sake
(S12/S13 flat).

2026-08-28 additions (proven by decode/battery): un-framed bare lines on
the gpt arm (S16's latency death) · forge k≥5 single-message on gpt_oss
(fx5 variance-collapse) · heavy multi-post challengers under a
sibling-filled chassis (teammate D-v2 44.935) · agent analyses promising
LB numbers without the c(p) cost model (the "90–180" failure mode —
always re-derive from the model above).

2026-08-29 additions (proven by S20 decode): keep-only-fired WITHOUT a
fill loop (ships only ~35-45 verified probes; the rival's 889/row comes
from a fill loop, not templates) · k=2/k=1 forge alone without fill
(S20 ~73 vs S21 predicted ~85-100 — the fill loop IS the lever).

## Historical endgame protocol (after S21 decode — superseded)

- S21_FILL is built and gated — upload it the moment a slot opens.
- S21 decode rules:
  - S21 ≥ 85: fill loop confirmed + k=2 edge additive. Re-ship S21 bytes
    for tail draws; final selection = S21-best.
  - S21 77–85: fill loop works but k=2 inert on one arm. Keep S21 in
    rotation; try S22 = pure fill loop with teammate_plain only (no forge).
  - S21 72–77: fill loop inert hosted (budget exceed or per-probe cost
    model wrong). Revert to S15 bytes (72.095 banked).
  - S21 < 72 or zombie: one identical re-upload, then revert to S15-class.
- If S19B ≥ 80 (when it lands): utilization lever confirmed independent
  of fill loop → keep S19B in rotation too.
- Last 2 days: no new builds. Upper-tail riding + final selection only.
