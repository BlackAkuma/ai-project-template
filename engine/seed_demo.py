"""Seed a self-contained DEMO project showing the governance WORKING (not an empty panel).

Creates engine/demo_data/ (its own task-board + work-log) — does NOT touch the real repo —
then runs the REAL engine (governed_turn) so every line shown is genuine engine output:
honest done (allowed) · fake done (blocked) · weak model code (refused) · prod deploy (escalated to Inbox).

  python engine/seed_demo.py
  ROOT=engine/demo_data python engine/api.py     # then open http://127.0.0.1:8777
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import governed_turn  # noqa: E402

DEMO_ROOT = "engine/demo_data"
LOG = "engine/events.log.jsonl"
INBOX = "engine/inbox.jsonl"

DEMO_BOARD = """<!-- AI-CONTEXT
schema_version: 0.1
total_tasks: 4
done: [DEMO-1]
in_progress: [DEMO-3]
blocked: []
todo: [DEMO-2,DEMO-4]
-->
# Demo Project — Acme Web App
"""

DEMO_WORKLOG = """# Work Log (demo)
- DEMO-1 done commit a1b2c3d evidence ✓ (auth module shipped + tests green)
"""


def seed(root=DEMO_ROOT):
    os.makedirs(os.path.join(root, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(root, "CoreAiWorkspaces/03-log"), exist_ok=True)
    os.makedirs(os.path.join(root, "engine"), exist_ok=True)
    open(os.path.join(root, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write(DEMO_BOARD)
    open(os.path.join(root, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write(DEMO_WORKLOG)
    for f in (LOG, INBOX):
        p = os.path.join(root, f)
        if os.path.exists(p):
            os.remove(p)

    turns = [
        ("✅ honest mark_done (has evidence)", "DEMO-1", "mark_done", 1, "claude-sonnet"),
        ("🔴 fake mark_done (no evidence)", "DEMO-2", "mark_done", 1, "claude-sonnet"),
        ("🔴 weak model writes code (role-floor)", "DEMO-3", "edit_code", 1, "local-3b"),
        ("🟡 deploy to prod (labeled low-risk)", "DEMO-4", "deploy_prod", 1, "claude-sonnet"),
    ]
    out = []
    for i, (label, task, intent, risk, model) in enumerate(turns):
        r = governed_turn(task, intent, risk, model=model, root=root, ts=2000 + i, log=LOG, inbox=INBOX)
        out.append((label, r["status"]))
    return out


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    for label, status in seed():
        print(f"  {label:42s} -> {status}")
    print(f"\nseeded demo project at {DEMO_ROOT}")
    print("run:  ROOT=engine/demo_data python engine/api.py   then open http://127.0.0.1:8777")
