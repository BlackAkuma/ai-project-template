"""P3-2: gated state mutation — the ONLY legit path to mark a task done.

Constitutive: mark_done() runs preconditions (gate), and ONLY on pass does it
update the task-board done-list AND append a signed Event (events.py).
audit_done() then reconciles: any task in done-list WITHOUT a matching legit event
= faked (direct edit) → detectable. Combined with hash-chain (P3-1), faking 'done'
is caught two ways. (Full FS-allowlist so direct writes are impossible = later P3.)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolvers import RESOLVERS  # noqa: E402
from events import append_event, verify_chain  # noqa: E402

BOARD = "CoreAiWorkspaces/02-task/task-board.md"
WORKLOG = "CoreAiWorkspaces/03-log/work-log-index.md"
LOG = "engine/events.log.jsonl"


def _read(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def _done_list(txt):
    m = re.search(r"done:\s*\[([^\]]*)\]", txt)
    if not m:
        return None, []
    items = [x.strip() for x in m.group(1).split(",") if x.strip()]
    return m, items


def mark_done(task_id, root=".", ts=0, actor="ai", board=BOARD, worklog=WORKLOG, log=LOG):
    """Gate then mutate. Returns {ok, missing, event}. The only legit way to set done."""
    ctx = {"root": root, "staged_diff": "", "staged_files": [], "staged_added": ""}
    missing = []
    if not RESOLVERS["entry_exists"](ctx, file=worklog, key=task_id):
        missing.append("worklog_entry")
    if not RESOLVERS["evidence_count_gte"](ctx, task=task_id, n=1):
        missing.append("evidence")
    if not RESOLVERS["tests_green"](ctx):
        missing.append("tests_red")  # BL-6: configured test command actually ran and FAILED
    if missing:
        ev = append_event(actor, "task.done", task_id, "blocked:" + ",".join(missing), ts=ts, root=root, log=log)
        return {"ok": False, "missing": missing, "event": ev, "effect": "decision-inbox"}

    p = os.path.join(root, board)
    txt = _read(p)
    m, items = _done_list(txt)
    if m is not None and task_id not in items:
        items.append(task_id)
        txt = txt[:m.start()] + "done: [" + ",".join(items) + "]" + txt[m.end():]
        open(p, "w", encoding="utf-8").write(txt)
    ev = append_event(actor, "task.done", task_id, "pass", ts=ts, root=root, log=log)
    return {"ok": True, "missing": [], "event": ev, "effect": "done"}


def audit_done(root=".", board=BOARD, log=LOG):
    """Reconcile done-list vs legit events. faked_done_no_event = direct-edit fakes."""
    _, done = _done_list(_read(os.path.join(root, board)))
    legit = set()
    evp = os.path.join(root, log)
    if os.path.exists(evp):
        for ln in open(evp, encoding="utf-8").read().splitlines():
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if r.get("action") == "task.done" and r.get("result") == "pass":
                legit.add(r.get("target"))
    chain_ok, reason = verify_chain(root=root, log=log)
    return {
        "done": done,
        "faked_done_no_event": [t for t in done if t not in legit],
        "chain_ok": chain_ok,
        "chain_reason": reason,
    }
