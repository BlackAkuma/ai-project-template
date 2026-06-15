"""BL-6/A3: real test evidence — run the project's test command, cache by git HEAD (G2).

Closes the most common fake: "tests pass" claimed without running them. The gate consumes
the REAL exit code. Config = engine/testcmd.txt in the target repo (one line command).
Policy (logged decision): configured -> ENFORCED · not configured -> not enforced
(visible in digest; `engine init` BL-7 writes a default). Cache by HEAD avoids re-running
on unchanged code (NFR-N5 latency).
"""
import json
import os
import subprocess

CMD_FILE = "engine/testcmd.txt"
CACHE = "engine/.testrun_cache.json"
MARKER = "engine/.testcmd_configured"  # FU-5: sticky proof tests were EVER configured (anti-silent-disable)


def _head(root):
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                           text=True, timeout=10)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def _tree_dirty(root):
    """True if working tree has uncommitted changes — cache must NOT be reused then
    (P1-panel consensus: stale-green loophole — edit after green run passed the gate)."""
    try:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True,
                           text=True, timeout=10)
        return bool(p.stdout.strip()) if p.returncode == 0 else True  # unknown -> treat dirty
    except Exception:
        return True


def get_command(root="."):
    p = os.path.join(root, CMD_FILE)
    if os.path.exists(p):
        cmd = open(p, encoding="utf-8").read().strip()
        return cmd or None
    return None


def _mark_configured(root, cmd):
    """FU-5: record (stickily) that tests were configured, so deleting testcmd.txt later is a
    detectable REGRESSION, not a silent un-enforce. Stores the last known command for the message."""
    try:
        with open(os.path.join(root, MARKER), "w", encoding="utf-8") as f:
            f.write(cmd)
    except Exception:
        pass


def _was_configured(root):
    return os.path.exists(os.path.join(root, MARKER))


def run_tests(root=".", use_cache=True, timeout=600):
    """Returns {configured, green, exit, head, cached, command, was_configured, regressed}.
    Real exit code only. FU-5: if tests were EVER configured (sticky marker) but testcmd.txt is now
    gone, that's a fail-closed REGRESSION (regressed=True) — the gate must block, not silently pass."""
    cmd = get_command(root)
    if not cmd:
        regressed = _was_configured(root)
        return {"configured": False, "green": False if regressed else None,
                "exit": None, "head": "", "cached": False, "command": None,
                "was_configured": regressed, "regressed": regressed}
    _mark_configured(root, cmd)

    head = _head(root)
    cp = os.path.join(root, CACHE)
    if use_cache and _tree_dirty(root):
        use_cache = False  # dirty tree -> always re-run (no stale green)
    if use_cache and head and os.path.exists(cp):
        try:
            c = json.load(open(cp, encoding="utf-8"))
            if c.get("head") == head and c.get("command") == cmd:
                return {"configured": True, "green": c["exit"] == 0, "exit": c["exit"],
                        "head": head, "cached": True, "command": cmd,
                        "was_configured": True, "regressed": False}
        except Exception:
            pass

    try:
        p = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        code = p.returncode
    except subprocess.TimeoutExpired:
        code = 124  # timeout = red (fail-closed)
    except Exception:
        code = 125

    if head:
        try:
            json.dump({"head": head, "exit": code, "command": cmd}, open(cp, "w", encoding="utf-8"))
        except Exception:
            pass
    return {"configured": True, "green": code == 0, "exit": code, "head": head, "cached": False,
            "command": cmd, "was_configured": True, "regressed": False}
