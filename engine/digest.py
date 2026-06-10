"""BL-2/A5: session-start memory digest — เปิด session ใหม่ AI รู้สถานะโปรเจ็กต์เองทันที (G3).

Renders a COMPACT deterministic digest from real repo state (work-status, task-board,
Decision Inbox, recent audit events, last work-log entry). NO LLM — rendered facts only,
so it cannot hallucinate. Injected into Claude Code context via SessionStart hook.

Dedupe note (panel dissent #2): this REPLACES the manual "read 3 AI-CONTEXT blocks" steps
of the Session Start Protocol with one pre-rendered block — same sources, zero extra reads.

  python engine/digest.py [--root .]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from inbox import list_open  # noqa: E402

LOG = "engine/events.log.jsonl"


def _ai_context(path):
    """Extract key: value pairs from a file's AI-CONTEXT block."""
    if not os.path.exists(path):
        return {}
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"<!--\s*AI-CONTEXT(.*?)-->", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        kv = re.match(r"\s*([A-Za-z_][\w-]*)\s*:\s*(.+)", line)
        if kv:
            out[kv.group(1)] = kv.group(2).strip()
    return out


def _git_branch(root):
    """Live branch from git directly (panel fix: never trust possibly-stale store for this)."""
    import subprocess
    try:
        p = subprocess.run(["git", "branch", "--show-current"], cwd=root, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=10)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def render_digest(root="."):
    ws = _ai_context(os.path.join(root, "CoreAiWorkspaces/01-plan/work-status.md"))
    tb = _ai_context(os.path.join(root, "CoreAiWorkspaces/02-task/task-board.md"))
    wl = _ai_context(os.path.join(root, "CoreAiWorkspaces/03-log/work-log-index.md"))
    held = list_open(root=root)

    evp = os.path.join(root, LOG)
    recent = []
    if os.path.exists(evp):
        lines = [x for x in open(evp, encoding="utf-8", errors="replace").read().splitlines() if x.strip()]
        for ln in lines[-3:]:
            try:
                e = json.loads(ln)
                recent.append(f"{e.get('action')} {e.get('target')} -> {str(e.get('result'))[:60]}")
            except Exception:
                pass

    L = ["[PROJECT-MEMORY DIGEST — rendered from store, not generated]"]
    if ws.get("phase"):
        L.append(f"phase: {ws['phase']}")
    live_branch = _git_branch(root)
    if live_branch:
        L.append(f"branch: {live_branch} (live from git)")
    elif ws.get("active_branch"):
        L.append(f"branch: {ws['active_branch']}")
    if ws.get("blocker"):
        L.append(f"blocker: {ws['blocker']}")
    if tb.get("priority_next"):
        L.append(f"priority_next: {tb['priority_next']}")
    if tb.get("todo"):
        L.append(f"todo: {tb['todo']}")
    if wl.get("checkpoint"):
        L.append(f"last_checkpoint: {wl['checkpoint'][:400]}")
    if ws.get("next_action"):
        L.append(f"next_action: {ws['next_action'][:300]}")
    L.append(f"decision_inbox_open: {len(held)}" + (
        " — " + "; ".join(f"[{i.get('id')}] L{i.get('risk_level')} {str(i.get('reason'))[:50]}" for i in held[:3]) if held else ""))
    if recent:
        L.append("recent_audit: " + " | ".join(recent))
    L.append("(full state: CoreAiWorkspaces/ + Cockpit http://127.0.0.1:8777 — this digest replaces manual AI-CONTEXT reads)")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    print(render_digest(ap.parse_args().root))
