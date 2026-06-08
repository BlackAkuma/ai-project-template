"""Phase A1 integration test — runnable CLI end-to-end via subprocess.
Run: python engine/test_cli.py
"""
import os
import subprocess
import sys
import tempfile

ENGINE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ENGINE, "..")
cases = []
def check(name, cond): cases.append((name, bool(cond)))


def cli(*args, root=None):
    a = list(args) + (["--root", root] if root else [])
    return subprocess.run([sys.executable, "engine/cli.py", *a], cwd=REPO, capture_output=True, text=True)


# cockpit on live repo -> renders, exit 0
r = cli("cockpit")
check("cockpit runs (exit 0)", r.returncode == 0)
check("cockpit shows COCKPIT header", "COCKPIT" in r.stdout)

# gate by id via CLI delegates to check.py
check("gate cmd resolves", cli("gate", "task_close_gate", "--task", "T-999").returncode != 2)

# audit on live repo
check("audit runs", cli("audit").returncode in (0, 1))

# governed turn on a TEMP fixture (don't mutate live)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"))
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"))
    os.makedirs(os.path.join(d, "engine"))
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write("<!-- AI-CONTEXT\ndone: []\n-->\n")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write("# Work Log\n- T-100 done commit a1b2c3d evidence ✓\n")
    rt = cli("turn", "T-100", "mark_done", "--risk", "1", "--model", "claude-sonnet", root=d)
    check("turn mark_done(evidence) -> status=done", "status=done" in rt.stdout)
    # weak model + code-author lane -> refused
    rw = cli("turn", "T-101", "mark_done", "--risk", "1", "--model", "local-3b", root=d)
    check("turn weak model -> refused", "status=refused" in rw.stdout)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} CLI integration tests passed")
