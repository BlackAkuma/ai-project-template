"""DEV-FP — coverage for the two forward-ported hooks (panel dissent: zero automated coverage).
govern-docs.sh (Edit/Write gate) + session-end-gate.sh (Stop gate).
Run: python engine/test_govern_docs.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GD = os.path.join(REPO, "platforms", "claude-code", "hooks", "govern-docs.sh")
SE = os.path.join(REPO, "platforms", "claude-code", "hooks", "session-end-gate.sh")
bash = shutil.which("bash") or shutil.which("bash.exe")
git = shutil.which("git")
cases = []
def check(name, cond): cases.append((name, bool(cond)))
if not bash or not git:
    print("[SKIP] bash/git not available"); sys.exit(0)


def edit_call(d, fp, new):
    mock = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": fp, "new_string": new}})
    return subprocess.run([bash, GD], input=mock, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=d).returncode


with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/00-source/versions/v1"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w").write("# WL\n")

    # govern-docs: requirement immutability
    check("edit 00-source directly -> BLOCK", edit_call(d, d + "/CoreAiWorkspaces/00-source/brd.md", "x") == 2)
    check("add 00-source VERSION -> ALLOW", edit_call(d, d + "/CoreAiWorkspaces/00-source/versions/v1/brd.md", "x") == 0)
    check("normal code edit -> ALLOW", edit_call(d, d + "/src/main.py", "print(1)") == 0)
    # govern-docs: Task Close Gate via Edit
    check("mark T-9 done w/o worklog -> BLOCK", edit_call(d, d + "/CoreAiWorkspaces/02-task/task-board.md", "T-9 [done] ok") == 2)
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "a").write("- T-9 done, evidence ok\n")
    check("mark T-9 done WITH worklog -> ALLOW", edit_call(d, d + "/CoreAiWorkspaces/02-task/task-board.md", "T-9 [done] ok") == 0)

    # session-end-gate
    subprocess.run([git, "init", "-q"], cwd=d); subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
    subprocess.run([git, "config", "user.name", "t"], cwd=d)
    open(os.path.join(d, "code.py"), "w").write("y=1\n"); subprocess.run([git, "add", "."], cwd=d)
    subprocess.run([git, "commit", "-qm", "T-9: work"], cwd=d)
    se = lambda inp: subprocess.run([bash, SE], input=inp, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=d).returncode
    check("loop-guard (stop_hook_active) -> ALLOW", se('{"stop_hook_active":true}') == 0)
    check("code today + no log today -> BLOCK end", se('{}') == 2)
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "a").write(f"\n## {__import__('datetime').date.today()} done\n")
    check("log today exists -> ALLOW end", se('{}') == 0)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} govern-docs + session-end-gate tests passed")
