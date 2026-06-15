"""P6-1: Decision Inbox data layer (Engine-side) — project-level durable human-gate.

Level 2-3 gate verdicts become durable Inbox items; a human resolves (approve/reject).
Every create/resolve is recorded in the Event log (P3-1) = auditable + tamper-evident.
Differentiator (BRD §3/FR-3): durable, PROJECT-level (not per-run like Conductor, not
per-ticket like Jira), inspectable. The UI that renders this = Shell (gated by G4/ADR-011).

inbox.jsonl = current state (derived, rewritable view). events.log = audit truth (chained).
"""
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import append_event  # noqa: E402

INBOX = "engine/inbox.jsonl"
LOG = "engine/events.log.jsonl"
LOCK_TIMEOUT = 10.0  # seconds before a stale lock is broken


_PROC_LOCK = threading.RLock()  # serialize threads IN-process (O_EXCL only covers cross-process)


def _pid_alive(pid):
    """Cross-platform pid liveness. POSIX: os.kill(pid,0). Windows: os.kill(pid,0) does NOT
    raise for a dead pid (re-review blocker) -> use ctypes OpenProcess + GetExitCodeProcess."""
    if sys.platform == "win32":
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            k = ctypes.WinDLL("kernel32", use_last_error=True)
            h = k.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
            if not h:
                # distinguish dead vs protected-but-alive (mirror POSIX PermissionError->alive):
                #   ERROR_INVALID_PARAMETER(87) = no such pid -> DEAD · ERROR_ACCESS_DENIED(5) = exists -> ALIVE
                return ctypes.get_last_error() == 5
            try:
                code = ctypes.c_ulong()
                if k.GetExitCodeProcess(h, ctypes.byref(code)):
                    return code.value == STILL_ACTIVE
                return False
            finally:
                k.CloseHandle(h)
        except Exception:  # noqa: BLE001
            return False  # probe failed -> treat dead (so stale-break can proceed, no deadlock)
    try:
        os.kill(int(pid), 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, owned by another user
    except OSError:
        return False


def _holder_alive(lockfile):
    """Is the lockfile's recorded holder still running? Only break locks of DEAD holders.
    Unreadable/own-pid -> breakable (we're the one waiting, so our own pid on it = stale crash)."""
    try:
        pid = int(open(lockfile, encoding="utf-8").read().strip() or "0")
    except (OSError, ValueError):
        return False
    if pid <= 0 or pid == os.getpid():
        return False  # own-pid on a lock we're waiting for = stale (re-review edge) -> breakable
    return _pid_alive(pid)


class _FileLock:
    """FU-2: atomic inbox RMW (prereq for Phase B multi-agent). Two layers:
    (1) in-process threading.RLock — serializes threads of THIS process (O_EXCL doesn't);
    (2) O_CREAT|O_EXCL lockfile + bounded wait + stale-break — serializes other PROCESSES.
    Paired with _write's tmp+os.replace (per-thread tmp) so a crash never leaves a torn file."""
    def __init__(self, path):
        self.lock = path + ".lock"
        self.fd = None

    def __enter__(self):
        _PROC_LOCK.acquire()
        try:
            d = os.path.dirname(self.lock)
            if d:
                os.makedirs(d, exist_ok=True)
            deadline = time.time() + LOCK_TIMEOUT
            while True:
                try:
                    self.fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    try:
                        os.write(self.fd, str(os.getpid()).encode())  # holder pid for stale liveness
                    except OSError:
                        pass
                    return self
                except (FileExistsError, PermissionError):
                    # PermissionError = Windows delete-pending/sharing-violation race on the lockfile
                    # (panel cross-process bug: was uncaught -> lost write). Must retry, not crash.
                    if time.time() > deadline and not _holder_alive(self.lock):
                        try:
                            os.remove(self.lock)  # stale lock, holder confirmed dead — break it
                        except OSError:
                            pass
                        deadline = time.time() + LOCK_TIMEOUT  # re-arm; avoid tight-spin
                    time.sleep(0.03)
        except BaseException:
            _PROC_LOCK.release()
            raise

    def __exit__(self, *a):
        try:
            if self.fd is not None:
                os.close(self.fd)
            try:
                os.remove(self.lock)
            except OSError:
                pass
        finally:
            _PROC_LOCK.release()
        return False


def _read(path):
    if not os.path.exists(path):
        return []
    return [json.loads(ln) for ln in open(path, encoding="utf-8").read().splitlines() if ln.strip()]


def _write(path, items):
    """Atomic write: tmp + os.replace (FU-2) — reader never sees a half-written inbox."""
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    body = "\n".join(json.dumps(i, ensure_ascii=False) for i in items) + ("\n" if items else "")
    tmp = path + f".tmp.{os.getpid()}.{threading.get_ident()}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(body)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)  # atomic on Windows + POSIX


def canon_scope(s):
    """FU-3: canonical approval scope key — so a human's reject/approve sticks to a command even
    when reworded by whitespace or surrounding quotes (the genuinely-equivalent cheap evasions).

    Deliberately does NOT lowercase (panel dissent FU-3): shell args are case-SENSITIVE on
    Linux/macOS (paths, git ref/branch names), so lowercasing would FALSE-MERGE two distinct
    commands — an approval of 'rm -rf build/' could be consumed by 'rm -rf Build/'. Whitespace and
    paired-quote wrapping are equivalent on every OS; case is not. A case-reworded retry that
    escapes a REJECT is fail-safe (re-opens a fresh item the human sees again); a case false-merge
    on APPROVE is fail-dangerous. So we normalize only the safe axes.
    Semantic rewording (git push -f vs --force) is also NOT caught — needs an alias/LLM layer (FU)."""
    s = (s or "").strip()
    while len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):  # unwrap paired wrapping quotes only
        s = s[1:-1].strip()
    return " ".join(s.split())


def create_item(gate, task, risk_level, reason, item_id=None, ts=0, root=".", inbox=INBOX, log=LOG, scope=None):
    """Create an Inbox item from a gate verdict. ONLY Level 2-3 create items (L0/L1 auto-pass).
    scope (FU-3): stable canonical key the approval is bound to (defaults to reason) — a reworded
    retry that canonicalizes to the same scope reuses the prior decision instead of escaping it."""
    if int(risk_level) < 2:
        return None  # risk-tiered: low-risk never reaches the human (ADR-008, anti approval-fatigue)
    path = os.path.join(root, inbox)
    with _FileLock(path):  # FU-2: atomic read-modify-write
        items = _read(path)
        item_id = item_id or f"DI-{len(items) + 1:04d}"
        item = {"id": item_id, "ts": ts, "gate": gate, "task": task, "risk_level": int(risk_level),
                "reason": reason, "scope": canon_scope(scope if scope is not None else reason),
                "status": "open", "resolved_by": None, "resolved_ts": None}
        items.append(item)
        _write(path, items)
    append_event("engine", "inbox.create", item_id, f"gate={gate};L{risk_level}", ts=ts, root=root, log=log)
    return item


def resolve_item(item_id, decision, by, ts=0, root=".", inbox=INBOX, log=LOG, reason=""):
    """Human resolves an open item. decision = 'approved' | 'rejected'. Recorded to audit log.
    reason: rationale (esp. for reject) — written to the item + audit chain (FR-3 accountability)."""
    assert decision in ("approved", "rejected")
    path = os.path.join(root, inbox)
    with _FileLock(path):  # FU-2: atomic RMW — no double-resolve under concurrency
        items = _read(path)
        target = None
        for it in items:
            if it["id"] == item_id and it["status"] == "open":
                it["status"], it["resolved_by"], it["resolved_ts"] = decision, by, ts
                if reason:
                    it["resolution_reason"] = reason
                target = it
        if target is None:
            return None  # not found or already resolved
        _write(path, items)
    append_event(by, "inbox.resolve", item_id, f"{decision}: {reason}" if reason else decision, ts=ts, root=root, log=log)
    return target


def list_open(root=".", inbox=INBOX):
    return [i for i in _read(os.path.join(root, inbox)) if i["status"] == "open"]


def reopen_item(item_id, by, ts=0, root=".", inbox=INBOX, log=LOG, reason=""):
    """FU-1: reconsider a resolved item IN-BAND (rejected/approved-consumed -> open) without
    hand-editing inbox.jsonl. Audited (inbox.reopen). Clears resolution + consumed so the
    decision is genuinely fresh. Returns the item, or None if not found / already open."""
    path = os.path.join(root, inbox)
    with _FileLock(path):  # FU-2: atomic RMW
        items = _read(path)
        target = None
        for it in items:
            if it["id"] == item_id and it["status"] != "open":
                it["status"] = "open"
                it["resolved_by"] = None
                it["resolved_ts"] = None
                it.pop("consumed", None)
                it.pop("resolution_reason", None)
                it.pop("escalated", None)  # panel dissent (FU-1): else reopened+overdue never re-escalates (R7)
                it.pop("escalated_ts", None)
                it["reopened_count"] = it.get("reopened_count", 0) + 1
                target = it
        if target is None:
            return None
        _write(path, items)
    append_event(by, "inbox.reopen", item_id, reason or "reconsider", ts=ts, root=root, log=log)
    return target


def approval_state(gate, reason, root=".", inbox=INBOX, log=LOG, ts=0, scope=None):
    """P0-fix (panel contrarian): make approval CAUSAL. Returns one of:
    'approved'  — a matching approved+unconsumed item existed; it is now CONSUMED (one-shot allow)
    'pending'   — a matching item is still open (do NOT create a duplicate)
    'rejected'  — human said no earlier (stays blocked)
    'none'      — no matching item (caller should hold/create one)
    Matching key (FU-3) = (gate, canon_scope) — canonical so a reworded retry can't escape a prior
    reject. scope defaults to reason; legacy items without a 'scope' field fall back to canon(reason).
    Single-use: each approval unblocks exactly one retry."""
    want = canon_scope(scope if scope is not None else reason)
    path = os.path.join(root, inbox)
    with _FileLock(path):  # FU-2: atomic consume — no double-consume of one approval (TOCTOU)
        items = _read(path)
        match = [i for i in items if i.get("gate") == gate
                 and i.get("scope", canon_scope(i.get("reason", ""))) == want]
        if any(i["status"] == "open" for i in match):
            return "pending"
        for it in match:
            if it["status"] == "approved" and not it.get("consumed"):
                it["consumed"] = True
                _write(path, items)
                append_event("engine", "inbox.consume", it["id"], "approval consumed (action allowed once)",
                             ts=ts, root=root, log=log)
                return "approved"
        if match and match[-1]["status"] == "rejected":
            return "rejected"
        return "none"


def escalate_overdue(now_ts, sla=86400, root=".", inbox=INBOX, log=LOG):
    """F10/FR-3.4: flag open items older than SLA (default 1 day) as escalated; record to audit.
    Returns the list of newly-escalated items. Prevents Level 2-3 items sitting forever (R7)."""
    path = os.path.join(root, inbox)
    with _FileLock(path):  # FU-2: atomic RMW
        items = _read(path)
        escalated = []
        for it in items:
            if it["status"] == "open" and not it.get("escalated") and (now_ts - it.get("ts", 0)) > sla:
                it["escalated"] = True
                it["escalated_ts"] = now_ts
                escalated.append(it)
                append_event("engine", "inbox.escalate", it["id"], f"overdue >{sla}s", ts=now_ts, root=root, log=log)
        if escalated:
            _write(path, items)
    return escalated

