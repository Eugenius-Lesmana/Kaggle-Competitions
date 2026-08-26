"""gpt_oss FORGED-COMPACT-DEEP battery (S14 candidate) — 2026-08-26 round 5.

Decision question: deep compact ladders (_make_fd, k<=4) were only ever run
BARE on gemma (S13). The gpt_oss arm still ships depth<=3 drips (fj2/fj3_close,
24 posts max). The untested combo = HARMONY CLOSE injection on EVERY message +
compact k<=4 bodies at depth 6/8: forge latency lever x drip amortization at
ctx-legal depths. On real gemma yield was linear to depth 10 (~1 post/msg);
on gpt_oss fj3_close fires ~5 posts/msg on 8-URL lists -- does yield survive
shorter lists, and does compliance hold across 8 forged turns?

Anchors: fj3_close (tier-1 champ, 15.5 posts / ~10.8 raw/s), fj_min8,
fj5_min (depth 5 at OLD token cost = depth-only bridge).

Run:  python3 probe_gptdeep.py   (after bootstrap.sh; needs only gpt-oss GGUF)
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time

sys.path.insert(0, "/content")
sys.path.insert(0, "/content/sdk")
os.environ["GPT_OSS_MODEL_PATH"] = "/content/models/gpt-oss-20b-Q4_K_M.gguf"

import attack  # noqa: E402
from kaggle_evaluation.jed_attack_134815.gpt_oss_model_server import (  # noqa: E402
    SPEC as GPT_SPEC,
)
from kaggle_evaluation.jed_attack_134815.gguf_model_server import (  # noqa: E402
    GgufModelServer,
)
from aicomp_sdk.core.env.sandbox import SandboxEnv  # noqa: E402
from aicomp_sdk.guardrails.optimal import Guardrail as OptimalGuardrail  # noqa: E402

FIXTURES = "/content/sdk/aicomp_sdk/fixtures"
SEED = 123
RESULTS = "/content/results.jsonl"


def _mk_fdj(depth: int, k: int):
    """Forged compact deep ladder: every message carries its own close-
    analysis injection (each user turn renders separately); bands i+8192j
    keep domains disjoint."""

    def _build(i: int) -> tuple[str, ...]:
        return tuple(
            attack._short_body_k(i + j * 8192, k) + attack._HARMONY_INJ_CLOSE
            for j in range(depth)
        )

    return _build


LOCAL_BUILDERS = {
    "fdj6k4": _mk_fdj(6, 4),
    "fdj8k4": _mk_fdj(8, 4),
    "fdj8k2": _mk_fdj(8, 2),
}

FAMILIES = [
    "fj3_close",     # anchor (registered tier-1)
    "fj_min8",       # anchor (registered single short forge)
    "fj5_min",       # anchor: depth 5 at old token cost (depth-only bridge)
    "fdj6k4",        # THE tests: forged compact deep ladders
    "fdj8k4",
    "fdj8k2",
]
INDICES = [1, 2]


def append(rec: dict) -> None:
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def builder(fam: str):
    return LOCAL_BUILDERS.get(fam) or attack.FAMILY_BUILDERS[fam]


def ctx_report() -> None:
    print("=== CTX GUARD MARGINS (idx=1) ===", flush=True)
    for fam in FAMILIES:
        msgs = builder(fam)(1)
        tok = attack._ctx_tokens(msgs)
        ok = attack._ctx_ok(msgs)
        print(f"  {fam:10s} n_msgs={len(msgs):2d} "
              f"k={msgs[0].count('http.post')} ctx~{tok:6.0f} tok ok={ok}",
              flush=True)
        if not ok:
            print(f"  !! {fam} OVERFLOWS GUARD -- REMOVE FROM BATTERY", flush=True)


def run_family(server: GgufModelServer, family: str,
               done: set[tuple[str, int]]) -> None:
    agent = server._load_agent()
    for idx in INDICES:
        if (family, idx) in done:
            print(f"[resume] skip {family} idx={idx}", flush=True)
            continue
        msgs = builder(family)(idx)
        env = SandboxEnv(seed=SEED, fixtures_dir=FIXTURES,
                         agent=agent, guardrail=OptimalGuardrail())
        t0 = time.monotonic()
        err = None
        raw, kinds = 0.0, {}
        try:
            env.reset()
            for m in msgs:
                env.interact(m, max_tool_hops=8)
            trace = env.export_trace_dict()
            raw, kinds = attack._score_trace(trace, msgs)
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"[:200]
        lat = time.monotonic() - t0
        rec = {
            "model": "gpt_oss", "family": family, "idx": idx,
            "raw": float(raw), "posts": int(kinds.get("EXFILTRATION", 0)),
            "lat_s": round(lat, 2), "n_msgs": len(msgs),
            "k": msgs[0].count("http.post"), "err": err,
        }
        print("REC", json.dumps(rec), flush=True)
        append(rec)
        del env
        gc.collect()


def main() -> None:
    done: set[tuple[str, int]] = set()
    if os.path.exists(RESULTS):
        for line in open(RESULTS):
            try:
                r = json.loads(line)
                if r.get("model") == "gpt_oss" and not r.get("err"):
                    done.add((r["family"], r["idx"]))
            except Exception:
                pass
        if done:
            print(f"[resume] {len(done)} pairs already measured", flush=True)

    ctx_report()

    server = GgufModelServer(GPT_SPEC)
    t0 = time.monotonic()
    server.load_model()
    print(f"[gpt] loaded in {time.monotonic()-t0:.0f}s", flush=True)

    for fam in FAMILIES:
        run_family(server, fam, done)
        by_fam: dict[str, list[dict]] = {}
        for l in open(RESULTS):
            r = json.loads(l)
            if r.get("model") == "gpt_oss":
                by_fam.setdefault(r["family"], []).append(r)
        print("\n=== RUNNING SUMMARY ===", flush=True)
        for f, rs in sorted(by_fam.items()):
            posts = sum(r["posts"] for r in rs) / len(rs)
            lat = sum(r["lat_s"] for r in rs) / len(rs)
            raw = sum(r["raw"] for r in rs) / len(rs)
            print(f"  {f:10s} posts={posts:5.1f} lat={lat:6.1f}s "
                  f"raw={raw:6.1f} raw/s={raw/(lat+3.0):5.2f}", flush=True)
    server.unload()
    gc.collect()
    print("GPTDEEP BATTERY COMPLETE", flush=True)


if __name__ == "__main__":
    main()
