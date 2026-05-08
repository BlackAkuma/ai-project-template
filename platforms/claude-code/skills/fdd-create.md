# /fdd-create

สร้าง Feature Design Document ใหม่จาก template
บันทึกใน `CoreAiWorkspaces/08-design/[feature-name].md`

## วิธีใช้

```
/fdd-create
/fdd-create "ชื่อ feature"
```

## สิ่งที่ทำ

1. ถามชื่อ feature (ถ้าไม่ได้ระบุ)
2. ดู FDD index ใน `CoreAiWorkspaces/08-design/README.md` เพื่อหา ID ถัดไป (FDD-NNN)
3. สร้างไฟล์ `CoreAiWorkspaces/08-design/[feature-name].md` จาก template ใน `skills/game/01-fdd-template.md`
4. กรอก: FDD ID, ชื่อ, วันที่, task reference (ถ้ามี)
5. เขียนส่วนที่ 1 ก่อน รอ approve ก่อนไปส่วนถัดไป (ตาม FDD protocol)
6. อัปเดต FDD index ใน `CoreAiWorkspaces/08-design/README.md`

## หมายเหตุ

- FDD ต้องได้รับ approve ก่อน task จะออกจาก design_validate
- เขียนทีละ section รอ approve ก่อนเสมอ — ห้ามเขียนครบทีเดียว
