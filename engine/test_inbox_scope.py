"""FU-3 — approval scoping: a human's reject/approve sticks to a command's CANONICAL scope, so a
reworded retry (whitespace/case/quoting) can't escape it; a genuinely different command still opens
a fresh decision. Run: python engine/test_inbox_scope.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import create_item, resolve_item, approval_state, canon_scope  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))
LOG = "engine/events.log.jsonl"
IB = "engine/inbox.jsonl"

# canon_scope normalization — safe axes ONLY (ws + paired quotes), NOT case (panel dissent fix)
check("canon strips paired quotes + collapses ws (case PRESERVED)",
      canon_scope("  'git push   --force'  ") == "git push --force")
check("canon ws-equivalent rewordings match",
      canon_scope("git  push --force") == canon_scope("git push    --force"))
check("canon does NOT lowercase (case-sensitive args kept distinct)",
      canon_scope("rm -rf Build/") != canon_scope("rm -rf build/"))
check("canon unwraps only matching paired quotes, not asymmetric",
      canon_scope("echo 'hi'") == "echo 'hi'" and canon_scope("'echo hi'") == "echo hi")

# core FU-3: reject a command, reworded retry stays rejected (does NOT escape via new item)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    cmd = "git push --force origin main"
    it = create_item("risky_git", "T-1", 2, f"force push :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG)
    resolve_item(it["id"], "rejected", by="u", ts=1, root=d, inbox=IB, log=LOG, reason="no force on main")

    # exact retry -> rejected
    check("exact command retry -> rejected",
          approval_state("risky_git", f"force push :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG) == "rejected")
    # reworded (extra spaces) retry -> STILL rejected (FU-3 fix)
    reword = "  git  push   --force   origin   main "
    check("reworded retry (whitespace) -> still rejected (no escape)",
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

# SECURITY (panel dissent): case-different command must NOT consume a different-case approval
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    cmd = "rm -rf build/"
    it = create_item("risky_git", "T-2", 2, f"clean :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG)
    resolve_item(it["id"], "approved", by="u", ts=1, root=d, inbox=IB, log=LOG)
    # ws-reworded (same case) consumes the approval once
    s1 = approval_state("risky_git", "x", scope="rm   -rf  build/", root=d, inbox=IB, log=LOG)
    check("ws-reworded approve -> approved once", s1 == "approved")
    # re-arm and prove a DIFFERENT-CASE path does NOT match (no false-merge widening)
    it2 = create_item("risky_git", "T-2b", 2, f"clean :: {cmd}", scope=cmd, root=d, inbox=IB, log=LOG)
    resolve_item(it2["id"], "approved", by="u", ts=2, root=d, inbox=IB, log=LOG)
    sc = approval_state("risky_git", "x", scope="rm -rf Build/", root=d, inbox=IB, log=LOG)
    check("different-CASE command -> none (NOT consumed by build/ approval)", sc == "none")

# backward compat: a TRUE legacy item (raw jsonl, NO 'scope' field) falls back to canon(reason)
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    legacy = {"id": "DI-0001", "ts": 1, "gate": "gate", "task": "T-3", "risk_level": 2,
              "reason": "deploy prod", "status": "rejected", "resolved_by": "u", "resolved_ts": 1}
    with open(os.path.join(d, IB), "w", encoding="utf-8") as f:
        f.write(json.dumps(legacy) + "\n")  # NO scope key — pre-FU-3 shape
    check("legacy no-scope item: reject still sticks via canon(reason)",
          approval_state("gate", "deploy prod", root=d, inbox=IB, log=LOG) == "rejected")
    check("legacy no-scope ws-reworded reason -> still rejected",
          approval_state("gate", "deploy   prod", root=d, inbox=IB, log=LOG) == "rejected")

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} approval-scope tests passed")
