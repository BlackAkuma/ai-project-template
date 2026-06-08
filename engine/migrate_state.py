"""F6/T-057: state schema migration tool — markdown AI-CONTEXT <-> canonical JSON.

Dual-authority cutover (ADR-007/012): parse existing live AI-CONTEXT blocks into canonical
state, then GENERATE the block from canonical (single source going forward).
--check (default, READ-ONLY) verifies round-trip; --apply writes generated blocks
(run when the active loop is idle — flagged, not auto-run, to avoid clobbering live edits).
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from store import render_task_board_block  # noqa: E402

STATUSES = ("done", "in_progress", "blocked", "todo")


def parse_board(text):
    """Extract task state from a task-board AI-CONTEXT block -> canonical state dict."""
    state = {"schema_version": "0.1", "tasks": []}
    for status in STATUSES:
        m = re.search(rf"\b{status}:\s*\[([^\]]*)\]", text)
        if not m:
            continue
        for tid in [x.strip() for x in m.group(1).split(",") if x.strip()]:
            if tid.startswith("T-") or tid.startswith("F"):  # task/feature ids only
                state["tasks"].append({"id": tid, "status": status})
    return state


def ids_by_status(state):
    out = {}
    for t in state["tasks"]:
        out.setdefault(t["status"], []).append(t["id"])
    return {k: sorted(v) for k, v in out.items()}


def check_roundtrip(board_text):
    """Read-only: parse -> state -> regenerate block. Returns (state, generated_block, ok)."""
    state = parse_board(board_text)
    gen = render_task_board_block(state)
    regen_state = parse_board(gen)
    ok = ids_by_status(state) == ids_by_status(regen_state)  # canonical is stable under re-render
    return state, gen, ok
