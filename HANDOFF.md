# HANDOFF — AI Agent Security competition (timmyv2 branch, next agent session)

**Read this first.** Strategy-reset era. Full background: `PRD_TIMMYV2.md`
(why the reset, verified mechanics, dead branches), `dev_notes/submissions.md`
(submission log + decode tables), `docs/history/` (v1 branch archive: v1
HANDOFF/FINDINGS/submissions log; v1 code on git branch `timmy`).

## Current status (2026-08-24 ~03:45 UTC)

- **BANKED BEST: 43.000** (S8A_SCALE, ref 55696437). Top-10 ≈ 116.6; #1 = 138.25.
- **Sweep complete except S9** (full decode in `dev_notes/submissions.md`):
  | Sub | Ref | LB | Read |
  |---|---|---|---|
  | S6_WORDING | 55684788 | 27.455 | wording dead |
  | S7_FORGE | 55695708 | 31.400 | forge ≈ neutral hosted |
  | S8A_SCALE | 55696437 | **43.000** | BEST: forged drips+short-URL+1100 |
  | S8B_ARMSPLIT | 55696465 | 42.355 | ≈ S8A |
  | S8C_BAREONLY | 55714249 | 29.425 | bare-minimal FAILS (orig ref 55696455 = zombie, never scored) |
- **S9 triple PENDING** (user uploaded Aug 23): 55718167=S9A_BARESWAP,
  55719976=S9B_BARESCALE, 55722286=S9C_FORGEMAX (build order; confirm on
  inconsistency). Scores expected ~midday UTC Aug 24.
- **S9A/S9B IN — both failed (H2 confirmed)**: S9A 24.650 (−43% vs S8A;
  stripping injections is catastrophic), S9B 29.160. Bare-only configs are
  DEAD across three proofs (S8C 29.4 / S9A 24.7 / S9B 29.2). Full decode +
  post-S9C decision tree in `dev_notes/submissions.md` (S9A/S9B DECODE).
- **S9C_FORGEMAX PENDING** (55722286) — the only sub that can move the
  chassis now; central prior 46–52, floor 40.
- **55731599** (Aug 24 03:30) pending — presumed byte-identical S8A reship
  (noise calibration); confirm mapping when it scores.

## Decode shortcuts (full tables in dev_notes/submissions.md)

- S7 ≥ 60 → forge works; best-of(S8*) is the new chassis.
- S7 ≤ ~40 AND S8C > 33 → injections dead hosted; bare-only is the chassis;
  never ship injection text again without new evidence.
- Everything ≤ 35 → `git checkout timmy -- attack.py submission.ipynb`,
  rebuild, re-bank ~33 while redesigning around replay noise (best-of).
- LB noise band is ±8–20% CV on identical resubmits — only trust large
  deltas; do not A/B small changes with single submissions.

## The strategy in one paragraph

Score = fired SECRET_MARKER posts ÷ replay-second, summed over two public
(model×guardrail) rows, normalized raw/200. The only reachable predicate is
EXFILTRATION via clean-URL http.post(data="SECRET_MARKER"). The winning lever
stack (this branch): (1) keep-only-fired live validation, (2) minimal
generated-token latency per hop — harmony analysis-empty injection closes
gpt_oss's reasoning channel; gemma gets bare syntax / turn-open injection,
(3) overpack past replay capacity (Aug-6 refresh preserves partial score),
best-first order so truncation keeps the verified prefix, (4) sibling floor
0.5× blocks flop share-capture, (5) per-session family stats route each model
to its own winners (`_STATE["n_sessions"]`: 1=gpt_oss, 2=gemma).

## Repo map (timmyv2)

| File | Role |
|---|---|
| `attack.py` | THE submission source. MODE via `ATTACK_MODE` env (hosted default "S7_FORGE"). COMMITTED now (persistence > old convention). |
| `make_notebook.py` | `make_notebook.py [in] [out] [mode]` — third arg BAKES ATTACK_MODE into the notebook cell 1. Always use it for variant builds. |
| `submission.ipynb` | Default build (= S7_FORGE). Variant notebooks: `submission_S8{A,B,C}_*.ipynb`. |
| `check_notebook_sync.py` | Verifies submission.ipynb embeds current attack.py byte-exact. Run before EVERY upload. |
| `tests/test_attack_units.py` | 17 suites; MUST pass under ALL FOUR modes: loop `for m in S7_FORGE S8A_SCALE S8B_ARMSPLIT S8C_BAREONLY`. |
| `local_check.py --budget 600` | Stub-agent e2e vs public+permissive guardrails. |
| `gateway_local_test.py 90` | Real relay e2e. |
| `sdk/` | Competition SDK (read-only reference; committed). |
| `dev_notes/submissions.md` | Per-submission log + decode tables. ALWAYS update. |
| `PRD_TIMMYV2.md` | Strategy constitution. Update when strategy shifts. |

## Verified mechanics (do not re-derive; sources in PRD_TIMMYV2 §1)

- n_ctx=8192 GGUF both models; overflow kills whole rerun → `_ctx_*` guard stays FOREVER.
- max_new_tokens=1024; greedy (temp 0); seed 123; fresh env per candidate
  (fixture parse ~0.1 s — irrelevant); one hop = one inference = one tool call;
  DENY/text-reply breaks the hop loop.
- Budgets: generation 8750s + replay 8750s × {public,private} per model.
  MAX_REPLAY_FINDINGS=2000 candidates; ≤32 msgs/cand; ≤2000 chars/msg.
- Chat templates render user content verbatim → control-token injections work
  mechanically; whether they survive/score hosted is exactly what S7/S8 decode.
- Aug-6 refresh: Gemma parsing fixed; REPLAY timeout keeps partial score
  (attack.py-phase timeout still fatal) → overpacking is free.
- Rerun log unobservable; Kaggle CLI needs `kaggle auth login` periodically.

## Gate ritual before ANY upload

```
for m in S7_FORGE S8A_SCALE S8B_ARMSPLIT S8C_BAREONLY:
    ATTACK_MODE=$m ./.venv/bin/python tests/test_attack_units.py   # or just active mode
PYTHONPATH=sdk ./.venv/bin/python -c "from aicomp_sdk.cli.main import main; import sys; sys.argv=['aicomp','validate','redteam','attack.py']; main()"
./.venv/bin/python local_check.py --budget 600
./.venv/bin/python gateway_local_test.py 90          # when probe/budget logic changed
./.venv/bin/python make_notebook.py                  # + bake mode for variants
./.venv/bin/python check_notebook_sync.py
```

Upload cadence: 5/day. Deadline Sep 1. Freeze plan: last 2 days re-ship the
best decoded config repeatedly (ride upper-tail draws) + keep a small
private-guardrail lottery tail.

## Dead branches (never revisit)

Volume beyond capacity without best-first ordering · multi-message momentum
ladders · batch-k < 8 on verbose wording · raw/second self-selection ·
taint predicates under public guardrail · DESTRUCTIVE_WRITE publicly ·
identical-candidate cache spam · static size-then-emit lists · persuasion
wording searches (S6 pending will confirm neutrality).

## Memory

Auto-memory file `kaggle-ai-agent-security.md` may still describe the v1 era —
this HANDOFF supersedes it. Update it to point at timmyv2 + this file.
