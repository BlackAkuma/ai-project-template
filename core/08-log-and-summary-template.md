# Log and Summary Template

ใช้ไฟล์นี้เป็นแม่แบบสำหรับ:

- `CoreAiWorkspaces/03-log/work-log-index.md`
- `CoreAiWorkspaces/03-log/templates/daily-log-template.md`
- `CoreAiWorkspaces/05-summary/templates.md`

---

## Work Log Index Template

`work-log-index.md` เป็นไฟล์ที่ AI อ่านทุก session เพื่อรู้ว่า session ก่อนหน้าทำอะไรไปแล้ว
AI-CONTEXT block บันทึก snapshot ของ session ล่าสุดเท่านั้น — body เก็บประวัติทั้งหมด

**Field ที่ใช้ใน AI-CONTEXT:**

| Field | ความหมาย | ตัวอย่าง |
|-------|----------|---------|
| `last_session` | วันที่ของ session ล่าสุด | `2026-04-28` |
| `tool` | AI tool ที่ใช้ใน session ล่าสุด | `Claude Code` |
| `completed` | task ที่เสร็จใน session นั้น | `[T-001, T-002]` หรือ `none` |
| `checkpoint` | task ที่ค้างกลางคัน (ถ้ามี) | `T-003: finished auth logic, pending tests` หรือ `none` |
| `next_from_last` | งานที่ session นั้นแนะนำให้ทำต่อ | `T-003 T-004` |
| `notes` | สิ่งสำคัญที่ session ถัดไปควรรู้ (สั้น) | `ADR-002 created` หรือ `none` |
| `deep_context` | path ไปยัง history เพิ่มเติมถ้าต้องการ | `archive: CoreAiWorkspaces/03-log/archive/` หรือ `none` |

**กฎสำคัญ:** อัปเดต AI-CONTEXT ทุกครั้งที่เพิ่ม entry ใหม่ ให้สะท้อน session ล่าสุดเสมอ

---

## หลักการจัดการขนาดไฟล์ (Token Management)

`work-log-index.md` มีแนวโน้มโตเรื่อย ๆ ทุก session จนอ่านแพง — ใช้ระบบ **สองชั้น** เพื่อแก้ปัญหานี้:

```
Tier 1: Milestone Summary  ← ไม่เคย archive ย่อเสมอ AI อ่านตรงนี้เพื่อไม่ทำซ้ำ
Tier 2: Recent Sessions    ← เก็บแค่ 20 session ล่าสุด ที่เก่ากว่า archive ไป
```

### โครงสร้าง work-log-index.md ที่ถูกต้อง

```md
<!-- AI-CONTEXT ... -->

# Work Log Index — <PROJECT_NAME>

## Milestone Summary  ← อ่านอันนี้ก่อนเสมอ ไม่เคย archive

สรุปสิ่งที่ทำเสร็จถาวร milestone ต่าง ๆ:
- v0.1 (2026-01): setup โครงสร้าง, auth system (T-001–T-010)
- v0.2 (2026-02): payment integration (T-011–T-025)

## Recent Sessions  ← เก็บแค่ 20 session ล่าสุด

### 2026-04-28 — [Claude Code]
...

### 2026-04-27 — [Claude Code]
...
```

### Archive Folder

```
CoreAiWorkspaces/03-log/
  work-log-index.md          ← AI อ่านทุก session
  archive/
    2026-01-sessions.md      ← session เก่าถูก compress มาที่นี่
    2026-02-sessions.md
  YYYY/MM/
    YYYY-MM-DD-log.md        ← detail รายวัน (archive ได้ทั้งหมด)
```

### Threshold และการแจ้งเตือน

| สิ่งที่ตรวจ | Threshold | Action |
|-----------|-----------|--------|
| work-log-index.md | > 300 บรรทัด | C-12: AI แจ้ง แนะนำ archive |
| task-board done section | > 15 รายการ | C-13: AI แจ้ง แนะนำ archive |

เมื่อ AI พบ threshold เกิน — แจ้งผู้ใช้ก่อนทำงานอื่น:

```
[INFO] work-log-index มี 340 บรรทัด (threshold: 300)
       พิมพ์ "archive logs" หรือ /archive-logs เพื่อ compress session เก่า
       หรือ "ข้ามได้" ถ้าอยากทำงานต่อก่อน
```

ผู้ใช้ตัดสินใจเอง — AI ไม่ archive เองโดยไม่ถาม

### Archive Protocol (เมื่อผู้ใช้สั่ง)

```
1. อ่าน Recent Sessions ทั้งหมดที่จะ archive
2. เขียน monthly summary ไว้ใน CoreAiWorkspaces/03-log/archive/YYYY-MM-sessions.md
   (ต้องมี: งานที่เสร็จ, decisions ที่ทำ, สิ่งที่ยกไปต่อ)
3. อัปเดต Milestone Summary ใน work-log-index ให้ครอบคลุม session ที่ archive
4. ลบ session entry เก่าออกจาก Recent Sessions เหลือแค่ 10 ล่าสุด
5. แจ้งผู้ใช้ว่า archive สำเร็จ พร้อม path ของ archive file

กฎ: archive file ต้องอ่านแล้วเข้าใจได้ว่า "ช่วงนั้นทำอะไรไปแล้ว"
     เพื่อให้ AI ใหม่ที่ต้องการรายละเอียดสามารถกลับมาอ่านได้
```

### Task Board Archive Protocol

เมื่อ done section > 15 รายการ:

```
1. ย้าย task done ที่เก่ากว่า 30 วัน ไปที่ CoreAiWorkspaces/02-task/archive/done-YYYY-MM.md
2. เก็บ 5 รายการล่าสุดไว้ใน task-board เพื่อ context
3. อัปเดต AI-CONTEXT block ของ task-board
```

```md
<!-- AI-CONTEXT
last_session: <CURRENT_DATE>
tool: <AI_TOOL_NAME>
completed: [<TASK_IDS>] | none
checkpoint: <T-XXX: detail> | none
next_from_last: <T-XXX> <T-XXX>
notes: <SHORT_NOTE> | none
deep_context: archive: CoreAiWorkspaces/03-log/archive/ | none
-->

---

# Work Log Index — <PROJECT_NAME>

อัปเดตล่าสุด: <CURRENT_DATE>

## Entries

### <CURRENT_DATE> — [<AI_TOOL_NAME>]

- **สรุป session:** <SUMMARY>
- **Tasks:** `T-XXX` `T-XXX`
- **Validation:** <วิธีที่ใช้ตรวจสอบ>
- **ผลลัพธ์:** <RESULT>
- **Daily Log:** `CoreAiWorkspaces/03-log/YYYY/MM/YYYY-MM-DD-log.md`
```

---

## Daily Log Template

ไฟล์นี้ไม่มี AI-CONTEXT block เพราะ AI ไม่อ่านทุก session — อ่านเฉพาะเมื่อต้องการรายละเอียด

```md
# YYYY-MM-DD Log

วันที่: YYYY-MM-DD
ผู้บันทึก: <ชื่อ หรือ "AI session — Claude Code">

## Source References

- <REF>

## Work Sessions

### Session 1

เวลา:
สิ่งที่ทำ:
- <ITEM>

สิ่งที่เพิ่มหรือแก้:
- <ITEM>

การทดสอบ:
- <ITEM>

ผลการทดสอบ:
- <ITEM>

ปัญหาที่พบ:
- <ITEM>

งานคงค้าง:
- <ITEM>
```

---

## Daily Summary Template

```md
# YYYY-MM-DD Summary

วันที่: YYYY-MM-DD

## สรุป

- <ITEM>

## การทดสอบ

- <ITEM>

## ขั้นถัดไป

- <ITEM>

## Log อ้างอิง

- `CoreAiWorkspaces/03-log/YYYY/MM/YYYY-MM-DD-log.md`
```

---

## Monthly Summary Template

```md
# YYYY-MM Summary

เดือน: YYYY-MM

## ความคืบหน้าโดยรวม

- <ITEM>

## งานสำคัญที่เสร็จ

- <ITEM>

## งานที่ยกไปเดือนหน้า

- <ITEM>

## การตัดสินใจสำคัญ

- <ITEM>

## ความเสี่ยง

- <ITEM>
```

---

## ตัวอย่าง work-log-index.md แบบสองชั้นที่กรอกแล้ว

ตัวอย่างนี้แสดงโครงสร้างจริงที่ควรมีหลังใช้งานมาสัก 2–3 milestone
สังเกตว่า Milestone Summary สั้นและถาวร ส่วน Recent Sessions เก็บแค่ที่จำเป็น

```md
<!-- AI-CONTEXT
last_session: 2026-04-28
tool: Claude Code
completed: [T-018, T-019]
checkpoint: none
next_from_last: T-020 T-021
notes: ADR-003 created — เลือก Stripe over Paddle เพราะ SDK official ครบกว่า
deep_context: archive: CoreAiWorkspaces/03-log/archive/2026-02-sessions.md
-->

---

# Work Log Index — ShopFlow

อัปเดตล่าสุด: 2026-04-28

## Milestone Summary

สรุปสิ่งที่เสร็จถาวรแต่ละ milestone — อ่านก่อนเสมอ ไม่เคย archive

- **v0.1 (2026-02): Foundation** — setup โครงสร้าง, auth system JWT+refresh (T-001–T-008) ADR-001 accepted
- **v0.2 (2026-03): Product Catalog** — CRUD สินค้า, image upload S3, search basic (T-009–T-015) ADR-002 accepted
- **v0.3 (กำลังทำ): Payment** — Stripe integration (T-016–), ADR-003 proposed รอ accept

## Recent Sessions

### 2026-04-28 — [Claude Code]

- **สรุป session:** implement Stripe webhook handler และ idempotency logic
- **Tasks:** `T-018` (webhook handler — done) `T-019` (idempotency key — done)
- **Validation:** unit test ผ่าน 12/12, manual test กับ Stripe CLI ผ่าน
- **ผลลัพธ์:** webhook รับ event ได้ถูกต้อง, duplicate event ถูก reject
- **Daily Log:** `CoreAiWorkspaces/03-log/2026/04/2026-04-28-log.md`

### 2026-04-25 — [Claude Code]

- **สรุป session:** setup Stripe SDK และ checkout session creation
- **Tasks:** `T-016` (SDK setup — done) `T-017` (checkout session — done)
- **Validation:** sandbox payment flow ทำงานได้ end-to-end
- **ผลลัพธ์:** สร้าง payment session ได้ redirect ไป Stripe hosted page ถูกต้อง
- **Daily Log:** `CoreAiWorkspaces/03-log/2026/04/2026-04-25-log.md`

### 2026-04-20 — [Claude.ai]

- **สรุป session:** review payment architecture, propose ADR-003
- **Tasks:** `T-016` (design review) — สร้าง ADR-003 draft
- **Validation:** ADR-003 review โดย human — pending accept
- **ผลลัพธ์:** ตัดสินใจใช้ Stripe over Paddle เหตุผลใน ADR-003
- **Daily Log:** `CoreAiWorkspaces/03-log/2026/04/2026-04-20-log.md`
```

**กฎ Milestone Summary:**
- เขียนหนึ่งบรรทัดต่อ milestone — สั้น ครอบคลุม, ไม่ขยาย
- ระบุ version, เดือน, งานหลักที่เสร็จ, ADR ที่เกี่ยวข้อง
- milestone ที่กำลังทำใส่ "(กำลังทำ)" — อัปเดตเมื่อ close milestone

**กฎ Recent Sessions:**
- เก็บแค่ 20 entries — entry เก่ากว่านั้น archive ไปที่ `CoreAiWorkspaces/03-log/archive/`
- ทุก entry ต้องมี: สรุป session, tasks ที่ทำ, validation, ผลลัพธ์, link ไป daily log

---

## Agent Diary Template

ใช้เมื่อโปรเจ็กต์มี AI tool มากกว่า 1 ตัว เพื่อแยก log ต่อ tool ไม่ให้ปนกัน
สร้างไฟล์ `CoreAiWorkspaces/03-log/agents/<tool-name>.md` ต่อ tool ที่ใช้

**กฎ:**
- ไฟล์นี้ AI tool นั้น ๆ เป็นผู้เขียนเอง — ไม่ cross-write ระหว่าง tool
- work-log-index ยังคงเป็น master index รวมทุก tool
- ถ้าใช้ tool เดียว ไม่ต้องสร้าง agents/ folder

```md
<!-- AI-CONTEXT
agent: <AI_TOOL_NAME>
last_session: <CURRENT_DATE>
focus: <TASK_ID_OR_TOPIC>
checkpoint: <สิ่งที่ทำค้างไว้> | none
-->

---

# Agent Diary — <AI_TOOL_NAME>

## <CURRENT_DATE>

- **งานที่ทำ:** <สิ่งที่ทำใน session นี้>
- **decisions:** <การตัดสินใจที่ทำเอง พร้อมเหตุผลสั้น>
- **blocked:** <สิ่งที่ติดขัด> | none
- **next:** <สิ่งที่ต้องทำต่อใน session ถัดไป>
```

**ตัวอย่างที่กรอกแล้ว:**

```md
<!-- AI-CONTEXT
agent: Claude Code
last_session: 2026-04-29
focus: T-018
checkpoint: webhook handler done, pending idempotency test
-->

## 2026-04-29

- **งานที่ทำ:** implement Stripe webhook handler (T-018)
- **decisions:** ใช้ idempotency key แทน deduplication table — เบากว่า ไม่ต้อง migrate schema
- **blocked:** none
- **next:** เขียน test กับ Stripe sandbox ก่อน mark done
```
