"""A2 test — Claude Code govern-action hook blocks REAL bad actions via the engine.
Sets up a temp git repo, stages a secret, runs the hook with a mock 'git commit' tool-call → expect BLOCK.
Run: python engine/test_hook_govern.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOOK = os.path.join(REPO, "platforms", "claude-code", "hooks", "govern-action.sh")
cases = []
def check(name, cond): cases.append((name, bool(cond)))

bash = shutil.which("bash") or shutil.which("bash.exe")
git = shutil.which("git")
if not bash or not git:
    print("[SKIP] bash/git not available — hook test needs git-bash"); sys.exit(0)


def run_hook(repo_dir, command):
    mock = '{"tool_name":"Bash","tool_input":{"command":"%s"}}' % command
    env = dict(os.environ, ENGINE_DIR=REPO)
    p = subprocess.run([bash, HOOK], input=mock, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=repo_dir, env=env)
    return p.returncode, (p.stderr or "")


def git_init(d):
    subprocess.run([git, "init", "-q"], cwd=d)
    subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
    subprocess.run([git, "config", "user.name", "t"], cwd=d)


with tempfile.TemporaryDirectory() as d:
    git_init(d)
    # stage a real secret -> hook must BLOCK (exit 2)
    open(os.path.join(d, "config.py"), "w").write('api_key = "sk-abcd1234efgh5678"\n')
    subprocess.run([git, "add", "."], cwd=d)
    code, err = run_hook(d, "git commit -m wip")
    check("commit with secret -> BLOCKED (exit 2)", code == 2)
    check("block reason mentions governance", "GOVERNANCE BLOCK" in err)

with tempfile.TemporaryDirectory() as d:
    git_init(d)
    # stage clean code -> hook must ALLOW (exit 0)
    open(os.path.join(d, "hello.py"), "w").write('print("hello world")\n')
    subprocess.run([git, "add", "."], cwd=d)
    code, err = run_hook(d, "git commit -m feat")
    check("clean commit -> ALLOWED (exit 0)", code == 0)

    # non-commit command -> not gated (exit 0)
    code2, _ = run_hook(d, "ls -la")
    check("non-commit command -> allowed (exit 0)", code2 == 0)

    # TEMPLATE-ONLY MODE: no engine/ present -> hook passes silently (template standalone must work)
    with tempfile.TemporaryDirectory() as empty_engine:
        mock = '{"tool_name":"Bash","tool_input":{"command":"git commit -m x"}}'
        env2 = dict(os.environ, ENGINE_DIR=empty_engine)
        p2 = subprocess.run([bash, HOOK], input=mock, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", cwd=d, env=env2)
        check("no engine/ -> template-only mode passes (exit 0)", p2.returncode == 0)

    # MASTER FREEZE (user rule 2026-06-11): any master-touching command -> hard block, no approval path
    for mc in ("git push origin master", "git checkout master", "git merge feature/x master"):
        c0, e0 = run_hook(d, mc)
        check(f"master freeze blocks: {mc}", c0 == 2 and "MASTER FREEZE" in e0)

    # A4: dangerous git op -> HELD (exit 2) + creates a real Decision Inbox item
    code3, err3 = run_hook(d, "git push --force origin main")
    check("force-push -> HELD for approval (exit 2)", code3 == 2 and "HELD" in err3)
    inbox_path = os.path.join(d, "engine", "inbox.jsonl")
    has_item = os.path.exists(inbox_path) and "risky_git_op" in open(inbox_path, encoding="utf-8").read()
    check("force-push created a Decision Inbox item", has_item)

    # P0-fix: human decision is CAUSAL (panel contrarian seam)
    # retry while pending -> blocked, NO duplicate item
    code4, err4 = run_hook(d, "git push --force origin main")
    items = [json.loads(x) for x in open(inbox_path, encoding="utf-8").read().splitlines() if x.strip()]
    check("retry while pending -> blocked + NO duplicate", code4 == 2 and "WAITING" in err4
          and len([i for i in items if i["status"] == "open"]) == 1)

    # approve in inbox -> SAME command now allowed once
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from inbox import resolve_item
    open_item = [i for i in items if i["status"] == "open"][0]
    resolve_item(open_item["id"], "approved", by="tester", ts=99, root=d)
    code5, err5 = run_hook(d, "git push --force origin main")
    check("after APPROVE -> action allowed once (exit 0)", code5 == 0 and "APPROVED" in err5)

    # approval consumed -> next retry is held again (new decision required)
    code6, err6 = run_hook(d, "git push --force origin main")
    check("approval consumed -> next retry held again", code6 == 2 and "HELD" in err6)

    # reject -> stays blocked with rejected message
    items2 = [json.loads(x) for x in open(inbox_path, encoding="utf-8").read().splitlines() if x.strip()]
    open2 = [i for i in items2 if i["status"] == "open"][0]
    resolve_item(open2["id"], "rejected", by="tester", ts=100, root=d)
    code7, err7 = run_hook(d, "git push --force origin main")
    check("after REJECT -> stays blocked (rejected msg)", code7 == 2 and "REJECTED" in err7)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} govern-hook tests passed")
