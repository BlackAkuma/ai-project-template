# Engine — Hero Demo / Adversarial-Bypass Proof

> Soft-ship asset (ADR-011/ADR-013) — the credibility proof competitors can't cheaply copy.
> Lead message: **"Governed Project Memory — enforcement เหนือ AGENTS.md + durable project Decision Inbox"**

## ▶ Runnable (<10 min, reproducible, no live files touched)
```bash
python engine/demo.py     # end-to-end narrated: fake-done blocked → legit done+signed event
                          # → adversarial fake DETECTED → risk-tiered Inbox + audit chain intact
```
= the demand-harvest instrument (ADR-013 B): publish with OSS soft-ship + show design partners.

## What this proves
Governance ที่ **เครื่องบังคับเป็น state จริง** — ไม่ใช่ advisory ที่โมเดลจะข้ามก็ได้

## Demo 1 — gate ตรวจ state จริง (block half, live วันนี้)
```bash
# agent แกล้ง mark task done โดยไม่มีหลักฐาน → ถูกบล็อก
$ python engine/check.py task-close --task T-999
[FAIL] task_close_gate (risk L2, effect=decision-inbox)
  missing: entry_exists, status_equals, evidence_count_gte
  -> ปิด T-999 ไม่ได้ — ขาดหลักฐาน (Task Close Gate)

# secret ใน commit → hard-stop (L3)
$ python engine/check.py secret-scan     # ตรวจ git staged จริง
```
predicate ตรวจ git/file/test จริง — **ไม่เชื่อคำพูด agent** (presence not quality)

## Demo 2 — tamper-evidence (constitutive, P3-1)
```bash
# แก้ governed state ตรงๆ เพื่อ "แกล้งว่า done" → hash-chain ตรวจจับได้
$ python engine/test_events.py
  PASS  clean chain verifies
  PASS  tampered record DETECTED        # ← แก้ result เป็น FAKED → จับได้
  PASS  deleted/reordered event DETECTED
```
agent แก้ไฟล์ state เพื่อโกง → **chain แตก = ตรวจจับได้** (ยังไม่ใช่ full interception แต่คือ data-level constitutive)

## Demo 3 — gated mutation + faked-done detection (P3-2)
```bash
$ python engine/test_govern.py
  PASS  legit mark_done ok                          # ผ่าน gate → done + signed event
  PASS  missing-evidence mark_done blocked          # ไม่มีหลักฐาน → block → Decision Inbox
  PASS  ADVERSARIAL: faked T-999 (direct edit) DETECTED   # ← แกล้ง done ตรงๆ → audit จับได้
```
**ทางเดียวที่ legit ที่จะ mark done = ผ่าน gate (มีหลักฐาน) + บันทึก signed Event** · แก้ board ตรงๆ เพื่อโกง → audit เจอ done-without-event → **โกงไม่ได้เชิงโครงสร้าง**

## Risk-tiered (ไม่ใช่ uniform — กัน approval fatigue)
L0 triage(always) · L1 auto-log · L2 → Decision Inbox · L3 hard-stop · classification = Engine-determined

## Interop, ไม่แข่ง
enforcement layer **เหนือ** advisory AGENTS.md — consume ไม่ reinvent

## ⏳ Arriving (ไม่ headline จนกว่าจะ ship — BRD §9)
full tool-call interception (FS allowlist) · Decision Inbox UI · model-agnostic (LiteLLM) · multi-repo

---
*adversarial suite expandable (BRD §2: bypass blocked = 100% ของ maintained suite). Publish ก่อน loud launch (ADR-011).*
