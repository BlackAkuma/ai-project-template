"""FU-2 — inbox concurrency: atomic write + file-lock (prereq for Phase B multi-agent).
Run: python engine/test_inbox_lock.py
"""
import os
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inbox  # noqa: E402
from inbox import create_item, resolve_item, approval_state, list_open, _FileLock, _read  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

LOG = "engine/events.log.jsonl"
IB = "engine/inbox.jsonl"

# atomic write: tmp + replace, no torn file, no leftover tmp
with tempfile.TemporaryDirectory() as d:
    for i in range(5):
        create_item("g", f"T-{i}", 2, f"r{i}", root=d, inbox=IB, log=LOG)
    items = _read(os.path.join(d, IB))
    check("all 5 items persisted (atomic write)", len(items) == 5)
    stray = [f for f in os.listdir(os.path.join(d, "engine")) if ".tmp." in f]
    check("no leftover .tmp files", stray == [])
    check("no leftover .lock file", not os.path.exists(os.path.join(d, IB + ".lock")))

# concurrent creates: N threads, all items survive (no lost write from RMW race)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    errs = []
    def worker(n):
        try:
            create_item("gc", f"C-{n}", 2, f"concurrent-{n}", root=d, inbox=IB, log=LOG)
        except Exception as e:  # noqa: BLE001
            errs.append(e)
    threads = [threading.Thread(target=worker, args=(n,)) for n in range(12)]
    for t in threads: t.start()
    for t in threads: t.join()
    items = _read(os.path.join(d, IB))
    check("12 concurrent creates -> all 12 survive (lock works)", len(items) == 12 and not errs)
    ids = {i["id"] for i in items}
    check("no duplicate ids from race", len(ids) == 12)

# concurrent approval consume: only ONE thread may consume a single approval (TOCTOU)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    it = create_item("gx", "T-9", 2, "deploy", root=d, inbox=IB, log=LOG)
    resolve_item(it["id"], "approved", by="u", ts=1, root=d, inbox=IB, log=LOG)
    results = []
    def consume():
        results.append(approval_state("gx", "deploy", root=d, inbox=IB, log=LOG))
    threads = [threading.Thread(target=consume) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    approved = results.count("approved")
    check("one-shot approval consumed exactly ONCE under 8-way race", approved == 1)

# lock is actually exclusive (second acquire blocks until first releases)
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "x.jsonl")
    held = _FileLock(p).__enter__()
    check("lockfile exists while held", os.path.exists(p + ".lock"))
    held.__exit__()
    check("lockfile removed on release", not os.path.exists(p + ".lock"))

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} inbox concurrency tests passed")
