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

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOOK = os.path.join(REPO, "platforms", "claude-code", "hooks", "govern-action.sh")
cases = []
def check(name, cond): cases.append((name, bool(cond)))

bash = shutil.which("bash") or shutil.which("bash.exe")
git = shutil.which("git")
if not bash or not git:
    print("[SKIP] bash/git not available — hook test needs git-bash"); sys.exit(0)


def run_hook(repo_dir, command, engine_dir=REPO):
    mock = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})  # proper escaping
    env = dict(os.environ, ENGINE_DIR=engine_dir)
    p = subprocess.run([bash, HOOK], input=mock, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=repo_dir, env=env)
    return p.returncode, (p.stderr or "")


def git_init(d):
    subprocess.run([git, "init", "-q", "-b", "work"], cwd=d)  # neutral branch (not master/dev) for gate tests
    subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
    subprocess.run([git, "config", "user.name", "t"], cwd=d)


with tempfile.TemporaryDirectory() as d:
    git_init(d)
    # stage a real secret -> hook must BLOCK (exit 2)
    open(os.path.join(d, "config.py"), "w").write('api_key = "sk-abcd1234efgh5678"\n')  # allowlist-secret (fake fixture)
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

    # DEV DIRECT FREEZE (user rule): marker on + branch=dev + CODE staged -> blocked; doc-only -> allowed
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "engine", ".dev-direct-freeze"), "w").write("on\n")
    subprocess.run([git, "branch", "-M", "dev"], cwd=d)
    open(os.path.join(d, "app.py"), "w").write("x=1\n"); subprocess.run([git, "add", "app.py"], cwd=d)
    cdf, edf = run_hook(d, "git commit -m direct-on-dev")
    check("dev-freeze: CODE commit on dev blocked", cdf == 2 and "DEV DIRECT FREEZE" in edf)
    # doc-only commit on dev -> allowed (fix: was over-broad). full reset first (clear stray staged code)
    subprocess.run([git, "reset", "-q"], cwd=d)
    os.remove(os.path.join(d, "app.py"))
    os.makedirs(os.path.join(d, "CoreAiWorkspaces"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces", "note.md"), "w").write("log\n"); subprocess.run([git, "add", "CoreAiWorkspaces/note.md"], cwd=d)
    cdoc, edoc = run_hook(d, "git commit -m doc-sync")
    check("dev-freeze: doc-only commit on dev ALLOWED", cdoc == 0)
    # feature branch: code commit allowed
    open(os.path.join(d, "app.py"), "w").write("x=1\n"); subprocess.run([git, "add", "app.py"], cwd=d)
    subprocess.run([git, "checkout", "-q", "-b", "feature/x"], cwd=d)
    cdf2, _ = run_hook(d, "git commit -m on-feature")
    check("dev-freeze: code commit on feature branch allowed", cdf2 == 0)
    # consume-once bypass marker (replaces broken env var)
    subprocess.run([git, "checkout", "-q", "dev"], cwd=d)
    open(os.path.join(d, "engine", ".govern-allow-once"), "w").write("1\n")
    cby, _ = run_hook(d, "git commit -m user-ordered")
    check("dev-freeze: consume-once bypass works", cby == 0)
    check("bypass marker consumed (one-shot)", not os.path.exists(os.path.join(d, "engine", ".govern-allow-once")))
    os.remove(os.path.join(d, "engine", ".dev-direct-freeze"))
    subprocess.run([git, "reset", "-q"], cwd=d); os.remove(os.path.join(d, "app.py"))

    # MASTER FREEZE (user rule 2026-06-11): any master-touching command -> hard block, no approval path
    for mc in ("git push origin master", "git checkout master", "git merge feature/x master"):
        c0, e0 = run_hook(d, mc)
        check(f"master freeze blocks: {mc}", c0 == 2 and "MASTER FREEZE" in e0)

    # DEV-FP: code commit must carry a task ref (T-/BL-/FU-/SPIKE)
    subprocess.run([git, "checkout", "-q", "-b", "feature/tref"], cwd=d)
    open(os.path.join(d, "q.py"), "w").write("q=1\n"); subprocess.run([git, "add", "q.py"], cwd=d)
    ct1, et1 = run_hook(d, 'git commit -m "no task ref here"')
    check("DEV-FP: code commit without task ref -> BLOCK", ct1 == 2 and "traceability" in et1)
    ct2, _ = run_hook(d, 'git commit -m "FU-2: add lock"')
    check("DEV-FP: code commit with task ref -> ALLOW", ct2 == 0)
    subprocess.run([git, "reset", "-q"], cwd=d); os.remove(os.path.join(d, "q.py"))

    # BL-13 regression: trigger words INSIDE a quoted commit message must NOT false-trigger freezes
    subprocess.run([git, "checkout", "-q", "-b", "feature/safe"], cwd=d)
    open(os.path.join(d, "z.py"), "w").write("z=1\n"); subprocess.run([git, "add", "z.py"], cwd=d)
    cq, eq = run_hook(d, 'git commit -m "T-1: fix git push origin master and reset --hard docs"')
    check("quoted msg with master/reset words -> NOT blocked (CMD_NOQ)", cq == 0)
    subprocess.run([git, "reset", "-q"], cwd=d); os.remove(os.path.join(d, "z.py"))

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

    # FU-4: evasions the OLD substring glob missed are now HELD end-to-end (hook -> gitguard)
    e1, _ = run_hook(d, "git push origin develop --force")      # flag at end (non-adjacent)
    check("FU-4 hook: flag-at-end force push -> HELD", e1 == 2)
    e2, _ = run_hook(d, "git push origin +develop")             # refspec '+' force (no --force flag)
    check("FU-4 hook: refspec '+' force push -> HELD", e2 == 2)
    e3, _ = run_hook(d, "git push  origin   develop   --force") # double/triple spacing
    check("FU-4 hook: whitespace-padded force push -> HELD", e3 == 2)
    e4, _ = run_hook(d, "git reset develop --hard")             # reset --hard flag-last
    check("FU-4 hook: reset --hard (flag-last) -> HELD", e4 == 2)
    e5, _ = run_hook(d, "git push origin develop")              # genuinely safe push stays allowed
    check("FU-4 hook: plain push -> allowed (no false-positive)", e5 == 0)

    # FU-4 re-review (panel blockers): =value force form + no cross-command misattribution, e2e
    e6, _ = run_hook(d, "git push --force-with-lease=develop origin develop")
    check("FU-4 re-review hook: --force-with-lease=VALUE -> HELD", e6 == 2)
    e7, _ = run_hook(d, "echo +foo && git push origin develop")
    check("FU-4 re-review hook: chained '+foo' misattribution -> allowed", e7 == 0)
    # re-review2: quote-aware end-to-end (hook now passes raw $cmd, not CMD_NOQ)
    e8, _ = run_hook(d, 'git push origin "+master"')
    check("FU-4 re-review2 hook: quoted '+master' refspec force -> HELD", e8 == 2)
    e9, _ = run_hook(d, 'git branch -d --force somebranch')
    check("FU-4 re-review2 hook: branch -d --force -> HELD", e9 == 2)

# FU-4 re-review BLOCKER: hook must FAIL-CLOSED if the classifier itself can't run.
# Fake engine whose cli.py always crashes (exit 3); a normally-SAFE 'git push' must still be HELD.
with tempfile.TemporaryDirectory() as fe, tempfile.TemporaryDirectory() as wd:
    git_init(wd)
    os.makedirs(os.path.join(fe, "engine"), exist_ok=True)
    open(os.path.join(fe, "engine", "check.py"), "w").write("import sys; sys.exit(0)\n")  # exists -> not template-only
    open(os.path.join(fe, "engine", "cli.py"), "w").write("import sys; sys.exit(3)\n")    # always crashes
    fc, ferr = run_hook(wd, "git push origin develop", engine_dir=fe)
    check("FU-4 fail-closed: classifier crash -> safe push HELD (not fail-open)",
          fc == 2 and "fail-closed" in ferr.lower())

# FU-5: committing a DELETION of engine/testcmd.txt is blocked (anti silent-disable propagate);
# explicit consume-once bypass makes intentional de-config auditable. Isolated repo.
with tempfile.TemporaryDirectory() as d:
    git_init(d)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "engine", "testcmd.txt"), "w").write("pytest -q\n")
    open(os.path.join(d, "keep.txt"), "w").write("x\n")  # keeps engine/ non-empty isn't needed; keep repo non-empty
    subprocess.run([git, "add", "."], cwd=d)
    subprocess.run([git, "commit", "-q", "-m", "T-1: add testcmd"], cwd=d)
    subprocess.run([git, "rm", "-q", "engine/testcmd.txt"], cwd=d)  # stage the deletion (removes empty dir too)
    cd1, ed1 = run_hook(d, 'git commit -m "T-1: drop tests"')
    check("FU-5: commit deleting testcmd.txt -> BLOCK", cd1 == 2 and "test gate" in ed1)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)  # git rm removed empty dir; recreate for marker
    open(os.path.join(d, "engine", ".govern-allow-once"), "w").write("")  # explicit auditable bypass
    cd2, _ = run_hook(d, 'git commit -m "T-1: drop tests (intentional)"')
    check("FU-5: with consume-once bypass -> deletion allowed (auditable)", cd2 == 0)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} govern-hook tests passed")
