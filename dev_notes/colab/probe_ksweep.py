"""Gemma K-SWEEP battery (S13 validation) — 2026-08-25 round 4.

Decision question: S13_DEEPGEMMA ships fd8c4 (depth-8, k=4 URLs/msg)
assuming yield stays ~1 post/message when the list shortens from 8 to 4
URLs (round-3 batteries only measured k=8 deep ladders). If k=4 collapses
yield, stage-B will catch it hosted-side but we want to know NOW.

Also probes k=2 (extreme) to map the curve, with fs5_short/fb3_bare anchors.

Run:  python probe_gemmaksweep.py   (after bootstrap_q3.sh)
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time

sys.path.insert(0, "/content")
sys.path.insert(0, "/content/sdk")
os.environ["GEMMA_MODEL_PATH"] = "/content/models/gemma-4-26B-A4B-it-UD-Q3_K_XL.gguf"

import attack  # noqa: E402
from kaggle_evaluation.jed_attack_134815.gemma_model_server import (  # noqa: E402
    SPEC as GEMMA_SPEC,
)
from kaggle_evaluation.jed_attack_134815.gguf_model_server import (  # noqa: E402
    GgufModelServer,
)
from aicomp_sdk.core.env.sandbox import SandboxEnv  # noqa: E402
from aicomp_sdk.guardrails.optimal import Guardrail as OptimalGuardrail  # noqa: E402

FIXTURES = "/content/sdk/aicomp_sdk/fixtures"
SEED = 123
RESULTS = "/content/results.jsonl"

# k-sweep at fixed depth 8 + anchors (fd8c4/fd6c4 are REGISTERED builders)
LOCAL_BUILDERS = {
    "fd8k2": attack._make_fd(8, k=2),
}
FAMILIES = [
    "fd8c4",        # THE shipped shape — validate its yield prior
    "fd8k2",        # extreme compact: maps the k-curve down
    "fd6c4",        # shipped secondary depth
    "fs5_short",    # anchor (registered, k=8, depth 5)
    "fb3_bare",     # anchor (long-form, round-2 winner)
]
INDICES = [1, 2]


def append(rec: dict) -> None:
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def builder(fam: str):
    return LOCAL_BUILDERS.get(fam) or attack.FAMILY_BUILDERS[fam]


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
            "model": "gemma", "family": family, "idx": idx,
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
                if r.get("model") == "gemma" and not r.get("err"):
                    done.add((r["family"], r["idx"]))
            except Exception:
                pass
        if done:
            print(f"[resume] {len(done)} pairs already measured", flush=True)

    server = GgufModelServer(GEMMA_SPEC)
    t0 = time.monotonic()
    server.load_model()
    print(f"[gemma] loaded (full offload) in {time.monotonic()-t0:.0f}s", flush=True)

    for fam in FAMILIES:
        run_family(server, fam, done)
        by_fam: dict[str, list[dict]] = {}
        for l in open(RESULTS):
            r = json.loads(l)
            if r.get("model") == "gemma":
                by_fam.setdefault(r["family"], []).append(r)
        print("\n=== RUNNING SUMMARY ===", flush=True)
        for f, rs in by_fam.items():
            posts = sum(r["posts"] for r in rs) / len(rs)
            lat = sum(r["lat_s"] for r in rs) / len(rs)
            raw = sum(r["raw"] for r in rs) / len(rs)
            print(f"  {f:12s} posts={posts:5.1f} lat={lat:6.1f}s "
                  f"raw={raw:6.1f} raw/s={raw/(lat+3.0):5.2f}", flush=True)
    server.unload()
    gc.collect()
    print("KSWEEP BATTERY COMPLETE", flush=True)


if __name__ == "__main__":
    main()
