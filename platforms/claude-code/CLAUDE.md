# CLAUDE.md — Project Bootstrap

ไฟล์นี้ถูกโหลดอัตโนมัติทุก session โดย Claude Code
แทน copy-paste prompt ที่ใช้กับ AI tool ทั่วไป

---

## Session Start Protocol

เมื่อเริ่ม session ใหม่ ให้ทำตามลำดับนี้:

1. อ่าน AI-CONTEXT block ของ `doc/01-plan/work-status.md`
2. อ่าน AI-CONTEXT block ของ `doc/03-log/work-log-index.md`
3. อ่าน AI-CONTEXT block ของ `doc/02-task/task-board.md`
4. ตรวจ gap ระหว่าง task board และ source docs (Scenario H ใน ai-decision-protocol.md)
5. รัน compliance scan อัตโนมัติ (ดู doc/04-way-of-work/compliance.md)
6. รายงานสถานะ: phase ปัจจุบัน, task ที่ active, สิ่งที่ต้องทำก่อน

## Project Context

- Source docs: `doc/00-source/`
- Work status: `doc/01-plan/work-status.md`
- Task board: `doc/02-task/task-board.md`
- Decision protocol: `doc/04-way-of-work/ai-decision-protocol.md`
- ADR index: `doc/07-decisions/README.md`

## Language Policy

- Internal reasoning: English (token-efficient)
- Output to user: ภาษาที่ตกลงกันไว้ใน `doc/04-way-of-work/way-of-work.md`
- AI-CONTEXT blocks: English เสมอ
- Code / identifiers: English เสมอ

## Key Rules

- ห้าม implement โดยไม่รู้ source reference
- ห้ามแก้ requirement โดยตรง — ต้อง version ใหม่หรือ extension doc
- ห้ามตัดสินใจเรื่อง architecture โดยไม่สร้าง ADR draft
- ทุก session ต้องอัปเดต work-status + work-log-index + task-board ก่อนจบ
- ถ้าไม่แน่ใจ: Do less, document more

## Skill Pack Detection

ถ้าโปรเจ็กต์มี `doc/08-design/` → โหลด game skill standards อัตโนมัติ:
- ทุก feature ใหม่ต้องมี FDD ก่อน implement
- task lifecycle: todo → design_validate → in_progress → playtest → review → done
- compliance rules G-01 ถึง G-07 และ A-01 ถึง A-04 บังคับใช้

## Available Slash Commands

```
/compliance-check   รัน compliance scan ทันที
/fdd-create         สร้าง FDD template สำหรับ feature ใหม่
/adr-create         สร้าง ADR สำหรับ architectural decision
/session-end        sync work-status + log + task-board ครบในคำสั่งเดียว
/scope-check        ตรวจ scope ของ task ปัจจุบัน
/launch-check       รัน launch checklist ก่อน deploy
/balance-check      รัน balance check สำหรับ game config (game projects)
/playtest-report    สร้าง playtest report template (game projects)
```
