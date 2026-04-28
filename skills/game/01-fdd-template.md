# Feature Design Document (FDD) Template

ใช้ก่อนเริ่ม implement game feature ใหม่ทุกครั้ง
เก็บใน `doc/08-design/[feature-name].md`

FDD ต้องอยู่ใน `design_validate` และได้รับ approve ก่อน task จะไป `in_progress`

---

## กฎ Incremental Approval

เมื่อ AI เขียน FDD ให้เขียนและบันทึกทีละ section แล้วรอ approve ก่อนเขียน section ถัดไป
ห้ามเขียนทั้ง 8 section แล้วค่อย approve ทีเดียว — ป้องกันงานหายเมื่อ context เต็ม

---

## Template

```md
# FDD: [ชื่อ Feature]

**วันที่:** YYYY-MM-DD
**สถานะ:** Draft / Approved / Superseded
**ผู้เขียน:** [ชื่อ หรือ "AI session — YYYY-MM-DD"]
**Task Reference:** T-XXX
**Source Reference:** doc/00-source/versions/vX.X/...
**Platform:** [Unity / Godot / Phaser / HTML5 / ฯลฯ]

---

## 1. Overview

อธิบายสั้น ๆ ว่า feature นี้คืออะไร และทำไมต้องมี
ใครใช้ feature นี้? ใช้ตอนไหนในเกม?

<!-- APPROVE SECTION 1 BEFORE CONTINUING -->

---

## 2. Player / User Experience

อธิบาย feel และ flow จากมุมมองผู้เล่น:
- ผู้เล่นเห็น/ได้ยิน/รู้สึกอะไร?
- ขั้นตอนที่ผู้เล่นทำ (input → feedback → outcome)
- ความรู้สึกที่ต้องการ (satisfying, tense, calm ฯลฯ)

<!-- APPROVE SECTION 2 BEFORE CONTINUING -->

---

## 3. Mechanics & Rules

กฎและกลไกที่แน่นอน:
- อธิบายทุก state ที่เป็นไปได้
- อธิบาย transitions ระหว่าง state
- กฎที่ชัดเจน (ถ้า X แล้ว Y)

<!-- APPROVE SECTION 3 BEFORE CONTINUING -->

---

## 4. Formulas & Parameters

ค่าตัวเลขและสูตรทั้งหมด — ต้องมาจาก config ห้าม hardcode:

```
// ตัวอย่าง
player_speed: 5.0          // units/second (config: gameplay.json)
jump_force: 10.0           // units (config: gameplay.json)
damage_formula: base * (1 + level * 0.1)
```

Parameter ทุกตัวต้องระบุ:
- ชื่อ config key
- ไฟล์ config ที่อยู่
- ค่า default และ range ที่ยอมรับได้

<!-- APPROVE SECTION 4 BEFORE CONTINUING -->

---

## 5. Edge Cases & Failure States

สิ่งที่อาจผิดพลาดและวิธีจัดการ:
- ถ้าผู้เล่นทำ X ในสถานะ Y → เกิดอะไร?
- ค่า boundary ที่ต้องระวัง (min, max, overflow)
- Network/async edge cases (ถ้าเกี่ยวข้อง)

<!-- APPROVE SECTION 5 BEFORE CONTINUING -->

---

## 6. Dependencies

- Feature อื่นที่ feature นี้ต้องอาศัย
- System ที่ feature นี้ส่งผลกระทบ
- ลำดับ implementation ที่แนะนำ

<!-- APPROVE SECTION 6 BEFORE CONTINUING -->

---

## 7. Performance Considerations

- Target FPS: [60 / 30 / ฯลฯ]
- Budget สำหรับ feature นี้: < X ms per frame
- Memory: [ถ้าเกี่ยวข้อง]
- ข้อควรระวังเฉพาะ platform: [mobile / web / desktop]
- สิ่งที่ต้อง profile หลัง implement

<!-- APPROVE SECTION 7 BEFORE CONTINUING -->

---

## 8. Acceptance Criteria

เกณฑ์ที่บอกว่า feature นี้ "เสร็จ":
- [ ] [พฤติกรรมที่ต้องเกิดขึ้น]
- [ ] [ค่าที่ต้องวัดได้]
- [ ] [edge case ที่ต้องผ่าน]
- [ ] Performance อยู่ใน budget ที่กำหนด
- [ ] ทดสอบบน platform เป้าหมายแล้ว

<!-- ALL 8 SECTIONS APPROVED — FDD COMPLETE -->
```

---

## FDD Index (สำหรับ `doc/08-design/README.md`)

```md
# Design Documents Index — <PROJECT_NAME>

| Feature | File | Status | Task | Updated |
|---------|------|--------|------|---------|
| [ชื่อ feature] | [feature-name.md] | Draft/Approved | T-XXX | YYYY-MM-DD |
```
