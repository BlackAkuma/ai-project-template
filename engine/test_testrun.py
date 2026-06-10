"""BL-6 test — real test evidence: actual exit codes, HEAD cache, enforced-when-configured.
Run: python engine/test_testrun.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from testrun import run_tests, get_command  # noqa: E402
from resolvers import RESOLVERS  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

git = shutil.which("git")


def repo(d, testcmd=None):
    if git:
        subprocess.run([git, "init", "-q"], cwd=d)
        subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
        subprocess.run([git, "config", "user.name", "t"], cwd=d)
        open(os.path.join(d, "x.txt"), "w").write("1")
        subprocess.run([git, "add", "."], cwd=d)
        subprocess.run([git, "commit", "-q", "-m", "c1"], cwd=d)
    if testcmd is not None:
        os.makedirs(os.path.join(d, "engine"), exist_ok=True)
        open(os.path.join(d, "engine", "testcmd.txt"), "w").write(testcmd)


# not configured -> not enforced (resolver passes, run_tests says so)
with tempfile.TemporaryDirectory() as d:
    repo(d)
    r = run_tests(d)
    check("not configured -> configured=False", r["configured"] is False)
    check("resolver passes when not configured (policy)", RESOLVERS["tests_green"]({"root": d}) is True)

# configured + green command -> green, enforced pass
with tempfile.TemporaryDirectory() as d:
    repo(d, testcmd=f'"{sys.executable}" -c "print(1)"')
    r = run_tests(d)
    check("green command -> green=True exit=0", r["green"] is True and r["exit"] == 0)
    check("resolver True on green", RESOLVERS["tests_green"]({"root": d}) is True)
    r2 = run_tests(d)
    check("second run cache-hit by HEAD", r2["cached"] is True and r2["green"] is True)

# configured + red command -> red, resolver blocks
with tempfile.TemporaryDirectory() as d:
    repo(d, testcmd=f'"{sys.executable}" -c "import sys; sys.exit(3)"')
    r = run_tests(d)
    check("red command -> green=False real exit", r["green"] is False and r["exit"] == 3)
    check("resolver False on red (done would be blocked)", RESOLVERS["tests_green"]({"root": d}) is False)

# mark_done integration: red tests -> blocked with tests_red
from govern import mark_done  # noqa: E402
with tempfile.TemporaryDirectory() as d:
    repo(d, testcmd=f'"{sys.executable}" -c "import sys; sys.exit(1)"')
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write("<!-- AI-CONTEXT\ndone: []\n-->\n")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write("# WL\n- T-1 done commit a1b2c3d evidence ✓\n")
    r = mark_done("T-1", root=d, ts=1)
    check("mark_done with RED tests -> blocked (tests_red)", r["ok"] is False and "tests_red" in r["missing"])

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} test-evidence tests passed")
