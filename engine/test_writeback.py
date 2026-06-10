"""BL-3/A5 test — session write-back updates machine-fact keys only + appends session record.
Run: python engine/test_writeback.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from writeback import writeback, _update_block_key  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

git = shutil.which("git")
if not git:
    print("[SKIP] git not available"); sys.exit(0)

WS = """<!-- AI-CONTEXT
phase: my-phase
active_branch: old-branch
last_updated: 2020-01-01
narrative_note: HUMAN WROTE THIS — must survive
-->
# Work Status body — must survive
"""


def init_repo(d):
    subprocess.run([git, "init", "-q", "-b", "main"], cwd=d)
    subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
    subprocess.run([git, "config", "user.name", "t"], cwd=d)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/01-plan"))
    open(os.path.join(d, "CoreAiWorkspaces/01-plan/work-status.md"), "w", encoding="utf-8").write(WS)
    open(os.path.join(d, "a.txt"), "w").write("1")
    subprocess.run([git, "add", "."], cwd=d)
    subprocess.run([git, "commit", "-q", "-m", "first commit"], cwd=d)


# block-key updater: replaces existing, inserts new, never touches body
t2 = _update_block_key(WS, "active_branch", "new-branch")
check("replaces existing key", "active_branch: new-branch" in t2 and "old-branch" not in t2)
t3 = _update_block_key(WS, "auto_session", "X")
check("inserts new key inside block", "auto_session: X" in t3 and t3.index("auto_session") < t3.index("-->"))
# panel regression pin: backslash/regex-template chars in value must stay literal (re.sub lambda fix)
t4 = _update_block_key(WS, "active_branch", r"fix\x \1 \g<1> path")
check("backslash value stays literal (no re.error)", r"fix\x \1 \g<1> path" in t4)
check("body + human narrative untouched", "must survive" in t2 and "narrative_note: HUMAN WROTE THIS" in t2)

with tempfile.TemporaryDirectory() as d:
    init_repo(d)
    rec = writeback(d)
    ws = open(os.path.join(d, "CoreAiWorkspaces/01-plan/work-status.md"), encoding="utf-8").read()
    check("active_branch updated from git", "active_branch: main" in ws)
    check("last_updated refreshed", "last_updated: 2020-01-01" not in ws)
    check("auto_session recorded", "auto_session:" in ws and "first commit" in ws)
    check("human narrative survives writeback", "narrative_note: HUMAN WROTE THIS" in ws and "must survive" in ws)
    check("session record appended", os.path.exists(os.path.join(d, "engine/sessions.log.jsonl")))

    # second run with a NEW commit -> reports only the new one
    open(os.path.join(d, "b.txt"), "w").write("2")
    subprocess.run([git, "add", "."], cwd=d)
    subprocess.run([git, "commit", "-q", "-m", "second commit"], cwd=d)
    rec2 = writeback(d)
    check("incremental: only new commit reported", len(rec2["new_commits"]) == 1 and "second" in rec2["new_commits"][0])

    # third run, no new commits -> zero reported (idempotent)
    rec3 = writeback(d)
    check("idempotent when nothing new", rec3["new_commits"] == [])

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} write-back tests passed")
