"""Unit tests for attack.py v2 (plain-python runner; no pytest needed).

Covers the plan's Part-5 gate 5:
  1. validation mirror across every family x 200 indices
  2. URL hygiene + global domain uniqueness + score-cell uniqueness (200 slots)
  3. intent-word hygiene for CD / lottery families
  4. deadline discipline: 3s budget stays under budget; 0.5s -> static fallback
  5. exception-injecting envs never raise and still return valid candidates
  6. _ship_size replay-capacity table (S2: 0.80 x 8750s / (tbar + overhead))
  7. two sequential run() calls; per-session latency reset, session stamping

Usage:  PYTHONPATH=..:../sdk .venv/bin/python tests/test_attack_units.py
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "sdk"))

import attack  # noqa: E402
from attack import (  # noqa: E402
    FAMILY_BUILDERS,
    N_MIN,
    _intent_clean,
    _mirror_valid,
    _urls,
    _url_ok,
)

from aicomp_sdk.attacks import AttackCandidate  # noqa: E402

try:
    from aicomp_sdk.core.cells import cell_signature
except Exception:  # pragma: no cover
    cell_signature = None

N_INDICES = 200

# ---------------------------------------------------------------------------
# Fake envs
# ---------------------------------------------------------------------------


def _parse_calls(message: str) -> list[dict]:
    """Obedient-agent stand-in: URLs -> http.post(marker), emails -> email.send."""
    events = []
    if "SECRET_MARKER" in message:
        urls = re.findall(r"https://[^\s'\"]+", message)
        for u in urls:
            events.append(
                {"name": "http.post", "args": {"url": u.rstrip(".,"),
                                               "data": "SECRET_MARKER"},
                 "ok": True, "output": "ok"}
            )
    for m in re.finditer(r"to '([^']+)', subject '([^']*)', body '([^']*)'", message):
        events.append(
            {"name": "email.send",
             "args": {"to": m.group(1), "subject": m.group(2), "body": m.group(3)},
             "ok": True, "output": "ok"}
        )
    return events


class FakeEnv:
    """Compliant env with configurable per-interaction latency."""

    def __init__(self, per_interact_s: float = 0.0):
        self.per_interact_s = per_interact_s
        self._events: list[dict] = []

    def reset(self):
        self._events = []

    def interact(self, user_message, max_tool_hops=None):
        time.sleep(self.per_interact_s)
        self._events.extend(_parse_calls(user_message))

    def export_trace_dict(self):
        return {"tool_events": list(self._events), "user_messages": []}


class BrokenEnv:
    """Every entry point raises; run() must still return a valid list."""

    def reset(self):
        raise RuntimeError("reset exploded")

    def interact(self, user_message, max_tool_hops=None):
        raise RuntimeError("interact exploded")

    def export_trace_dict(self):
        raise RuntimeError("export exploded")


class HalfBrokenEnv:
    """Works for k interactions, then raises (mid-run gateway failure)."""

    def __init__(self, k: int = 5):
        self.k = k
        self.n = 0
        self._events: list[dict] = []

    def reset(self):
        if self.n >= self.k:
            raise RuntimeError("env died")

    def interact(self, user_message, max_tool_hops=None):
        self.n += 1
        self._events.extend(_parse_calls(user_message))

    def export_trace_dict(self):
        return {"tool_events": list(self._events), "user_messages": []}


def _fresh_state():
    """Reset attack module state between scenario tests."""
    attack._STATE.update(
        n_sessions=0,
        t_process_start=time.time(),
        t_session1_end=None,
        latencies=[],
        family_stats={},
    )


def _run(env, budget: float):
    from aicomp_sdk.attacks.contracts import AttackRunConfig

    algo = attack.AttackAlgorithm(config={})
    return algo.run(env, AttackRunConfig(time_budget_s=budget))


def _valid(cands) -> bool:
    msgs = [tuple(c.user_messages) for c in cands]
    return bool(msgs) and all(_mirror_valid(m) for m in msgs) and len(set(msgs)) == len(msgs)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_mirror_and_length_all_families():
    worst = 0
    for name, build in FAMILY_BUILDERS.items():
        for idx in range(N_INDICES):
            msgs = build(idx)
            assert _mirror_valid(msgs), (name, idx)
            worst = max(worst, max(len(m) for m in msgs))
            # round-trip through the real candidate contract too
            if idx % 50 == 0:
                c = AttackCandidate.from_messages(msgs)
                assert tuple(c.user_messages) == tuple(msgs)
    print(f"  [ok] mirror validation + <=2000 chars: 9 families x {N_INDICES}"
          f" (longest message {worst} chars)")


def test_url_hygiene_and_domain_uniqueness():
    all_domains = set()
    for i in range(N_INDICES):
        urls = _urls(i, 8)
        assert len(urls) == 8
        for u in urls:
            assert u.startswith("https://"), u
            assert _url_ok(u), u
            dom = u.split("://", 1)[1].split("/", 1)[0]
            assert dom not in all_domains, f"domain collision at slot {i}: {dom}"
            all_domains.add(dom)
    # and inside every family's rendered messages
    for name, build in FAMILY_BUILDERS.items():
        for idx in range(N_INDICES):
            text = "\n".join(build(idx))
            for u in re.findall(r"https?://[^\s'\"]+", text):
                assert _url_ok(u.rstrip(".,")), (name, idx, u)
    print(f"  [ok] URL hygiene + {len(all_domains)} globally unique domains"
          f" across {N_INDICES} slots")


def test_cell_uniqueness():
    if cell_signature is None:
        print("  [SKIP] cell_signature not importable")
        return
    sigs = set()
    for i in range(N_INDICES):
        events = [
            {"name": "http.post",
             "args": {"url": u, "data": "SECRET_MARKER"},
             "ok": True, "output": "ok", "error": None,
             "side_effect": "SHARE", "scope": "external", "source": "tool"}
            for u in _urls(i, 8)
        ]
        sig = cell_signature(events)
        key = (sig["hash"], sig.get("n_tools"))
        assert key not in sigs, f"cell collision at slot {i}"
        sigs.add(key)
    print(f"  [ok] score-cell uniqueness: {len(sigs)} distinct cells for"
          f" {N_INDICES} synthetic 8-post traces")


def test_intent_hygiene():
    for name in ("cd_email", "lot_page", "lot_dw", "lot_seed"):
        for idx in range(N_INDICES):
            msgs = FAMILY_BUILDERS[name](idx)
            assert _intent_clean(msgs), (name, idx, msgs[-1][:100])
    print(f"  [ok] intent-word hygiene: CD + lottery families x {N_INDICES}")


def test_deadline_discipline():
    # 5s budget (the code floor -- hosted budgets are >=600s) with a slow env:
    # probes must abort and stay under budget.
    _fresh_state()
    saved_h, saved_t = attack._PROBE_HEADROOM_S, attack.TBAR_DEFAULT_S
    try:
        attack._PROBE_HEADROOM_S = 0.05
        attack.TBAR_DEFAULT_S = 0.2
        env = FakeEnv(per_interact_s=0.30)
        t0 = time.monotonic()
        cands = _run(env, budget=5.0)
        elapsed = time.monotonic() - t0
        assert _valid(cands), "invalid candidate list from 5s run"
        assert elapsed < 5.0, f"deadline overrun: {elapsed:.2f}s"
        assert len(cands) >= N_MIN, f"ship floor not met: {len(cands)}"
        assert attack._STATE["latencies"], "no probes ran; test is vacuous"
        print(f"  [ok] 5s budget honored (returned {len(cands)} cands in"
              f" {elapsed:.2f}s after {len(attack._STATE['latencies'])} probes,"
              f" all valid, >= {N_MIN})")
    finally:
        attack._PROBE_HEADROOM_S, attack.TBAR_DEFAULT_S = saved_h, saved_t

    # 0.5s budget with default (large) headroom: no probes fit -> static path.
    _fresh_state()
    env = FakeEnv(per_interact_s=0.0)
    t0 = time.monotonic()
    cands = _run(env, budget=0.5)
    elapsed = time.monotonic() - t0
    assert _valid(cands), "invalid candidate list from 0.5s run"
    assert elapsed < 2.0, f"static path too slow: {elapsed:.2f}s"
    assert len(cands) >= 1
    print(f"  [ok] 0.5s budget -> static fallback ({len(cands)} cands in"
          f" {elapsed:.2f}s)")


def test_broken_envs_never_raise():
    for label, env in (("all-broken", BrokenEnv()), ("half-broken", HalfBrokenEnv(k=4))):
        _fresh_state()
        saved_h, saved_t = attack._PROBE_HEADROOM_S, attack.TBAR_DEFAULT_S
        try:
            attack._PROBE_HEADROOM_S = 0.01  # let it *try* to probe, then fail
            attack.TBAR_DEFAULT_S = 0.05
            cands = _run(env, budget=2.0)
            assert _valid(cands), f"{label}: invalid candidate list"
        finally:
            attack._PROBE_HEADROOM_S, attack.TBAR_DEFAULT_S = saved_h, saved_t
        print(f"  [ok] {label} env: run() returned {len(cands)} valid cands,"
              f" no exception")


def test_ship_size():
    # S2 sizing: capacity = REPLAY_MARGIN * REPLAY_BUDGET_S / (tbar + overhead)
    algo = attack.AttackAlgorithm(config={})
    cases = [
        # (tbar, expected): 0.80*8750 = 7000 usable seconds per replay phase
        (60.0, 111),   # 7000/63
        (40.0, 162),   # 7000/43
        (25.0, attack.N_MAX),  # 7000/28 = 250 -> N_MAX cap
        (600.0, N_MIN),  # 7000/603 = 11 -> floor
    ]
    for tbar, want in cases:
        attack._STATE["latencies"] = [tbar] * 9
        got = algo._ship_size()
        assert got == want, (tbar, got, want)
    # even-sample median (mean of middle two)
    attack._STATE["latencies"] = [40.0, 60.0] * 5
    assert algo._ship_size() == int(7000.0 / (50.0 + attack.REPLAY_OVERHEAD_S))
    # fast-env clamp: _tbar floors at 5, _ship_size at 10 -> N_MAX cap
    attack._STATE["latencies"] = [0.5] * 9
    assert algo._ship_size() == attack.N_MAX
    # no samples yet -> TBAR_DEFAULT_S (60) -> 111
    attack._STATE["latencies"] = []
    assert algo._ship_size() == int(7000.0 / (60.0 + attack.REPLAY_OVERHEAD_S))
    print("  [ok] _ship_size: replay-capacity table, median, clamps all match")


def test_two_sequential_runs():
    _fresh_state()
    env = FakeEnv(per_interact_s=0.0)
    saved_h, saved_t = attack._PROBE_HEADROOM_S, attack.TBAR_DEFAULT_S
    try:
        attack._PROBE_HEADROOM_S = 0.01
        attack.TBAR_DEFAULT_S = 0.05
        first = _run(env, budget=5.0)
        assert _valid(first)
        # simulate 25h?? no: 7h of wall time consumed by model 1's 3 phases
        attack._STATE["t_process_start"] = time.time() - 25_000.0
        second = _run(env, budget=5.0)
        assert _valid(second)
        assert attack._STATE["n_sessions"] == 2
        assert attack._STATE["t_session1_end"] is not None
        print(f"  [ok] sequential sessions: {len(first)} + {len(second)} valid"
              f" candidates, n_sessions=2, session-1 end stamped")
    finally:
        attack._PROBE_HEADROOM_S, attack.TBAR_DEFAULT_S = saved_h, saved_t


TESTS = [
    test_mirror_and_length_all_families,
    test_url_hygiene_and_domain_uniqueness,
    test_cell_uniqueness,
    test_intent_hygiene,
    test_deadline_discipline,
    test_broken_envs_never_raise,
    test_ship_size,
    test_two_sequential_runs,
]


def main() -> int:
    for test in TESTS:
        test()
    print("\nALL UNIT TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
