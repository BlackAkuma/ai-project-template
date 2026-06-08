"""P6-1: Decision Inbox data layer (Engine-side) — project-level durable human-gate.

Level 2-3 gate verdicts become durable Inbox items; a human resolves (approve/reject).
Every create/resolve is recorded in the Event log (P3-1) = auditable + tamper-evident.
Differentiator (BRD §3/FR-3): durable, PROJECT-level (not per-run like Conductor, not
per-ticket like Jira), inspectable. The UI that renders this = Shell (gated by G4/ADR-011).

inbox.jsonl = current state (derived, rewritable view). events.log = audit truth (chained).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import append_event  # noqa: E402

INBOX = "engine/inbox.jsonl"
LOG = "engine/events.log.jsonl"


def _read(path):
    if not os.path.exists(path):
        return []
    return [json.loads(ln) for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]


def _write(path, items):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + ("\n" if items else ""))


def create_item(gate, task, risk_level, reason, item_id=None, ts=0, root=".", inbox=INBOX, log=LOG):
    """Create an Inbox item from a gate verdict. ONLY Level 2-3 create items (L0/L1 auto-pass)."""
    if int(risk_level) < 2:
        return None  # risk-tiered: low-risk never reaches the human (ADR-008, anti approval-fatigue)
    path = os.path.join(root, inbox)
    items = _read(path)
    item_id = item_id or f"DI-{len(items) + 1:04d}"
    item = {"id": item_id, "ts": ts, "gate": gate, "task": task, "risk_level": int(risk_level),
            "reason": reason, "status": "open", "resolved_by": None, "resolved_ts": None}
    items.append(item)
    _write(path, items)
    append_event("engine", "inbox.create", item_id, f"gate={gate};L{risk_level}", ts=ts, root=root, log=log)
    return item


def resolve_item(item_id, decision, by, ts=0, root=".", inbox=INBOX, log=LOG):
    """Human resolves an open item. decision = 'approved' | 'rejected'. Recorded to audit log."""
    assert decision in ("approved", "rejected")
    path = os.path.join(root, inbox)
    items = _read(path)
    target = None
    for it in items:
        if it["id"] == item_id and it["status"] == "open":
            it["status"], it["resolved_by"], it["resolved_ts"] = decision, by, ts
            target = it
    if target is None:
        return None  # not found or already resolved
    _write(path, items)
    append_event(by, "inbox.resolve", item_id, decision, ts=ts, root=root, log=log)
    return target


def list_open(root=".", inbox=INBOX):
    return [i for i in _read(os.path.join(root, inbox)) if i["status"] == "open"]
