"""engine check <gate> — evaluate a gate against real repo state (P2-1).

Usage:
  python engine/check.py <gate-id> [--task T-XXX] [--root .]

Exit 0 = pass (or non-blocking fail); exit 1 = blocking fail (block/hard-stop).
Verdict carries risk_level + effect (ADR-008 risk-tier).
"""
import argparse
import os
import subprocess
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolvers import RESOLVERS  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Thai output on Windows console (cp1252 fix)
except Exception:
    pass


def gather_ctx(root):
    def git(*a):
        try:
            return subprocess.run(
                ["git", *a], cwd=root, capture_output=True, text=True,
                encoding="utf-8", errors="replace"  # git diff อาจมีภาษาไทย — กัน cp1252 crash
            ).stdout
        except Exception:
            return ""
    files = [f for f in git("diff", "--cached", "--name-only").splitlines() if f]
    # FU: secret/placeholder scan must exclude files that DEFINE patterns (the scanner itself) +
    # test fixtures with intentional fake secrets — else the scanner flags its own definitions.
    EXCLUDE = ("platforms/claude-code/hooks/", "/test_", "test_", "tests/", "engine/gates/")
    def _excluded(f):
        return any(x in f for x in EXCLUDE)
    # full diff for context; scanned 'added' excludes scanner/test files (pathspec-scoped)
    diff = git("diff", "--cached")
    scan_files = [f for f in files if not _excluded(f)]
    scan_diff = git("diff", "--cached", "--", *scan_files) if scan_files else ""
    added = "\n".join(
        ln[1:] for ln in scan_diff.splitlines()
        if ln.startswith("+") and not ln.startswith("+++")
    )
    return {"root": root, "staged_diff": diff, "staged_files": files, "staged_added": added}


def resolve_args(d, ns):
    out = {}
    for k, v in d.items():
        if isinstance(v, str) and v.startswith("$args."):
            out[k] = getattr(ns, v.split(".", 1)[1], None)
        else:
            out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gate")
    ap.add_argument("--task", dest="task_id")
    ap.add_argument("--root", default=".")
    ns = ap.parse_args()
    root = os.path.abspath(ns.root)  # the PROJECT being checked (what resolvers scan)
    # gates live with the ENGINE (this file's dir), NOT in the target project — these are separate
    # locations: you can govern any repo without copying gates into it (A2 fix).
    gates_root = os.path.dirname(os.path.abspath(__file__))

    gpath = os.path.join(gates_root, "gates", ns.gate + ".yaml")
    gate = None
    if os.path.exists(gpath):
        gate = yaml.safe_load(open(gpath, encoding="utf-8"))
    else:
        # fallback: match by gate `id` (so BRD-traced ids like 'task_close_gate' work too)
        gdir = os.path.join(gates_root, "gates")
        for fn in sorted(os.listdir(gdir)) if os.path.isdir(gdir) else []:
            if fn.endswith(".yaml"):
                g = yaml.safe_load(open(os.path.join(gdir, fn), encoding="utf-8"))
                if g.get("id") == ns.gate:
                    gate = g
                    break
    if gate is None:
        print(f"[ERR] gate not found (by filename or id): {ns.gate}")
        sys.exit(2)
    ctx = gather_ctx(root)

    fails = []
    for req in gate.get("requires", []):
        check = req["check"]
        kw = {k: v for k, v in req.items() if k not in ("check", "class")}
        kw = resolve_args(kw, ns)
        fn = RESOLVERS.get(check)
        if fn is None:
            fails.append(f"{check}[no-resolver]")
            continue
        try:
            if not fn(ctx, **kw):
                fails.append(check)
        except Exception as e:  # noqa: BLE001
            fails.append(f"{check}[err:{e}]")

    risk = gate.get("risk_level", 2)
    effect = gate.get("on_fail", {}).get("effect", "block")
    if fails:
        msg = (gate.get("on_fail", {}).get("message", "")
               .replace("{failed_checks}", ", ".join(fails))
               .replace("{task_id}", str(ns.task_id)))
        print(f"[FAIL] {gate['id']} (risk L{risk}, effect={effect})")
        print(f"  missing: {', '.join(fails)}")
        if msg:
            print(f"  -> {msg}")
        sys.exit(1 if effect in ("block", "hard-stop") else 0)

    print(f"[PASS] {gate['id']} (risk L{risk})")
    sys.exit(0)


if __name__ == "__main__":
    main()
