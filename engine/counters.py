"""BL-11: bypass-path counters — OBSERVABILITY, not a gate (M-A3 panel verdict 2026-06-17).

The dogfood week produced only 3 governance holds across 90 commits. That low hold-count
can mean EITHER "well-calibrated" OR "silent friction" — the bypass paths quietly waving
work past the gates. The panel's BL-11 verdict was CONFIRM CALIBRATED but: instrument
before tuning. This module counts how often each bypass path fires so the signal is
measurable, not assumed. Instrumented bypass paths (govern-action.sh):

  - doc_exempt    : a doc-only commit on dev that the DEV-DIRECT FREEZE let through (the
                    feature-branch/traceability gates were skipped because no code was staged).
  - consume_once  : the engine/.govern-allow-once one-shot user-order bypass was consumed.
  - inbox_approved: a risky git op that was HELD then APPROVED in the Decision Inbox and let
                    through once (BL-11 panel/contrarian fix: this is a genuine bypass of the
                    git-risk gate and it inversely correlates with hold-count — every approval
                    raises the hold-count by 1 while the bypass itself was previously invisible).

KNOWN-UNCOUNTED (accepted scope, not "exactly these three" — fast-follow BL-11b):
  - govern-docs.sh GOVERN_USER_ORDER=1 (requirement-immutability / Task-Close-Gate escape) and
    validate-commit.sh SKIP_DOC_SYNC=1 live in OTHER hooks; instrumenting them is deferred.
    bump() accepts any name, so adding them later is a one-line call with no schema change.

SCOPE: the counter file is LOCAL + gitignored — a per-CHECKOUT health gauge ("is governance
calibrated on THIS machine"), NOT shared/exportable audit evidence. A fresh clone starts at
zero; that zero means "no bypass observed here yet", not "calibrated elsewhere".

Cumulative totals are PRESERVED (so a weekly calibration judgment is possible); the digest
shows a per-session DELTA via a "seen" marker. Near-zero deltas => calibrated, leave rules
alone. High deltas => the low hold-count is hiding friction => that is the tune trigger.

Atomic + lock-serialized (reuses FU-2 _FileLock + FU-8 _atomic_write), so concurrent hook
invocations and concurrent SessionStarts never tear the file or double-count the delta.

LIVENESS (BL-11 panel: all 3 lenses): bump is fire-and-forget (callers `|| true`) so a broken
counters.py would silently no-op and a real bypass would read as "0 = calibrated" — the exact
false-negative this feature exists to kill. The digest therefore renders instrument health
LOUDLY: if this module can't be imported/read, the SessionStart digest says so instead of
silently showing nothing (see digest.py + health()). Fail-safe (never block the action) is
preserved — the loudness lives on the READ side, not in the hook.

  python engine/counters.py bump <name> [--root .]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

COUNTERS = "engine/.bypass-counters.json"
# The bypass paths we track. Unknown names are still accepted by bump() (forward-compat),
# but the digest renders these in a stable order.
KNOWN = ("doc_exempt", "consume_once", "inbox_approved")


def _path(root):
    return os.path.join(root, COUNTERS)


def _load(p):
    if os.path.exists(p):
        try:
            d = json.load(open(p, encoding="utf-8"))
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}
    return {}


def bump(name, root="."):
    """Atomically increment a named counter. Returns the new value. Fail-safe by design:
    callers (the hook) suppress errors — a counter failure must NEVER block a real action."""
    from store import _atomic_write          # FU-8 atomic writer (tmp+fsync+os.replace)
    from inbox import _FileLock              # FU-2 cross-process lock (lazy: avoid import cost)
    p = _path(root)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with _FileLock(p):
        data = _load(p)
        counts = data.get("counts", {})
        counts[name] = int(counts.get(name, 0)) + 1
        data["counts"] = counts
        _atomic_write(p, json.dumps(data, ensure_ascii=False))
    return counts[name]


def read(root="."):
    """Current cumulative counts (no mutation)."""
    return _load(_path(root)).get("counts", {})


def session_view(root="."):
    """Return {name: (delta_since_last_view, cumulative_total)} and advance the seen-marker
    atomically (so two SessionStarts can't both claim the same delta). Empty dict if no
    counter file yet. Read-and-advance is done under the lock to stay race-free."""
    from store import _atomic_write
    from inbox import _FileLock
    p = _path(root)
    if not os.path.exists(p):
        return {}
    with _FileLock(p):
        data = _load(p)
        counts = data.get("counts", {})
        seen = data.get("seen", {})
        view = {k: (int(v) - int(seen.get(k, 0)), int(v)) for k, v in counts.items()}
        data["seen"] = {k: int(v) for k, v in counts.items()}
        _atomic_write(p, json.dumps(data, ensure_ascii=False))
    return view


def health(root="."):
    """Liveness self-check (BL-11 panel: distinguish a genuine 0 from a broken/dead instrument).
    Returns (ok: bool, note: str). ok=False means the counter file EXISTS but is unreadable/
    malformed — a real instrument failure the digest must surface loudly. A simply-absent file
    is ok=True ("no bypass observed here yet") — that is the correct quiet state, not a fault."""
    p = _path(root)
    if not os.path.exists(p):
        return True, "no bypass observed on this checkout yet"
    try:
        d = json.load(open(p, encoding="utf-8"))
        if not isinstance(d, dict):
            return False, "counter file malformed (not an object)"
        return True, "live"
    except Exception as e:  # noqa: BLE001
        return False, f"counter file unreadable: {e}"


def digest_line(root="."):
    """One compact line for the SessionStart digest, or "" if nothing to show.
    Advances the seen-marker (per-session delta semantics)."""
    view = session_view(root)
    if not view:
        return ""
    ordered = [k for k in KNOWN if k in view] + [k for k in view if k not in KNOWN]
    parts = [f"{k}={view[k][0]} ({view[k][1]} total)" for k in ordered]
    return ("bypass_paths (BL-11): " + " · ".join(parts)
            + " — near-zero=calibrated; high=low-hold-count hides friction")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["bump", "show"])
    ap.add_argument("name", nargs="?", default="")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    if a.cmd == "bump":
        if not a.name:
            sys.exit(2)
        print(bump(a.name, a.root))
    else:
        print(json.dumps(read(a.root), ensure_ascii=False))
