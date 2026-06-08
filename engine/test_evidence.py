"""F11/FR-2.4 test — evidence 2-class verification (machine vs human-attested).
Run: python engine/test_evidence.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evidence import verify  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

# machine-verifiable: deterministic checks
check("commit valid sha", verify({"class": "machine-verifiable", "type": "commit", "ref": "a1b2c3d"})[0] is True)
check("commit bad sha -> fail", verify({"class": "machine-verifiable", "type": "commit", "ref": "nope"})[0] is False)
check("test exit 0 -> verified", verify({"class": "machine-verifiable", "type": "test", "exit": 0})[0] is True)
check("test exit 1 -> fail", verify({"class": "machine-verifiable", "type": "test", "exit": 1})[0] is False)

with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "out.bin"), "w").write("x")
    check("artifact exists -> verified", verify({"class": "machine-verifiable", "type": "artifact", "ref": "out.bin"}, root=d)[0] is True)
    check("artifact missing -> fail", verify({"class": "machine-verifiable", "type": "artifact", "ref": "no.bin"}, root=d)[0] is False)

# human-attested: presence-only (Engine doesn't judge truth)
check("human-attested with signoff -> verified(presence)", verify({"class": "human-attested", "signoff": "user@2026"})[0] is True)
check("human-attested no signoff -> fail", verify({"class": "human-attested"})[0] is False)

# unknown class -> fail closed
check("unknown class -> fail", verify({"class": "vibes"})[0] is False)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} evidence 2-class tests passed")
