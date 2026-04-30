# /playtest-report

สร้าง playtest report template สำหรับ feature ที่อยู่ในขั้น `playtest`

**ใช้กับ:** game projects เท่านั้น (ต้องมี `doc/08-design/`)

---

## สิ่งที่ทำ

1. ตรวจ task board หา task ที่มีสถานะ `playtest`
2. อ่าน FDD ที่ task นั้นอ้างถึง — โดยเฉพาะส่วนที่ 8 (เกณฑ์การยืนยัน)
3. สร้าง report template พร้อม checklist จาก FDD ส่วนที่ 8
4. บันทึกไว้ใน `doc/08-design/playtest-<feature-name>-YYYY-MM-DD.md`

---

## Output Template

```markdown
# Playtest Report — <Feature Name>

**วันที่:** YYYY-MM-DD
**Tester:** <ชื่อ>
**FDD Reference:** FDD-NNN
**Task:** T-XXX
**Version:** <commit hash หรือ build version>
**Platform:** <platform ที่ทดสอบ>

---

## สภาพแวดล้อม

- OS / Browser: ...
- Resolution: ...
- Input: ...

---

## Checklist (จาก FDD ส่วนที่ 8)

- [ ] <เกณฑ์ข้อ 1 จาก FDD>
- [ ] <เกณฑ์ข้อ 2 จาก FDD>
- [ ] ประสิทธิภาพอยู่ใน budget ที่กำหนด (เป้า: X ms/frame, วัดได้: Y ms/frame)
- [ ] ทดสอบ edge cases ครบ

---

## สิ่งที่พบ

| # | คำอธิบาย | ระดับ (Critical/High/Low) | FDD Section ที่เกี่ยวข้อง |
|---|---------|--------------------------|--------------------------|
| 1 | ...     | ...                      | ...                      |

---

## สรุป

- [ ] PASS — feature พร้อมไป `review`
- [ ] FAIL — ต้องแก้ไขก่อน (ดู issues ด้านบน)

**หมายเหตุ:** ...
```

---

## หลังสร้าง Report

- ถ้า PASS → เปลี่ยน task เป็น `review` และอัปเดต work-status
- ถ้า FAIL → เปลี่ยน task กลับเป็น `in_progress` พร้อมระบุ issue ที่ต้องแก้ใน task description
- บันทึก link ของ report ใน task board

---

## Compliance Rule

ตรวจสอบตาม **G-05** (playtest before review) จาก `skills/game/02-game-coding-standards.md`
