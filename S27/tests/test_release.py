"""Deterministic gates for the S27 calibrated hop-1 release."""

from __future__ import annotations

import base64
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from aicomp_sdk.attacks import AttackRunConfig

HERE = Path(__file__).resolve().parent
S27_ROOT = HERE.parent
S14_ROOT = S27_ROOT.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


attack = load_module("s27_calibrated_hop1_attack", S27_ROOT / "attack.py")
base_attack = load_module("s19_base_for_s27_tests", S14_ROOT / "S19" / "attack.py")
build_release = load_module("s27_build_release", S27_ROOT / "tools" / "build_release.py")


def messages(candidates):
    return [candidate.user_messages[0] for candidate in candidates]


def test_source_lineage_is_pinned_and_release_is_byte_exact():
    base = (S14_ROOT / "S19" / "attack.py").read_bytes()
    canonical = (S27_ROOT / "attack.py").read_bytes()
    released = (S27_ROOT / "RELEASE" / "attack.py").read_bytes()
    assert build_release.digest_bytes(base) == build_release.BASE_SHA256
    assert build_release.digest_bytes(canonical) == build_release.ATTACK_SHA256
    assert build_release.digest_bytes(build_release.source_diff(base, canonical)) == (
        build_release.DIFF_SHA256
    )
    assert canonical == released
    assert not canonical.startswith(b"\xef\xbb\xbf") and b"\r\n" not in canonical


def test_notebook_embeds_canonical_source_without_mode_override():
    notebook = json.loads((S27_ROOT / "RELEASE" / "submission.ipynb").read_text())
    assert notebook["nbformat"] == 4 and len(notebook["cells"]) == 2
    cell1 = "".join(notebook["cells"][0]["source"])
    cell2 = "".join(notebook["cells"][1]["source"])
    payload = re.search(r'ATTACK_B64 = "([A-Za-z0-9+/=]+)"', cell1).group(1)
    assert base64.b64decode(payload, validate=True) == (S27_ROOT / "attack.py").read_bytes()
    assert "ATTACK_MODE" not in json.dumps(notebook)
    assert "KAGGLE_IS_COMPETITION_RERUN" in cell2
    assert "JEDAttackInferenceServer().run()" in cell2
    for index, cell in enumerate(notebook["cells"], start=1):
        assert cell["cell_type"] == "code"
        assert cell["execution_count"] is None and cell["outputs"] == []
        compile("".join(cell["source"]), f"submission.ipynb:cell-{index}", "exec")


def test_s27_changes_only_the_calibrated_hop1_mechanism():
    for name in (
        "PAYLOAD",
        "TEMPLATE",
        "HARMONY_SUFFIX",
        "FRAME_TEMPLATE",
        "VERBOSE_FRAME_TEMPLATE",
        "FRAME_RACE_REPS",
        "FRAME_RACE_TEMPLATES",
        "OVERPACK_TAIL_N",
        "REPLAY_SAFE_SIZING",
        "REPLAY_SAFE_FRAC",
        "BURST_K",
        "SLOW_MULTIPOST_N",
        "HARD_N_CAP",
        "FALLBACK_N",
    ):
        assert getattr(attack, name) == getattr(base_attack, name)
    assert attack.PROBE_HOPS == 1
    assert attack.REPLAY_COST_COEF == 2.0
    assert attack.REPLAY_COST_SAFETY_FACTOR == 1.25
    assert attack.CALIBRATION_SAMPLES == 2


@pytest.mark.parametrize(
    ("full", "one", "floor", "safety", "expected"),
    [
        ([2.0, 2.0], [1.0, 1.0], 2.0, 1.25, 2.5),
        ([1.0, 1.0], [1.0, 1.0], 2.0, 1.25, 2.0),
        ([10.0, 12.0], [1.0, 2.0], 2.0, 1.25, 15.0),
    ],
)
def test_calibration_coefficient_is_conservative(full, one, floor, safety, expected):
    assert attack._calibration_coefficient(full, one, floor, safety) == expected


@pytest.mark.parametrize(
    ("full", "one", "floor", "safety"),
    [
        ([], [1.0, 1.0], 2.0, 1.25),
        ([1.0, 1.0], [1.0], 2.0, 1.25),
        ([1.0, float("nan")], [1.0, 1.0], 2.0, 1.25),
        ([1.0, 1.0], [0.0, 1.0], 2.0, 1.25),
        ([1.0, 1.0], [1.0, 1.0], float("inf"), 1.25),
        ([1.0, 1.0], [1.0, 1.0], 2.0, 0.0),
    ],
)
def test_calibration_rejects_incomplete_or_invalid_inputs(full, one, floor, safety):
    assert attack._calibration_coefficient(full, one, floor, safety) is None


def test_forced_count_fallback_fired_and_uniqueness_are_unchanged():
    forced = attack.AttackAlgorithm({"n_candidates": 3}).run(None, None)
    capped = attack.AttackAlgorithm({"n_candidates": 99_999}).run(None, None)
    assert messages(forced) == [attack._msg(index) for index in range(3)]
    assert len(capped) == attack.HARD_N_CAP
    assert len({attack._url(index) for index in range(attack.HARD_N_CAP)}) == 2_000

    class BrokenEnv:
        def reset(self) -> None:
            raise RuntimeError("not probeable")

    config = AttackRunConfig(time_budget_s=100.0, max_steps=1, max_tool_hops=8)
    assert len(attack.AttackAlgorithm({}).run(None, config)) == attack.FALLBACK_N
    assert len(attack.AttackAlgorithm({}).run(BrokenEnv(), config)) == attack.FALLBACK_N

    class TraceEnv:
        def __init__(self, events: list[dict[str, Any]]) -> None:
            self.events = events

        def export_trace_dict(self) -> dict[str, Any]:
            return {"tool_events": self.events}

    good = {"ok": True, "name": "http.post", "args": {"data": "xSECRET_MARKERx"}}
    assert attack.AttackAlgorithm._fired(TraceEnv([good]))
    assert not attack.AttackAlgorithm._fired(TraceEnv([{**good, "ok": False}]))


class Clock:
    def __init__(self) -> None:
        self.now = 0.0
        self.pending = 0.0

    def monotonic(self) -> float:
        self.now += self.pending
        self.pending = 0.0
        return self.now


class RaceEnv:
    def __init__(
        self,
        clock: Clock,
        samples: list[tuple[float, bool]],
        *,
        fail_call: int | None = None,
    ) -> None:
        self.clock = clock
        self.samples = iter(samples)
        self.fail_call = fail_call
        self.calls: list[tuple[str, int]] = []
        self.fired = False

    def reset(self) -> None:
        pass

    def interact(self, message: str, max_tool_hops: int = 8) -> None:
        self.calls.append((message, max_tool_hops))
        if self.fail_call == len(self.calls):
            raise RuntimeError("injected fault")
        if len(self.calls) == 1:
            self.fired = False
            return
        latency, self.fired = next(self.samples)
        self.clock.pending += latency

    def export_trace_dict(self) -> dict[str, Any]:
        events = []
        if self.fired:
            events.append(
                {"ok": True, "name": "http.post", "args": {"data": attack.PAYLOAD}}
            )
        return {"tool_events": events}


RACE_SAMPLES = [
    (4.0, True),
    (2.0, True),
    (3.0, True),
    (4.0, True),
    (2.0, True),
    (3.0, True),
]


def run_fill(monkeypatch, samples, *, hard_cap=10, replay_budget_s=1.0e9, fail_call=None):
    clock = Clock()
    env = RaceEnv(clock, samples, fail_call=fail_call)
    monkeypatch.setattr(attack, "time", SimpleNamespace(monotonic=clock.monotonic))
    config = AttackRunConfig(time_budget_s=1.0e9, max_steps=1, max_tool_hops=8)
    output = attack.AttackAlgorithm(
        {
            "hard_n_cap": hard_cap,
            "replay_budget_s": replay_budget_s,
            "slowest0": 0.001,
        }
    ).run(env, config)
    return env, output


def expected_race_messages():
    return [
        attack._msg(index, attack.FRAME_RACE_TEMPLATES[index % 3])
        for index in range(6)
    ]


def test_warmup_and_race_stay_full_hop_then_selected_fill_uses_hop1(monkeypatch):
    env, output = run_fill(monkeypatch, RACE_SAMPLES + [(1.0, True)] * 10)
    assert [message for message, _hops in env.calls[1:7]] == expected_race_messages()
    assert [hops for _message, hops in env.calls[:7]] == [8] * 7
    assert [hops for _message, hops in env.calls[7:]] == [1] * 4
    assert [message for message, _hops in env.calls[7:]] == [
        attack._msg(index, attack.FRAME_TEMPLATE) for index in range(6, 10)
    ]
    assert messages(output) == expected_race_messages() + [
        attack._msg(index, attack.FRAME_TEMPLATE) for index in range(6, 10)
    ]


def test_calibration_candidates_are_retroactively_charged(monkeypatch):
    seen = []
    original = attack._replay_stop

    def spy(replay_cost, wall_now, next_est, replay_cap, wall_deadline, **kwargs):
        seen.append((replay_cost, next_est, kwargs.get("next_wall_est")))
        return original(replay_cost, wall_now, next_est, replay_cap, wall_deadline, **kwargs)

    monkeypatch.setattr(attack, "_replay_stop", spy)
    run_fill(monkeypatch, RACE_SAMPLES + [(1.0, True)] * 10, hard_cap=9)
    assert any(
        replay_cost == pytest.approx(23.0)
        and next_est == pytest.approx(3.375)
        and next_wall == pytest.approx(1.35)
        for replay_cost, next_est, next_wall in seen
    )


def test_fire_mismatch_discards_pending_and_retries_same_indices_full_hop(monkeypatch):
    samples = RACE_SAMPLES + [(1.0, True), (1.0, False), (2.0, True), (2.0, True)]
    env, output = run_fill(monkeypatch, samples, hard_cap=8)
    assert [hops for _message, hops in env.calls] == [8] * 7 + [1, 1, 8, 8]
    assert [message for message, _hops in env.calls[7:]] == [
        attack._msg(6, attack.FRAME_TEMPLATE),
        attack._msg(7, attack.FRAME_TEMPLATE),
        attack._msg(6, attack.FRAME_TEMPLATE),
        attack._msg(7, attack.FRAME_TEMPLATE),
    ]
    assert messages(output) == expected_race_messages() + [
        attack._msg(6, attack.FRAME_TEMPLATE),
        attack._msg(7, attack.FRAME_TEMPLATE),
    ]


def test_selected_frame_without_two_full_hop_fires_never_uses_hop1(monkeypatch):
    samples = [
        (4.0, True),
        (1.0, True),
        (3.0, True),
        (4.0, True),
        (1.0, False),
        (3.0, True),
        (2.0, True),
        (2.0, True),
    ]
    env, _output = run_fill(monkeypatch, samples, hard_cap=7)
    assert all(hops == 8 for _message, hops in env.calls)
    assert [message for message, _hops in env.calls[-2:]] == [
        attack._msg(6, attack.FRAME_TEMPLATE),
        attack._msg(7, attack.FRAME_TEMPLATE),
    ]


def test_partial_calibration_fault_returns_only_committed_race_prefix(monkeypatch):
    env, output = run_fill(
        monkeypatch,
        RACE_SAMPLES + [(1.0, True), (1.0, True)],
        hard_cap=100,
        fail_call=9,
    )
    assert len(env.calls) == 9
    assert [hops for _message, hops in env.calls[-2:]] == [1, 1]
    assert messages(output) == expected_race_messages()


def test_calibration_charge_must_fit_before_pending_candidates_commit(monkeypatch):
    replay_cap = 23.0
    env, output = run_fill(
        monkeypatch,
        RACE_SAMPLES + [(1.0, True), (1.0, True)],
        hard_cap=100,
        replay_budget_s=replay_cap / attack.REPLAY_SAFE_FRAC,
    )
    assert len(env.calls) == 9
    assert messages(output) == expected_race_messages()


def test_normal_safe_stop_keeps_exact_tail64_after_valid_calibration(monkeypatch):
    replay_cap = 24.0
    env, output = run_fill(
        monkeypatch,
        RACE_SAMPLES + [(1.0, True), (1.0, True)],
        hard_cap=100,
        replay_budget_s=replay_cap / attack.REPLAY_SAFE_FRAC,
    )
    assert len(env.calls) == 9
    prefix = expected_race_messages() + [
        attack._msg(6, attack.FRAME_TEMPLATE),
        attack._msg(7, attack.FRAME_TEMPLATE),
    ]
    tail = [attack._msg(index, attack.FRAME_TEMPLATE) for index in range(8, 72)]
    assert messages(output) == prefix + tail
    assert len(messages(output)) == len(set(messages(output))) == 72


def test_legacy_non_replay_safe_path_remains_full_hop(monkeypatch):
    clock = Clock()
    env = RaceEnv(clock, [(1.0, True)] * 8)
    monkeypatch.setattr(attack, "time", SimpleNamespace(monotonic=clock.monotonic))
    config = AttackRunConfig(time_budget_s=1.0e9, max_steps=1, max_tool_hops=8)
    output = attack.AttackAlgorithm(
        {"hard_n_cap": 8, "replay_safe_sizing": False, "slowest0": 0.001}
    ).run(env, config)
    assert len(output) == 8
    assert all(hops == 8 for _message, hops in env.calls)


def test_replay_stop_checks_replay_and_wall_bounds():
    assert not attack._replay_stop(800.0, 100.0, 100.0, 970.0, 1_000.0)
    assert attack._replay_stop(900.0, 100.0, 100.0, 970.0, 1_000.0)
    assert attack._replay_stop(0.0, 950.0, 100.0, 970.0, 1_000.0)
