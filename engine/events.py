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
    """Append a hash-chained event. ts passed in (deterministic for tests / caller stamps real time)."""
    path = os.path.join(root, log)
    prev = ""
    if os.path.exists(path):
        lines = [ln for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
    payload = {"ts": ts, "actor": actor, "action": action, "target": target, "result": result, "prev": prev}
    rec = dict(payload, hash=_hash(prev, payload))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


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
