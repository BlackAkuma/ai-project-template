"""P4-1 test — canonical JSON store + generated view, drift=0 invariant.
Run: python engine/test_store.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from store import (  # noqa: E402
    load, save, render_ai_context, verify_no_drift,
    render_work_status_block, render_task_board_block, validate_ai_context,
)

cases = []
def check(name, cond): cases.append((name, bool(cond)))

state = {"schema_version": "0.1", "tasks": [
    {"id": "T-001", "status": "done"},
    {"id": "T-003", "status": "done"},
    {"id": "T-002", "status": "in_progress"},
    {"id": "T-004", "status": "todo"},
]}

with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "state", "tasks.json")
    save(state, p)
    check("round-trip load == save", load(p) == state)

    view = render_ai_context(state)
    check("view: done sorted", "done: [T-001,T-003]" in view)
    check("view: in_progress", "in_progress: [T-002]" in view)
    check("view: todo", "todo: [T-004]" in view)

    # drift=0: regenerated view matches itself
    check("no-drift on fresh render", verify_no_drift(state, view) is True)

    # mutate canonical -> view changes (truth drives view, single source)
    state["tasks"].append({"id": "T-005", "status": "done"})
    view2 = render_ai_context(state)
    check("canonical change drives view", "done: [T-001,T-003,T-005]" in view2)
    # the OLD view is now stale vs new canonical -> drift detectable
    check("stale view detected vs new canonical", verify_no_drift(state, view) is False)

# P4-2/T-057: unified work-status + task-board blocks from canonical (single source)
state2 = {"schema_version": "0.1",
          "project": {"phase": "stage2", "active_branch": "explore/x", "git_pipeline": "dev->main",
                      "blocker": "none", "next": "P4-2", "updated": "2026-06-07"},
          "tasks": [{"id": "T-001", "status": "done"}, {"id": "T-002", "status": "in_progress"},
                    {"id": "T-003", "status": "todo"}]}
ws = render_work_status_block(state2)
tb = render_task_board_block(state2)
check("work-status: active_tasks from in_progress", "active_tasks: [T-002]" in ws)
check("work-status: phase + git_pipeline rendered", "phase: stage2" in ws and "git_pipeline: dev->main" in ws)
check("task-board: total_tasks counted", "total_tasks: 3" in tb)
check("task-board: done list", "done: [T-001]" in tb)
check("both views from ONE canonical (no 2nd source)", verify_no_drift(state2, ws, render_work_status_block) and verify_no_drift(state2, tb, render_task_board_block))

# F12/FR-2.2: AI-CONTEXT schema validation per file kind
good_ws = "schema_version: 0.1\nphase: stage2\nupdated: 2026-06-08\n"
check("valid work-status block validates", validate_ai_context(good_ws, "work-status")[0] is True)
ok_m, missing = validate_ai_context("phase: x\n", "work-status")
check("missing schema_version+updated -> fail", ok_m is False and "schema_version" in missing)
check("valid task-board block", validate_ai_context("schema_version: 0.1\ntotal_tasks: 5\ndone: [T-1]\n", "task-board")[0] is True)
check("unknown kind -> fail", validate_ai_context("x: 1", "bogus")[0] is False)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} canonical-store + drift=0 tests passed")
