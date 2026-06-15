"""P3-1: append-only Event log with prev_hash chain (NFR-4 concurrency serialization + FR-2.6 audit/tamper-evidence).

Constitutive piece: governed state changes are recorded as a hash-chained Event.
Any out-of-band edit/reorder/delete of the log breaks the chain → detectable (verify_chain).
This is the data-level foundation of "agent can't fake state without detection" (BRD FR-1).
Full interception (FS allowlist + tool-gating so direct writes are impossible) = later P3 increments.
"""
import hashlib
import json
import os

LOG = "engine/events.log.jsonl"


def _hash(prev, payload):
    blob = prev + json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _payload(rec):
    return {k: rec[k] for k in ("ts", "actor", "action", "target", "result", "prev")}


def append_event(actor, action, target, result, ts=0, root=".", log=LOG):
    """Append a hash-chained event. ts passed in (deterministic for tests / caller stamps real time).

    FU-6 (prereq Phase B): the read-prev -> hash -> append sequence MUST be serialized. Without a
    lock, two concurrent writers read the same prev_hash and both append against it -> a CHAIN FORK
    (two records share one prev) that verify_chain reports as tampered. We reuse FU-2's _FileLock
    (atomic, pid-liveness stale-break) via a lazy import — events is imported BY inbox, so importing
    it at module top would be circular; importing inside the call is safe (inbox is loaded by then).

    DEADLOCK SAFETY (panel-corrected): some inbox mutators (approval_state, escalate_overdue) call
    append_event WHILE still holding the inbox lock; others (create/resolve/reopen) call it after
    releasing. Both are safe ONLY because this lock is a strict LEAF on a DIFFERENT file
    (events.log.jsonl.lock != inbox.jsonl.lock) — events.py must NEVER acquire the inbox lock here,
    or an ABBA deadlock appears. Keep this function a lock-leaf."""
    from inbox import _FileLock  # lazy: break the events<->inbox import cycle (and stay a lock-leaf)
    path = os.path.join(root, log)
    with _FileLock(path):  # serialize read-prev + append so the chain never forks under concurrency
        prev = _last_hash(path)
        payload = {"ts": ts, "actor": actor, "action": action, "target": target, "result": result, "prev": prev}
        rec = dict(payload, hash=_hash(prev, payload))
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())  # durability: the audit record is on disk before the lock releases
    return rec


def _last_hash(path):
    """Read the chain head (last record's hash), self-healing against a TORN TAIL. append uses a
    plain append (not tmp+replace), so a crash mid-write can leave a corrupt final line. That line
    was never acknowledged to any caller, so we drop trailing corrupt line(s) and persist the
    truncation before chaining — keeps the chain intact instead of crashing the next append (panel
    FU-6 dissent). Only the TRAILING line is recoverable; mid-file corruption stays a verify_chain
    failure (real tamper). Caller MUST hold the lock."""
    if not os.path.exists(path):
        return ""
    lines = [ln for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]
    n = len(lines)
    head = ""
    while lines:
        try:
            head = json.loads(lines[-1])["hash"]
            break
        except Exception:
            lines.pop()  # torn/corrupt trailing line from a crashed append -> discard
    if len(lines) != n:       # we dropped torn tail line(s) -> persist the truncation
        _rewrite(path, lines)
    return head


def _rewrite(path, lines):
    """Atomic truncate-rewrite (tmp + os.replace) used only on the rare torn-tail recovery path."""
    tmp = path + f".tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(("\n".join(lines) + "\n") if lines else "")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def verify_chain(root=".", log=LOG):
    """Return (ok, reason). False => tampered/reordered/deleted."""
    path = os.path.join(root, log)
    if not os.path.exists(path):
        return True, "empty"
    prev = ""
    lines = [ln for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]
    for i, line in enumerate(lines):
        try:
            rec = json.loads(line)
        except Exception:
            return False, f"line {i}: corrupt json"
        if rec.get("prev") != prev:
            return False, f"line {i}: prev-link mismatch (reordered/deleted)"
        if _hash(prev, _payload(rec)) != rec.get("hash"):
            return False, f"line {i}: hash mismatch (record tampered)"
        prev = rec["hash"]
    return True, f"valid ({len(lines)} events)"
