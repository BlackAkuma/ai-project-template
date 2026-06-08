# Compliance Check Template

Protocol สำหรับตรวจสอบ code quality และ documentation standards อัตโนมัติ
ทำงานทุกครั้งที่ AI รับงานจากคนอื่น จนกว่าจะสั่ง `pause compliance`

---

## คำสั่ง Control

| คำสั่ง | ผล |
|--------|-----|
| *(ไม่มีคำสั่ง)* | scan อัตโนมัติทุก session |
| `pause compliance` | หยุด scan ชั่วคราว session นี้ |
| `resume compliance` | เปิด scan กลับ |
| `scan` | scan ทันที ออก report ทั้งหมด |
| `scan refactor` | เฉพาะ REFACTOR-PENDING ทั้งโปรเจ็กต์ |

## การบันทึก Compliance Status

เพิ่มบรรทัดนี้ใน `CoreAiWorkspaces/04-way-of-work/way-of-work.md` ของโปรเจ็กต์ เพื่อให้ AI ทุก session รู้สถานะปัจจุบัน:

```
## Compliance Status

สถานะ: active | paused
เหตุผล (ถ้า paused): <เหตุผล เช่น "spike session — ทดลอง approach ใหม่">
```

**กฎ:** ถ้า compliance ถูก pause ไว้ → AI session ถัดไปต้องเห็นสถานะนี้ก่อนเริ่มทำงาน และถามผู้ใช้ว่าจะ resume หรือยัง

---

## สิ่งที่ตรวจ

### ⛔ Task Close Gate — ต้องผ่านก่อนปิด task เป็น DONE เสมอ

ก่อน mark task ใด ๆ เป็น `done` ต้องมีครบทั้ง 3 ข้อนี้ก่อน — ขาดข้อใดข้อหนึ่งไม่ได้:

| # | เงื่อนไข | วิธีตรวจ |
|---|---------|---------|
| 1 | work-log มี entry สำหรับ task นี้ | grep task ID ใน work-log-index.md |
| 2 | task-board อัปเดต status แล้ว | ตรวจ status ใน task-board.md |
| 3 | validation evidence ระบุไว้ (code tasks) | work-log บอกว่าตรวจสอบอย่างไร — test ผ่าน, ทดสอบ scenario ใด |

→ ถ้าขาดข้อใด: ห้ามปิด — mark เป็น `[IN_PROGRESS: pending close — <ระบุว่าขาดอะไร>]`
→ non-code task (เช่น doc update, ADR draft): ข้อ 3 ใช้ "human reviewed" หรือ "no code changed" แทน

---

### ระดับ 1 — Fix Now หรือ Defer (ต้องตัดสินใจ)

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| C-01 | File size | > 500 บรรทัด |
| C-02 | Task ไม่มี source reference | ทุก task ที่ไม่มี `CoreAiWorkspaces/00-source/...` |
| C-03 | Task `done` ไม่มี validation evidence | ไม่มีบันทึกว่าตรวจสอบอย่างไร — ดู Task Close Gate ด้านบน |
| C-04 | Placeholder ยังค้างในไฟล์ | `<PROJECT_NAME>`, `<NEEDS_CLARIFICATION>` ฯลฯ |

### ระดับ 2 — Defer เสมอ พร้อม tag ในโค้ด

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| C-05 | Function/method ยาวเกิน | > 50 บรรทัด |
| C-06 | Dependency ใหม่ ไม่มี ADR | import ที่ไม่เคยมีในโปรเจ็กต์ |
| C-07 | block ≠ body mismatch | **enforceable-state → block authoritative** (ADR-007 dual-authority); narrative → body; regenerate view on drift *(เดิม "เชื่อ body" superseded, T-053)* |
| C-08 | TODO / FIXME ไม่มี task reference | comment ที่ไม่มี T-XXX กำกับ |

### ระดับ 3 — แจ้งเตือนอย่างเดียว

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| C-09 | work-status ไม่ได้อัปเดตนานเกิน | มี task `in_progress` แต่ไม่อัปเดต > 3 วัน |
| C-10 | Session ก่อนไม่มี log entry | work-log-index ไม่มีบันทึก session ล่าสุด |
| C-11 | Security baseline ไม่ผ่าน | ดูรายการตรวจด้านล่าง |
| C-12 | work-log-index ใหญ่เกิน | > 300 บรรทัด — แนะนำ archive |
| C-13 | task-board done section ใหญ่เกิน | > 15 รายการ — แนะนำ archive |
| C-14 | entity-register ไม่ได้อัปเดตเมื่อ tech เปลี่ยน | task ที่ deprecated/เพิ่ม tech ใหม่ แต่ entity-register ไม่เปลี่ยน |

> **C-15–C-19 = reserved (ยังไม่ใช้)** — compliance code ถัดไปคือ C-20–C-22 ใน `core/19` (memory architecture)
> ⚠️ `tests/audit/run-audit.sh` ใช้ label "C-15".."C-19" เป็น *test-assertion ID* (คนละ namespace) → ควร rename เป็น prefix อื่น (task T-044b)

---

---

## Security Baseline (C-11)

ตรวจทุก session เมื่อมีการแก้ไข code — แจ้งเตือนทันทีถ้าพบ:

| ประเด็น | สิ่งที่ตรวจ |
|--------|-----------|
| Hardcoded secrets | API key, password, token ใน code หรือ config ที่ไม่ได้ encrypt |
| SQL injection | query ที่ต่อ string ตรงโดยไม่ใช้ parameterized query |
| XSS | render HTML จาก user input โดยไม่ sanitize |
| Insecure direct object reference | ใช้ user-supplied ID โดยไม่ตรวจ ownership |
| Sensitive data ใน log | log ที่มี password, token, PII |
| Dependency ที่รู้ว่ามี vulnerability | package version ที่มี CVE ที่ทราบ |

ถ้าพบ C-11 → **Fix ทันที** ก่อนดำเนินงานต่อ ไม่ defer

---

## Tech Debt Register

ใช้ติดตาม REFACTOR-PENDING ทั้งหมดในโปรเจ็กต์
เก็บไว้ใน `CoreAiWorkspaces/05-tech-debt/debt-register.md`

```md
# Tech Debt Register

| ID | Code | ไฟล์ | คำอธิบาย | Task | Priority | เพิ่มเมื่อ |
|----|------|------|---------|------|----------|-----------|
| TD-001 | C-01 | src/game/player.ts | file too long (820 lines) | T-042 | Medium | 2026-04-28 |
| TD-002 | G-01 | src/enemy/ai.ts | hardcoded speed value 3.5 | T-043 | High | 2026-04-28 |
```

**Priority:**
- High — กระทบ behavior หรือ maintainability อย่างชัดเจน
- Medium — ควรแก้ใน milestone ถัดไป
- Low — แก้เมื่อผ่านมา ไม่เร่งด่วน

**กฎ:** task ทุก task ที่ `done` ต้องตรวจก่อนว่ามี REFACTOR-PENDING ค้างอยู่ไหม ถ้ามีต้องมี entry ใน debt register

---

## Violation Tag Format

ใส่ใน code comment เมื่อ defer:

```
// REFACTOR-PENDING[C-01]: file too long (850 lines), needs splitting — T-042
// REFACTOR-PENDING[C-05]: function too long (80 lines) — T-043
// REFACTOR-PENDING[C-06]: new lib introduced, ADR needed — T-044
// REFACTOR-PENDING[C-08]: TODO without task reference — T-045
```

รูปแบบ: `// REFACTOR-PENDING[C-XX]: <คำอธิบาย> — <T-XXX>`

---

## Report Format

เมื่อ scan เสร็จ AI ต้อง output ในรูปแบบนี้:

```
=== Compliance Report — YYYY-MM-DD ===

LEVEL 1 (Fix or Defer):
  [C-01] src/game/player.ts — 820 lines (limit: 500)
  [C-03] T-012 marked done — no validation evidence

LEVEL 2 (Defer):
  [C-05] src/ui/hud.ts:GameHUD.render() — 72 lines
  [C-06] import 'three.js' in src/scene.ts — no ADR found

LEVEL 3 (Notice):
  [C-09] T-008 in_progress — work-status not updated for 4 days

Action required:
  - Fix or create REFACTOR-PENDING tasks for Level 1 items
  - Create REFACTOR-PENDING tasks for Level 2 items
  - Note Level 3 items in work-log
```

---

### C-12 / C-13 — Archive Notification Format

เมื่อพบ C-12 หรือ C-13 ให้แจ้งผู้ใช้ก่อนทำงานอื่น รูปแบบ:

```
[INFO] C-12: work-log-index มี 340 บรรทัด (threshold: 300)
       ไฟล์กำลังโตขึ้นเรื่อย ๆ — อาจทำให้ session ถัดไปใช้ token มากขึ้น
       ตัวเลือก:
         "archive logs"  → AI compress session เก่าเป็น monthly summary
         "ข้ามได้"       → ทำงานต่อ ไม่ archive ตอนนี้
```

**กฎ:** AI ไม่ archive โดยไม่ได้รับคำสั่ง — ผู้ใช้ตัดสินใจเสมอ

---

## กฎการตัดสินใจ Fix vs Defer

**Fix ทันที เมื่อ:**
- เป็น task ที่กำลังทำอยู่อยู่แล้ว (ไม่มี extra cost)
- แก้ใช้เวลา < 30 นาที
- มีผลต่อ correctness ไม่ใช่แค่ cleanliness

**Defer เมื่อ:**
- ไม่ใช่ scope ของ task ปัจจุบัน
- ต้องใช้เวลามากกว่า 30 นาที
- เป็นเรื่อง refactor ล้วน ๆ ไม่มีผลต่อ behavior

เมื่อ defer → สร้าง task T-XXX ใน task-board ทันที แท็ก `[COMPLIANCE-DEFER]`
