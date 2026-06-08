"""F2/P6 test — governed agent dispatch (role-floor by derived lane + risk-tier + gated done).
Includes the F1-panel-consensus fix: lane is bound to the action, not caller-asserted.
Run: python engine/test_agent.py
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import governed_turn, lane_for  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))


def fixture(d):
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write("<!-- AI-CONTEXT\ndone: []\n-->\n")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write("# Work Log\n- T-100 done, commit a1b2c3d, evidence ✓\n")


# lane binding (the F1 fix): action determines lane, not the caller
check("lane_for(mark_done) = code-author", lane_for("mark_done") == "code-author")
check("lane_for(read_status) = read-only", lane_for("read_status") == "read-only")
check("lane_for(edit_foo) = code-author", lane_for("edit_foo") == "code-author")
check("lane_for(adr_decide) = architect", lane_for("adr_decide") == "architect")

with tempfile.TemporaryDirectory() as d:
    fixture(d)
    lg = "engine/events.log.jsonl"
    # CLOSED SEAM: weak model attempts mark_done (lane=code-author, floor2) -> refused (can't mislabel)
    r = governed_turn("T-100", "mark_done", 1, model="local-3b", root=d, ts=1, log=lg)
    check("weak model + mark_done -> REFUSED (seam closed)", r["status"] == "refused" and r["lane"] == "code-author")

    # weak model CAN do read-only work (lane allows tier 0)
    r2 = governed_turn("T-100", "read_status", 1, model="local-3b", root=d, ts=2, log=lg)
    check("weak model + read -> executed", r2["status"] == "executed")

    # strong model + L1 mark_done with evidence -> done
    r3 = governed_turn("T-100", "mark_done", 1, model="claude-sonnet", root=d, ts=3, log=lg)
    check("strong + L1 mark_done(evidence) -> done", r3["status"] == "done")
    board = open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), encoding="utf-8").read()
    check("T-100 in done-list", "T-100" in re.search(r"done:\s*\[([^\]]*)\]", board).group(1))

    # L2 action -> Decision Inbox (not executed, awaits human)
    r4 = governed_turn("T-200", "edit_code", 2, model="claude-sonnet", root=d, ts=4, log=lg, inbox="engine/inbox.jsonl")
    check("L2 action -> Decision Inbox", r4["status"] == "inbox")

    # L1 mark_done WITHOUT evidence -> blocked (gate)
    r5 = governed_turn("T-300", "mark_done", 1, model="claude-sonnet", root=d, ts=5, log=lg)
    check("mark_done no evidence -> blocked", r5["status"] == "blocked")

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} governed-dispatch tests passed")
