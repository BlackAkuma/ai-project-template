"""FU-6 — audit-log concurrency: append_event must serialize read-prev+append so the hash-chain
never FORKS under concurrent writers (prereq for Phase B multi-agent). Run: python engine/test_events_lock.py
"""
import os
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import append_event, verify_chain, _hash, _payload  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))
LOG = "engine/events.log.jsonl"


def _read_recs(path):
    import json
    return [json.loads(ln) for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]


# concurrent THREADS: every event survives, chain stays valid, no fork (no duplicate prev)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    N = 25
    errs = []
    def worker(n):
        try:
            append_event(f"a{n}", "act", f"T-{n}", "ok", ts=n, root=d, log=LOG)
        except Exception as e:  # noqa: BLE001
            errs.append(e)
    threads = [threading.Thread(target=worker, args=(n,)) for n in range(N)]
    for t in threads: t.start()
    for t in threads: t.join()
    path = os.path.join(d, LOG)
    recs = _read_recs(path)
    check(f"{N} concurrent thread-appends all survive", len(recs) == N and not errs)
    ok, reason = verify_chain(root=d, log=LOG)
    check(f"chain valid after concurrent threads ({reason})", ok is True)
    prevs = [r["prev"] for r in recs]
    check("no chain fork (every prev unique)", len(set(prevs)) == len(prevs))
    check("no leftover .lock", not os.path.exists(path + ".lock"))

# CROSS-PROCESS appends (real processes, not threads) — the case threads can mask
import subprocess  # noqa: E402
ENGINE = os.path.dirname(os.path.abspath(__file__))
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    N = 16
    code = ("import sys; sys.path.insert(0, r'%s'); from events import append_event; "
            "import sys as s; n=s.argv[1]; "
            "append_event('p'+n, 'act', 'P-'+n, 'ok', ts=int(n), root=r'%s', log='engine/events.log.jsonl')"
            % (ENGINE, d))
    procs = [subprocess.Popen([sys.executable, "-c", code, str(i)]) for i in range(N)]
    rcs = [p.wait() for p in procs]
    path = os.path.join(d, LOG)
    recs = _read_recs(path)
    check("cross-process: no worker crashed", all(rc == 0 for rc in rcs))
    check(f"cross-process: all {N} events survive", len(recs) == N)
    ok, reason = verify_chain(root=d, log=LOG)
    check(f"cross-process: chain valid (no fork) ({reason})", ok is True)
    check("cross-process: every prev unique (no fork)", len({r["prev"] for r in recs}) == len(recs))

# sanity: verify_chain still DETECTS a real tamper (lock didn't weaken integrity check)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    append_event("a", "act", "T-1", "ok", ts=1, root=d, log=LOG)
    append_event("a", "act", "T-2", "ok", ts=2, root=d, log=LOG)
    path = os.path.join(d, LOG)
    lines = open(path, encoding="utf-8").read().splitlines()
    import json
    rec0 = json.loads(lines[0]); rec0["result"] = "TAMPERED"
    lines[0] = json.dumps(rec0, ensure_ascii=False)
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    ok, _ = verify_chain(root=d, log=LOG)
    check("tamper still detected (integrity intact)", ok is False)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} audit-log concurrency tests passed")
