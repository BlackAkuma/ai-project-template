"""FU-7 — in-process last-hash cache: kills O(n^2) re-read while staying correct (cache invalidated
by any on-disk size change so it can never serve a stale head). Run: python engine/test_events_cache.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402
from events import append_event, verify_chain, _hash, _LAST_HASH  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))
LOG = "engine/events.log.jsonl"


def _recs(path):
    return [json.loads(ln) for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]


# many sequential appends: cache hit path produces a valid, unforked chain
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    for i in range(50):
        append_event("a", "act", f"T-{i}", "ok", ts=i, root=d, log=LOG)
    path = os.path.join(d, LOG)
    recs = _recs(path)
    check("50 sequential appends persisted", len(recs) == 50)
    ok, _ = verify_chain(root=d, log=LOG)
    check("chain valid via cache path", ok is True)
    check("no fork (every prev unique)", len({r["prev"] for r in recs}) == 50)
    # cache is populated for this path
    check("cache populated after appends", os.path.abspath(path) in _LAST_HASH)
    # cache head == on-disk last hash
    check("cached head == on-disk last hash", _LAST_HASH[os.path.abspath(path)][2] == recs[-1]["hash"])

# OUT-OF-BAND external append (simulating another process) -> size changes -> cache MUST miss and
# chain from the real last record, not the stale cached head (else FORK).
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    r1 = append_event("a", "act", "T-1", "ok", ts=1, root=d, log=LOG)  # populates cache
    path = os.path.join(d, LOG)
    # append a VALID chained record directly to the file, bypassing the function (external writer)
    ext_payload = {"ts": 2, "actor": "ext", "action": "act", "target": "T-EXT", "result": "ok", "prev": r1["hash"]}
    ext = dict(ext_payload, hash=_hash(r1["hash"], ext_payload))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(ext, ensure_ascii=False) + "\n")
    # now append via the function — stale cache would chain from r1 (FORK); correct = chain from ext
    r3 = append_event("a", "act", "T-3", "ok", ts=3, root=d, log=LOG)
    check("after out-of-band write: new record chains from REAL last (cache invalidated)",
          r3["prev"] == ext["hash"])
    ok, reason = verify_chain(root=d, log=LOG)
    check(f"chain valid after out-of-band + cache-miss recovery ({reason})", ok is True)
    recs = _recs(path)
    check("no fork after out-of-band write", len({r["prev"] for r in recs}) == len(recs))

# cross-call after a fresh import (cold cache) reads correctly
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    append_event("a", "act", "T-1", "ok", ts=1, root=d, log=LOG)
    _LAST_HASH.clear()  # simulate a brand-new process (cold cache)
    r2 = append_event("a", "act", "T-2", "ok", ts=2, root=d, log=LOG)
    path = os.path.join(d, LOG)
    check("cold cache -> reads last hash correctly (chains, no fork)",
          r2["prev"] == _recs(path)[0]["hash"] and verify_chain(root=d, log=LOG)[0] is True)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} last-hash cache tests passed")
