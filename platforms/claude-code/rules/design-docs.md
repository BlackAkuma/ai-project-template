---
globs: ["CoreAiWorkspaces/**/*"]
---

# Design Document Standards

Rules สำหรับไฟล์ทั้งหมดใน CoreAiWorkspaces/ — โหลดอัตโนมัติเมื่อแก้ไข documentation

## AI-CONTEXT Block

- ไฟล์ work-status, task-board, work-log-index **ต้องมี** AI-CONTEXT block ด้านบนสุด
- block และ body ต้องสะท้อนข้อมูลเดียวกัน (C-07)
- ถ้าแก้ body ต้องอัปเดต block ในครั้งเดียวกันเสมอ

## Source Docs (CoreAiWorkspaces/00-source/)

- ห้ามแก้ไขไฟล์ใน versions/ โดยตรง
- การเปลี่ยน requirement = สร้าง version ใหม่ใน versions/vX.X/
- ถ้าต้องเพิ่ม context: สร้าง extension doc ใน CoreAiWorkspaces/06-extensions/

## Placeholders

- ห้าม commit ไฟล์ที่มี `<PROJECT_NAME>`, `<CURRENT_DATE>`, `<NEEDS_CLARIFICATION>` ค้างอยู่
- placeholder ในไฟล์ที่ยังเป็น template (ยังไม่ได้ copy ไปใช้งาน) ไม่นับ

## FDD (CoreAiWorkspaces/08-design/) — Game Projects

- ทุก FDD ต้องมี status: Draft / Approved / Superseded
- task ออกจาก design_validate ได้เฉพาะเมื่อ FDD status = Approved
- FDD ที่ Superseded ต้องระบุ FDD ใหม่ที่แทนที่
