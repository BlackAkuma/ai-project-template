"""P4-1: JSON-in-git canonical store + generated views (ADR-012 + ADR-007 dual-authority).

Truth = JSON (sovereign, git-diffable). The AI-CONTEXT block / prose = a GENERATED VIEW.
drift is impossible by construction: the view is always re-derived from canonical JSON,
never hand-edited as a second source. (BRD FR-2.1: drift=0.)
SQLite index = deferred (ADR-012) — build only on real query pressure; never authoritative.
"""
import json
import os

SCHEMA_VERSION = "0.1"


def load(path):
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return {"schema_version": SCHEMA_VERSION, "tasks": []}


_VALID_STATUS = {"todo", "design_validate", "in_progress", "review", "done", "blocked"}


def validate_state(state):
    """Auto-enforced contract on the write path (re-audit dissent fix): schema_version + valid tasks."""
    errs = []
    if not state.get("schema_version"):
        errs.append("missing schema_version")
    for t in state.get("tasks", []):
        if not t.get("id"):
            errs.append("task missing id")
        if t.get("status") not in _VALID_STATUS:
            errs.append(f"task {t.get('id')} bad status {t.get('status')}")
    return (not errs), errs


def save(state, path, validate=True):
    if validate:
        ok, errs = validate_state(state)
        if not ok:
            raise ValueError("invalid state, refusing to persist: " + "; ".join(errs))
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    # sorted keys + indent => stable, git-diffable
    json.dump(state, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)


def render_ai_context(state):
    """Generate AI-CONTEXT status lists from canonical JSON (view — never authoritative)."""
    by = {}
    for t in state.get("tasks", []):
        by.setdefault(t.get("status", "todo"), []).append(t["id"])

    def lst(s):
        return "[" + ",".join(sorted(by.get(s, []))) + "]"

    return "\n".join([
        f"schema_version: {state.get('schema_version', SCHEMA_VERSION)}",
        f"done: {lst('done')}",
        f"in_progress: {lst('in_progress')}",
        f"blocked: {lst('blocked')}",
        f"todo: {lst('todo')}",
    ])


def _by_status(state):
    by = {}
    for t in state.get("tasks", []):
        by.setdefault(t.get("status", "todo"), []).append(t["id"])
    return by


def _lst(ids):
    return "[" + ",".join(sorted(ids)) + "]"


def render_work_status_block(state):
    """P4-2/T-057: generate unified work-status AI-CONTEXT block from canonical JSON."""
    p = state.get("project", {})
    by = _by_status(state)
    return "\n".join([
        f"schema_version: {state.get('schema_version', SCHEMA_VERSION)}",
        f"phase: {p.get('phase', '')}",
        f"active_tasks: {_lst(by.get('in_progress', []))}",
        f"blocker: {p.get('blocker', 'none')}",
        f"next: {p.get('next', '')}",
        f"active_branch: {p.get('active_branch', '')}",
        f"git_pipeline: {p.get('git_pipeline', '')}",
        f"updated: {p.get('updated', '')}",
    ])


def render_task_board_block(state):
    """P4-2/T-057: generate unified task-board AI-CONTEXT block from canonical JSON."""
    by = _by_status(state)
    return "\n".join([
        f"schema_version: {state.get('schema_version', SCHEMA_VERSION)}",
        f"total_tasks: {len(state.get('tasks', []))}",
        f"done: {_lst(by.get('done', []))}",
        f"in_progress: {_lst(by.get('in_progress', []))}",
        f"blocked: {_lst(by.get('blocked', []))}",
        f"todo: {_lst(by.get('todo', []))}",
    ])


def verify_no_drift(state, rendered_block, renderer=render_ai_context):
    """drift=0 invariant: regenerate from canonical == the rendered view in the file."""
    return renderer(state) == rendered_block


import re as _re  # noqa: E402

# F12/FR-2.2: required AI-CONTEXT fields per state-file kind (typed schema, single source).
AI_CONTEXT_REQUIRED = {
    "work-status": ["schema_version", "phase", "updated"],
    "task-board": ["schema_version", "total_tasks", "done"],
    "work-log": ["schema_version", "last_session"],
}


def validate_ai_context(block_text, kind):
    """Return (ok, missing). Checks the AI-CONTEXT block has required fields for its kind (FR-2.2)."""
    req = AI_CONTEXT_REQUIRED.get(kind)
    if req is None:
        return False, [f"unknown file_kind '{kind}'"]
    missing = [f for f in req if not _re.search(rf"^\s*{_re.escape(f)}\s*:", block_text, _re.M)]
    return (not missing), missing
