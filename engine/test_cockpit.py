"""F5/P5 test — Cockpit read-only renderer (FR-3).
Run: python engine/test_cockpit.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cockpit import render_cockpit  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

state = {"project": {"phase": "stage2", "active_branch": "dev", "blocker": "none"},
         "tasks": [{"id": "T-1", "status": "done"}, {"id": "T-2", "status": "in_progress"},
                   {"id": "T-3", "status": "todo"}]}
open_items = [{"id": "DI-0001", "risk_level": 2, "gate": "task_close", "reason": "missing evidence"}]
events = [{"action": "task.done", "target": "T-1", "result": "pass"}]

out = render_cockpit(state, open_items, events)
check("renders phase", "phase: stage2" in out)
check("renders task counts", "done=1" in out and "in_progress=1" in out and "todo=1" in out)
check("renders open inbox item", "DI-0001" in out and "missing evidence" in out)
check("renders recent activity", "task.done T-1" in out)

# empty inbox -> 'all clear'
out2 = render_cockpit(state, [], [])
check("empty inbox shows all-clear", "all clear" in out2)
check("no events shows placeholder", "no events" in out2)

# read-only: render must not mutate state
import copy  # noqa: E402
snap = copy.deepcopy(state)
render_cockpit(state, open_items, events)
check("render does not mutate state (read-only)", state == snap)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} cockpit-render tests passed")
