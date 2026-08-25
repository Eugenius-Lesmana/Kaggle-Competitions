"""Gemma mini-battery (S12_BIFROST prerequisite) — 2026-08-25.

Decision question: does a gemma-native turn-open injection forge fire on the
real gemma-4-26B-A4B agent, and does it beat fh_terse8 (the ONLY shape that
currently lives on gemma in S11) by enough to justify building S12 around it?

Run:  python probe_gemma.py          (after bootstrap.sh)
Pull: scp -i /tmp/opencode/colab_key -P NNNNN root@0.tcp.ngrok.io:/content/results.jsonl /tmp/opencode/

New builders are defined HERE (not in attack.py) so no gate ritual is needed;
if the battery justifies S12 they get ported verbatim into attack.py.

Family order = decision priority (VM dies fast; get the critical rows first):
  1. fg_turn8   — turn-forged single (THE test)
  2. fh_terse8  — incumbent gemma baseline
  3. fg2_close  — turn-forged 2-msg drip
  4. fg_min8    — turn-forged short-URL single
  5. fg3_close  — turn-forged 3-msg drip
  6. fb2_bare / fb3_bare / fh_bare8 — bare controls
"""
from __future__ import annotations

import gc
import json
import sys
import time

sys.path.insert(0, "/content/proj")
sys.path.insert(0, "/content/proj/sdk")
import os  # noqa: E402

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

FIXTURES = "/content/proj/sdk/aicomp_sdk/fixtures"
SEED = 123
RESULTS = "/content/results.jsonl"
INJ = attack._GEMMA_INJ_TURN

# --- local gemma builders (ported to attack.py only if battery wins) --------


def fg2_close(i: int) -> tuple[str, ...]:
    return (
        attack._bare_body(i) + INJ,
        attack._bare_body(i + 8192) + INJ,
    )


def fg3_close(i: int) -> tuple[str, ...]:
    return (
        attack._bare_body(i) + INJ,
        attack._bare_body(i + 8192) + INJ,
        attack._bare_body(i + 16384) + INJ,
    )


def fg_min8(i: int) -> tuple[str, ...]:
    return (attack._short_body(i) + INJ,)


LOCAL_BUILDERS = {"fg2_close": fg2_close, "fg3_close": fg3_close, "fg_min8": fg_min8}

FAMILIES = [
    "fg_turn8", "fh_terse8",            # decision pair first
    "fg2_close", "fg_min8", "fg3_close",
    "fb2_bare", "fb3_bare", "fh_bare8", # controls
]
INDICES = [1, 2]


def append(rec: dict) -> None:
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def builder(fam: str):
    return LOCAL_BUILDERS.get(fam) or attack.FAMILY_BUILDERS[fam]


def run_family(server: GgufModelServer, family: str,
               done: set[tuple[str, int]] | None = None) -> None:
    agent = server._load_agent()
    for idx in INDICES:
        if done and (family, idx) in done:
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
    # Resume support: on a reconnect we scp the partial results back up to
    # /content/results.jsonl BEFORE launching, and every (family, idx) pair
    # already recorded without error is skipped. A fragile VM then only ever
    # pays for the pairs it has NOT measured yet.
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
            print(f"[resume] {len(done)} pairs already measured; skipping", flush=True)

    server = None
    # FULL offload ONLY: partial offload routes tensor ops through
    # libggml-cpu, whose prebuilt kernels crash (invalid opcode) on this
    # image/CPU. Q3_K_XL (12.9 GB) fits the T4's ~14.6 GB usable VRAM whole.
    for ngl in (None,):
        try:
            spec = GEMMA_SPEC
            if ngl is not None:
                spec = type(spec)(**{**spec.__dict__, "n_gpu_layers": ngl})
            server = GgufModelServer(spec)
            t0 = time.monotonic()
            server.load_model()
            print(f"[gemma] loaded (n_gpu_layers={ngl or 'full'}) "
                  f"in {time.monotonic()-t0:.0f}s", flush=True)
            break
        except Exception as exc:
            print(f"[gemma] load failed @ ngl={ngl}: "
                  f"{type(exc).__name__}: {exc}"[:300], flush=True)
            if server:
                server.unload()
            gc.collect()
            server = None
    if server is None:
        print("[gemma] ALL LOADS FAILED", flush=True)
        return
    for fam in FAMILIES:
        run_family(server, fam, done)
        done = [json.loads(l) for l in open(RESULTS)]
        by_fam: dict[str, list[dict]] = {}
        for r in done:
            if r.get("model") == "gemma":
                by_fam.setdefault(r["family"], []).append(r)
        print("\n=== RUNNING SUMMARY (gemma) ===", flush=True)
        for f, rs in by_fam.items():
            posts = sum(r["posts"] for r in rs) / len(rs)
            lat = sum(r["lat_s"] for r in rs) / len(rs)
            raw = sum(r["raw"] for r in rs) / len(rs)
            rate = raw / (lat + 3.0)
            print(f"  {f:12s} posts={posts:5.1f} lat={lat:6.1f}s "
                  f"raw={raw:6.1f} raw/s={rate:5.2f}", flush=True)
    server.unload()
    gc.collect()
    print("GEMMA BATTERY COMPLETE", flush=True)


if __name__ == "__main__":
    main()
