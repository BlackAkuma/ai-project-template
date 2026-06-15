"""FU-1 — reject re-open flow: a resolved item can be reconsidered IN-BAND (audited), no hand-edit.
Run: python engine/test_inbox_reopen.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import create_item, resolve_item, reopen_item, approval_state, list_open  # noqa: E402
from events import verify_chain  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))
LOG = "engine/events.log.jsonl"
IB = "engine/inbox.jsonl"

with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    it = create_item("gx", "T-1", 2, "deploy", root=d, inbox=IB, log=LOG)

    # reject -> approval_state rejected (the FU-1 problem: stuck forever in-band)
    resolve_item(it["id"], "rejected", by="u", ts=1, root=d, inbox=IB, log=LOG, reason="too risky now")
    check("rejected -> approval_state 'rejected'", approval_state("gx", "deploy", root=d, inbox=IB, log=LOG) == "rejected")

    # FU-1: reopen -> back to open, decision fresh
    r = reopen_item(it["id"], by="user", ts=2, root=d, inbox=IB, log=LOG, reason="situation changed")
    check("reopen returns item", r is not None and r["status"] == "open")
    check("reopened item appears in list_open", any(i["id"] == it["id"] for i in list_open(root=d, inbox=IB)))
    check("approval_state now 'pending' (fresh decision)", approval_state("gx", "deploy", root=d, inbox=IB, log=LOG) == "pending")
    check("resolution cleared on reopen", r.get("resolved_by") is None and "resolution_reason" not in r)
    check("reopened_count tracked", r.get("reopened_count") == 1)

    # now approve the reopened item -> consumable once
    resolve_item(it["id"], "approved", by="u", ts=3, root=d, inbox=IB, log=LOG)
    check("after reopen+approve -> approved (once)", approval_state("gx", "deploy", root=d, inbox=IB, log=LOG) == "approved")

    # reopen of a non-existent / already-open item -> None
    check("reopen unknown id -> None", reopen_item("DI-9999", by="u", root=d, inbox=IB, log=LOG) is None)

    # audit chain intact through reject->reopen->approve->consume
    ok, _ = verify_chain(root=d, log=LOG)
    check("audit chain intact (reject/reopen/approve all logged)", ok is True)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} reject-reopen tests passed")
