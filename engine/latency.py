"""BL-10/N5: hook latency budget — measure the REAL overhead governance adds per action.

Budget: deterministic gate path < 1000ms (NFR-N5) — governance ที่ช้าจะโดนปิดทิ้ง (R1).
  python engine/latency.py [--root .]
"""
import argparse
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ENGINE = os.path.dirname(os.path.abspath(__file__))


def _t(fn, n=3):
    best = None
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        dt = (time.perf_counter() - t0) * 1000
        best = dt if best is None else min(best, dt)
    return round(best, 1)


def measure(root="."):
    """Returns {name: ms} for each governance touchpoint (best of 3)."""
    py = sys.executable

    def gate(g):
        return lambda: subprocess.run([py, os.path.join(ENGINE, "check.py"), g, "--root", root],
                                      capture_output=True)

    def cli(*args):
        return lambda: subprocess.run([py, os.path.join(ENGINE, "cli.py"), *args, "--root", root],
                                      capture_output=True)

    def digest():
        return subprocess.run([py, os.path.join(ENGINE, "digest.py"), "--root", root], capture_output=True)

    return {
        "gate:secret-scan": _t(gate("secret-scan")),
        "gate:placeholder-scan": _t(gate("placeholder-scan")),
        "cli:approval-state": _t(cli("approval-state", "g", "r")),
        "session:digest": _t(lambda: digest()),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--budget", type=int, default=1000)
    a = ap.parse_args()
    r = measure(a.root)
    worst = max(r.values())
    for k, v in r.items():
        flag = "✓" if v < a.budget else "✗ OVER BUDGET"
        print(f"  {k:24s} {v:8.1f} ms  {flag}")
    print(f"\n  worst: {worst:.1f} ms · budget: {a.budget} ms · {'PASS' if worst < a.budget else 'FAIL'}")
    sys.exit(0 if worst < a.budget else 1)
