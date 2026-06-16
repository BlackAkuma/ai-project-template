"""FU-8 — state writes are atomic + serialized (no torn file / lost canonical update under concurrency).
Run: python engine/test_state_atomic.py
"""
import json
import os
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import store  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))


def _valid_state(n):
    # minimal schema-valid state (mirrors what validate_state expects); vary by n
    return {"schema_version": store.SCHEMA_VERSION, "project": {"phase": "p", "active_branch": "dev"},
            "tasks": [{"id": f"T-{n}", "status": "todo"}]}


# atomic write: no leftover tmp, file is complete + parseable
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "engine", "state.json")
    store.save(_valid_state(1), p)
    check("saved file parses (not torn)", json.load(open(p, encoding="utf-8"))["tasks"][0]["id"] == "T-1")
    stray = [f for f in os.listdir(os.path.dirname(p)) if ".tmp." in f]
    check("no leftover .tmp", stray == [])
    check("no leftover .lock", not os.path.exists(p + ".lock"))

# concurrent saves to the SAME canonical path: file always ends valid (no torn json), no lost tmp
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "engine", "state.json")
    store.save(_valid_state(0), p)
    errs = []
    def worker(n):
        try:
            store.save(_valid_state(n), p)
        except Exception as e:  # noqa: BLE001
            errs.append(e)
    threads = [threading.Thread(target=worker, args=(n,)) for n in range(16)]
    for t in threads: t.start()
    for t in threads: t.join()
    check("16 concurrent saves: no error", not errs)
    # the final file must be COMPLETE + valid (one of the writers won; never a torn merge)
    obj = json.load(open(p, encoding="utf-8"))
    check("final state is a complete valid json (no tear)", obj["tasks"][0]["id"].startswith("T-"))
    stray = [f for f in os.listdir(os.path.dirname(p)) if ".tmp." in f]
    check("no leftover .tmp after concurrent saves", stray == [])
    check("no leftover .lock after concurrent saves", not os.path.exists(p + ".lock"))

# CROSS-PROCESS saves to same canonical path: every process exits 0, file ends valid
import subprocess  # noqa: E402
ENGINE = os.path.dirname(os.path.abspath(__file__))
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "engine", "state.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    code = ("import sys; sys.path.insert(0, r'%s'); import store; n=sys.argv[1]; "
            "store.save({'schema_version': store.SCHEMA_VERSION, 'project': {'phase':'p','active_branch':'dev'}, "
            "'tasks': [{'id': 'T-'+n, 'status': 'todo'}]}, r'%s')" % (ENGINE, p))
    procs = [subprocess.Popen([sys.executable, "-c", code, str(i)]) for i in range(12)]
    rcs = [pr.wait() for pr in procs]
    check("cross-process: all saves exit 0 (lock held, no crash)", all(rc == 0 for rc in rcs))
    obj = json.load(open(p, encoding="utf-8"))  # must parse = not torn
    check("cross-process: final file is complete valid json", "tasks" in obj and len(obj["tasks"]) == 1)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} state-atomic tests passed")
