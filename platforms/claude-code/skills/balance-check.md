# /balance-check

ตรวจสอบ balance config values ทั้งหมดในโปรเจ็กต์ว่าอยู่ใน range ที่ FDD กำหนดไว้

**ใช้กับ:** game projects เท่านั้น (ต้องมี `doc/08-design/`)

---

## สิ่งที่ทำ

1. อ่าน FDD ทุกไฟล์ใน `doc/08-design/` ที่มีสถานะ Approved
2. รวบรวม config keys และ range ที่ FDD กำหนด (ส่วนที่ 4 ของแต่ละ FDD)
3. อ่าน config files ที่ระบุไว้ (เช่น `gameplay.json`, `balance.json`)
4. ตรวจแต่ละค่าว่าอยู่ใน range ที่ยอมรับได้หรือไม่
5. รายงานผล

---

## Output Format

```
Balance Check — <PROJECT_NAME>
Date: YYYY-MM-DD

Checking FDD-001: <feature name>
  [PASS] player.speed = 5.0 (range: 1.0–20.0)
  [FAIL] player.jumpForce = 30.0 (range: 5.0–25.0) ← เกิน max
  [WARN] levelScale = 0.5 (range: 0.1–2.0) ← ใกล้ min

Summary: X PASS | Y FAIL | Z WARN
```

---

## Compliance Rule

ตรวจสอบตาม **G-07** (balance check ก่อน playtest) จาก `skills/game/05-balance-check-template.md`

ถ้ามี FAIL → อัปเดต work-status เป็น `[BLOCKED: balance out of range]` และอย่าเปลี่ยน task จาก `in_progress` ไป `playtest` จนกว่าจะแก้ไขค่าให้อยู่ใน range

---

## กรณีที่ไม่สามารถรันได้

- ไม่มี `doc/08-design/` → แจ้งว่า project นี้ไม่ใช่ game project
- FDD ทั้งหมดเป็น Draft → แจ้งว่าไม่มี Approved FDD ให้ตรวจ
- Config file ไม่มีอยู่ → แจ้ง path ที่หา แล้ว mark เป็น `[WARN: config not found]`
