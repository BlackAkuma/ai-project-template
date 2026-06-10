"""BL-10 test — latency measurement works + deterministic gate path within (generous CI) budget.
Run: python engine/test_latency.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from latency import measure  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

ROOT = os.path.join(os.path.dirname(__file__), "..")
r = measure(ROOT)
check("measures all 4 touchpoints", len(r) == 4 and all(isinstance(v, float) for v in r.values()))
for k, v in r.items():
    print(f"  [measure] {k}: {v} ms")
# CI-generous threshold (3s); the 1s NFR-N5 budget is enforced by `python engine/latency.py` in dogfood
check("deterministic path under 3s (CI-generous)", max(r.values()) < 3000)
check("no negative/zero timing", all(v > 0 for v in r.values()))

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} latency tests passed")
