"""BL-11 — bypass-path counters: correct delta/cumulative + atomic under concurrency.
Run: python engine/test_counters.py
"""
import json
import os
import subprocess
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import counters  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

ENGINE = os.path.dirname(os.path.abspath(__file__))


# --- basic bump + read ---
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"))
    check("read empty before any bump", counters.read(d) == {})
    check("digest_line empty when no file", counters.digest_line(d) == "")
    counters.bump("doc_exempt", d)
    counters.bump("doc_exempt", d)
    counters.bump("consume_once", d)
    r = counters.read(d)
    check("doc_exempt counted 2", r.get("doc_exempt") == 2)
    check("consume_once counted 1", r.get("consume_once") == 1)
    # counter file must be the gitignored name (no tree pollution)
    check("counter file is .bypass-counters.json", os.path.exists(os.path.join(d, "engine", ".bypass-counters.json")))
    check("no leftover .tmp", not [f for f in os.listdir(os.path.join(d, "engine")) if ".tmp." in f])
    check("no leftover .lock", not os.path.exists(os.path.join(d, "engine", ".bypass-counters.json.lock")))

    # --- session_view: delta then zero, cumulative preserved ---
    v1 = counters.session_view(d)
    check("view1 doc_exempt delta=2 total=2", v1.get("doc_exempt") == (2, 2))
    check("view1 consume_once delta=1 total=1", v1.get("consume_once") == (1, 1))
    v2 = counters.session_view(d)  # nothing bumped since -> delta 0, total unchanged
    check("view2 delta resets to 0", v2.get("doc_exempt") == (0, 2) and v2.get("consume_once") == (0, 1))
    counters.bump("doc_exempt", d)
    v3 = counters.session_view(d)
    check("view3 delta=1 since last view, total accumulates to 3", v3.get("doc_exempt") == (1, 3))

    # --- unknown name accepted (forward-compat) ---
    counters.bump("some_future_path", d)
    check("unknown name accepted", counters.read(d).get("some_future_path") == 1)


# --- digest_line format + KNOWN ordering incl. inbox_approved ---
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"))
    counters.bump("doc_exempt", d)
    line = counters.digest_line(d)
    check("digest_line mentions BL-11 + doc_exempt + total", "BL-11" in line and "doc_exempt=1" in line and "total" in line)
    # advancing means a second call shows delta 0
    check("digest_line second call delta 0", "doc_exempt=0" in counters.digest_line(d))
    # inbox_approved (panel/contrarian fix) is a first-class KNOWN path, rendered in stable order
    check("inbox_approved is a KNOWN path", "inbox_approved" in counters.KNOWN)
    counters.bump("inbox_approved", d)
    l2 = counters.digest_line(d)
    check("digest_line renders inbox_approved", "inbox_approved=1" in l2)


# --- liveness health() — panel: a broken instrument must be distinguishable from a genuine 0 ---
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"))
    ok, note = counters.health(d)
    check("health: absent file -> ok (genuine 'no bypass yet', not a fault)", ok and "yet" in note)
    counters.bump("doc_exempt", d)
    ok2, note2 = counters.health(d)
    check("health: after a bump -> live", ok2 and note2 == "live")
    # corrupt the file -> health must report BROKEN (not silently read as 0=calibrated)
    open(os.path.join(d, "engine", ".bypass-counters.json"), "w", encoding="utf-8").write("{not json")
    ok3, note3 = counters.health(d)
    check("health: corrupt file -> NOT ok (loud)", (not ok3) and "unreadable" in note3)


# --- digest liveness wiring: a corrupt counter file surfaces LOUDLY in the rendered digest ---
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"))
    counters.bump("consume_once", d)  # create a valid file first
    import digest as _digest
    out_ok = _digest.render_digest(d)
    bl_line = next((l for l in out_ok.splitlines() if "bypass_paths (BL-11)" in l), "")
    check("digest shows bypass line when instrument live", bool(bl_line) and "⚠️" not in bl_line)
    open(os.path.join(d, "engine", ".bypass-counters.json"), "w", encoding="utf-8").write("{broken")
    out_bad = _digest.render_digest(d)
    check("digest is LOUD when instrument broken (not silent 0=calibrated)",
          "INSTRUMENT BROKEN" in out_bad and "do NOT read a low hold-count as calibrated" in out_bad)


# --- concurrent bumps in-process: no lost increment, file stays valid ---
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"))
    errs = []
    def worker():
        try:
            for _ in range(10):
                counters.bump("doc_exempt", d)
        except Exception as e:  # noqa: BLE001
            errs.append(e)
    threads = [threading.Thread(target=worker) for _ in range(16)]
    for t in threads: t.start()
    for t in threads: t.join()
    check("16x10 concurrent bumps: no error", not errs)
    check("no lost increment (==160)", counters.read(d).get("doc_exempt") == 160)
    p = os.path.join(d, "engine", ".bypass-counters.json")
    json.load(open(p, encoding="utf-8"))  # must parse = not torn
    check("file parses after concurrency (not torn)", True)


# --- cross-process bumps via CLI: every process exits 0, total correct ---
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"))
    code = ("import sys; sys.path.insert(0, r'%s'); import counters; "
            "counters.bump('consume_once', r'%s')" % (ENGINE, d))
    procs = [subprocess.Popen([sys.executable, "-c", code]) for _ in range(12)]
    rcs = [p.wait() for p in procs]
    check("cross-process: all bumps exit 0", all(rc == 0 for rc in rcs))
    check("cross-process: total == 12 (lock held, no lost update)", counters.read(d).get("consume_once") == 12)


for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} counter tests passed")
