"""Timeout-path gateway test — the "never lose the whole run" guarantee.

Forces the hosted failure mode we must survive: the attack generation phase
blows its budget mid-probe.  Verifies (against the REAL kagble relay, same
code path as the hosted rerun):

  1. the gateway times the attack out but *harvests* the candidates whose
     interactions completed before the deadline ("preserving N completed"),
  2. replay still runs on the harvested list, and
  3. submission.csv is still written with parseable rows.

Mechanism: tiny budget (10s) + a stub agent that is fast for ~1.5 probes and
then stalls every LLM call, so probe #2 blocks past the deadline.  The stock
attack.py would decline to probe at all under a 10s budget (its headroom
formula assumes hosted-scale latencies), so we run a copy with the two
latency constants tuned down -- everything else is byte-identical.

Usage: .venv/bin/python gateway_timeout_test.py
"""

from __future__ import annotations

import io
import os
import re
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))            # attack.py lookup for the inference server
sys.path.insert(0, str(ROOT / "sdk"))    # aicomp_sdk + kaggle_evaluation

BUDGET = 10.0
N_FAST_CALLS = 14   # ~probe 1 (9 calls) + part of probe 2
SLOW_S = 5.0

os.environ["AICOMP_MODEL_NAMES"] = "deterministic"

import kaggle_evaluation.jed_attack_134815.jed_attack_gateway as gw_mod  # noqa: E402
import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as isrv_mod  # noqa: E402


class TeeStdout(io.TextIOBase):
    """Capture prints from every thread while still showing them."""

    def __init__(self):
        self.lock = threading.Lock()
        self.captured = io.StringIO()
        self._real = sys.stdout

    def write(self, s):
        with self.lock:
            self.captured.write(s)
            return self._real.write(s)

    def flush(self):
        self._real.flush()


class StallingStubAgent:
    """Obedient stub that freezes after N_FAST_CALLS LLM calls.

    Generation uses ONE agent instance for the whole attack session, so the
    per-instance call counter survives env resets: probe 1 completes fast and
    is harvested; probe 2 stalls mid-interact past the deadline.  Replay
    builds a fresh agent per candidate, so replay itself stays fast.
    """

    def __init__(self):
        from local_check import ObedientStubAgent

        self._inner = ObedientStubAgent()
        self._calls = 0

    def reset_state(self):
        self._inner.reset_state()  # keep the call counter on purpose

    def snapshot_state(self):
        return self._inner.snapshot_state()

    def restore_state(self, snap):
        self._inner.restore_state(snap)

    def next_action(self, *, history, tools):
        self._calls += 1
        if self._calls > N_FAST_CALLS:
            time.sleep(SLOW_S)
        return self._inner.next_action(history=history, tools=tools)


def main() -> int:
    # -- tune the attack copy for tiny-budget probing ------------------------
    src = (ROOT / "attack.py").read_text()
    tuned = src.replace("TBAR_DEFAULT_S = 60.0", "TBAR_DEFAULT_S = 0.3").replace(
        "_PROBE_HEADROOM_S = 90.0", "_PROBE_HEADROOM_S = 0.1"
    )
    assert tuned != src, "tuning constants not found in attack.py"
    submit_dir = ROOT / ".timeout_test_submission"
    submit_dir.mkdir(exist_ok=True)
    (submit_dir / "attack.py").write_text(tuned)

    gw_mod.DEFAULT_BUDGET_S = BUDGET
    gw_mod.GATEWAY_RESPONSE_TIMEOUT_S = int(BUDGET + 60)
    isrv_mod.DEFAULT_SUBMISSION_DIR = submit_dir
    gw_mod.build_agent_factory = lambda name: (lambda: StallingStubAgent())

    from kaggle_evaluation.jed_attack_134815.jed_attack_inference_server import (
        JEDAttackInferenceServer,
    )

    tee = TeeStdout()
    sys.stdout = tee
    failures: list[str] = []
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)  # submission.csv lands here
            server = JEDAttackInferenceServer()
            server.run(
                competition_data_folder=str(ROOT / "sdk" / "aicomp_sdk" / "fixtures")
            )

            out = tee.captured.getvalue()
            csv_path = Path(tmpdir) / "submission.csv"
            print("\n" + "=" * 70)
            print("TIMEOUT-PATH GATEWAY TEST")
            print("=" * 70)
            if csv_path.exists():
                csv_text = csv_path.read_text()
                print(csv_text)
            else:
                failures.append("submission.csv NOT written")
                csv_text = ""

            # 1) the timeout path actually fired (not a clean done)
            m = re.search(r"timed out; preserving (\d+) completed", out)
            if not m:
                failures.append(
                    "generation-timeout harvest path did not fire "
                    f"(no 'preserving N completed' line; probe status: "
                    f"{re.findall(r'Final status: .*', out)})"
                )
            else:
                n = int(m.group(1))
                print(f"[ok] gateway timed out and preserved {n} harvested candidate(s)")
                if n < 1:
                    failures.append("timeout preserved 0 candidates (expected >=1)")

            # 2) no INVALID_SUBMISSION / fatal error
            if "INVALID_SUBMISSION" in out or "Attack returned error" in out:
                failures.append("attack error escalated to INVALID_SUBMISSION")

            # 3) CSV shape (hosted = 4 rows; local deterministic = 1 row)
            rows = [r for r in csv_text.splitlines() if r.strip()]
            if len(rows) < 2 or not rows[0].lower().startswith("id"):
                failures.append(f"submission.csv malformed: {rows!r}")
            else:
                print(f"[ok] submission.csv has {len(rows) - 1} data rows")
                scores = [float(r.split(",")[1]) for r in rows[1:]]
                if max(scores, default=0.0) <= 0:
                    failures.append(f"all rows scored 0 despite harvested candidates: {scores}")
                else:
                    print(f"[ok] harvested candidates still scored: {scores}")
    finally:
        sys.stdout = tee._real

    if failures:
        for f in failures:
            print("FAIL:", f)
        return 1
    print("\nTIMEOUT-PATH TEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
