# CLAUDE.md — Project Bootstrap

ไฟล์นี้ถูกโหลดอัตโนมัติทุก session โดย Claude Code
แทน copy-paste prompt ที่ใช้กับ AI tool ทั่วไป

---

## เริ่มต้น Session

**ก่อนทำอะไร** ตรวจว่า `doc/` มีอยู่ไหม:

- **ยังไม่มี** → ทำ **First Run Bootstrap** (ด้านล่าง)
- **มีแล้ว** → ทำ **Session Start Protocol** (ด้านล่าง)

---

## First Run Bootstrap

ทำครั้งเดียวตอนสร้างโปรเจ็กต์ใหม่:

1. ถามผู้ใช้ว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. ตรวจว่ามี `~/ai-workspace/cross-project-memory.md` ไหม — ถ้ามีให้อ่านก่อน เพื่อดู pattern และ lesson จากโปรเจ็กต์เก่า
3. อ่านไฟล์ใน `core/` ทั้งหมดตามลำดับ (00 → 18)
4. ถ้าโปรเจ็กต์เป็น game หรือ web game → อ่าน `skills/game/` ต่อด้วย (00 → 06)
5. สร้างโครงสร้าง `doc/` ตาม core/01 template
6. กรอกข้อมูลโปรเจ็กต์จาก context ที่มี — ใส่ placeholder ชัดเจนถ้าไม่พอ ห้ามเดา
7. เพิ่มโปรเจ็กต์นี้ลงใน Project Registry ของ `~/ai-workspace/cross-project-memory.md` (ถ้ามีไฟล์นั้นอยู่)
8. ตรวจสอบกับ `core/10-bootstrap-checklist-template.md` ก่อนประกาศว่าเสร็จ

จากนั้น → ทำ Session Start Protocol ต่อ

---

## Session Start Protocol

ทำตามลำดับนี้ทุก session:

1. อ่าน AI-CONTEXT block ของ `doc/01-plan/work-status.md`
2. อ่าน AI-CONTEXT block ของ `doc/03-log/work-log-index.md`
3. อ่าน AI-CONTEXT block ของ `doc/02-task/task-board.md`
4. ถ้า `doc/03-log/agents/claude-code.md` มีอยู่ → อ่าน AI-CONTEXT block ของไฟล์นั้นด้วย เพื่อรับ checkpoint ที่ Claude Code session ก่อนหน้าบันทึกไว้ *(ไฟล์นี้มีเฉพาะโปรเจ็กต์ที่ใช้ AI tool มากกว่า 1 ตัว)*
5. ถ้า work-status มี `read_more` field → แสดงให้ผู้ใช้เห็นว่าอ่านเพิ่มได้ที่ไหนถ้าต้องการ context เจาะจง
6. ตรวจ gap ระหว่าง task board และ source docs (Scenario H ใน `doc/04-way-of-work/ai-decision-protocol.md`)
7. รัน compliance scan อัตโนมัติ (ดู `doc/04-way-of-work/compliance.md`)
8. รายงานสถานะ: phase ปัจจุบัน, task ที่ active, สิ่งที่ต้องทำก่อน

---

## Session End Protocol

ก่อนจบ session ทุกครั้ง — รัน `/session-end` หรือทำตามลำดับ:

1. อัปเดต `work-status` — body **และ** AI-CONTEXT block
2. เพิ่ม entry ใน `work-log-index` — body **และ** AI-CONTEXT block
3. อัปเดต `task-board` — status **และ** AI-CONTEXT block (ถ้ามี task เปลี่ยน)
4. task ที่ยัง in_progress → mark เป็น `[IN_PROGRESS: checkpoint saved — <สิ่งที่ทำไปแล้ว>]`

**กฎ sync:** AI-CONTEXT block ต้องสะท้อน body เสมอ — ถ้าไม่ตรงให้เชื่อ body และอัปเดต block

---

## Context Window Management

**เมื่อ context ใกล้เต็ม — Pre-compact:**

1. บันทึก checkpoint ใน `work-log-index`: สรุปสิ่งที่ทำไปแล้วและหยุดตรงไหน
2. อัปเดต `work-status` ให้สะท้อนสถานะปัจจุบัน
3. mark task เป็น `[IN_PROGRESS: checkpoint saved — <สรุปสั้น>]`
4. บันทึก next action ที่ชัดเจน

**หลัง context ถูก compact — Post-compact:**

1. อ่าน AI-CONTEXT block ของ 3 ไฟล์หลัก + `doc/07-decisions/README.md`
2. ยืนยันว่า task ที่กำลังทำตรงกับ checkpoint ที่บันทึกไว้
3. ถ้าพบความไม่สอดคล้อง → ทำตาม Scenario B ใน `ai-decision-protocol.md`

---

## Project Context

- Source docs: `doc/00-source/`
- Work status: `doc/01-plan/work-status.md`
- Task board: `doc/02-task/task-board.md`
- Way of work: `doc/04-way-of-work/way-of-work.md`
- Decision protocol: `doc/04-way-of-work/ai-decision-protocol.md`
- Compliance rules: `doc/04-way-of-work/compliance.md`
- ADR index: `doc/07-decisions/README.md`

---

## Language Policy

- Internal reasoning: English (token-efficient)
- Output to user: ภาษาที่ตกลงกันไว้ใน `doc/04-way-of-work/way-of-work.md`
- AI-CONTEXT blocks: English เสมอ
- Code / identifiers: English เสมอ

---

## Key Rules

- ห้าม implement โดยไม่รู้ source reference
- ห้ามแก้ requirement โดยตรง — ต้อง version ใหม่หรือ extension doc
- ห้ามตัดสินใจเรื่อง architecture โดยไม่สร้าง ADR draft
- ทุก session ต้องทำ Session End Protocol ก่อนจบ
- ถ้าไม่แน่ใจ: Do less, document more
- เมื่อพบข้อมูลใหม่ที่ต้องเก็บ → ใช้ Memory Scope decision tree (Scenario K ใน `ai-decision-protocol.md`) ตัดสินว่าเก็บที่ไหน
- ห้ามเขียนลง `~/ai-workspace/cross-project-memory.md` โดยไม่ถามผู้ใช้ก่อน

---

## Skill Pack Detection

ถ้าโปรเจ็กต์มี `doc/08-design/` → โหลด game skill standards อัตโนมัติ (skills/game/ 00–06):
- ทุก feature ใหม่ต้องมี FDD ก่อน implement
- task lifecycle: todo → design_validate → in_progress → playtest → review → done
- compliance rules G-01 ถึง G-07 และ A-01 ถึง A-04 บังคับใช้

---

## Available Slash Commands

```
/compliance-check   รัน compliance scan ทันที
/fdd-create         สร้าง FDD template สำหรับ feature ใหม่
/adr-create         สร้าง ADR สำหรับ architectural decision
/session-end        sync work-status + log + task-board ครบในคำสั่งเดียว
/scope-check        ตรวจ scope ของ task ปัจจุบัน
/launch-check       รัน launch checklist ก่อน deploy
/archive-logs       compress session เก่าเป็น monthly archive
/balance-check      รัน balance check สำหรับ game config (game projects)
/playtest-report    สร้าง playtest report template (game projects)
```
