# /compliance-check

รัน compliance scan ทันที ออก report ตาม core/15 format

## วิธีใช้

```
/compliance-check
/compliance-check src/game/player.ts    ← scan เฉพาะไฟล์
/compliance-check --refactor-only       ← แสดงเฉพาะ REFACTOR-PENDING
/compliance-check --security-only       ← แสดงเฉพาะ C-11
```

## สิ่งที่ทำ

1. Scan code files ทั้งหมดตาม C-01 ถึง C-11
2. ถ้าเป็น game project: scan G-01 ถึง G-07 และ A-01 ถึง A-04 ด้วย
3. Output report format ตาม core/15-compliance-check-template.md
4. สำหรับ Level 1 violations: ถาม fix now หรือ create REFACTOR-PENDING task
5. สำหรับ C-11 (security): แจ้งเตือนทันทีและ block จนกว่าจะแก้
