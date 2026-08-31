# S22 investigation log

This file records evidence and decisions after each investigation iteration.
It is not a private reasoning transcript. Each iteration is append-only unless
later evidence explicitly corrects it.

## Iteration 1 — score truth, teammate lineage, and S21 control-flow audit

**Recorded:** 2026-08-30 Asia/Jakarta

### Evidence collected

- Official Kaggle CLI history:
  - `55856909` = `73.740`
  - `55857006` = `86.670`
  - `55864702` = `86.580`
  - `55870282` = `88.155`
  - `55871920` = `76.980` (S21 per user)
  - `55883308` = pending (Eugene V19/S19 per user and timestamp)
- Competition deadline: 2026-09-01 23:59 UTC; 4,188 teams when queried.
- Latest Eugene source was fetched over HTTPS at commit `002a038` because the
  configured SSH remote cannot authenticate and `.git` refs are read-only.
- Eugene's documented scored ladder:
  - S15 `84.950`: fixed-route, single-post fill.
  - S16 `86.670`: six-probe direct race across verbose plain, bare+Harmony,
    and verbose+Harmony; fired-only fill; replay-safe accounting.
  - S17 `86.580`: fixed-route control with 0.99 packing.
  - S18 `88.155`: exact S16 plus `REPLAY_SAFE_FRAC 0.97 -> 0.99`.
  - S19 pending: exact S18 prefix plus an eligible 64-candidate cutoff tail.
- The frozen S21 notebook embeds current `attack.py` byte-exact at SHA-256
  `7254d222862ad04721b2b4d717102f91da0380f469734ae46bdb8167c791580f`.
- S21's advertised Stage E fill is normally starved:
  - Stage D UCB has no convergence condition.
  - It loops until `n_target`, an empty pool, or `can_probe()` failure.
  - Stage E runs only afterward with the same `n_target` and budget gate.
  - Therefore Stage E usually receives neither remaining capacity nor enough
    remaining budget. The S20→S21 score move (`73.740`→`76.980`) is consistent
    with a near-control/noisy repeat, not the predicted +12–27 point fill gain.
- `dev_notes/S21_analysis.md` incorrectly assigns `86.670` to S21. That score
  belongs to a different earlier submission and matches Eugene S16. Its claim
  that S21 beat the teammate is invalid.

### Working conclusions

1. Eugene's advantage is architectural discipline, not a magic prompt:
   warm once, race a tiny per-model frame set, select by latency/fire rate,
   fill immediately, return only fired singles, and cap the returned prefix by
   measured replay cost.
2. Timmy S21 spends budget on a broad screen/verify/UCB pipeline, relies on a
   wall-clock/p95 gate, has no untimed model-load warm-up, and places its new
   exploitation stage after an already budget-exhausting loop.
3. S22 should not patch Stage E in place while retaining Stage D. The minimum
   interpretable build is a clean S21-template transplant onto Eugene S18's
   proven control flow, or an exact S18 control if teammate artifact reuse is
   allowed within the team.
4. The honest target for the next single-post submission is to recover the
   proven 86–89 band first. A 90–100 target requires either favorable variance,
   a validated tail/capacity gain, or a separate score-density mechanism; it is
   not supported by S21's current multipost evidence.

### Next iteration

- Map every recent Kaggle ref to its exact artifact and correct stale docs.
- Quantify S21 versus S18 probe count, candidate count, and stopping rules.
- Query the completed graph and use it to check for missed call/data paths.
- Produce a ranked S22 experiment matrix with one mechanism per upload.

## Iteration 2 — exact architecture diff and causal failure proof

**Recorded:** 2026-08-30 16:08 WIB

### Evidence collected

- Latest Eugene branch was inspected from a clean clone at commit `002a038`.
  Frozen notebook payloads, release manifests, and tests agree byte-for-byte.
- Eugene S18 attack source: 460 lines, 13 functions, one class. Timmy S21:
  2,433 lines, 99 functions, one class. Size is not itself a scoring defect;
  it made the active path and ineffective tests materially harder to audit.
- S16→S18 is a controlled packing ladder. S18 changes only
  `REPLAY_SAFE_FRAC` from 0.97 to 0.99. S18→S19 adds only a 64-candidate
  guarded tail at `_replay_stop`; prompt frames, race, and packing are fixed.
- S18 performs one untimed model-load warm-up, races three complete prompt
  frames twice, retains every fired race probe, selects by
  `median(latency) / (fires / probes)`, then fills that exact frame.
- Replay packing subtracts warm-up time and accumulates measured latency only
  for fired candidates. S21 instead gates on generation wall time and p95.
- S21 screens four probes, but `_compose()` ignores `screened`. Stage D has no
  convergence exit. An always-fire trace at cap 40 returned 2 verification and
  38 UCB candidates, with zero screen or Stage E candidates.
- `ATTACK_MODE=S21_FILL ./.venv/bin/python tests/test_attack_units.py` passes,
  proving the regression suite lacks an execution/effect assertion for Stage E.

### Score math

The SDK gives a successful unique single-post candidate 18 raw points and
aggregates two model rows as `(raw_gpt + raw_gemma) / 400`.

| Target | Gain over 88.155 | Perfect singles needed across rows | Average/model |
|---|---:|---:|---:|
| 90 | 1.845 | 41 | 20.5 |
| 95 | 6.845 | 152.1 | 76.1 |
| 100 | 11.845 | 263.2 | 131.6 |

S18 is equivalent to 1,959 perfect singles across both rows. S21 is only
1,710.7 single equivalents because its multipost raw values need not divide by
18. The observed gap is about 124 single equivalents/model.

### Conclusion

The certain defect explains why S21's claimed lever was not exercised; it does
not by itself explain all 11.175 LB because Stage D still performs a fill. The
highest-confidence remaining differences are Eugene's direct per-model frame
selection, retained calibration hits, measured replay-cost packing, and causal
one-mechanism releases.

## Iteration 3 — leaderboard calibration, public designs, and S22 decision

**Recorded:** 2026-08-30 16:08 WIB

### Evidence collected

- Public leaderboard snapshot: 4,189 teams; `TimmyTurner` rank 911, best
  88.155, 42 submissions. Median is 79.920. There are 487 teams at 90+, 190 at
  95+, and 107 at 100+.
- V19 remains pending. Its 64 perfect tail candidates/model can add at most
  `128 * 18 / 400 = 5.760`, giving a theoretical 93.915 ceiling.
- Public notebooks were downloaded rather than inferred from titles:
  - `ai-agent-security-v15`: S18-like validation/fill, Harmony frame, 0.98 cap.
  - `jed-slow-multipost`: that base plus `SLOW_MULTIPOST_N=3` and a 0.95 cap.
  - `ai-agent`: aggressive 0.9999 packing, k=10/8 burst tail.
  - `relay-push100`: warm-up, five terse single-post templates, retained
    calibration hits, time-aware Thompson selection, measured replay packing.
  Kaggle kernel metadata did not expose trustworthy scores, so these are design
  leads, not leaderboard proof.
- Refreshed Graphify output has 2,259 nodes, 4,545 edges, and 158 communities.
  Queries correctly surfaced `_run_impl`, `_compose`, `_probe_cost_s`, and the
  gateway replay path. It also reports 742 dangling endpoint warnings, so graph
  output is navigation evidence only; source and deterministic traces remain
  authoritative.

### Ranked hypotheses

1. **Certain:** S21's control flow and tests did not exercise the new lever.
2. **High confidence:** S18's tiny complete-frame race selects better hosted
   behavior than S21's pre-routed k2/k1 families and broad UCB path.
3. **High confidence:** measured fired-candidate replay accounting packs the
   safe prefix more reliably than a generation-wall/p95 gate.
4. **Small but certain:** retaining calibration hits avoids throwing away up to
   four successful S21 screen probes per model.
5. **Operational:** byte-frozen, one-mechanism diffs make scores interpretable.
6. **Unproven/high risk:** multipost or burst density may be required for 100,
   but Timmy's hosted multipost evidence is negative and public scores are not
   verified.

### S22 decision

1. Wait for V19; it is already the isolated tail experiment.
2. Freeze Eugene S18 as the control chassis. Do not patch S21 in place.
3. Test at most two additional single-post frames against S18's three frames on
   both real models. Gate on at least 3% lower `median_latency / fire_rate`, no
   more than 1 percentage-point fire loss, and no p90 regression over 5%.
4. If a candidate clears every gate, S22 changes only the frame-race set and
   omits the V19 tail. Otherwise do not manufacture a frame submission; exact
   S18 is the recovery/control artifact.
5. Combine a proven frame gain and proven tail only after both isolate positive.
   Treat 100 as a later density experiment, not an S22 promise.

Detailed execution and stop rules: `tasks/plan.md` and `tasks/todo.md`.

## Iteration 4 — durable handoff and verification

**Recorded:** 2026-08-30 16:08 WIB

- Refreshed Kaggle history: V19/ref `55883308` is still pending.
- Updated `HANDOFF.md` with a timestamped authority block and marked the prior
  S21 status, fill hypothesis, score model, and endgame headings historical.
- Added the official decode correction to the end of the append-only submission
  ledger and a correction banner to `dev_notes/S21_analysis.md`.
- Wrote `tasks/plan.md` and `tasks/todo.md`; no S22 attack code was created.
- `git diff --check` passes. The existing S21 unit suite had passed during the
  audit; its generated tracked SDK bytecode changes were restored afterward.
- Graphify artifacts exist and reflection is current. The graph's code topology
  remains valid because this iteration changed documentation only.

## Iteration 5 — frozen control recovery and five-frame RED/GREEN slice

**Recorded:** 2026-08-30 16:36 WIB

- Recovered Eugene S18 from commit `002a038` and verified the extracted
  `S22/attack.py` bytes: 25,746 bytes, SHA-256
  `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`.
- Proceeded without V19 as requested. The two conditional frames are the
  shortest distinct `relay-push100` shapes: `{payload} to {url}` and
  `http.post url={url} data={payload} now.`. They are public design leads, not
  claimed winners; no real-model battery result exists for this exact pair.
- Added five-frame effect and lineage tests first. Against frozen S18 the focused
  gate failed in four expected places: missing constants, three-frame tuple,
  six-probe race, and lineage mismatch.
- Added only the two constants and tuple entries, plus matching comments. The
  focused gate then passed `5 passed, 8 deselected`.
- The test reverses the three pinned byte transforms and recovers the exact S18
  hash, proving packing, fill, warm-up, selection, and replay-stop code is fixed.
- Current experimental source SHA-256:
  `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`.

Next: copy the proven deterministic S18 release tooling, adapt its lineage
guard to the pinned S22 diff, generate the notebook/manifest, then run full
release and SDK gates. No upload is authorized.

## Iteration 6 — deterministic release packet

**Recorded:** 2026-08-30 16:48 WIB

- Established the release RED gate before generation: the full S22 suite had
  `1 failed, 12 passed` because `S22/RELEASE/attack.py` did not exist.
- Adapted S18's deterministic builder and checker. The builder rejects any
  source hash drift and reverses exactly three pinned frame-related byte blocks
  to recover the 25,746-byte S18 SHA-256.
- Generated a clean two-cell notebook with a byte-exact base64 payload and the
  unchanged `KAGGLE_IS_COMPETITION_RERUN` server gate.
- Release checker passed with nine ordered provenance records. The full S22
  suite then passed `13 passed in 0.35s`.
- Frozen artifact identity at this checkpoint:
  - `S22/attack.py` and `S22/RELEASE/attack.py`: 25,901 bytes,
    `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`;
  - `S22/RELEASE/submission.ipynb`: 36,640 bytes,
    `689c9634d78fa60e0e8151e5662a9382a13b350f24528670e7b1f8291576a873`.
- The real-model battery remains unrun because the user explicitly directed
  work to proceed from logical assumptions without waiting. S22 remains a
  conditional artifact; deterministic gates prove causality and integrity,
  not score improvement.

Next: SDK validation and final release review, then prepare only a separate
conditional follow-up so S22's one-mechanism attribution remains intact.

## Iteration 7 — separate conditional frame-plus-tail union

**Recorded:** 2026-08-30 16:52 WIB

- S22 passed the SDK red-team structure validator without changing its frozen
  source or notebook bytes.
- Eugene S19/V19 is already the isolated tail-only experiment, so duplicating
  it would add no information. The useful next preparation is the exact union
  of S22's frame delta and S19's bounded tail, isolated under `S23/`.
- Started S23 from the frozen S22 source. Focused tests failed in four expected
  places before implementation: missing tail lineage block, missing constant,
  no appended tail, and no cap fill.
- Applied only S19's three mechanisms: `OVERPACK_TAIL_N=64`, clamp configured
  capacity to the SDK 2,000 limit, and append fresh winner-frame candidates
  only after an eligible replay-safe cutoff.
- Focused tests then passed `5 passed, 11 deselected`. They establish exact
  S22-prefix identity, identical live calls, a 64-candidate fresh tail, cap
  safety, and no tail after an environment fault, cap exit, or legacy deadline.
- S23 source identity: 26,611 bytes,
  `32cc018df05c534f747ad171ad7aa17af6f3df887f439caa67bbc927cbee1265`.

S23 remains non-uploadable until both dependencies are positive: S22 must score
at least 90 (or otherwise establish a frame gain), and T7 must classify V19/S19
as `tail-positive`. Packaging it now is operational preparation, not approval.

## Iteration 8 — S23 conditional release packet

**Recorded:** 2026-08-30 16:55 WIB

- Added S23 deterministic builder, independent checker, two-cell notebook,
  11-record manifest, experiment record, and explicit activation conditions.
- The first full suite run found one stale inherited S22 expectation: total
  candidate counts were asserted as 95/97 even though the S23 contract adds 64.
  The test now independently asserts S22 prefixes `(95, 97)` and S23 totals
  `(159, 161)`, proving the original packing boundary remains unchanged.
- Final S23 gates at this checkpoint:
  - full tests: `16 passed in 0.38s`;
  - release checker: pass, 11 provenance records;
  - SDK red-team validation: pass;
  - source/release bytes: 26,611,
    `32cc018df05c534f747ad171ad7aa17af6f3df887f439caa67bbc927cbee1265`;
  - notebook: 37,588 bytes,
    `612e6366b5e4bd7e160b8e570f82a4c6799ff69791b893e6af4215884ed1c8a2`.

This completes preparation only. T8 is not complete and S23 cannot be uploaded
until its two hosted evidence dependencies pass.

## Iteration 9 — joint integration gate and review correction

**Recorded:** 2026-08-30 17:01 WIB

- Five-axis review found no attack-source correctness, security, architecture,
  or performance blocker. Test names were clarified to describe their exact
  lineage and tail contracts; manifests were regenerated afterward.
- The first combined `pytest S22/tests S23/tests` collection failed before test
  execution because both directories exposed a top-level `test_release` module.
  Isolated suite success had hidden that integration defect.
- Renamed only S23's suite to `test_s23_release.py`, rebuilt its manifest, and
  reran the joint gate: `29 passed in 0.43s`.
- Both release checkers pass after the final test-path change. Both sources pass
  SDK red-team validation, all 12 Python files compile in memory, and
  `git diff --check` is clean.

Remaining: complete the incremental Graphify merge/health report, stage only
S22/S23 and their durable notes, review the staged diff for secrets and scope,
then create the planned local commit. No upload or push is authorized.

## Iteration 10 — incremental Graphify refresh

**Recorded:** 2026-08-30 17:12 WIB

- Incremental detection found 24 changed inputs: 12 code and 12 documents. Two
  known SDK credential fixtures remained skipped as sensitive.
- AST extraction produced 227 nodes and 443 edges. Gemini semantic extraction
  failed because the configured API key was invalid; one host-agent fallback
  covered all 12 documents with 69 nodes, 80 edges, and three hyperedges.
- Merge replaced stale nodes from re-extracted sources and produced a graph of
  2,508 nodes, 4,953 edges, and 145 communities. Diff from the prior graph:
  +288 nodes, +454 edges, -39 replaced nodes, and -46 replaced edges.
- Graph health is clean: zero dangling or missing endpoints, self-loops, exact
  duplicate edges, and directed/undirected endpoint collapses.
- Updated traversal starts directly from S23 lineage/default/prefix tests,
  S22 release builders, and the conditional evidence requirement. The token
  benchmark reports 27.9x reduction per query.
- Cost metadata under-reports this run as zero because host-agent usage was not
  available after the Gemini fallback. Graphify also warned that its installed
  skill text is 0.9.17 while the package is 0.9.46; the generated graph passed
  the current package's integrity gate.

Graph outputs remain generated/untracked and are intentionally excluded from
the isolated source/release commit.

## Iteration 11 — isolated local commit

**Recorded:** 2026-08-30 17:14 WIB

- Staged allowlist contained only `S22/`, `S23/`, `HANDOFF.md`, this
  investigation log, and `tasks/plan.md`/`tasks/todo.md`.
- Unrelated modified `attack.py`, `tests/test_attack_units.py`, and
  `dev_notes/submissions.md`, plus historical untracked files and generated
  Graphify outputs, remained unstaged.
- Staged whitespace check passed. The only credential-pattern scan match was
  prose documenting Graphify's invalid configured API key; no credential value
  or sensitive fixture was staged.
- Created one local atomic commit for the S22/S23 release work. No push and no
  Kaggle upload occurred.

## Iteration 12 — fresh hosted-score intake

**Recorded:** 2026-08-31 09:42 WIB

- Authenticated `kaggle competitions submissions` returned:
  - ref `55883308`: complete, **92.475** (user identifies this as Eugene V19);
  - ref `55888268`: complete, **87.390** (chronological/user-label match for
    Timmy S22; notebook metadata verification remains open);
  - ref `55889026`: complete, **79.020** (user identifies Eugene V20 as the
    ~79 result; exact version/ref metadata verification remains open);
  - refs `55892238` and `55895453`: pending (likely Eugene V21/V22 in order;
    exact mapping remains open).
- V19's isolated tail marginal is `92.475 - 88.155 = +4.320`. Relative to its
  preregistered maximum `+5.760`, observed/theoretical capture is `0.75`.
  Classify T7 as `tail-positive`.
- S22's frame marginal is `87.390 - 88.155 = -0.765`. Its hosted acceptance
  gate failed; the two extra frames must not be carried into the next build.
- V20 lost `13.455` versus V19 and `9.135` versus S18. Until its exact code
  delta is inspected, this is a stop signal rather than evidence for any one
  suspected mechanism.
- S23 cannot activate because its required frame dependency failed even though
  the tail dependency passed. The next experiment must branch from exact V19.

Next: prove version/ref/source hashes, isolate V19→V20/V21/V22 diffs, and rank
one-variable V19-based experiments. No upload or source implementation yet.

## Iteration 13 — exact API mapping and source provenance

**Recorded:** 2026-08-31 10:00 WIB

- Authenticated Kaggle API metadata maps refs to script versions directly:
  - Eugene V19 `345982069` / ref `55883308` / **92.475**;
  - Timmy S22 `346026772` / ref `55888268` / **87.390**;
  - Eugene V20 `346033952` / ref `55889026` / **79.020**;
  - Eugene V21 `346063944` / ref `55892238` / pending;
  - Eugene V22 `346092100` / ref `55895453` / pending.
  This supersedes Iteration 12's chronological qualifiers.
- Timmy S22's scored notebook embeds the exact local source hash
  `c94487df48ed4be22d7753cbb7fca7dc925ac16218f4f1ea7a9a86ce27ac90cb`.
  Its only effective delta from S18 is the five-frame expansion, so that lever
  failed its hosted acceptance gate.
- Repo V19/S19 source hash is
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
  It is exact S18 plus the 64-tail mechanism and a default-inert cap clamp.
  Kaggle rejects historical private-version pulls with 403, so the scored
  upload cannot be cryptographically rebound to this hash from the API.
- The current pulled Eugene notebook embeds
  `366ff1346b5d89a3545814abad8c4d765b2d8568a714b32bff99a4b00e61c826`:
  S18 plus a one-time runner-up-frame failover after six consecutive misses,
  with no V19 tail. It is presumed V22 from the current/latest pull; V20 and
  V21 source diffs remain unavailable.
- Historical raw submission files now resolve to deleted objects, and the
  submission-episode endpoint returns no rows. Per-model score attribution is
  unavailable and must remain unknown.
- Preserved dangling Eugene commit `002a03830b66e228bdb65daab2a79565d38f72cb`
  as local branch `archive/eugene-s19`. This touched no working-tree file and
  no remote.

Target arithmetic from the banked 92.475 uses the documented 0.045 aggregate
per successful single in one model row: 100 requires 168 additional successful
single-row equivalents in total (84/model only if perfectly balanced), while
110 requires 390 total (195/model only if balanced). These are ceilings math,
not forecasts.

Durable details: `dev_notes/kaggle_versions/README.md`. Next: replace the stale
S22 plan with V19-based decision gates, then refresh Graphify.

## Iteration 14 — resumed-state audit and V21 decode

**Recorded:** 2026-08-31 10:16 WIB

- Recovered the existing handoff, V19-anchored plan, artifact ledger, prior
  Graphify queries, and dirty-worktree state before making any implementation
  change. The prior causal decision remains valid: V19 tail64 gained +4.320;
  Timmy S22's frame expansion lost 0.765; V20's unknown bundle lost 13.455.
- Refreshed authenticated Kaggle team history. Eugene V21/ref `55892238`,
  script `346063944`, is now complete at **90.900**. V22/ref `55895453`, script
  `346092100`, remains pending.
- V21 is +2.745 versus S18 and -1.575 versus V19. Since its historical source
  is unavailable, this is bundle-level evidence only. V19 remains the banked
  control and no V21 mechanism may be inferred from the score.
- Queried the existing graph using vocabulary-constrained terms. It confirmed
  the relevant seams—scoring, replay packing, model-specific arms, and the
  Eugene/Timmy control lineage—but introduced no stronger causal evidence than
  the hosted one-diff results above.

Next: wait for or refresh V22, attempt source recovery without guessing, then
execute Checkpoint A. No new attack source, upload, push, or branch checkout.

## Iteration 15 — resumed inventory and evidence plan

**Recorded:** 2026-08-31 10:40 WIB

- Preserved the dirty `timmyv2` worktree and recovered prior handoff, score log,
  V19-anchored plan, artifact ledger, graph memories, and branch history.
- The latest established score ladder is V19 92.475, S22 87.390, V20 79.020,
  V21 90.900, with V22 pending at the last authenticated refresh.
- Queried the existing Graphify graph. Its useful comparison seams are replay
  cutoff/tail capacity, frame selection, candidate packing, model-specific
  arms, and SDK score accounting. Graph traversal is navigation evidence, not
  proof of a causal score effect.
- Selected an iterative experiment plan: refresh scores and notebook sources;
  build an exact code/score delta table; retain only isolated hosted effects;
  choose one V19-based next change with offline invariants and a rollback.
- No attack source, Kaggle upload, remote push, or active worktree switch was
  performed.

Next: refresh V22 and linked notebook metadata, then bind all recoverable
V19–V22 sources before interpreting score differences.

## Iteration 16 — live score, rank, and source-access refresh

**Recorded:** 2026-08-31 10:49 WIB

- Authenticated submissions still report V22/ref `55895453` pending. The
  completed comparison remains V19 92.475, S22 87.390, V20 79.020, and V21
  90.900.
- Downloaded the current leaderboard: 4,207 teams; `TimmyTurner` rank 277,
  best 92.475, 46 submissions, members `timsurreal,zombiespecz`. Counts are
  108 teams at 100+ and 55 at 110+; leader 147.530.
- Retried an authenticated historical pull for V19/script `345982069`; Kaggle
  returned HTTP 403. V20/V21 code remains unavailable, so their scores cannot
  support mechanism-level claims.
- The latest Eugene download still supplies only the presumed V22 snapshot,
  whose exact known delta from S18 is a six-consecutive-miss switch to the
  race runner-up and removal/absence of V19's tail.
- Competition documentation confirms replay-validated scoring across GPT-OSS
  and Gemma, independent public/private guardrail replays, and a September 1,
  2026 23:59 UTC deadline. Public reports independently reinforce the local
  finding that separate short single-post candidates often beat multipost
  chains on score per replay second; these reports are corroboration, not team
  causal evidence.

Next: compare the exact S18→V19, S18→S22, and S18→presumed-V22 diffs and
separate proven levers from score noise and unknown bundles.

## Iteration 17 — shared-control causal decomposition

**Recorded:** 2026-08-31 10:52 WIB

| Artifact | Exact known delta from S18 | Score | Delta from S18 | Evidence |
|---|---|---:|---:|---|
| Eugene S18/V18 | control | 88.155 | — | frozen source/hash |
| Eugene V19 | guarded 64-candidate winner-frame tail; inert cap clamp | 92.475 | +4.320 | isolated hosted delta; scored-upload hash still open |
| Timmy S22 | add two frames to the 3-frame race | 87.390 | -0.765 | isolated and byte-bound |
| Eugene V20 | source unavailable | 79.020 | -9.135 | unknown bundle only |
| Eugene V21 | source unavailable | 90.900 | +2.745 | unknown bundle only |
| Eugene V22 | presumed latest: six-miss runner-up failover, no tail | pending | — | current snapshot, version binding not closed |

The decisive arithmetic is exact:

`(V19 - S18) - (S22 - S18) = 4.320 - (-0.765) = 5.085 = V19 - S22`.

Subject to hosted variance and V19's remaining hash caveat, the full observed
gap is accounted for: Eugene added replay-capacity tail and gained; Timmy added
unmeasured frame choices and lost. S21→S22's +10.410 is not evidence for the
new frames because that step also replaced Timmy's 2,433-line screen/verify/UCB
chassis with Eugene's compact S18 path.

Why the compact path transfers:

1. one untimed model-load warm-up;
2. six interleaved probes across three complete frames;
3. retain all successful race probes;
4. select by observed median latency/fire rate and fill immediately;
5. return only fired single-post candidates;
6. charge actual elapsed cost to the ordered replay prefix and stop safely;
7. place blind capacity candidates after that prefix so replay truncation cannot
   displace validated findings.

S21 violated this discipline: screen hits were discarded, Stage D exhausted
capacity before Stage E, and tests asserted Stage E's presence rather than its
reachability/effect. S22 fixed the chassis but enlarged a noisy two-sample race
from three to five frames without real-model evidence, spending four extra
probes and increasing selection error.

Next: choose the tail size using target arithmetic, observed V19 capture, and
the gateway's prefix-preserving replay timeout behavior.

## Iteration 18 — cutoff recovery and scope lock

**Recorded:** 2026-08-31 10:56 WIB

- Recovered all prior notes, the exact score/ref/script map, branch tips,
  generated Graphify outputs, and the existing V19-based endgame plan.
- The worktree contains prior/user changes and generated artifacts. Preserve it;
  inspect teammate branches with `git show`/`git diff`, not checkout.
- Working assumptions are explicit: scores are 92.475/87.390 on Kaggle's scale;
  target is 100–110; this analysis may design but may not upload; only exact
  shared-control deltas receive mechanism-level causal weight.
- The next iteration will refresh hosted status and bind any new score before
  changing the experiment ranking.

No attack source, Kaggle upload, remote push, or branch checkout occurred.
