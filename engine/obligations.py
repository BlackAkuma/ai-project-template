"""OBS-1: re-inject ACTIVE obligations on every user prompt (fight recency decay).

SessionStart injects a full digest once; over a long conversation those standing constraints
(freezes, pending human decisions, a regressed test gate) decay out of the model's effective
attention and get violated — the exact "AI ignores the rules after a while" failure this addresses.
This renders a TINY, token-aware reminder (only what is LIVE and actionable) for a UserPromptSubmit
hook to inject each turn. Deterministic, rendered from real state — no LLM, cannot hallucinate.

Design: keep it short. Standing freezes are always shown (that's the whole point — they decay);
inbox / regression / prod-branch lines appear only when present. Empty engine -> nothing.

  python engine/obligations.py [--root .]
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from inbox import list_open  # noqa: E402

WORK_STATUS = "CoreAiWorkspaces/01-plan/work-status.md"


def _branch(root):
    try:
        p = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                           capture_output=True, text=True, timeout=5)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def _prod_branch(root):
    path = os.path.join(root, WORK_STATUS)
    if not os.path.exists(path):
        return ""
    m = re.search(r"git_prod_branch\s*:\s*(\S+)", open(path, encoding="utf-8", errors="replace").read())
    return m.group(1) if m else ""


def render(root="."):
    """Return the obligations reminder string (empty if nothing to surface / no engine)."""
    if not os.path.exists(os.path.join(root, "engine")):
        return ""
    lines = []

    # standing freezes — shown EVERY turn because recency decay on these is the core failure mode
    freezes = ["MASTER FREEZE (ห้ามแตะ master จนกว่า user สั่งปลด)"]  # hardcoded-on in govern hook
    if os.path.exists(os.path.join(root, "engine", ".dev-direct-freeze")):
        freezes.append("DEV-DIRECT FREEZE (งานฟีเจอร์ → แตก feature branch; doc-only commit บน dev ได้)")
    lines.append("🔒 active rules: " + " · ".join(freezes))

    # current branch + prod-branch guard
    br = _branch(root)
    prod = _prod_branch(root)
    if br:
        warn = "  ⚠️ คุณอยู่บน PRODUCTION branch — switch ไป dev ก่อน" if (prod and br == prod) else ""
        lines.append(f"🌿 branch: {br}{warn}")

    # open human decisions — the AI must respect pending/rejected, not re-decide on its own
    try:
        items = list_open(root=root)
    except Exception:
        items = []
    if items:
        ids = ", ".join(i.get("id", "?") for i in items[:8])
        lines.append(f"📥 decision-inbox: {len(items)} open ({ids}) — รอ human; ห้าม bypass/ตัดสินเอง")

    # FU-5 test-gate regression (deleted testcmd after enforce) -> done-gate fail-closed
    try:
        from testrun import get_command, _was_configured
        if not get_command(root) and _was_configured(root):
            lines.append("🛑 test_gate REGRESSED — testcmd.txt หาย; done-gate ถูก BLOCK (กู้ engine/testcmd.txt)")
    except Exception:
        pass

    if len(lines) == 1 and not items:  # only the freeze line — still worth the one-line reminder
        pass
    return "[ACTIVE OBLIGATIONS — re-injected each turn]\n" + "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    out = render(ap.parse_args().root)
    if out:
        print(out)
