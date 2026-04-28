# Extension Document Template

คัดลอกและปรับไฟล์นี้เป็นเอกสารภายใต้ `doc/06-extensions/`

```md
# <EXTENSION_TITLE>

วันที่: <CURRENT_DATE>
สถานะ: Draft

## Reason

อธิบายว่าทำไมต้องมีเอกสารนี้ และสิ่งนี้ต่างจาก source docs เดิมอย่างไร

## Related Source References

- `doc/00-source/versions/<CURRENT_SOURCE_VERSION>/<SOURCE_DOC>.md`

## Description

อธิบายสิ่งที่เพิ่ม

## Impact

- กระทบแผนอย่างไร
- กระทบ task อะไร
- กระทบ data model / API / UX หรือไม่

## Required Updates

- `doc/01-plan/project-plan.md`
- `doc/01-plan/work-status.md`
- `doc/02-task/task-board.md`
```

---

## Reverse-Document Protocol

ใช้เมื่อ AI พบ code ที่ทำงานอยู่แล้วแต่ไม่มีเอกสารรองรับ เช่น พบ function ที่ implement logic ซับซ้อนแต่ไม่มี requirement หรือ design doc ใดอ้างถึง

### เมื่อไหร่ต้องทำ

- พบ code ที่ไม่มี task reference ใน task-board
- พบ logic ที่ไม่สอดคล้องกับ source docs ใด ๆ
- ถูกขอให้แก้ไข code ที่ไม่มีใครรู้ว่าทำอะไรอยู่

### ขั้นตอน

```
1. ห้ามแก้ไข code ที่ไม่เข้าใจก่อนทำ reverse-document
2. อ่าน code แล้วสรุปว่ามันทำอะไร (เขียนเป็น plain language)
3. สร้าง extension doc ใน doc/06-extensions/reverse-<ชื่อ>.md โดยใช้ template ด้านบน
   - Reason: "code นี้มีอยู่แล้วแต่ไม่มี documentation"
   - Description: สรุปสิ่งที่ code ทำ พร้อมอ้างอิง file:line
   - Impact: ไม่รู้ — ระบุ <NEEDS_CLARIFICATION: ต้องการ owner ยืนยัน>
4. สร้าง task ใน task-board แท็ก [REVERSE-DOC] รอ human review
5. อัปเดต work-status ว่าพบ undocumented code
6. รอ human confirm ก่อนแก้ไข code นั้น
```

### Template Reverse-Doc

```md
# Reverse-Doc: <ชื่อ module/function>

วันที่: <CURRENT_DATE>
สถานะ: Needs Review
ไฟล์: <path/to/file.ts:line>

## สิ่งที่ code ทำ (สรุปจากการอ่าน)

<อธิบาย logic ที่พบ>

## สิ่งที่ไม่ทราบ

- ทำไมถึงเขียนแบบนี้?
- มี requirement ใดอ้างถึงหรือไม่?
- ใครเป็น owner?

## Action Required

- [ ] Human ยืนยันว่า code นี้ยังต้องการอยู่
- [ ] ถ้าใช่: สร้าง source doc หรือ task reference
- [ ] ถ้าไม่: สร้าง task เพื่อ remove
```
