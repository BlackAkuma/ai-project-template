"""Phase A1: runnable CLI — turns the engine library into a usable tool (not just modules).

  python engine/cli.py cockpit [--root .]
  python engine/cli.py gate <gate-id> [--task T-XXX]
  python engine/cli.py turn <task> <intent> [--risk N] [--model M] [--root .]
  python engine/cli.py inbox [--root .]
  python engine/cli.py inbox-resolve <id> <approved|rejected> [--by NAME]
  python engine/cli.py audit [--root .]

This is the real command surface a person/script uses; Phase A2 wraps these as an HTTP API.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from cockpit import render_cockpit  # noqa: E402
from migrate_state import parse_board  # noqa: E402
from inbox import list_open, resolve_item  # noqa: E402
from agent import governed_turn  # noqa: E402
from events import verify_chain  # noqa: E402

LOG = "engine/events.log.jsonl"
INBOX = "engine/inbox.jsonl"


def _state(root):
    bp = os.path.join(root, "CoreAiWorkspaces/02-task/task-board.md")
    st = parse_board(open(bp, encoding="utf-8").read()) if os.path.exists(bp) else {"tasks": []}
    st.setdefault("project", {"phase": "stage2", "active_branch": "dev"})
    return st


def cmd_cockpit(a):
    evp = os.path.join(a.root, LOG)
    events = []
    if os.path.exists(evp):
        import json
        events = [json.loads(x) for x in open(evp, encoding="utf-8").read().splitlines() if x.strip()]
    print(render_cockpit(_state(a.root), list_open(root=a.root, inbox=INBOX), events))
    return 0


def cmd_gate(a):
    # delegate to check.py (single source of gate-eval logic)
    return subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "check.py"),
                           a.gate] + (["--task", a.task] if a.task else []) + ["--root", a.root]).returncode


def cmd_turn(a):
    r = governed_turn(a.task, a.intent, a.risk, model=a.model, root=a.root, ts=a.ts, log=LOG, inbox=INBOX)
    print(f"status={r['status']}  " + "  ".join(f"{k}={v}" for k, v in r.items() if k != "status"))
    return 0 if r["status"] in ("done", "executed", "inbox") else 1


def cmd_inbox(a):
    items = list_open(root=a.root, inbox=INBOX)
    print(f"{len(items)} open Decision Inbox item(s):")
    for it in items:
        print(f"  [{it.get('id')}] L{it.get('risk_level')} {it.get('gate')}: {it.get('reason', '')}")
    return 0


def cmd_inbox_resolve(a):
    r = resolve_item(a.id, a.decision, by=a.by, ts=a.ts, root=a.root, inbox=INBOX, log=LOG)
    print("resolved:" if r else "not found / already resolved:", a.id, "->", a.decision)
    return 0 if r else 1


def cmd_audit(a):
    ok, reason = verify_chain(root=a.root, log=LOG)
    print(f"audit chain: {'INTACT' if ok else 'TAMPERED'} ({reason})")
    return 0 if ok else 1


def build_parser():
    ap = argparse.ArgumentParser(prog="engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("cockpit", "inbox", "audit"):
        s = sub.add_parser(name)
        s.add_argument("--root", default=".")
    g = sub.add_parser("gate"); g.add_argument("gate"); g.add_argument("--task"); g.add_argument("--root", default=".")
    t = sub.add_parser("turn"); t.add_argument("task"); t.add_argument("intent")
    t.add_argument("--risk", type=int, default=1); t.add_argument("--model", default="stub-strong")
    t.add_argument("--ts", type=int, default=0); t.add_argument("--root", default=".")
    r = sub.add_parser("inbox-resolve"); r.add_argument("id"); r.add_argument("decision", choices=["approved", "rejected"])
    r.add_argument("--by", default="user"); r.add_argument("--ts", type=int, default=0); r.add_argument("--root", default=".")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    return {"cockpit": cmd_cockpit, "gate": cmd_gate, "turn": cmd_turn, "inbox": cmd_inbox,
            "inbox-resolve": cmd_inbox_resolve, "audit": cmd_audit}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
