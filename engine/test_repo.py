"""F3/P9 test — multi-repo manifest + cross-repo impact detection (FR-5).
Run: python engine/test_repo.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo import load_manifest, impacted_by, detect_drift, deprecated_entities, project_map  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

manifest = {
    "repos": [
        {"id": "backend", "role": "service", "purpose": "API + auth"},
        {"id": "frontend", "role": "web", "purpose": "user UI"},
        {"id": "mobile", "role": "app", "purpose": "mobile client"},
    ],
    "entities": [
        {"id": "E1", "name": "Auth contract", "owner_repo": "backend", "consumers": ["frontend", "mobile"], "status": "active"},
        {"id": "E2", "name": "Event schema v1", "owner_repo": "backend", "consumers": ["frontend"], "status": "deprecated"},
    ],
}

with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "manifest.json")
    json.dump(manifest, open(p, "w", encoding="utf-8"))
    m = load_manifest(p)
    check("manifest round-trips", m == manifest)

check("impacted_by(Auth) = frontend+mobile", set(impacted_by(manifest, "E1")) == {"frontend", "mobile"})
check("impacted_by(unknown) = []", impacted_by(manifest, "E9") == [])

drift = detect_drift(manifest, ["E1"])
check("detect_drift flags owner+impacted", drift and drift[0]["owner_repo"] == "backend" and set(drift[0]["impacted"]) == {"frontend", "mobile"})

check("deprecated_entities = [E2]", deprecated_entities(manifest) == ["E2"])

pm = project_map(manifest)
check("project_map lists repos", "repo backend" in pm and "repo mobile" in pm)
check("project_map shows seams", "Auth contract" in pm and "backend -> [frontend,mobile]" in pm)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} multi-repo tests passed")
