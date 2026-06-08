"""Phase A2: HTTP API over the engine (stdlib http.server — no framework dep).

handle(method, path, body, root) is a PURE function -> (status, dict) = testable headless
with no socket. serve(port) wraps it in http.server for a real running backend (the Shell calls this).
FastAPI is optional later (BRD §7) — stdlib keeps it dependency-free + sovereign.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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


def handle(method, path, body=None, root="."):
    """Pure router. Returns (status_code, dict). No socket — directly testable."""
    body = body or {}
    if method == "GET" and path == "/cockpit":
        return 200, {"cockpit": render_cockpit(_state(root), list_open(root=root, inbox=INBOX), [])}
    if method == "GET" and path == "/inbox":
        return 200, {"open": list_open(root=root, inbox=INBOX)}
    if method == "GET" and path == "/audit":
        ok, reason = verify_chain(root=root, log=LOG)
        return 200, {"chain_ok": ok, "reason": reason}
    if method == "POST" and path == "/turn":
        if "task" not in body or "intent" not in body:
            return 400, {"error": "task and intent required"}
        r = governed_turn(body["task"], body["intent"], body.get("risk", 1),
                          model=body.get("model", "stub-strong"), root=root, ts=body.get("ts", 0), log=LOG, inbox=INBOX)
        return 200, r
    if method == "POST" and path == "/inbox/resolve":
        r = resolve_item(body.get("id"), body.get("decision"), by=body.get("by", "user"),
                         ts=body.get("ts", 0), root=root, inbox=INBOX, log=LOG)
        return (200, r) if r else (404, {"error": "not found / already resolved"})
    return 404, {"error": "not found", "method": method, "path": path}


def serve(port=8777, root="."):  # pragma: no cover (real server — needs a running process)
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class H(BaseHTTPRequestHandler):
        def _go(self, method):
            ln = int(self.headers.get("content-length", 0) or 0)
            raw = self.rfile.read(ln) if ln else b""
            try:
                body = json.loads(raw or b"{}")
            except Exception:
                body = {}
            st, res = handle(method, self.path, body, root=root)
            payload = json.dumps(res, ensure_ascii=False).encode()
            self.send_response(st)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            self._go("GET")

        def do_POST(self):
            self._go("POST")

        def log_message(self, *a):
            pass

    print(f"engine API on http://127.0.0.1:{port} (root={root})")
    HTTPServer(("127.0.0.1", port), H).serve_forever()


if __name__ == "__main__":  # pragma: no cover
    serve(int(os.environ.get("PORT", "8777")), os.environ.get("ROOT", "."))
