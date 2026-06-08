"""test — check.py gate resolution: by-filename, by-id fallback, unknown (re-audit dissent fix).
Run: python engine/test_check.py
"""
import os
import subprocess
import sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
cases = []
def check(name, cond): cases.append((name, bool(cond)))


def run(*args):
    return subprocess.run([sys.executable, "engine/check.py", *args], cwd=root,
                          capture_output=True, text=True).returncode


# by filename (secret-scan.yaml) -> resolves (0 pass / 1 block, never 2=not-found)
check("by-filename resolves", run("secret-scan") != 2)
# by gate id (task_close_gate, file is task-close.yaml) -> resolves via id fallback
check("by-id fallback resolves (task_close_gate)", run("task_close_gate", "--task", "T-999") != 2)
# truly unknown -> exit 2
check("unknown gate -> exit 2", run("no_such_gate_xyz") == 2)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} gate-resolution tests passed")
