"""P3-1 test — Event log hash chain + tamper detection (the adversarial proof core).
Run: python engine/test_events.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import append_event, verify_chain  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

with tempfile.TemporaryDirectory() as d:
    log = "ev.jsonl"
    append_event("ai", "task.done", "T-001", "pass", ts=1, root=d, log=log)
    append_event("ai", "task.done", "T-002", "pass", ts=2, root=d, log=log)
    ok, reason = verify_chain(root=d, log=log)
    check("clean chain verifies", ok is True)

    # ADVERSARIAL: tamper a record (fake a result) directly in the log
    p = os.path.join(d, log)
    lines = open(p, encoding="utf-8").read().splitlines()
    rec = json.loads(lines[0]); rec["result"] = "FAKED"
    lines[0] = json.dumps(rec, ensure_ascii=False)
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    ok2, reason2 = verify_chain(root=d, log=log)
    check("tampered record DETECTED", ok2 is False)

with tempfile.TemporaryDirectory() as d2:
    log = "ev2.jsonl"
    append_event("ai", "a", "x", "pass", ts=1, root=d2, log=log)
    append_event("ai", "b", "y", "pass", ts=2, root=d2, log=log)
    # ADVERSARIAL: delete/reorder — drop first line
    p = os.path.join(d2, log)
    lines = open(p, encoding="utf-8").read().splitlines()
    open(p, "w", encoding="utf-8").write(lines[1] + "\n")
    ok3, _ = verify_chain(root=d2, log=log)
    check("deleted/reordered event DETECTED", ok3 is False)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} event-chain tamper tests passed")
