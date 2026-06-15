"""BL-7 test — engine init installs working governance into a fresh repo (end-to-end).
Run: python engine/test_init.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from init_repo import init_repo  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

git = shutil.which("git")

with tempfile.TemporaryDirectory() as d:
    # pre-existing settings.json with a user's own hook — must survive merge
    os.makedirs(os.path.join(d, ".claude"))
    json.dump({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo user-own-hook"}]}]}},
              open(os.path.join(d, ".claude", "settings.json"), "w"))

    r = init_repo(d)
    check("copies engine core (>=20 files)", r["copied"] >= 20)
    check("scaffolds 3 state files", len(r["scaffolded"]) == 3)
    check("engine files exist in target", os.path.exists(os.path.join(d, "engine", "check.py"))
          and os.path.exists(os.path.join(d, "engine", "gates", "secret-scan.yaml")))
    check("hooks copied", os.path.exists(os.path.join(d, "platforms/claude-code/hooks/govern-action.sh")))

    cfg = json.load(open(os.path.join(d, ".claude", "settings.json"), encoding="utf-8"))
    flat = json.dumps(cfg)
    check("settings merged: our 3 hooks added", all(k in flat for k in ("session-digest", "session-writeback", "govern-action")))
    check("settings merge preserves user's own hook", "user-own-hook" in flat)

    # P1-panel fix: unparseable settings.json -> ABORT (never overwrite user's broken config)
    with tempfile.TemporaryDirectory() as d2:
        os.makedirs(os.path.join(d2, ".claude"))
        open(os.path.join(d2, ".claude", "settings.json"), "w").write("{broken json!!")
        raised = False
        try:
            init_repo(d2)
        except ValueError:
            raised = True
        check("broken settings.json -> abort, not overwrite", raised
              and open(os.path.join(d2, ".claude", "settings.json")).read() == "{broken json!!")

    # idempotent: run again -> no duplicate hook entries
    init_repo(d)
    cfg2 = json.load(open(os.path.join(d, ".claude", "settings.json"), encoding="utf-8"))
    check("idempotent: no duplicate hook entries", json.dumps(cfg2).count("govern-action.sh") == 1)

    # END-TO-END: governance actually WORKS from the target's own engine
    if git:
        subprocess.run([git, "init", "-q"], cwd=d)
        subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
        subprocess.run([git, "config", "user.name", "t"], cwd=d)
        open(os.path.join(d, "leak.py"), "w").write('api_key = "sk-abcd1234efgh5678"\n')  # allowlist-secret (fake fixture)
        subprocess.run([git, "add", "."], cwd=d)
        p = subprocess.run([sys.executable, os.path.join(d, "engine", "check.py"), "secret-scan", "--root", d],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        check("target's OWN engine blocks secret commit (exit 1)", p.returncode == 1)
        # digest renders from target's own engine
        p2 = subprocess.run([sys.executable, os.path.join(d, "engine", "digest.py"), "--root", d],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        check("target's OWN digest renders", p2.returncode == 0 and "PROJECT-MEMORY DIGEST" in p2.stdout)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} engine-init tests passed")
