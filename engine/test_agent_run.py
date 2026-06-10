"""BL-12 test — governed agent run mechanics: gated write, real test evidence, gated done.
(Stub provider = offline/deterministic; live Ollama run is exercised by agent_run.py __main__.)
Run: python engine/test_agent_run.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent_run import run_task  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

# happy path: plan -> gated write -> real test (exit 0) -> done via Task Close Gate
with tempfile.TemporaryDirectory() as d:
    r = run_task(d, task_id="SPIKE-1")
    check("run completes done=True", r["done"] is True)
    check("4 steps recorded", len(r["steps"]) == 4)
    check("test evidence is real exit 0", r.get("test_exit") == 0)
    check("file actually written", os.path.exists(os.path.join(d, "calc.py")))
    check("transcript saved", os.path.exists(os.path.join(d, "agent-run-report.md")))
    check("audit events recorded", os.path.exists(os.path.join(d, "engine/events.log.jsonl")))
    board = open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), encoding="utf-8").read()
    check("SPIKE-1 in done list (via gate)", "SPIKE-1" in board)

# adversarial: model proposes code with a SECRET -> deterministic gate blocks BEFORE disk
with tempfile.TemporaryDirectory() as d:
    r = run_task(d, task_id="SPIKE-2", inject_content='api_key = "sk-evil12345678"\ndef add(a,b): return a+b\n')
    check("secret in proposed code -> BLOCKED at write", r["done"] is False and r["blocked_at"] == "write")
    check("nothing written to disk", not os.path.exists(os.path.join(d, "calc.py")))

# adversarial: code that fails tests -> RED evidence -> done never reached
with tempfile.TemporaryDirectory() as d:
    r = run_task(d, task_id="SPIKE-3", inject_content='def add(a, b):\n    return a - b\n')
    check("broken code -> blocked at test (real red exit)", r["done"] is False and r["blocked_at"] == "test")
    board = open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), encoding="utf-8").read()
    check("SPIKE-3 NOT marked done", "SPIKE-3" not in board)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} governed-agent-run tests passed")
