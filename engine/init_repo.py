"""BL-7/A6: `engine init` — one command installs governance into ANY repo (G1).

Self-contained install (sovereignty): copies the engine core + hooks into the target repo,
merges hook entries into .claude/settings.json WITHOUT clobbering existing config, scaffolds
CoreAiWorkspaces state files if absent. After init the target repo is governed standalone.

  python engine/cli.py init --target /path/to/repo
"""
import json
import os
import shutil

# engine core shipped to targets (no tests/demo/runtime)
CORE_FILES = [
    "check.py", "resolvers.py", "events.py", "govern.py", "store.py", "inbox.py",
    "llm.py", "agent.py", "repo.py", "memory.py", "migrate_state.py", "entities.py",
    "evidence.py", "cockpit.py", "digest.py", "writeback.py", "testrun.py", "cli.py",
    "api.py", "init_repo.py", "requirements.txt",
]
HOOKS = ["govern-action.sh", "session-digest.sh", "session-writeback.sh"]
HOOK_CMDS = {
    "SessionStart": "bash platforms/claude-code/hooks/session-digest.sh",
    "SessionEnd": "bash platforms/claude-code/hooks/session-writeback.sh",
    "PreToolUse": "bash platforms/claude-code/hooks/govern-action.sh",
}

BOARD_MIN = "<!-- AI-CONTEXT\nschema_version: 0.1\ntotal_tasks: 0\ndone: []\nin_progress: []\nblocked: []\ntodo: []\n-->\n# Task Board\n"
WS_MIN = "<!-- AI-CONTEXT\nschema_version: 0.1\nphase: bootstrap\nblocker: none\nlast_updated: -\n-->\n# Work Status\n"
WL_MIN = "<!-- AI-CONTEXT\nschema_version: 0.1\nlast_session: -\n-->\n# Work Log\n"


def _merge_settings(path):
    """Append our hook entries into .claude/settings.json — never remove/replace existing ones."""
    cfg = {}
    if os.path.exists(path):
        try:
            cfg = json.load(open(path, encoding="utf-8"))
        except Exception:
            cfg = {}
    hooks = cfg.setdefault("hooks", {})
    added = []
    for event, cmd in HOOK_CMDS.items():
        entries = hooks.setdefault(event, [])
        flat = json.dumps(entries)
        if cmd not in flat:
            entry = {"hooks": [{"type": "command", "command": cmd}]}
            if event == "PreToolUse":
                entry["matcher"] = "Bash"
            entries.append(entry)
            added.append(event)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(cfg, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return added


def init_repo(target, src_engine=None):
    """Install governance into `target` repo. Returns summary dict. Idempotent."""
    src = src_engine or os.path.dirname(os.path.abspath(__file__))
    src_hooks = os.path.join(src, "..", "platforms", "claude-code", "hooks")
    t_engine = os.path.join(target, "engine")
    t_hooks = os.path.join(target, "platforms", "claude-code", "hooks")
    os.makedirs(os.path.join(t_engine, "gates"), exist_ok=True)
    os.makedirs(os.path.join(t_engine, "schemas"), exist_ok=True)
    os.makedirs(os.path.join(t_engine, "web"), exist_ok=True)
    os.makedirs(t_hooks, exist_ok=True)

    copied = 0
    for f in CORE_FILES:
        sp = os.path.join(src, f)
        if os.path.exists(sp):
            shutil.copy2(sp, os.path.join(t_engine, f)); copied += 1
    for sub in ("gates", "schemas", "web"):
        sd = os.path.join(src, sub)
        if os.path.isdir(sd):
            for f in os.listdir(sd):
                if f.endswith((".yaml", ".json", ".md", ".html")):
                    shutil.copy2(os.path.join(sd, f), os.path.join(t_engine, sub, f)); copied += 1
    for h in HOOKS:
        sp = os.path.join(src_hooks, h)
        if os.path.exists(sp):
            shutil.copy2(sp, os.path.join(t_hooks, h)); copied += 1

    # .gitignore engine runtime
    gi = os.path.join(t_engine, ".gitignore")
    open(gi, "w", encoding="utf-8").write("__pycache__/\n*.pyc\n*.jsonl\n.writeback_state.json\n.testrun_cache.json\n")

    added = _merge_settings(os.path.join(target, ".claude", "settings.json"))

    # CoreAiWorkspaces scaffold (only if absent — never overwrite an existing project)
    scaffold = []
    for rel, content in [("CoreAiWorkspaces/02-task/task-board.md", BOARD_MIN),
                         ("CoreAiWorkspaces/01-plan/work-status.md", WS_MIN),
                         ("CoreAiWorkspaces/03-log/work-log-index.md", WL_MIN)]:
        p = os.path.join(target, rel)
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(content)
            scaffold.append(rel)

    # test command: example only — user sets the real one (enforced once set)
    ex = os.path.join(t_engine, "testcmd.txt.example")
    if not os.path.exists(ex):
        open(ex, "w", encoding="utf-8").write("# คัดลอกไฟล์นี้เป็น testcmd.txt แล้วใส่คำสั่งเทสจริง 1 บรรทัด เช่น:\n# python -m pytest -q\n")

    return {"copied": copied, "hooks_added": added, "scaffolded": scaffold, "target": os.path.abspath(target)}
