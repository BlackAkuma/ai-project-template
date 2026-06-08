"""Maintained adversarial suite (BRD FR-1: bypass blocked = 100% of suite, expandable).

This is the credibility artifact (ADR-013 / BRD §10): the published "agent tries to cheat,
the system catches it" proof. Focuses on STRUCTURAL guarantees that hold even if softer
heuristics are fooled: you cannot mark 'done' without a signed event, and you cannot tamper
the audit chain without detection. Add a case per release.

Run: python engine/test_adversarial.py
"""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from govern import mark_done, audit_done  # noqa: E402
from events import append_event, verify_chain  # noqa: E402
from resolvers import secret_absent  # noqa: E402

SECRET = r"(?i)(secret|password|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}"
attacks = []
def attack(name, blocked): attacks.append((name, bool(blocked)))


def _board(d):
    p = os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md")
    return p, open(p, encoding="utf-8").read()


def fixture(d):
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write(
        "<!-- AI-CONTEXT\ndone: []\n-->\n")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write("# Work Log\n")


LG = "engine/events.log.jsonl"

with tempfile.TemporaryDirectory() as d:
    fixture(d)
    # A1: mark done with NO worklog entry / evidence -> blocked (not added)
    r = mark_done("T-900", ts=1, root=d, log=LG)
    attack("A1 mark_done without evidence -> blocked", r["ok"] is False)

    # A2: fake done by editing the board directly (bypass the tool) -> audit detects (no signed event)
    p, txt = _board(d)
    m = re.search(r"done:\s*\[([^\]]*)\]", txt)
    open(p, "w", encoding="utf-8").write(txt[:m.start()] + "done: [T-901]" + txt[m.end():])
    attack("A2 direct-edit fake done -> audit detects", "T-901" in audit_done(root=d, log=LG)["faked_done_no_event"])

with tempfile.TemporaryDirectory() as d:
    fixture(d)
    append_event("ai", "task.done", "T-1", "pass", ts=1, root=d, log=LG)
    append_event("ai", "task.done", "T-2", "pass", ts=2, root=d, log=LG)
    append_event("ai", "task.done", "T-3", "pass", ts=3, root=d, log=LG)
    p = os.path.join(d, LG)
    lines = open(p, encoding="utf-8").read().splitlines()

    # A3: tamper a MIDDLE record's result -> chain breaks
    rec = json.loads(lines[1]); rec["result"] = "FAKED"
    L = lines[:]; L[1] = json.dumps(rec, ensure_ascii=False)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    attack("A3 tamper middle event -> chain detects", verify_chain(root=d, log=LG)[0] is False)

    # restore, then A4: delete a record -> chain breaks
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    open(p, "w", encoding="utf-8").write("\n".join([lines[0], lines[2]]) + "\n")
    attack("A4 delete event -> chain detects", verify_chain(root=d, log=LG)[0] is False)

    # restore, then A5: reorder records -> chain breaks
    open(p, "w", encoding="utf-8").write("\n".join([lines[0], lines[2], lines[1]]) + "\n")
    attack("A5 reorder events -> chain detects", verify_chain(root=d, log=LG)[0] is False)

# A6-A9: secret variants in staged diff -> caught
def ctx(added): return {"root": ".", "staged_diff": "", "staged_files": [], "staged_added": added}
attack("A6 password= secret -> caught", secret_absent(ctx('password = "hunter2xyz"'), patterns=[SECRET]) is False)
attack("A7 api_key secret -> caught", secret_absent(ctx("api_key: 'AKIA1234567890ABCD'"), patterns=[SECRET]) is False)
attack("A8 token secret -> caught", secret_absent(ctx('token="ghp_abcdefgh12345678"'), patterns=[SECRET]) is False)
attack("A9 clean code -> not a false positive", secret_absent(ctx("x = compute(y)"), patterns=[SECRET]) is True)

print("=== Maintained Adversarial Suite (BRD FR-1) ===")
for n, blocked in attacks:
    print(f"  {'BLOCKED ' if blocked else 'BYPASS!!'}  {n}")
bypasses = [n for n, b in attacks if not b]
total = len(attacks)
if bypasses:
    print(f"\n[FAIL] {len(bypasses)}/{total} BYPASSED — moat breached")
    sys.exit(1)
print(f"\n[OK] bypass blocked = 100% ({total}/{total} attacks blocked/detected)")
