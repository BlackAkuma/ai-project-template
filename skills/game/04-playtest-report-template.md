# Playtest Report Template

ใช้หลัง implement feature ใหม่ ก่อน task เข้า `review`
เก็บใน `CoreAiWorkspaces/08-design/playtest-[feature]-[date].md`

ผลของ playtest รายงานโดย AI ได้ (จากการทดสอบ logic) แต่ **feel และ fun factor** ต้องให้มนุษย์ยืนยัน

---

```md
# Playtest Report — [Feature Name]

วันที่: YYYY-MM-DD
FDD Reference: FDD-NNN
Task: T-XXX
ทดสอบโดย: [ชื่อ หรือ "AI session — YYYY-MM-DD"]
Platform: [Unity / Godot / Phaser / HTML5 / ฯลฯ]

---

## ผลการทดสอบ Functional

| สิ่งที่ทดสอบ | ผลที่คาดหวัง | ผลจริง | ผ่าน |
|-------------|-------------|--------|------|
| [กรณีทดสอบ] | [ผลที่ควรเกิด] | [ผลที่เกิดจริง] | ✓ / ✗ |

## ผลการทดสอบ Edge Cases

| กรณีพิเศษ | ผลที่คาดหวัง | ผลจริง | ผ่าน |
|----------|-------------|--------|------|
| [edge case จาก FDD ส่วนที่ 5] | [ผลที่ควรเกิด] | [ผลจริง] | ✓ / ✗ |

## Performance

| ตัวชี้วัด | Target (จาก FDD) | วัดได้ | ผ่าน |
|---------|-----------------|--------|------|
| FPS | [target] fps | [ค่าจริง] fps | ✓ / ✗ |
| ms per frame | < [X] ms | [ค่าจริง] ms | ✓ / ✗ |

## Feel & Experience (Human Playtest)

*ส่วนนี้ต้องให้มนุษย์กรอก — AI ไม่สามารถวัด feel ได้*

- ความรู้สึกที่ได้รับ: [ตื่นเต้น / ผ่อนคลาย / กดดัน / ฯลฯ]
- ตรงกับ FDD ส่วนที่ 2 หรือไม่: ใช่ / ไม่ใช่ → [อธิบาย]
- สิ่งที่รู้สึกดี:
- สิ่งที่ต้องปรับ:

## ปัญหาที่พบ

| ID | คำอธิบาย | ระดับ | Task |
|----|---------|-------|------|
| PL-001 | [คำอธิบาย bug/issue] | Critical / Major / Minor | T-XXX |

## สรุป

- [ ] Functional tests: ผ่านทั้งหมด
- [ ] Edge cases: ผ่านทั้งหมด
- [ ] Performance: อยู่ใน budget
- [ ] Human feel: ยืนยันแล้ว
- [ ] Critical/Major issues: ไม่มี (หรือมี task สร้างแล้ว)

**สถานะ:** Ready for Review / Needs Fix → [ระบุ task]
```

---

## เมื่อไหร่ Playtest ผ่าน

task ออกจาก `playtest` ได้เมื่อ:
- Functional ผ่านครบ
- ไม่มี Critical issue
- Human ยืนยัน feel แล้ว (ถ้า feature มี player-facing experience)
- Performance อยู่ใน budget ที่ FDD กำหนด
