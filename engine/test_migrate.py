"""F6/T-057 test — markdown<->canonical migration round-trip (read-only check).
Run: python engine/test_migrate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from migrate_state import parse_board, check_roundtrip, ids_by_status  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

board = """<!-- AI-CONTEXT
total_tasks: 4
done: [T-001,T-003]
in_progress: [T-002]
blocked: []
todo: [T-004]
note: blah
-->
# Task Board
"""

state = parse_board(board)
check("parsed done", set(ids_by_status(state).get("done", [])) == {"T-001", "T-003"})
check("parsed in_progress", ids_by_status(state).get("in_progress") == ["T-002"])
check("parsed todo", ids_by_status(state).get("todo") == ["T-004"])
check("ignores prose 'note:' line", all(t["id"].startswith(("T-", "F")) for t in state["tasks"]))

st, gen, ok = check_roundtrip(board)
check("round-trip stable (canonical re-renders same)", ok is True)
check("generated block has done list", "done: [T-001,T-003]" in gen)

# real repo board (read-only sanity — must parse without error)
repo_board = os.path.join(os.path.dirname(__file__), "..", "CoreAiWorkspaces", "02-task", "task-board.md")
if os.path.exists(repo_board):
    txt = open(repo_board, encoding="utf-8").read()
    _, _, rok = check_roundtrip(txt)
    check("live task-board round-trips", rok is True)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} migration round-trip tests passed")
