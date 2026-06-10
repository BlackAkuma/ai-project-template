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


def _head(root):
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                           text=True, timeout=10)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def get_command(root="."):
    p = os.path.join(root, CMD_FILE)
    if os.path.exists(p):
        cmd = open(p, encoding="utf-8").read().strip()
        return cmd or None
    return None


def run_tests(root=".", use_cache=True, timeout=600):
    """Returns {configured, green, exit, head, cached, command}. Real exit code only."""
    cmd = get_command(root)
    if not cmd:
        return {"configured": False, "green": None, "exit": None, "head": "", "cached": False, "command": None}

    head = _head(root)
    cp = os.path.join(root, CACHE)
    if use_cache and head and os.path.exists(cp):
        try:
            c = json.load(open(cp, encoding="utf-8"))
            if c.get("head") == head and c.get("command") == cmd:
                return {"configured": True, "green": c["exit"] == 0, "exit": c["exit"],
                        "head": head, "cached": True, "command": cmd}
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
    return {"configured": True, "green": code == 0, "exit": code, "head": head, "cached": False, "command": cmd}
