"""P6-1 test — Decision Inbox: risk-tiered create + resolve + audit trail.
Run: python engine/test_inbox.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import create_item, resolve_item, list_open, escalate_overdue  # noqa: E402
from events import verify_chain  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

with tempfile.TemporaryDirectory() as d:
    ib = "engine/inbox.jsonl"
    lg = "engine/events.log.jsonl"

    # L1 auto-pass -> no inbox item (anti approval-fatigue, ADR-008)
    check("L1 creates no item", create_item("task_close", "T-001", 1, "low", ts=1, root=d, inbox=ib, log=lg) is None)

    # L2 -> durable item, appears open
    it = create_item("task_close", "T-100", 2, "missing evidence", item_id="DI-0001", ts=2, root=d, inbox=ib, log=lg)
    check("L2 creates item", it is not None and it["status"] == "open")
    check("open list has it", any(x["id"] == "DI-0001" for x in list_open(root=d, inbox=ib)))

    # L3 -> item too
    create_item("secret_scan", "-", 3, "secret detected", item_id="DI-0002", ts=3, root=d, inbox=ib, log=lg)
    check("two open items", len(list_open(root=d, inbox=ib)) == 2)

    # resolve approved -> leaves open list, recorded
    r = resolve_item("DI-0001", "approved", by="user", ts=4, root=d, inbox=ib, log=lg)
    check("resolve returns item", r is not None and r["status"] == "approved")
    check("resolved item left open list", all(x["id"] != "DI-0001" for x in list_open(root=d, inbox=ib)))
    check("one open item remains", len(list_open(root=d, inbox=ib)) == 1)

    # resolving already-resolved / unknown -> None
    check("re-resolve returns None", resolve_item("DI-0001", "rejected", by="user", ts=5, root=d, inbox=ib, log=lg) is None)

    # audit: every create+resolve chained in events, intact
    ok, _ = verify_chain(root=d, log=lg)
    check("audit chain intact (create+resolve logged)", ok is True)

    # F10/FR-3.4: SLA escalation — DI-0002 created at ts=3; now far past SLA -> escalated
    esc = escalate_overdue(now_ts=100000, sla=86400, root=d, inbox=ib, log=lg)
    check("overdue open item escalated", any(i["id"] == "DI-0002" for i in esc))
    # idempotent: not re-escalated
    esc2 = escalate_overdue(now_ts=100001, sla=86400, root=d, inbox=ib, log=lg)
    check("escalation idempotent", esc2 == [])

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} Decision Inbox tests passed")
