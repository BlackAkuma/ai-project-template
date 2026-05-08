# Source Document Versioning Template

ใช้ template นี้เพื่อวางระบบ source docs ของโปรเจ็กต์

## Purpose

ทำให้ requirement, product docs, technical docs, และ architecture docs ถูกเก็บแบบมีประวัติ ไม่หายเมื่อมีการเปลี่ยนแปลง

## Rules

- source docs revision เดิมห้ามถูกเขียนทับแบบเงียบ ๆ
- revision จริงเก็บใต้ `CoreAiWorkspaces/00-source/versions/`
- ไฟล์ชื่อหลักใน `CoreAiWorkspaces/00-source/` เป็น pointer/index เท่านั้น
- planning docs ต้องอ้างอิง version ที่ใช้อยู่เสมอ

## Example Index File

```md
# PRD Index

## Current Version

- `v0.2`
- ไฟล์หลัก: `CoreAiWorkspaces/00-source/versions/v0.2/02-PRD.md`

## Previous Versions

- `v0.1`: `CoreAiWorkspaces/00-source/versions/v0.1/02-PRD.md`

## Version Note

- `v0.2` เพิ่ม requirement เรื่อง ...
```

## When To Create a New Source Version

- เปลี่ยน scope ของ MVP
- เปลี่ยน product flow หลัก
- เปลี่ยน data model หลัก
- เปลี่ยน architecture หลัก
- เปลี่ยน execution workflow หลัก
- เปลี่ยน acceptance criteria สำคัญ

## When To Use Extension Docs Instead

- รายละเอียดเพิ่มที่ยังไม่ต้องยกระดับเป็น source revision ใหม่
- feature idea ที่ยังอยู่ระหว่างสำรวจ
- design decision เฉพาะส่วนที่ยังไม่เปลี่ยน product truth ทั้งชุด
