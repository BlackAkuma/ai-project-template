# AI Bootstrap Master Template

เอกสารนี้เป็น instruction หลักสำหรับ AI ที่ต้อง setup โปรเจ็กต์ใหม่

## Purpose

เมื่อ AI อ่านเอกสารนี้แล้ว ต้องสามารถ:

- สร้างระบบเอกสารเริ่มต้นสำหรับโปรเจ็กต์ใหม่
- จัดโครงสร้างโฟลเดอร์ `doc/`
- วาง source docs แบบ versioned documents
- สร้างเอกสารปฏิบัติงาน เช่น plan, work status, task board, log index, way of work, coding standards
- ทำให้โปรเจ็กต์ใหม่มี baseline พร้อมสำหรับการพัฒนาต่อ

## Required Inputs

AI ควรพยายามหาหรือรับข้อมูลอย่างน้อยดังนี้:

- `<PROJECT_NAME>`
- `<PROJECT_ROOT_PATH>`
- `<CURRENT_DATE>`
- `<SOURCE_DOC_LIST>` รายการเอกสารต้นแบบที่มีอยู่
- `<CURRENT_SOURCE_VERSION>` เช่น `v0.1`
- `<PROJECT_GOAL_SUMMARY>` สรุปสั้นของโปรเจ็กต์

ถ้ายังไม่มี source docs:

- AI ต้องสร้างโครงเอกสารรองรับไว้ก่อน
- ต้องระบุชัดว่า source docs ยังไม่ถูกนำเข้า
- ต้องไม่แต่ง requirement เชิงผลิตภัณฑ์เองเกินข้อมูลที่มี

## Required Outputs

AI ต้องเตรียมอย่างน้อย:

- `doc/README.md`
- `doc/00-source/`
- `doc/00-source/versions/<CURRENT_SOURCE_VERSION>/`
- `doc/01-plan/project-plan.md`
- `doc/01-plan/work-status.md`
- `doc/02-task/task-board.md`
- `doc/03-log/work-log-index.md`
- `doc/04-way-of-work/way-of-work.md`
- `doc/04-way-of-work/coding-standards.md`
- `doc/04-way-of-work/ai-decision-protocol.md` (จาก `11-ai-decision-protocol-template.md`)
- `doc/04-way-of-work/compliance.md` (จาก `15-compliance-check-template.md`)
- `doc/05-summary/`
- `doc/06-extensions/`
- `doc/07-decisions/README.md` (ADR index จาก `12-adr-template.md`)
- `doc/07-decisions/entity-register.md` (จาก `17-entity-register-template.md`)

## Core Rules

- ห้ามให้เอกสารต่อยอดขัดกับ source docs
- ห้ามเขียนทับ source docs revision เดิมแบบเงียบ ๆ
- ถ้าความต้องการเปลี่ยน ต้องสร้าง source docs เวอร์ชันใหม่หรือ extension doc
- plan, status, task, log ต้องอ้างอิง source docs เวอร์ชันที่ใช้อยู่
- daily logs และ daily summaries อาจเป็น local working records และไม่จำเป็นต้องเก็บใน git
- เมื่อเจอสถานการณ์คลุมเครือหรือขัดแย้ง ให้ปฏิบัติตาม `doc/04-way-of-work/ai-decision-protocol.md`
- ก่อนตัดสินใจเชิง architecture ต้องอ่าน `doc/07-decisions/README.md` ก่อน
- ถ้ามี `~/ai-workspace/cross-project-memory.md` ให้อ่านก่อน bootstrap โปรเจ็กต์ใหม่
- Memory system overview: `19-memory-architecture-overview.md`

## AI Execution Steps

1. **ถามภาษา:** "เราจะสื่อสารกันเป็นภาษาอะไร?" — รอคำตอบก่อน บันทึกลง `way-of-work.md`
2. **ถามประเภทโปรเจ็กต์:** "โปรเจ็กต์นี้เป็นประเภทอะไร?" พร้อมตัวเลือก:
   - Software ทั่วไป (web app, API, tool, mobile app)
   - Game / Web Game (มีกลไก gameplay, physics, scoring)
   - อื่น ๆ (ระบุ)
3. **โหลด skill pack** ตามคำตอบ:
   - Game / Web Game → อ่าน `skills/game/` ทั้งหมดเพิ่มเติมจาก core → สร้าง `doc/08-design/` ด้วย
   - อื่น ๆ → ใช้ core เท่านั้น
   - **การตรวจสอบ session ถัดไป:** ถ้าโปรเจ็กต์มี `doc/08-design/` แปลว่าเป็น game project — โหลด game skill standards อัตโนมัติ
4. อ่าน source docs ที่มีอยู่
5. สร้าง `doc/` ตาม template folder structure (เพิ่ม `doc/08-design/` ถ้าเป็น game)
6. สร้าง source docs index และ version folders
7. วางเอกสารปฏิบัติงานตั้งต้นจาก core templates
8. ถ้าเป็น game → วาง game skill templates เพิ่มเติมใน `doc/04-way-of-work/` และ `doc/08-design/`
9. เติมข้อมูลเฉพาะโปรเจ็กต์ที่หาได้จริง ถ้าไม่พอใส่ placeholder ชัดเจน ห้ามเดา
10. สร้าง work status และ task board ที่สะท้อนสถานะเริ่มต้นจริง
11. จัดการ `.gitignore` — เพิ่ม `_template/` เข้าไปถ้ายังไม่มี (ป้องกัน commit template โดยไม่ตั้งใจ)
12. บันทึกสิ่งที่ setup ไปใน log index

## Placeholder Policy

ใช้ placeholder แบบนี้เมื่อยังไม่มีข้อมูล:

- `<PROJECT_NAME>`
- `<TEAM_NAME_OR_OWNER>`
- `<CURRENT_SOURCE_VERSION>`
- `<PROJECT_PHASE>`
- `<NEXT_REQUIRED_WORK>`

## What AI Must Not Do

- ไม่สร้าง requirement เชิงธุรกิจเองเกิน source docs
- ไม่เขียนทับเอกสารต้นแบบเดิมโดยไม่มีเวอร์ชันใหม่
- ไม่ประกาศว่างานเสร็จถ้ายังไม่มี status/log ที่รองรับ
- ไม่รวมของ domain-specific ของโปรเจ็กต์ก่อนหน้าเข้าไปในโปรเจ็กต์ใหม่
- ดู `14-anti-patterns-template.md` สำหรับรายการสิ่งที่ไม่ควรทำทั้งหมด

## Anti-Patterns Reference

สิ่งที่ไม่ควรทำสรุปไว้ใน `14-anti-patterns-template.md` แบ่งเป็น 5 หมวด:
1. Source Docs & Requirements
2. Session Discipline
3. การตัดสินใจ
4. Git & Version Control
5. Scope

## Retrospective

ทุก milestone หรืออย่างน้อยทุกเดือน ให้ทำ retrospective ตาม `13-retrospective-template.md`
เก็บไว้ใน `doc/05-summary/YYYY/`
