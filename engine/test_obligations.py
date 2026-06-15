"""OBS-1 — re-inject active obligations (fight recency decay). Run: python engine/test_obligations.py"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obligations import render  # noqa: E402
from inbox import create_item  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))
git = shutil.which("git")


def _engine(d):
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)


# no engine -> empty (template-only safe)
with tempfile.TemporaryDirectory() as d:
    check("no engine/ -> empty (template-only)", render(d) == "")

# engine present -> MASTER FREEZE always shown (the standing rule that decays)
with tempfile.TemporaryDirectory() as d:
    _engine(d)
    out = render(d)
    check("engine -> obligations header present", "ACTIVE OBLIGATIONS" in out)
    check("MASTER FREEZE always shown", "MASTER FREEZE" in out)
    check("no dev-freeze marker -> DEV-DIRECT not shown", "DEV-DIRECT FREEZE" not in out)

# dev-direct-freeze marker -> shown
with tempfile.TemporaryDirectory() as d:
    _engine(d)
    open(os.path.join(d, "engine", ".dev-direct-freeze"), "w").write("on")
    check("dev-freeze marker -> DEV-DIRECT shown", "DEV-DIRECT FREEZE" in render(d))

# open decision-inbox items surfaced (must respect pending human decisions)
with tempfile.TemporaryDirectory() as d:
    _engine(d)
    create_item("risky_git_op", "T-1", 2, "deploy", root=d)
    out = render(d)
    check("open inbox item surfaced with id", "decision-inbox: 1 open" in out and "DI-0001" in out)
    check("inbox line warns against self-bypass", "ห้าม bypass" in out)

# FU-5 test-gate regression surfaced
with tempfile.TemporaryDirectory() as d:
    _engine(d)
    open(os.path.join(d, "engine", ".testcmd_configured"), "w").write("pytest")  # marker, but no testcmd.txt
    check("test-gate REGRESSED surfaced", "REGRESSED" in render(d))

# prod-branch guard: on prod branch -> warn
if git:
    with tempfile.TemporaryDirectory() as d:
        _engine(d)
        os.makedirs(os.path.join(d, "CoreAiWorkspaces/01-plan"), exist_ok=True)
        open(os.path.join(d, "CoreAiWorkspaces/01-plan/work-status.md"), "w", encoding="utf-8").write(
            "<!-- AI-CONTEXT\ngit_prod_branch: master\n-->\n")
        subprocess.run([git, "init", "-q", "-b", "master"], cwd=d)
        subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
        subprocess.run([git, "config", "user.name", "t"], cwd=d)
        out = render(d)
        check("on prod branch -> PRODUCTION warning", "PRODUCTION branch" in out and "branch: master" in out)
    with tempfile.TemporaryDirectory() as d:
        _engine(d)
        os.makedirs(os.path.join(d, "CoreAiWorkspaces/01-plan"), exist_ok=True)
        open(os.path.join(d, "CoreAiWorkspaces/01-plan/work-status.md"), "w", encoding="utf-8").write(
            "<!-- AI-CONTEXT\ngit_prod_branch: master\n-->\n")
        subprocess.run([git, "init", "-q", "-b", "dev"], cwd=d)
        subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
        subprocess.run([git, "config", "user.name", "t"], cwd=d)
        out = render(d)
        check("on dev branch -> no PRODUCTION warning", "PRODUCTION branch" not in out and "branch: dev" in out)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} obligations tests passed")
