"""Runnable hero-demo (<10 min) — the demand-harvest instrument (ADR-013 B / BRD §10).

Runs the REAL engine end-to-end on a temp fixture and narrates each step, proving the
differentiator: governance enforced as state, agent can't fake 'done', tamper-evident audit,
risk-tiered Decision Inbox. Reproducible: `python engine/demo.py` (no live files touched).

This is the asset to publish with the OSS soft-ship + show design partners.
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")  # Thai output on Windows cp1252 console
except Exception:
    pass
from govern import mark_done, audit_done  # noqa: E402
from inbox import create_item, resolve_item, list_open  # noqa: E402
from events import verify_chain  # noqa: E402


def hr(t):
    print("\n" + "=" * 64 + f"\n  {t}\n" + "=" * 64)


def fixture(d):
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(d, "CoreAiWorkspaces/03-log"), exist_ok=True)
    os.makedirs(os.path.join(d, "engine"), exist_ok=True)
    open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), "w", encoding="utf-8").write(
        "<!-- AI-CONTEXT\ndone: [T-001]\n-->\n")
    open(os.path.join(d, "CoreAiWorkspaces/03-log/work-log-index.md"), "w", encoding="utf-8").write(
        "# Work Log\n- T-100 implemented + tested, commit a1b2c3d, evidence ✓\n")


def board_done(d):
    txt = open(os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md"), encoding="utf-8").read()
    return re.search(r"done:\s*\[([^\]]*)\]", txt).group(1)


def main():
    print("Governed Project Memory — hero demo")
    print("enforcement เหนือ AGENTS.md: governance ที่เครื่องบังคับ ไม่ใช่หวังให้โมเดลทำตาม")
    with tempfile.TemporaryDirectory() as d:
        fixture(d)
        kw = dict(root=d, inbox="engine/inbox.jsonl", log="engine/events.log.jsonl")

        hr("1. agent แกล้ง mark task done โดยไม่มีหลักฐาน (T-200)")
        r = mark_done("T-200", ts=1, root=d, log="engine/events.log.jsonl")
        print(f"   result: ok={r['ok']} effect={r['effect']} missing={r['missing']}")
        di = create_item("task_close", "T-200", 2, "missing: " + ",".join(r["missing"]), ts=1, **kw)
        print(f"   → BLOCKED → Decision Inbox item {di['id']} (L{di['risk_level']}) — โกงไม่ได้")
        print(f"   board done = [{board_done(d)}]  (T-200 ไม่ถูกเพิ่ม)")

        hr("2. งานที่มีหลักฐานจริง (T-100) → ผ่าน gate + บันทึก signed event")
        r2 = mark_done("T-100", ts=2, root=d, log="engine/events.log.jsonl")
        print(f"   result: ok={r2['ok']}  board done = [{board_done(d)}]")
        print(f"   signed event: {r2['event']['action']} {r2['event']['target']} hash={r2['event']['hash'][:12]}...")

        hr("3. ADVERSARIAL — agent แก้ board ตรงๆ เพื่อแกล้ง done (T-999)")
        bp = os.path.join(d, "CoreAiWorkspaces/02-task/task-board.md")
        txt = open(bp, encoding="utf-8").read()
        m = re.search(r"done:\s*\[([^\]]*)\]", txt)
        items = [x.strip() for x in m.group(1).split(",") if x.strip()] + ["T-999"]
        open(bp, "w", encoding="utf-8").write(txt[:m.start()] + "done: [" + ",".join(items) + "]" + txt[m.end():])
        a = audit_done(root=d, log="engine/events.log.jsonl")
        print(f"   board done = [{board_done(d)}]  (ดูเหมือน done)")
        print(f"   → audit: faked_done_no_event = {a['faked_done_no_event']}  ← จับได้! (ไม่มี signed event)")

        hr("4. risk-tiered Decision Inbox + audit chain")
        create_item("secret_scan", "-", 3, "secret detected", ts=3, **kw)
        print(f"   open inbox items: {[i['id'] + ' L' + str(i['risk_level']) for i in list_open(root=d, inbox='engine/inbox.jsonl')]}")
        resolve_item(di["id"], "rejected", by="user", ts=4, **kw)
        print(f"   user resolved {di['id']} = rejected (recorded)")
        ok, reason = verify_chain(root=d, log="engine/events.log.jsonl")
        print(f"   audit chain: {'INTACT' if ok else 'TAMPERED'} ({reason}) — ทุก decision ตรวจย้อนได้")

        hr("สรุป: agent ทำ done ปลอมไม่ได้เชิงโครงสร้าง · ทุกการตัดสิน audit ได้ · risk-tier กัน approval fatigue")
        print("  → นี่คือ governance-of-record ที่ per-run ของคู่แข่งทำไม่ได้ (ADR-013 paid layer)\n")


if __name__ == "__main__":
    main()
