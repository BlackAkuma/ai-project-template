"""F9/FR-2.3 test — CORE 11 entities typed validation.
Run: python engine/test_entities.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entities import validate, CORE_KINDS  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

check("exactly 11 CORE entities", len(CORE_KINDS) == 11)
for k in ["Project", "Requirement", "Plan", "Task", "Evidence", "Decision",
          "TeamMember", "Gate", "Repo", "Entity", "Event"]:
    check(f"{k} defined", k in CORE_KINDS)

# valid records
check("valid Task", validate("Task", {"id": "T-1", "title": "x", "status": "done", "source_ref": "BRD-1"})[0])
check("valid Evidence", validate("Evidence", {"id": "E1", "task_ref": "T-1", "class": "machine-verifiable"})[0])
check("valid Decision", validate("Decision", {"id": "ADR-1", "status": "Accepted"})[0])
check("valid TeamMember", validate("TeamMember", {"id": "u1", "role": "dev", "kind": "human"})[0])

# missing required -> fail
ok, errs = validate("Task", {"id": "T-2", "title": "x"})  # missing status, source_ref
check("Task missing required -> fail", ok is False and any("status" in e for e in errs))

# bad enum -> fail
check("bad Task.status enum -> fail", validate("Task", {"id": "T-3", "title": "x", "status": "wat", "source_ref": "r"})[0] is False)
check("bad Evidence.class enum -> fail", validate("Evidence", {"id": "E2", "task_ref": "T", "class": "vibes"})[0] is False)

# unknown kind -> fail
check("unknown kind -> fail", validate("Wizard", {"id": "x"})[0] is False)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} CORE-entity validation tests passed")
