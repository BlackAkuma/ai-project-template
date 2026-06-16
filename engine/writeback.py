"""BL-3/A5: session write-back — บันทึกสิ่งที่เกิดขึ้นจริงลง store อัตโนมัติตอนจบ session (G3).

Deterministic facts only (git + events log) — no LLM. Updates ONLY machine-fact keys in the
work-status AI-CONTEXT block (active_branch, last_updated, auto_session); never touches
human-authored narrative (dual-authority, ADR-007). Also appends a JSONL session record.

Root cause it fixes: digest (BL-2) exposed stale work-status — state drifted because nothing
wrote back automatically. This closes the loop: auto-load (BL-2) + auto-save (BL-3).

  python engine/writeback.py [--root .]
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from store import _atomic_write  # noqa: E402 — FU-8: shared atomic writer (tmp+fsync+os.replace)

SESSIONS = "engine/sessions.log.jsonl"
STATE = "engine/.writeback_state.json"


def _git(root, *args):
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=15)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def collect(root="."):
    """Gather deterministic session facts from git + engine logs."""
    branch = _git(root, "branch", "--show-current") or "?"
    head = _git(root, "rev-parse", "--short", "HEAD") or "?"
    ts = _git(root, "log", "-1", "--format=%cI") or ""

    sp = os.path.join(root, STATE)
    last = {}
    if os.path.exists(sp):
        try:
            last = json.load(open(sp, encoding="utf-8"))
        except Exception:
            last = {}
    since = last.get("head")
    if since and since != head:
        log = _git(root, "log", "--oneline", f"{since}..HEAD")
    else:
        log = "" if since == head else _git(root, "log", "--oneline", "-5")
    commits = [l for l in log.splitlines() if l.strip()]

    return {"branch": branch, "head": head, "ts": ts, "new_commits": commits}


def _update_block_key(text, key, value):
    """Set key in the AI-CONTEXT block (replace if present, insert before --> if not)."""
    m = re.search(r"(<!--\s*AI-CONTEXT)(.*?)(-->)", text, re.S)
    if not m:
        return text
    body = m.group(2)
    line = f"{key}: {value}"
    if re.search(rf"^\s*{re.escape(key)}\s*:.*$", body, re.M):
        # lambda replacement: value is literal text, never re-escape-interpreted (panel bug-fix —
        # a commit message containing backslashes must not crash the writeback)
        body = re.sub(rf"^\s*{re.escape(key)}\s*:.*$", lambda _m: line, body, count=1, flags=re.M)
    else:
        body = body.rstrip("\n") + "\n" + line + "\n"
    return text[:m.start()] + m.group(1) + body + m.group(3) + text[m.end():]


def writeback(root="."):
    """Persist session facts. Returns the session record. Safe: machine-fact keys only."""
    facts = collect(root)
    date = (facts["ts"] or "")[:10]

    # 1) update work-status AI-CONTEXT (machine facts only — never narrative)
    # FU-8 invariant: this write touches ONLY machine-fact keys (active_branch/last_updated/
    # auto_session). It is atomic (torn-read safe) but intentionally NOT locked — work-status is a
    # DERIVED view (re-derived from git+events next run), so a concurrent lost update self-heals.
    # If a non-re-derivable (human-authored) key is ever written here, add a _FileLock.
    ws = os.path.join(root, "CoreAiWorkspaces/01-plan/work-status.md")
    if os.path.exists(ws):
        text = open(ws, encoding="utf-8", errors="replace").read()
        text = _update_block_key(text, "active_branch", facts["branch"])
        if date:
            text = _update_block_key(text, "last_updated", date)
        n = len(facts["new_commits"])
        latest = facts["new_commits"][0] if facts["new_commits"] else "(no new commits)"
        text = _update_block_key(text, "auto_session", f"{n} commit(s) @ {facts['head']} | latest: {latest[:90]}")
        _atomic_write(ws, text)  # FU-8: atomic — reader never sees a half-written work-status

    # 2) append machine session record (JSONL, append-only) — FU-8: serialize so concurrent appends
    #    can't interleave into a torn line
    rec = {"head": facts["head"], "branch": facts["branch"], "ts": facts["ts"],
           "new_commits": facts["new_commits"][:20]}
    sp = os.path.join(root, SESSIONS)
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    from inbox import _FileLock  # lazy: avoid import cycle; reuse FU-2 lock
    with _FileLock(sp):
        with open(sp, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())

    # 3) remember HEAD so next run reports only NEW commits — FU-8: atomic (torn-read safe)
    _atomic_write(os.path.join(root, STATE), json.dumps({"head": facts["head"]}, ensure_ascii=False))
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    r = writeback(ap.parse_args().root)
    print(f"writeback: {len(r['new_commits'])} new commit(s) on {r['branch']} @ {r['head']}")
