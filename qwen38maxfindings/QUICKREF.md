# Quick Reference: S14/S15 Diagnosis & S16 Strategy

## What Happened

| Sub | Ref | Score | Status |
|---|---|---|---|
| S14_SINGLEFILE | 55792978 | blank | COMPLETE (zombie) |
| S15_SINGLEPURE | 55794899 | **72.095** | COMPLETE |
| mystery | 55797222 | blank | COMPLETE (zombie) |

## Why S15 = 72 vs Rival = 80

1. **S15 ships ~1227 synthetic siblings** (unverified, never probed) that waste replay budget
2. **Gemma arm fire rate likely <90%** (fb1_demo/fb1_notex untested on hosted gemma)
3. **Per-candidate replay cost ~9.6 sec** (same as rival, not optimized)

## Why S14 Zombied

Likely Kaggle-side infra (total wall time ≈ 14.6 hours ≈ 15-hour limit). Not a code bug.
Re-upload S14 bytes to confirm.

## Path to 120+

**Core insight**: Per-candidate replay cost must drop from 9.6 → 6 sec.

| Lever | Impact |
|---|---|
| Ultra-short URLs (`http://q{i}/p` vs `https://q{i}.test/p`) | -33% URL length → less prefill |
| Keep-only-fired shipping (drop synthetic siblings) | No wasted replay on unfired |
| Reduced stage overhead (skip A, reduce B/C) | More generation budget for fill |
| Rival's plain template on gemma arm | Higher fire rate than untested variants |
| Drop fe1_dual (multi-predicate) | 2 hops = 2× cost, only +4 raw. Not worth it. |

## Critical Discovery: EXFILTRATION Fires Per Event

Each http.post event with SECRET_MARKER = 1 EXFIL predicate = 16 raw.
A drip with 8 posts = 128 raw per finding. BUT replay cost scales O(posts²).
**Singles still maximize findings per second** (confirmed by prefill model).

## Files in This Folder

- `ANALYSIS.md` — Full deep analysis (scoring, rival autopsy, economics)
- `S16_IMPLEMENTATION.md` — Concrete code changes for S16 build
- `QUICKREF.md` — This file (one-page summary)

## Next Actions

1. Re-upload S14 bytes (diagnose zombie)
2. Build S16 (ultra-short + keep-only-fired + reduced overhead)
3. Upload S16, decode vs 120 target
4. Iterate S17+ based on decode
