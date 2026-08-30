# S19 analysis and submission plan

## Decision

Build and submit `S19_S18_R099_REPLAY_CUTOFF_TAIL64`:

> exact S18 plus one 64-candidate tail, emitted only after an eligible
> replay-safe cutoff and only in the race-winning frame.

Do not add multipost, a new frame, a replay-fraction change, or a new selector.
S19 must be both a competitive attempt and a readable experiment. Its result
should answer one question: **does S18 leave scoreable replay capacity after its
validated prefix?**

## Why S18 is the anchor

Latest scores supplied by the user form a near-factorial ladder:

| Artifact | Score | Difference from S15 |
|---|---:|---:|
| S15 fixed-route V12 control | `84.950` | — |
| S16 three-frame race | `86.670` | `+1.720` |
| S17 bundled fixed-route packing arm | `86.580` | `+1.630` |
| additive S18 prediction | `88.300` | `+3.350` |
| S18 observed | `88.155` | `+3.205` |

The additive residual is `88.155 - 88.300 = -0.145`. That is strong enough to
freeze both S18 ingredients operationally: the direct three-frame race and
`REPLAY_SAFE_FRAC=0.99`.

It is not proof of causal additivity. Each artifact has one aggregate hosted
draw, per-row evidence is missing, and S17 bundled frame wording and budget
settings rather than isolating replay fraction. Identical public
implementations have also spanned several leaderboard points. The defensible
conclusion is narrower: **do not replace S18's validated path in S19.**

## Score economics

The bundled scorer gives a successful severity-5 finding with a fresh score
cell `16 + 2 = 18` raw, which normalizes to `0.09` points per row. Therefore:

- gap from S18 to 95: `95 - 88.155 = 6.845`;
- required improvement: about `6.845 / 0.09 = 76.06` successful unique-candidate
  equivalents per row after aggregation;
- 64 perfect tail candidates have a hard theoretical ceiling of `64 * 0.09 =
  5.76` points per row.

S19 alone cannot honestly promise 95. Its realistic gain is smaller because the
tail begins only after S18 has already packed 99% of its measured replay budget.
At the hosted 8,750-second inner replay budget, the explicit 1% reserve is 87.5
seconds, plus S18's excluded-next-candidate allowance. At historical 8.5–20.4
second candidate latency, only a fraction of the 64 candidates is likely to be
started before the deadline. The 64 value is a ceiling, not a requirement that
the gateway replay all 64.

The size is still rational for this final-window attempt:

- 8 candidates can leave known 87.5-second reserve unused on a fast row;
- 16 is the conservative capacity estimate but cannot capture an unexpectedly
  larger accounting gap;
- 64 remains bounded at 3.2% of the 2,000-candidate SDK cap;
- the gateway replays in list order and checks the deadline before each next
  candidate, so unreached tail entries do not displace the S18 prefix;
- local serialization and candidate validation are negligible compared with
  model inference.

## Exact mechanism

S19 has three source transforms relative to SHA-pinned S18:

1. define `OVERPACK_TAIL_N = 64`;
2. clamp configured `hard_n_cap` to `HARD_N_CAP=2000`;
3. when `_replay_stop()` fires, append fresh winner-frame messages only if the
   race completed, its winner fired, the prefix is non-empty, and capacity
   remains.

No tail message is sent to the live generation environment. Tail indices start
at `idx`, after every attempted S18 index, so their hosts and score cells are
fresh even when some live probes failed. Returned ordering is:

```text
[exact S18 successful race/fill prefix] + [0..64 fresh winner-frame candidates]
```

This ordering is load-bearing. The gateway validates the list, replays it
sequentially under an 8,750-second inner deadline, breaks when the deadline is
reached, and scores findings accumulated before that break. An outer deadline
adds 180 seconds of grace, but it does not make replay exceptions safe.

## Failure analysis and containment

| Risk | Consequence | S19 containment |
|---|---|---|
| Tail message does not fire | Spends residual time for zero | Use the empirically selected winner frame; keep tail behind all validated candidates. |
| Tail replay reaches inner deadline | Final candidate may be discarded | Gateway retains earlier validated findings and breaks. |
| Tail replay raises | Model evaluation can fail | Bound tail at 64; never add it after an environment fault or incomplete race. |
| Race selects the wrong frame | Tail repeats a weak frame | Preserve S18's proven race exactly; no new selector noise. |
| Candidate cap overflow | Gateway truncation or invalid assumptions | Clamp total returned candidates to 2,000 and the configured cap. |
| All race frames miss | Blind tail would be unsafe | Return the unchanged S18 fallback; tail eligibility fails closed. |
| Mid-fill environment failure | Untested additions could mask diagnosis | Return only S18 fired-so-far; no tail. |

### Why `SLOW_MULTIPOST_N=4` is excluded

The code exists, but it is not a free S19 addition:

- all audited high-scoring defaults leave it dormant at `1`;
- local comments claim four posts for about 3.6 times replay cost, only about a
  1.11-times rate improvement before hosted overhead;
- separate hosted evidence says growing multi-post history can scale roughly
  quadratically and previously plateaued far below the single-post regime;
- in S18, activation is gated by `chosen_template == FRAME_TEMPLATE`, not a
  trustworthy model identity, so Gemma can be exposed if it selects that frame;
- combining it with the tail would make any score uninterpretable.

It remains a separate, explicitly gated high-upside experiment after S19, not
part of the S19 upload.

## Mandatory acceptance gates

1. S18 base hash equals
   `a09ac2a8b42e64893705c0579356c03180df2a36e41622b1446463434f01f60a`.
2. S19 equals that base after exactly the three pinned transforms above.
3. `REPLAY_SAFE_FRAC == 0.99`, `FRAME_RACE_REPS == 2`, `BURST_K == 1`,
   `SLOW_MULTIPOST_N == 1`, `PROBE_HOPS == 0`, and
   `REPLAY_COST_COEF == 1.0`.
4. Synthetic cutoff keeps the entire S18 prefix byte/order-identical and adds
   exactly 64 fresh winner-frame candidates.
5. No tail on warm-up/mid-fill failure, all-zero race, cap exit, or legacy
   deadline.
6. Candidate messages and hosts are unique; returned count never exceeds 2,000.
7. Release `attack.py` equals canonical source byte-for-byte.
8. The generated notebook is clean, deterministic, exactly two code cells,
   embeds the canonical bytes and SHA-256, has no `ATTACK_MODE`, and serves only
   under `KAGGLE_IS_COMPETITION_RERUN`.
9. Manifest allowlist and every recorded digest verify.
10. Unit tests, SDK red-team validation, and the full S14 bundle check pass.

## Submission and evidence capture

Upload only `S19/RELEASE/submission.ipynb`. Before upload, record its SHA-256.
After Kaggle processes it, re-download or otherwise verify the scored notebook
hash and capture the gateway lines for:

- Phase-1 candidate count for GPT-OSS and Gemma;
- candidates replayed, validated findings, timeout flag, and row score for each
  public/private replay;
- any candidate index or exception at the cutoff.

Those fields distinguish three outcomes that an aggregate score alone cannot:

1. **more candidates replayed and scored:** real residual capacity; S19 is a
   valid next anchor;
2. **64 returned but no extra replayed:** ledger already saturates Phase 2;
   future work must improve score per replay-second;
3. **tail candidates replayed but not scored or raised:** winner-frame transfer
   is unreliable without live validation; keep S18.

Do not edit the scored artifact after submission. Record the result in
`EXPERIMENT.md`; any follow-up receives new source bytes and a new experiment ID.
