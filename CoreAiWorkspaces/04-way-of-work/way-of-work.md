# Way of Work — ai-project-template

## ภาษา

- สื่อสารกัน: **ภาษาไทย**
- Internal reasoning (AI): English (token-efficient)
- Code / identifiers / comments: English
- AI-CONTEXT blocks: English เสมอ

## Project Type

template system — ระบบ template สำหรับ AI-human collaboration ในโปรเจ็กต์ software

## บทบาทและความรับผิดชอบ

| บทบาท | ทำ | ไม่ทำ |
|--------|-----|-------|
| AI (Claude Code) | ออกแบบ template, เขียนเนื้อหา, เขียน tests, refactor | ตัดสินใจทิศทาง product โดยลำพัง |
| ผู้ใช้ | กำหนดทิศทาง, approve design decisions, test ด้วยโปรเจ็กต์จริง | — |

## Session Protocol

ใช้ ai-project-template session protocol (core/00):

**Session Start:**
1. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/01-plan/work-status.md`
2. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/03-log/work-log-index.md`
3. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/02-task/task-board.md`
4. ตรวจ branch ปัจจุบัน — ทำงานบน `dev` เท่านั้น ห้าม commit ตรงไปที่ `master`
5. รัน compliance scan

**Session End:**
- รัน `/caw-session-end` หรือ Session End Protocol ด้วยมือ
- Push ไปที่ `dev` branch

## Git Workflow

- **dev** — branch หลักสำหรับการพัฒนา — ทำงานที่นี่เท่านั้น
- **master** — stable release เท่านั้น — ห้าม commit หรือ merge โดยตรงโดยไม่ผ่านขั้นตอนด้านล่าง
- **gh-pages** — web pages เท่านั้น (how-it-works.html, workflow-diagram.html)
- Feature branches — ตั้งชื่อตาม `feat/`, `fix/`, `refactor/`, `test/`

### ขั้นตอน Merge dev → master (ห้ามข้าม)

AI ต้องทำตามลำดับนี้ก่อน merge ทุกครั้ง:

1. **สรุปสิ่งที่จะขึ้น master** ให้ครบก่อน:
   - ไฟล์ที่เปลี่ยน + สิ่งที่เปลี่ยน
   - tests ผ่านกี่/กี่
   - version ที่จะ release
   - ไฟล์ที่จะ **ไม่** ขึ้น (เช่น CoreAiWorkspaces/)
2. **รอผู้ใช้อนุมัติ** — ต้องได้รับคำยืนยันชัดเจน
3. **merge + push** — เมื่อได้รับอนุมัติแล้วเท่านั้น
4. **รายงานผล** — บอกว่าขึ้นสำเร็จ branch ไหน commit hash อะไร

**ห้าม:** จู่ๆ merge master โดยไม่สรุปงานก่อน ไม่ว่าบริบทจะชัดแค่ไหน

## กฎพิเศษสำหรับโปรเจ็กต์นี้

- "Template ต้องใช้ระบบตัวเอง" — ทุก session ต้องทำตาม protocol ที่เราสร้างไว้
- บอก plan ก่อนเขียน code/template เสมอ — รอ confirm ก่อน implement
- การเปลี่ยนแปลง core/ ต้องสร้าง ADR ก่อน

## Compliance Status

สถานะ: active
อ้างอิง: `CoreAiWorkspaces/04-way-of-work/compliance.md`
