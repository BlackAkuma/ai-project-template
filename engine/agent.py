"""F2 / P6: governed agent dispatch — one governed turn (the SHIP core, BRD FR-1/FR-3).

A turn: role-floor check → risk-tier routing → L1 auto-execute (gated) / L2-3 → Decision Inbox.
mark_done goes through the Task Close Gate (evidence) + signed event. Everything audited.
Ties together llm (role-floor) + govern (gated mutation) + inbox (human-gate) + events (audit).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm import assign  # noqa: E402
from govern import mark_done  # noqa: E402
from inbox import create_item  # noqa: E402
from events import append_event  # noqa: E402

LOG = "engine/events.log.jsonl"
INBOX = "engine/inbox.jsonl"

# Lane is DERIVED from the action — NOT caller-asserted (closes F1 panel consensus seam:
# a caller can't mislabel code-work as 'advisory' to slip a weak model through the floor).
ACTION_LANE = {
    "mark_done": "code-author",
    "edit_code": "code-author",
    "commit": "code-author",
    "architect_change": "architect",
    "adr_decide": "architect",
    "read": "read-only",
    "inspect": "read-only",
    "comment": "advisory",
    "review": "advisory",
}


# Dangerous intents force Level 3 (FR-1.3 hard-stop: data-loss/security/prod) regardless of
# caller-supplied risk_level — closes the F2-panel risk-axis mislabel seam.
DANGEROUS = {"deploy_prod", "run_migration", "drop_table", "delete_data", "push_prod",
             "rotate_keys", "prod_release", "force_push"}


def lane_for(intent):
    """Map an action to its REQUIRED lane (bound to the work, not the caller's claim).
    Fail-CLOSED: unknown intents default to code-author (high floor), not advisory."""
    if intent in ACTION_LANE:
        return ACTION_LANE[intent]
    low = intent.lower()
    if "architect" in low or "adr" in low or "deploy" in low or "migrat" in low:
        return "architect"
    if low.startswith(("read", "inspect", "list", "show", "get")):
        return "read-only"
    if low.startswith(("comment", "review", "suggest", "note")):
        return "advisory"
    return "code-author"  # fail-closed: unknown/mutating work needs a capable model


def normalize_risk(risk_level, intent):
    """Clamp risk to 0-3 (invalid -> 2 conservative, ADR-008); dangerous intents forced to 3 (FR-1.3)."""
    try:
        r = int(risk_level)
        if r < 0 or r > 3:
            r = 2
    except (TypeError, ValueError):
        r = 2
    low = intent.lower()
    if intent in DANGEROUS or any(k in low for k in ("prod", "migrat", "drop_", "delete_", "rotate_key")):
        r = max(r, 3)
    return r


def governed_turn(task_id, intent, risk_level, model="stub-strong",
                  root=".", ts=0, log=LOG, inbox=INBOX):
    """One governed agent action. intent: 'mark_done' | free-form. Returns {status, ...}.

    status: refused (role-floor) | inbox (L2-3 awaits human) | done | blocked | executed
    Lane is derived from intent (lane_for) — caller cannot self-downgrade the floor.
    """
    # 1) role-floor on the DERIVED lane — weak model can't take code/architect work (structural)
    role = lane_for(intent)
    ok, reason = assign(model, role)
    if not ok:
        append_event(model, "agent.refused", task_id, f"{reason} [lane={role} for intent={intent}]", ts=ts, root=root, log=log)
        return {"status": "refused", "reason": reason, "lane": role}

    # 2) risk-tier (ADR-008): normalize risk (clamp + dangerous-intent force-L3, FR-1.3) — caller
    #    can't downgrade risk to skip the gate. L0/L1 auto, L2-3 -> Decision Inbox (await human).
    risk = normalize_risk(risk_level, intent)
    if risk >= 2:
        item = create_item("agent_action", task_id, risk, intent, ts=ts, root=root, inbox=inbox, log=log)
        return {"status": "inbox", "item": item["id"], "risk_level": risk}

    # 3) L1 auto-execute — mark_done passes through the Task Close Gate (evidence required)
    if intent == "mark_done":
        r = mark_done(task_id, root=root, ts=ts, log=log)
        return {"status": "done" if r["ok"] else "blocked", "detail": r}

    # other low-risk action: log + (stub) execute
    append_event(model, "agent.action", task_id, intent, ts=ts, root=root, log=log)
    return {"status": "executed", "intent": intent}
