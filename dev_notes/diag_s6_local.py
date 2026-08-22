"""One-off diagnostic (2026-08-22): why did local_check return 175
candidates for S6 (S5 returned 260 at the same budget)?  Replicates
local_check.run_check's env and reports stage/compose internals.
Run: PYTHONPATH=sdk:. ./.venv/bin/python dev_notes/diag_s6_local.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "sdk"))

import attack  # noqa: E402
import local_check  # noqa: E402
from aicomp_sdk.attacks.contracts import AttackRunConfig  # noqa: E402
from aicomp_sdk.core.env.api import EnvSelection  # noqa: E402
from aicomp_sdk.evaluation.ops import build_attack_env  # noqa: E402


def main() -> None:
    env = build_attack_env(
        seed=123,
        fixtures_dir=local_check.FIXTURES,
        agent_factory=local_check.ObedientStubAgent,
        guardrail=local_check.OptimalGuardrail(),
        env_selection=EnvSelection.GYM,
        max_tool_hops=8,
    )
    attack._STATE.update(n_sessions=0, latencies=[], family_stats={})

    orig_compose = attack.AttackAlgorithm._compose

    def compose_spy(self, verified, screened, n_target):
        rank = sorted(
            attack.FIREHOSE_FAMILIES,
            key=lambda f: -attack._family_mean_raw(f),
        )
        means = {f: round(attack._family_mean_raw(f), 1) for f in rank}
        best = means[rank[0]]
        cut = attack.SIBLING_FLOOR_FRAC * best
        fams = [f for f in rank if attack._family_mean_raw(f) >= cut]
        print(f"compose: verified={len(verified)} n_target={n_target}")
        print(f"  means={means}")
        print(f"  best={best} cut={cut} fams_in_fill={len(fams)}")
        n_multi = sum(1 for r in verified if len(r['messages']) > 1)
        print(f"  verified multi-msg={n_multi}"
              f" (lad cap={max(2, int(attack.LADDER_MAX_FRAC * n_target))})")
        out = orig_compose(self, verified, screened, n_target)
        print(f"  ship={len(out)}")
        return out

    attack.AttackAlgorithm._compose = compose_spy
    try:
        algo = attack.AttackAlgorithm(config={})
        cands = algo.run(env, AttackRunConfig(time_budget_s=600.0))
        print(f"run() returned {len(cands)} candidates;"
              f" probes={len(attack._STATE['latencies'])}")
    finally:
        attack.AttackAlgorithm._compose = orig_compose


if __name__ == "__main__":
    main()
