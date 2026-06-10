"""BL-2/A5 test — session-start digest renders real state, deterministic, no LLM.
Run: python engine/test_digest.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from digest import render_digest  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))


def fixture(d):
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/01-plan"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/01-plan/work-status.md"), "w", encoding="utf-8").write(
        "<!-- AI-CONTEXT\nphase: test-phase-7\nactive_branch: dev\nblocker: none\nnext_action: do X then Y\n-->\nbody")
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write(
        "<!-- AI-CONTEXT\ntodo: [BL-9]\npriority_next: finish BL-9\n-->\nbody")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write(
        "<!-- AI-CONTEXT\ncheckpoint: did A and B last session\n-->\nbody")


with tempfile.TemporaryDirectory() as d:
    fixture(d)
    out = render_digest(d)
    check("has phase from work-status", "test-phase-7" in out)
    check("has priority from task-board", "finish BL-9" in out)
    check("has last checkpoint from work-log", "did A and B" in out)
    check("has inbox count", "decision_inbox_open: 0" in out)
    check("labeled as rendered-not-generated", "rendered from store" in out)
    check("deterministic (same input -> same output)", render_digest(d) == out)
    check("compact (<2000 chars)", len(out) < 2000)

    # held item appears
    from inbox import create_item
    create_item("agent_action", "T-9", 3, "deploy_prod", ts=1, root=d)
    out2 = render_digest(d)
    check("open inbox item surfaces in digest", "decision_inbox_open: 1" in out2 and "deploy_prod" in out2)

# live repo smoke: digest renders without error and mentions real phase
live = render_digest(os.path.join(os.path.dirname(__file__), ".."))
check("live repo digest renders", "PROJECT-MEMORY DIGEST" in live and len(live) > 100)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} digest tests passed")
