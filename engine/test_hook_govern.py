"""A2 test — Claude Code govern-action hook blocks REAL bad actions via the engine.
Sets up a temp git repo, stages a secret, runs the hook with a mock 'git commit' tool-call → expect BLOCK.
Run: python engine/test_hook_govern.py
"""
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

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} govern-hook tests passed")
