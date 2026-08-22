"""Local end-to-end gateway test — replicates the hosted Kaggle rerun.

Runs the real kaggle_evaluation relay: JEDAttackGateway (trusted side, real
GymAttackEnv + OptimalGuardrail + replay scoring) <-> JEDAttackInferenceServer
(competitor side, loads ./attack.py and runs AttackAlgorithm through RemoteEnv
over the gRPC command-response protocol).

Differences from the hosted run (for local speed):
- AICOMP_MODEL_NAMES=deterministic (vulnerable deterministic agent instead of
  gpt_oss/gemma model servers)
- Short budgets via env monkeypatching before gateway construction.

Usage: .venv/bin/python gateway_local_test.py [budget_s]
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))            # attack.py lookup for the inference server
sys.path.insert(0, str(ROOT / "sdk"))    # aicomp_sdk + kaggle_evaluation

BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0

os.environ["AICOMP_MODEL_NAMES"] = "deterministic"

import kaggle_evaluation.jed_attack_134815.jed_attack_gateway as gw_mod
import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as isrv_mod

# Shrink the hosted budgets so the test finishes quickly.
gw_mod.DEFAULT_BUDGET_S = BUDGET
gw_mod.GATEWAY_RESPONSE_TIMEOUT_S = int(BUDGET + 60)
# The inference server reads attack.py from DEFAULT_SUBMISSION_DIR.
isrv_mod.DEFAULT_SUBMISSION_DIR = ROOT

# Replace the vulnerable deterministic agent with a compliant stub agent that
# models what gpt_oss/gemma would do when they follow our instructions: issue
# the requested http.post(email.send/...) calls one per hop.
if os.environ.get("STUB_AGENT", "1") == "1":
    from local_check import ObedientStubAgent

    gw_mod.build_agent_factory = lambda name: (lambda: ObedientStubAgent())
    print("[test] Using ObedientStubAgent in place of the target model")

from kaggle_evaluation.jed_attack_134815.jed_attack_inference_server import (
    JEDAttackInferenceServer,
)

with tempfile.TemporaryDirectory() as tmpdir:
    os.chdir(tmpdir)  # submission.csv lands here
    server = JEDAttackInferenceServer()
    server.run(competition_data_folder=str(ROOT / "sdk" / "aicomp_sdk" / "fixtures"))

    print("\n" + "=" * 70)
    print("GATEWAY TEST COMPLETE")
    print("=" * 70)
    csv_path = Path(tmpdir) / "submission.csv"
    if csv_path.exists():
        print(csv_path.read_text())
    else:
        print("!! submission.csv NOT written")
        sys.exit(1)
