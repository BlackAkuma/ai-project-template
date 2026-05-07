# Project Plan Template

คัดลอกและปรับไฟล์นี้เป็น `ai/01-plan/project-plan.md`

```md
# Project Plan

สถานะ: Draft baseline
วันที่เริ่มใช้เอกสาร: <CURRENT_DATE>

## Source References

- `ai/00-source/versions/<CURRENT_SOURCE_VERSION>/<SOURCE_DOC_1>.md`
- `ai/00-source/versions/<CURRENT_SOURCE_VERSION>/<SOURCE_DOC_2>.md`

## Project Objective

สรุปเป้าหมายของ `<PROJECT_NAME>`

## Scope

สิ่งที่อยู่ในขอบเขต MVP:

- <ITEM>

สิ่งที่อยู่นอกขอบเขต MVP:

- <ITEM>

## Deliverables

- <ITEM>

## Milestones

| Milestone | Description | Source Reference | Status |
| --- | --- | --- | --- |
| M1 | <DESC> | <REF> | Pending |

## Risks and Assumptions

ความเสี่ยง:

- <RISK>

สมมติฐาน:

- <ASSUMPTION>

## Change Control

1. ถ้า scope ใหม่เกิน source docs ให้สร้าง extension doc หรือ source version ใหม่
2. อัปเดต `work-status` และ `task-board`
3. ลงรายละเอียดใน log และ summary

## Quality Gates

ก่อนประกาศว่า milestone เสร็จ ต้องผ่านเช็คลิสต์ต่อไปนี้:

**Verdict ที่ใช้:**
- `PASS` — ผ่านทุกข้อ ดำเนินต่อได้
- `CONCERNS` — มีข้อที่น่าเป็นห่วงแต่ไม่ blocking ให้บันทึกและระวัง
- `FAIL` — มีข้อที่ blocking ห้ามดำเนินต่อจนกว่าจะแก้ไข

### Gate ก่อนเริ่ม Milestone (Entry Gate)

- [ ] Source docs version ที่ใช้ระบุชัดเจนใน project-plan
- [ ] ทุก task ใน milestone นี้มี source reference
- [ ] ไม่มี task `blocked` ที่ยังไม่มี resolution plan
- [ ] ADR index ถูกอ่านและไม่มี decision ที่ขัดกับงานที่จะทำ

**Verdict Entry Gate:** `PASS` / `CONCERNS` / `FAIL`
ถ้า FAIL → ห้ามเริ่ม milestone จนกว่าจะแก้ข้อที่ fail

### Gate ก่อนปิด Milestone (Exit Gate)

- [ ] ทุก task ใน milestone เป็น `done` หรือมีเหตุผลชัดเจนว่าทำไมไม่ได้ทำ
- [ ] แต่ละ task ที่ `done` ผ่าน review และมี validation evidence
- [ ] ไม่มี task ค้างอยู่ที่ `design_validate` หรือ `in_progress`
- [ ] `work-status.md` สะท้อนสถานะหลัง milestone
- [ ] `work-log-index.md` มี entry ของ milestone นี้
- [ ] ถ้ามีการตัดสินใจ architecture — มี ADR รองรับ
- [ ] ไม่มี scope ที่เพิ่มโดยไม่มี source reference หรือ extension doc

**Verdict Exit Gate:** `PASS` / `CONCERNS` / `FAIL`
ถ้า FAIL → milestone ยังไม่ปิด ต้องแก้ก่อน
```
