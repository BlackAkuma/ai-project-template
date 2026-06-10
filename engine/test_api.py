"""Phase A2 test — HTTP API router (pure handle(), headless) + live socket smoke.
Run: python engine/test_api.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api import handle  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))


def fixture(d):
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write("<!-- AI-CONTEXT\ndone: []\n-->\n")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write("# Work Log\n- T-100 done commit a1b2c3d evidence ✓\n")


with tempfile.TemporaryDirectory() as d:
    fixture(d)
    st, res = handle("GET", "/cockpit", root=d)
    check("GET /cockpit -> 200 + cockpit", st == 200 and "COCKPIT" in res["cockpit"])
    check("cockpit reports watching root + mode (BL-1)", res.get("watching") and res.get("mode") in ("live", "demo"))

    st, res = handle("GET", "/inbox", root=d)
    check("GET /inbox -> 200 + open list", st == 200 and "open" in res)

    st, res = handle("GET", "/audit", root=d)
    check("GET /audit -> 200 + chain_ok", st == 200 and "chain_ok" in res)

    st, res = handle("POST", "/turn", {"task": "T-100", "intent": "mark_done", "risk": 1, "model": "claude-sonnet"}, root=d)
    check("POST /turn mark_done(evidence) -> done", st == 200 and res["status"] == "done")

    st, res = handle("POST", "/turn", {"task": "T-9", "intent": "mark_done", "risk": 1, "model": "local-3b"}, root=d)
    check("POST /turn weak model -> refused", res["status"] == "refused")

    st, res = handle("POST", "/turn", {"task": "x"}, root=d)
    check("POST /turn missing intent -> 400", st == 400)

    st, res = handle("GET", "/nope", root=d)
    check("unknown path -> 404", st == 404)

    # Phase C: web Cockpit served at /
    st, res = handle("GET", "/", root=d)
    check("GET / serves web Cockpit HTML", st == 200 and "_html" in res and "Governed Project Memory" in res["_html"])

# live socket smoke (start server in thread, real HTTP GET)
import threading  # noqa: E402
import urllib.request  # noqa: E402
import time  # noqa: E402
from api import serve  # noqa: E402
with tempfile.TemporaryDirectory() as d:
    fixture(d)
    th = threading.Thread(target=serve, kwargs={"port": 8799, "root": d}, daemon=True)
    th.start()
    ok = False
    for _ in range(20):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8799/audit", timeout=1) as resp:
                ok = resp.status == 200 and b"chain_ok" in resp.read()
            break
        except Exception:
            time.sleep(0.1)
    check("live server responds over HTTP", ok)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} API tests passed")
