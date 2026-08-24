"""Colab probe battery: real GGUF agents + OptimalGuardrail + SandboxEnv.

Mirrors hosted replay semantics: seed=123, greedy, n_ctx=8192,
max_new_tokens=1024, guardrail applied per hop. Appends every result to
/content/results.jsonl so partial progress survives session death.
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time

sys.path.insert(0, "/content/proj")
sys.path.insert(0, "/content/proj/sdk")
os.environ["GPT_OSS_MODEL_PATH"] = "/content/models/gpt-oss-20b-Q4_K_M.gguf"
os.environ["GEMMA_MODEL_PATH"] = "/content/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"

import attack  # noqa: E402
from kaggle_evaluation.jed_attack_134815.gpt_oss_model_server import (  # noqa: E402
    SPEC as GPT_SPEC,
)
from kaggle_evaluation.jed_attack_134815.gemma_model_server import (  # noqa: E402
    SPEC as GEMMA_SPEC,
)
from kaggle_evaluation.jed_attack_134815.gguf_model_server import (  # noqa: E402
    GgufModelServer,
)
from aicomp_sdk.core.env.sandbox import SandboxEnv  # noqa: E402
from aicomp_sdk.guardrails.optimal import Guardrail as OptimalGuardrail  # noqa: E402

FIXTURES = "/content/proj/sdk/aicomp_sdk/fixtures"
SEED = 123
RESULTS = "/content/results.jsonl"

# Decision-critical order: short-vs-long forged pairs adjacent.
FAMILIES = [
    "fj_min8", "fj_close8",          # single: short vs long forge
    "fj2_min", "fj2_close",          # drip2: short vs long
    "fj3_min", "fj3_close",          # drip3: short vs long
    "fj4_min", "fj5_min",            # depth 4/5
    "fh_terse8", "fh_bare8",         # verbose control + bare control
    "fb2_bare", "fb3_bare",          # bare drips
    "fj_last8",                      # url-last long forge
]
INDICES = [1, 2]


def append(rec: dict) -> None:
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def make_server(spec, n_gpu_layers=None):
    if n_gpu_layers is not None:
        spec = type(spec)(**{**spec.__dict__, "n_gpu_layers": n_gpu_layers})
    return GgufModelServer(spec)


def run_family(label: str, server: GgufModelServer, family: str) -> None:
    agent = server._load_agent()
    for idx in INDICES:
        msgs = attack.FAMILY_BUILDERS[family](idx)
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
        except Exception as exc:  # never die mid-battery
            err = f"{type(exc).__name__}: {exc}"[:200]
        lat = time.monotonic() - t0
        rec = {
            "model": label, "family": family, "idx": idx,
            "raw": float(raw), "posts": int(kinds.get("EXFILTRATION", 0)),
            "lat_s": round(lat, 2), "n_msgs": len(msgs),
            "kinds": kinds, "err": err,
        }
        print("REC", json.dumps(rec), flush=True)
        append(rec)
        del env
        gc.collect()


def run_model(label: str, base_spec) -> None:
    ngl_try = [None, 40, 32, 24]
    last_err = None
    for ngl in ngl_try:
        server = make_server(base_spec, ngl)
        try:
            t0 = time.monotonic()
            server.load_model()
            print(f"[{label}] loaded (n_gpu_layers={ngl or 'default'}) "
                  f"in {time.monotonic()-t0:.0f}s", flush=True)
            break
        except Exception as exc:
            last_err = f"{type(exc).__name__}: {exc}"[:300]
            print(f"[{label}] load failed @ ngl={ngl}: {last_err}", flush=True)
            server.unload()
            gc.collect()
    else:
        print(f"[{label}] ALL LOADS FAILED: {last_err}", flush=True)
        return
    for fam in FAMILIES:
        run_family(label, server, fam)
    server.unload()
    gc.collect()
    print(f"[{label}] DONE", flush=True)


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    if only in ("", "smoke"):
        # smoke: one bare candidate on gpt-oss validates the whole pipeline
        srv = make_server(GPT_SPEC)
        srv.load_model()
        run_family("gpt_oss_smoke", srv, "fh_bare8")
        srv.unload()
        gc.collect()
        print("SMOKE OK", flush=True)
    if only in ("", "gpt"):
        run_model("gpt_oss", GPT_SPEC)
    if only in ("", "gemma"):
        run_model("gemma", GEMMA_SPEC)
    print("BATTERY COMPLETE", flush=True)
