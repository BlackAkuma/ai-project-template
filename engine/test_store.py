"""P4-1 test — canonical JSON store + generated view, drift=0 invariant.
Run: python engine/test_store.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from store import load, save, render_ai_context, verify_no_drift  # noqa: E402

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

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} canonical-store + drift=0 tests passed")
