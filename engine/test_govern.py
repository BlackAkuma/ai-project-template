"""P3-2 test — gated mark_done + audit detects faked done (the constitutive proof).
Run: python engine/test_govern.py
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from govern import mark_done, audit_done  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))


def fixture(d):
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write(
        "<!-- AI-CONTEXT\ndone: [T-001]\n-->\n# Task Board\n")
    # T-100 has worklog entry + evidence marker (commit hash); T-200 has neither
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write(
        "# Work Log\n- T-100 implemented, tested, commit abc1234 evidence ✓\n")


with tempfile.TemporaryDirectory() as d:
    fixture(d)
    # legit: T-100 meets preconditions -> mark_done succeeds + event recorded
    r1 = mark_done("T-100", root=d, ts=1)
    check("legit mark_done ok", r1["ok"] is True)
    board = open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), encoding="utf-8").read()
    check("T-100 added to done-list", "T-100" in re.search(r"done:\s*\[([^\]]*)\]", board).group(1))

    # blocked: T-200 has no worklog entry / evidence -> blocked to inbox, NOT added
    r2 = mark_done("T-200", root=d, ts=2)
    check("missing-evidence mark_done blocked", r2["ok"] is False and "worklog_entry" in r2["missing"])
    board2 = open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), encoding="utf-8").read()
    check("T-200 NOT in done-list", "T-200" not in re.search(r"done:\s*\[([^\]]*)\]", board2).group(1))

    # audit so far: T-001 (seed, no event) is flagged; T-100 legit (has event)
    a1 = audit_done(root=d)
    check("audit: T-100 not faked (has event)", "T-100" not in a1["faked_done_no_event"])
    check("audit chain intact", a1["chain_ok"] is True)

    # ADVERSARIAL: directly edit board to fake T-999 done (bypass the tool)
    bp = os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md")
    txt = open(bp, encoding="utf-8").read()
    m = re.search(r"done:\s*\[([^\]]*)\]", txt)
    items = [x.strip() for x in m.group(1).split(",") if x.strip()] + ["T-999"]
    open(bp, "w", encoding="utf-8").write(txt[:m.start()] + "done: [" + ",".join(items) + "]" + txt[m.end():])
    a2 = audit_done(root=d)
    check("ADVERSARIAL: faked T-999 (direct edit) DETECTED", "T-999" in a2["faked_done_no_event"])

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} gated-mutation + faked-done-detection tests passed")
