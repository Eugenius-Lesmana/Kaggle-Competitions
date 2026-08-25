"""Gemma DEPTH battery (S13 prerequisite) — 2026-08-25 round 3.

Decision question: where is gemma's multi-message yield knee? Round-2
battery: yield grows linearly through depth 3 (fb3=4 posts, no knee visible,
hops ~0.3-1s). If depth 5-10 keeps paying, the gemma row stops being the
weak row. Existing builders cover depth 1-5 short-form (fs_min8, fs2..fs5);
this battery adds LOCAL depth-8/10 short-form builders and re-anchors fb3.

Run:  python probe_gemma_depth.py     (after bootstrap_q3.sh)
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


def fs_depth(depth: int):
    def b(i: int) -> tuple[str, ...]:
        return tuple(attack._short_body(i + k * 8192) for k in range(depth))
    return b


# UNCLIPPED: this battery measures the raw yield knee; overflow raises inside
# interact(), gets recorded per-record, never kills the battery. Shipable
# variants come later (compact bodies sized to the worst-case ctx guard).
LOCAL_BUILDERS = {
    f"fd{d}_short": fs_depth(d) for d in (6, 8, 10)
}

FAMILIES = [
    "fd8_short",            # decision-critical: deep knee test
    "fd10_short",           # extreme depth
    "fs5_short",            # deepest REGISTERED (=shippable) drip
    "fd6_short",
    "fs4_short",
    "fs3_short",            # anchor
    "fb3_bare",             # round-2 winner anchor (long form)
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
            "kinds": kinds, "err": err,
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

    server = None
    spec = GEMMA_SPEC
    server = GgufModelServer(spec)
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
    print("DEPTH BATTERY COMPLETE", flush=True)


if __name__ == "__main__":
    main()
