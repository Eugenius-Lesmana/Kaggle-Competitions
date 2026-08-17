# Submission log — AI Agent Security (AIAgentSecurity-Eugene)

One entry per Kaggle submission. Never delete rows; annotate with what we
learned. Score rows: leaderboard shows the aggregate; the CSV written by the
rerun has per-(model, guardrail) rows.

**Metric units (decoded from S1): the leaderboard is in RAW-equivalent
units = 200 × Σ(CSV row scores)**, i.e. it un-normalizes the per-row
min(1000, raw/200) values and sums. Proof: 4 capped rows sum to ≤ 4000, but
we scored 4215 and #1 has 137130. So "leaderboard points ÷ 200" = sum of the
4 normalized rows; "÷ 800" ≈ avg normalized row.

Predicted vs actual decoding (r = actual / predicted_public, in normalized
row units):

| r | Diagnosis | Action |
|---|---|---|
| ≈1.0 | pipeline + private row behave like public lab | scale N, tune families |
| ≈0.5 | private rows ≈ 0 (private guardrail screens `data` or blocks marker) or replay truncation | S3a/S3b A/B; check per-row CSV |
| ≈0 | pipeline bug (harvest empty / INVALID / CSV placeholder) | debug from rerun logs, do not resubmit blind |

## S1 — SAFE baseline (v2, first score)

- **Date**: 2026-08-16 (target)
- **attack.py**: v2 (sha256 logged by check_notebook_sync.py at build time)
- **Config**: GEN_CAP_S=1200, N_MAX=20, N_MIN=12, MODEL_ALLOC_S1=12600,
  ships ≤20 candidates/model in measured-raw order + CD/lottery insurance
- **Gates**: aicomp validate ✅ · local_check (public raw=2162/norm=10.81,
  20 cands; permissive raw=2236) ✅ · unit tests ✅ · gateway relay 90s ✅ ·
  timeout-path ✅ · notebook sync ✅
- **Predicted**: public rows ≈ 10-11 normalized each IF gpt_oss/gemma comply
  like the stub (real-model compliance is the unknown being measured);
  aggregate ≈ 20-40 if compliance ≥ 50%
- **Purpose**: (1) prove the pipeline end-to-end (beat the 0-score quartile),
  (2) measure real-model compliance rate + real probe latency from elapsed
- **Result**: **4215 points, 1485th / 1655** (top-10: 113000–137130).
  **r ≈ 0.97 vs the public-row prediction** — the pipeline and the attack
  design are fully validated; the old "aggregate 20–40" framing was in the
  wrong units (see metric note above). Decode: Σ norm ≈ 4215/200 = 21.08 ≈
  2 public rows at ~10.5 norm each (~2100 raw, ~97% of the stub's 2162)
  with private rows ≈ 0 — pending per-row confirmation from the rerun log.
  Real-model compliance ≈ stub; the ONLY limit was self-imposed volume
  (20 ships × 8 posts × 16 ≈ 2560 raw ceiling per row; we got ~2100).
  Gap to top-10: 137130/200 ≈ 686 norm ≈ 171/row ≈ 34k raw/row — that is
  the replay-throughput ceiling (8750s ÷ per-post latency), so the leaders
  saturate replay time and likely score under the private guardrail too.

## S2 — THROUGHPUT (v2, fill the time budget)

- **Date**: 2026-08-17 (target)
- **attack.py**: v2-s2 (sha256 e21d476b6f94fbc3508dcaedda6a2e13df7ce7c4be09a9ccf154d18f87a21fcf)
- **One lever changed**: scale. N_MAX 20→220, GEN_CAP_S 1200→7800 (gateway
  allots 8750s generation per model), `_ship_size` → replay-capacity formula
  `0.80 × 8750s / (tbar + 3s)` (per-session tbar), sibling fill to n_target.
  No family/template changes.
- **Gates**: aicomp validate ✅ · unit tests ✅ (incl. new _ship_size table;
  fixed a leaked TBAR_DEFAULT_S monkeypatch in test_broken_envs) ·
  local_check --budget 600: **public raw=28162 / norm=140.81** with 220
  candidates (219 cells, 1732 marker posts ≈ 7.9/cand), permissive 28236 ✅ ·
  gateway relay 90s ✅ · timeout/harvest ✅ · notebook sync ✅
- **Predicted**: public rows ≈ 130–140 norm each if compliance holds at
  S1's ~97% of stub (n_target self-sizes 110–220 by measured tbar; replay
  truncation is graceful and keeps the best prefix). Leaderboard ≈
  200 × (2 × ~135 + private 0..small) ≈ **54000–56000**, i.e. ~1485th →
  rough mid-pack or better. Private rows expected ≈ 0 (unchanged families).
- **Purpose**: (1) capture the ~13× volume multiplier, (2) measure real
  tbar / ships from the rerun log, (3) per-row values decide S3 (private
  A/B vs mega-candidates).

## Template

- **Date**:
- **attack.py sha256**:
- **One lever changed**:
- **Predicted**:
- **Result / r**:
- **Decision**:
