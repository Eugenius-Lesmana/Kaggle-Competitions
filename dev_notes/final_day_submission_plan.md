# Final-Day Submission Plan — Recovery Checkpoint

Updated: 2026-09-01 (active final-day planning pass)

## Live correction — 2026-09-01 22:07 WIB

- S25 Tail96/ref `55932157` is already pending; do not duplicate it.
- New ref `55942688`, submitted by `timsurreal` at 22:05 WIB, is pending and
  consumes the fifth slot. Limits are now five today / 57 lifetime / none
  available. Its script and hashes remain unbound.
- Tail96 adds at most 64 candidates across the two model rows versus V19:
  theoretical incremental ceiling `+2.880`, total **95.355** before variance.
  Select it over V19 only at `>=92.925`; otherwise retain V19.

## Live authority — 2026-09-01 21:17 WIB

- Authenticated submissions at 21:12 WIB: refs `55932157`, `55933430`,
  `55935763`, and `55935769` are still pending. Limits: four today, 56
  lifetime, **one remaining**.
- Public leaderboard: `TimmyTurner` rank **291**, score **92.475**; rank 200
  **95.680**; rank 100 **101.965**.
- The oldest pending run has exceeded nine hours. Do not wait for a decode:
  launch the fifth slot as byte-exact V19 now. At record time about 9h42m
  remained to the 06:59 WIB deadline, shorter than the documented common
  scoring interval.
- Exact V19 notebook was reverified from both the frozen archive and live
  Eugene clone: SHA-256 `cd65fe8e4b44cf99ad289974b590ccba2fe095b44e0b4e66ef4ffff9ac78c670`,
  embedding attack SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`.
- Recommendation remains a variance hedge. It has plausible top-200 option
  value but no defensible expected 100–110 claim. No unsubmitted mechanism has
  stronger hosted evidence.
- Final no-change refresh at **21:32 WIB**: the same four refs remain pending;
  authenticated limits remain four today / 56 lifetime / one available.

### Causal evidence matrix

| Artifact | Score | Effective change from best recoverable control | Decision | Confounder |
|---|---:|---|---|---|
| Eugene S18/V18 | 88.155 | compact three-frame fired-only chassis | shared control | one hosted draw |
| Eugene V19 | **92.475** | S18 + guarded Tail64 | bank; only strong positive isolated lever (`+4.320`) | scored-upload hash unavailable; hosted variance |
| Timmy S22 | 87.390 | S18 + two race frames | reject (`-0.765`) | one hosted draw |
| Eugene V20 | 79.020 | repo lineage labels best-first | reject | historical scored bytes not API-bound |
| Eugene V21 | 90.900 | unknown bundle | do not infer or rerun | source unavailable |
| Eugene V22 | 86.940 | repo lineage labels six-miss frame failover, no Tail64 | reject | historical scored bytes not hash-bound |
| Eugene V23 | 81.945 | repo lineage labels Tail128 | reject | historical scored bytes not hash-bound |
| Timmy S24 | 90.540 | exact V19 Tail64 -> Tail256 | reject larger unconditional tail (`-1.935`) | one hosted draw |
| Eugene V25 | 88.875 | byte-exact V19 control | proves material rerun variance (`-3.600`) | only two identical-code draws |
| Eugene V26 | 73.710 | V19 + multipost-4 | reject decisively (`-15.165` vs same-day V25) | one hosted draw, but large margin |
| Timmy S25 | pending | exact V19 Tail64 -> Tail96 | await; do not duplicate | no score yet |
| 3 Eugene runs | pending | one likely S27 hop-1; exact bindings unproven | await; never infer | historical pulls return 403 |

What Eugene did better than Timmy: preserve a compact measured prefix, retain
successful calibration probes, select among only three complete frames, fill
the winner immediately, return fired single-post candidates ordered by observed
findings/replay-second, stop on measured replay cost, then place bounded blind
capacity after the validated prefix. Timmy S21 discarded useful screen hits and
starved its fill stage; S22 recovered Eugene's chassis but added noisy frame
choices that lost against the same S18 control.

## Objective

Choose the final few Kaggle submissions for `ai-agent-security-multi-step-tool-attacks`, maximizing expected score before today's deadline without losing the V19 control.

## User-reported leaderboard history

| Eugene version | Script version | Score |
|---|---:|---:|
| V19 | 345982069 | 92.475 |
| V20 | 346033952 | 79.020 |
| V21 | 346063944 | 90.900 |
| V22 | 346092100 | 86.940 (assumed correction of `86940`) |
| V23 | 346201152 | 81.945 |
| V24 | 346274330 | 75.015 |
| V25 | 346292818 | 88.875 |
| V26 | 346341384 | 73.710 |
| Timmy S24 tail256 | 346189152 | 90.540 |

## Working assumptions

- Public leaderboard is today's only immediate feedback, but final selection should avoid obvious public-LB overfit.
- V19 is the immutable control; remaining experiments should change one causal variable each.
- Increasing the V19 tail from 64 to 256 is negative evidence against a larger unconditional tail.

## Evidence gathered

- Repository has an existing `graphify-out/graph.json`; queried rather than rebuilt.
- Recovery query rerun after interruption with graph-vocabulary terms; it again
  anchored on `Eugene Scored Ladder`, `Eugene S18 Control Chassis`,
  `S22 Causal Execution Plan`, and `S18 Direct Frame Selection`. No conflicting
  project relationship was found.
- Graph preferred sources: `Eugene S18 Control Chassis`, `Measured Fired-Candidate Replay Packing`, `S18 Direct Frame Selection`, and the S22 cutoff/tail test.
- Relevant local artifacts: `HANDOFF.md`, `dev_notes/S22_investigation.md`, `dev_notes/submissions.md`, `tasks/plan.md`, `S22/`, `S23/`, `S24/`, and downloaded Kaggle-version material under `dev_notes/kaggle_versions/`.
- Current worktree was already dirty. No submission code has been edited by this planning pass.

## Current hypothesis

The post-V19 search appears to have bundled or progressively accumulated changes. Scores show high variance and no monotonic improvement. The best remaining use of submissions is likely V19 revalidation plus one or two surgical ablations/restorations, not another broad strategy rewrite.

## Verified final-day state

- Authenticated Kaggle submission history: V26/ref `55921741` finished at
  **73.710**; S24/ref `55907229` is **90.540**.
- Morning submission-limit snapshot was five available / 52 lifetime; the live
  refresh below supersedes it.
- Official rules: five submissions/day and up to two final selections.
- Deadline: **2026-09-01 23:59 UTC = 2026-09-02 06:59 WIB**.
- Current leaderboard snapshot (2026-09-01 11:48 UTC): team TimmyTurner is
  rank **291** at 92.475; rank 200 is 95.680, rank 100 is 101.965.
- Competition pages conflict on runtime: Data Description and official FAQ say
  9,000 seconds/model; Evaluation says 18,000. Plan and code stay safe at 9,000.
- Community reports identical notebooks can score differently and scoring can
  take 8–18 hours. New attempts must be launched early; pending submissions may
  not be selectable at deadline.

### Live refresh — 2026-09-01 18:43 WIB

- Authenticated team history now has four submissions dated 2026-09-01, all
  pending: refs `55932157`, `55933430`, `55935763`, and `55935769`.
- Exact binding: `55932157` = Timmy S25 tail96 / script `346419345`;
  `55933430` = Eugene script `346432884`; `55935763` = Eugene script
  `346460501`; `55935769` = Eugene script `346460338`.
- Therefore only **one** of today's five submission slots remains. The old
  five-slot queue below is retained as historical reasoning, not the current
  execution plan.
- `kaggle competitions submission-limits` confirms: four today, 56 lifetime,
  **one remaining today**.
- Final refresh at approximately 18:55 WIB: all four refs remain pending and
  the quota still reports one remaining.
- V26/ref `55921741` is confirmed complete at **73.710**; V22/ref `55895453`
  is **86.940**; S24/ref `55907229` is **90.540**.
- Immediate blocker to choosing the last artifact: bind the four pending refs
  to exact notebook/script/source hashes, then use the final slot for the
  highest-value non-duplicate hedge.
- S25 is fully bound: Kaggle-normalized notebook SHA-256 `58d76e1b…` embeds
  attack SHA-256 `4e6d31a…`, exactly V19 with only tail64 -> tail96. Local
  release verification passes; the optional pytest executable is not installed
  in the default shell, so that redundant test command was not run.
- Historical pulls for all three pending Eugene script versions return HTTP
  403. Eugene's latest downloadable snapshot embeds attack SHA-256 `b96b83a0…`
  and bundles tail256 with slow-multipost4. It must not be used for the last
  slot: tail256 already lost 1.935 and the union is not attributable.
- Version-qualified output downloads misleadingly returned the same latest
  `b96b83a0…` file for every requested version; they do not bind historical
  pending scripts and must not be treated as evidence.

## Live `Eugene` branch recovery — 2026-09-01 19:27 WIB

- The workspace refs `Eugene` and `origin/Eugene` were stale at commit
  `40eb35cd3d38591ddd7ec6c46e79a3a991b42715` (2026-08-29 09:24 WIB).
- SSH fetch failed because no usable GitHub SSH key was available and the local
  `gh` token is invalid. A read-only HTTPS query succeeded; live branch head is
  `412ce0b02795e95136538c48d63d231c02f31c33` (2026-09-01 13:13 WIB). It was
  shallow-cloned to `/tmp/eugene-live-branch`; the dirty workspace was untouched.
- Live branch artifacts added after V19:
  - `S25/V25`: byte-exact V19 control, attack `3169466c…`, notebook
    `cd65fe8e…`. This binds Eugene V25 (`346292818`, ref `55916871`) to the
    reported `88.875`: an identical-code draw `3.600` below V19.
  - `S26/V26`: isolated `SLOW_MULTIPOST_N 1 -> 4`, Tail64 retained; attack
    `4e9a7dd4…`, notebook `16768f7c…`. Claimed theoretical rate gain is only
    about `1.11x`; documented risks include Gemma exposure and nonlinear replay
    cost. This binds Eugene V26 (`346341384`, ref `55921741`) to `73.710`, a
    `-15.165` regression versus the same-day V25 control and `-18.765` versus
    historical V19. Reject multipost-4 decisively.
  - `S27`: isolated calibrated hop-1 live validation; attack `fff81d3f…`,
    notebook `742c993a…`. It keeps Tail64 and excludes multipost; estimated upside
    is `0-1.44` points with whole-row timeout risk if replay cost is undercharged.
  - `S28`: byte-identical copy of `S26` despite its directory name; its notebook
    and manifest are exactly S26 (`16768f7c…` / `4e9a7dd4…`). It is not a fourth
    mechanism or independent hedge.
- The branch therefore confirms Eugene was testing a clean control, isolated
  multipost-4, and isolated calibrated hop-1. It does not contain the later
  downloaded `b96b83a0…` tail256 + multipost4 union, and its last commit predates
  later pending Kaggle scripts. Do not infer their identities from branch names.
- The branch also identifies V20 as best-first, V22 as frame failover, and V23
  as Tail128. Their reported scores (`79.020`, `86.940`, `81.945`) reject all
  three mechanisms; Tail128 is no longer a valid fallback.
- Decision impact: keep exact V19 as the default last slot. V25 proves a repeat
  can move `3.600` points without a byte change, so another exact draw has upside
  while the original `92.475` remains selectable. S26 is known-bad, S28
  duplicates S26, S27 is already represented by the likely V27 pending arm, and
  the latest tail256 + multipost4 bundle remains rejected.
- Kaggle refresh at approximately 19:29 WIB: refs `55932157`, `55933430`,
  `55935763`, and `55935769` are still pending. Current private-notebook pull is
  still `b96b83a0…`; historical ordinal pulls return HTTP 403, so the three
  pending Eugene script-to-hash bindings remain unproven.

## Live refresh — 2026-09-01 19:54 WIB

- Authenticated Kaggle API still reports refs `55932157`, `55933430`,
  `55935763`, and `55935769` as pending with no public score.
- Submission limits remain four today / 56 lifetime / exactly **one remaining**.
- The oldest pending run was uploaded at 11:52 WIB and has waited about eight
  hours. Queue latency now dominates the last-slot decision: waiting for a score
  before launching the fifth run risks leaving it incomplete at final selection.
- Decision unchanged: launch the exact V19 control immediately; do not wait for
  the four pending scores.
- Kaggle competition metadata confirms team rank **291**, deadline
  **2026-09-01 23:59 UTC / 2026-09-02 06:59 WIB**, and rank 200 at **95.680**.
  V19 needs `+3.205` to cross that public threshold. The observed exact-code
  V19/V25 spread is `3.600`, so another control draw has plausible top-200
  upside; no tested mechanism has a cleaner risk/reward case.
- Community evidence independently reports same-notebook score variation and
  typical 12–17 hour completion, sometimes over 24 hours:
  https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/735521
  and
  https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/734961.
  The competition host also confirms candidate count/message length increase
  replay time:
  https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/708272.
- V21 remains source-unrecoverable and scored `90.900`, `-1.575` versus V19.
  It is eligible as an existing final only if Eugene binds its mechanism; it is
  not a defensible last-slot rerun without those bytes.
- Frozen V19 artifact reverified: archive and live Eugene clone notebooks are
  byte-identical at SHA-256 `cd65fe8e…`; their embedded `ATTACK_SHA256` is
  `3169466c…`, and the competition-rerun server gate is present.

## Current one-slot execution plan — authoritative

1. **Ask Eugene for four bindings:** completed V21/script `346063944`, plus
   pending scripts `346432884`, `346460501`, and `346460338`. For each, request
   experiment ID, notebook SHA-256, embedded attack SHA-256, and one-line diff
   from V19. Branch chronology makes `346432884` likely S27 calibrated hop-1,
   but do not call that exact until its embedded hash is confirmed. The later
   two remain unbound.
2. **Use the last slot for another exact V19 rerun.** Use attack SHA-256
   `3169466c…` and notebook SHA-256 `cd65fe8e…` from the frozen archive. This is
   a third draw of the only 92.475 chassis; V25's exact-code `88.875` establishes
   that rerun variance is material. Safest path: have Eugene submit the existing
   V19 output at script version `345982069` directly if Kaggle permits. Otherwise
   import only `archive/eugene-s19:S19/RELEASE/submission.ipynb`; do not edit the
   latest notebook back toward V19 by hand.
3. **No tail fallback.** Timmy tail96 is already pending; Eugene V23 binds
   Tail128 to `81.945`; Timmy Tail256 scored `90.540`. Do not spend the last slot
   interpolating a ladder whose two larger tested rungs both lost.
4. **Submit immediately.** At the 19:54 WIB refresh only 11h05m remained until
   the 06:59 WIB deadline; the last job has a real risk of finishing too late
   for selection.
5. Record the new ref, script ID, upload time, normalized notebook SHA, embedded
   attack SHA, and the exact diff in this file as soon as Kaggle accepts it.

### Last-slot rejection list

- Latest Eugene `b96b83a0…` union: tail256 + slow-multipost4.
- V20 best-first, V22 frame failover, V23 Tail128, V26 multipost-4, or any
  descendant/combination of them.
- Tail128+, S22 frame failover expansion, calibrated-hop union,
  frame-portfolio code written under deadline, or any multi-mechanism bundle.

### Final-selection playbook

- Keep completed V19 `55883308` / 92.475 as Final #1 unless an exact-source
  candidate completes and clearly beats it.
- Final #2 decision order:
  1. a completed, source-bound pending arm that remains near the V19 band and
     changes attack-frame composition rather than only multiplying replay cost;
  2. a last-slot exact V19 rerun that clearly beats V19 (public improvement
     threshold: `>=92.925`);
  3. otherwise Timmy S22/ref `55888268` / `87.390`, whose exact source is bound
     and whose extra-frame pool is a real private-guardrail hedge.
- Tail96/tail256 change volume, not attack class. Prefer them over the structural
  fallback only if the team deliberately prioritizes the public proxy rather
  than private-guardrail diversification.
- Do not select V20/V23/V26 regressions or an unbound pending bundle merely
  because it is newer. V21/V22 become eligible only after source/mechanism
  binding; V22's known frame-failover score is weaker than the exact-source
  Timmy S22 hedge.
- Check status at 20:00, 22:00, 00:00, 03:00, and 05:00 WIB. Manually lock the
  two finals by **05:30 WIB**; never wait until the 06:59 deadline.

## Source recovery and causal evidence

- Exact intended V19 source recovered from
  `archive/eugene-s19:S19/RELEASE/submission.ipynb`: embedded attack SHA-256
  `3169466cc3a2f01fafaf6a0ca4adb335f7a5698334e18b89711eea7daf82ae32`;
  archive notebook SHA-256 `cd65fe8e4b44cf99ad289974b590ccba2fe095b44e0b4e66ef4ffff9ac78c670`.
- Exact V18 source SHA-256:
  `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`.
- V18 -> V19 is only: guarded winner-frame tail64 plus an inert hard-cap clamp.
  Score delta is +4.320.
- V19 -> S24 is only tail64 -> tail256. Score delta is -1.935.
- A three-point quadratic through tail0/V18, tail64/V19, and tail256/S24 has a
  purely exploratory vertex near tail143 (predicted 94.38). This is a search
  heuristic, not a causal model; hosted timing noise is a major confounder.
- Historical private V20–V26 revisions still return HTTP 403, so their scores
  remain bundle-level evidence. Do not attribute any individual mechanism.
- Superseded Eugene draft pulled after V26 had attack SHA-256
  `fff81d3f98b3112562617753418692236c46e71233a5933ec4937f81151e1236`.
  It is V19 tail64 plus 130 insertions/14 deletions implementing calibrated
  hop-1 probing after a full-hop race. Treat as an unsubmitted S27 candidate
  only after Eugene confirms that hash was not the scored V26 artifact.

## Superseded five-slot queue — historical rationale only

Launch early rather than waiting serially for scores:

1. **V19 exact control rerun** — tests the reconstructed source and hosted-noise
   level; it cannot prove the original scored upload's unavailable hash.
2. **V19 tail96** — conservative tail increase; exactly one constant changes.
3. **V19 tail128** — higher-upside midpoint below failed tail256; exactly one
   constant changes.
4. **Calibrated hop-1 draft (`fff81d3f…`)** — moonshot, only if confirmed
   unsubmitted and all offline gates pass; otherwise replace with V19 tail160.
5. **V19 frame-portfolio tail** — keep total tail64 and the validated V19 prefix,
   but distribute fresh tail candidates 32/16/16 across the three existing race
   frames. This is the structurally distinct private-guardrail hedge.

Do not submit V20–V26 descendants, tail256 again, S22/S23 frame expansion, or a
multi-mechanism combination.

## Superseded timing and decisions

- Target all builds/gates by **13:00 WIB** and submit by **14:00 WIB**.
- Treat **18:00 WIB** as a hard last-launch cutoff unless a slot is deliberately
  accepted as a likely-unselectable lottery ticket.
- Public decode around V19: `>=92.925` meaningful improvement; `92.025–92.925`
  noise/tie band; `<92.025` reject for the public lane.
- Final slot 1: original completed V19 unless a source-known candidate beats it
  by at least 0.450.
- Final slot 2: frame-portfolio hedge if it completes cleanly and is not a major
  public/runtime collapse; otherwise the best completed source-known non-control
  variant. Do not rely on an unrecoverable V21 bundle unless Eugene can bind it.
- Manually select final submissions by **05:30 WIB**, leaving 90 minutes of UI
  and coordination buffer.

## Superseded next actions

1. Ask Eugene whether `fff81d3f…` is post-V26/unsubmitted.
2. Materialize the five source-known variants without touching the dirty root
   `attack.py`; use isolated release directories and byte/hash manifests.
3. Gate each notebook for syntax, source round-trip, exact one-diff identity,
   candidate cap, V19 prefix preservation, and a short deterministic replay.
4. Submit early, record ref/script/hash immediately, and monitor completion.
5. Make the two manual final selections before the buffer cutoff.

## Recovery instruction

Resume from this file. Do not modify attack/submission code unless the user expands scope beyond planning.
