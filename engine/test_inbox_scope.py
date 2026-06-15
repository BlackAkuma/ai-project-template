"""FU-3 — approval scoping: a human's reject/approve sticks to a command's CANONICAL scope, so a
reworded retry (whitespace/case/quoting) can't escape it; a genuinely different command still opens
a fresh decision. Run: python engine/test_inbox_scope.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import create_item, resolve_item, approval_state, canon_scope  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))
LOG = "engine/events.log.jsonl"
IB = "engine/inbox.jsonl"

# canon_scope normalization
check("canon strips quotes + lowercases + collapses ws",
      canon_scope("  'Git Push   --FORCE'  ") == "git push --force")
check("canon of equivalent rewordings match",
      canon_scope("git  push --force") == canon_scope("GIT PUSH    --force"))

# core FU-3: reject a command, reworded retry stays rejected (does NOT escape via new item)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    cmd = "git push --force origin main"
    it = create_item("risky_git", "T-1", 2, f"force push :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG)
    resolve_item(it["id"], "rejected", by="u", ts=1, root=d, inbox=IB, log=LOG, reason="no force on main")

    # exact retry -> rejected
    check("exact command retry -> rejected",
          approval_state("risky_git", f"force push :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG) == "rejected")
    # reworded (extra spaces + case + quotes) retry -> STILL rejected (FU-3 fix)
    reword = "  GIT  PUSH   --force   origin   main "
    check("reworded retry (ws/case) -> still rejected (no escape)",
          approval_state("risky_git", "totally different human text", scope=reword, root=d, inbox=IB, log=LOG) == "rejected")
    quoted = "'git push --force origin main'"
    check("quoted retry -> still rejected",
          approval_state("risky_git", "x", scope=quoted, root=d, inbox=IB, log=LOG) == "rejected")

    # a genuinely different command -> 'none' (legitimately opens a fresh decision)
    check("different command -> none (fresh decision allowed)",
          approval_state("risky_git", "y", scope="git push origin feature/x", root=d, inbox=IB, log=LOG) == "none")
    # different gate, same scope -> none (gate is part of the key)
    check("different gate -> none",
          approval_state("other_gate", "z", scope=cmd, root=d, inbox=IB, log=LOG) == "none")

# approve sticks to scope too: reworded retry consumes the SAME approval once
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    cmd = "rm -rf build/"
    it = create_item("risky_git", "T-2", 2, f"clean :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG)
    resolve_item(it["id"], "approved", by="u", ts=1, root=d, inbox=IB, log=LOG)
    s1 = approval_state("risky_git", "x", scope="RM   -rf  build/", root=d, inbox=IB, log=LOG)
    s2 = approval_state("risky_git", "x", scope="rm -rf build/", root=d, inbox=IB, log=LOG)
    check("reworded approve -> approved once then consumed", s1 == "approved" and s2 == "none")

# backward compat: legacy item with NO scope field falls back to canon(reason)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    # simulate legacy item (no 'scope' key) by writing one then matching via reason only
    it = create_item("gate", "T-3", 2, "deploy prod", root=d, inbox=IB, log=LOG)  # scope defaults to canon(reason)
    resolve_item(it["id"], "rejected", by="u", ts=1, root=d, inbox=IB, log=LOG)
    check("no-scope caller matches by reason (legacy path)",
          approval_state("gate", "deploy prod", root=d, inbox=IB, log=LOG) == "rejected")
    check("no-scope reworded reason -> still rejected (canon of reason)",
          approval_state("gate", "DEPLOY   PROD", root=d, inbox=IB, log=LOG) == "rejected")

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} approval-scope tests passed")
