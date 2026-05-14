# Task Board Template

คัดลอกและปรับไฟล์นี้เป็น `CoreAiWorkspaces/02-task/task-board.md`

**กฎสำคัญ:** เมื่อเปลี่ยน status ของ task ใด ต้องอัปเดต `AI-CONTEXT` block ด้านบนพร้อมกันเสมอ

---

## รูปแบบ AI-CONTEXT Block

**Field ที่ใช้:**

| Field | ความหมาย | ตัวอย่าง |
|-------|----------|---------|
| `active` | task ที่ยังไม่เสร็จ รูปแบบ `ID(status)` | `T-003(in_progress) T-004(todo)` |
| `blocked` | task ที่ติดขัด + เหตุผลสั้น | `T-005: needs API spec` หรือ `none` |
| `done` | ID ของ task ที่เสร็จแล้ว | `T-001 T-002` |
| `priority_next` | ID ของ task ที่ควรทำก่อน | `T-003` |
| `src` | source doc version | `v0.2` |
| `updated` | วันที่อัปเดตล่าสุด | `2026-04-28` |

Status ที่ใช้ได้: `todo` `design_validate` `in_progress` `review` `done` `blocked`

| Status | ความหมาย |
|--------|----------|
| `todo` | รอ pick up |
| `design_validate` | กำลังตรวจว่า scope/design ชัดพอก่อนเริ่มเขียนโค้ด |
| `in_progress` | ผ่าน design validate แล้ว กำลัง implement |
| `review` | implement เสร็จ รอตรวจสอบก่อนปิด |
| `done` | ผ่าน review แล้ว ปิดสมบูรณ์ |
| `blocked` | ติดขัด รอ input ภายนอก |

**กฎ lifecycle:** `todo → design_validate → in_progress → review → done`
ห้ามข้าม `design_validate` — ถ้า scope ชัดอยู่แล้วให้ผ่านทันทีและบันทึกว่า "scope clear, no changes needed"

---

## Definition of Ready (ก่อนย้ายเข้า `in_progress`)

task พร้อม implement เมื่อผ่านทุกข้อ:

- [ ] มี source reference ที่ชัดเจน (CoreAiWorkspaces/00-source/...)
- [ ] scope ระบุชัดว่าทำอะไร ไม่ทำอะไร
- [ ] ไม่มี dependency ที่ยังค้างอยู่
- [ ] ถ้าเป็น game feature: มี FDD ที่ approved แล้ว

ถ้าไม่ผ่านข้อใดข้อหนึ่ง → ให้อยู่ที่ `design_validate` และระบุสิ่งที่ขาดใน column หมายเหตุ

## Definition of Done (ก่อนย้ายเข้า `review`)

task เสร็จเมื่อผ่านทุกข้อ:

- [ ] งานตรงกับ scope ที่กำหนดใน design_validate
- [ ] compliance scan ผ่าน (ไม่มี Level 1 violation ค้าง)
- [ ] มีหลักฐาน validation (test pass / manual check / screenshot)
- [ ] อัปเดต work-status และ work-log แล้ว
- [ ] ถ้ามี REFACTOR-PENDING: สร้าง task ใน board แล้ว

ถ้าไม่ผ่านข้อใดข้อหนึ่ง → task ยังอยู่ที่ `in_progress` พร้อมบันทึกสิ่งที่ขาด

---

## Template ไฟล์จริง

```md
<!-- AI-CONTEXT
active: <T-XXX(status)> <T-XXX(status)>
blocked: <T-XXX: reason> | none
done: <T-XXX> <T-XXX>
priority_next: <T-XXX>
src: <CURRENT_SOURCE_VERSION>
updated: <CURRENT_DATE>
-->

---

# Task Board — <PROJECT_NAME>

อัปเดตล่าสุด: <CURRENT_DATE>

## กฎการใช้งาน

- ทุก task ต้องมี source reference
- สถานะที่ใช้: `todo` `design_validate` `in_progress` `review` `done` `blocked`
- ถ้า task ทำให้ scope เปลี่ยน ต้องสร้าง extension doc หรือ source version ใหม่
- task ที่พบโดยไม่ได้วางแผน ให้แท็ก `[FOUND-IN-PASSING]`

## งานปัจจุบัน

| ID | Task | ประเภท | Source Reference | Priority | Status | หมายเหตุ |
|----|------|--------|-----------------|----------|--------|---------|
| T-001 | <ชื่องาน> | <feature/bug/chore> | <REF> | High | todo | <หมายเหตุ> |

## งานที่ติดขัด

| ID | Task | เหตุผล | รอจาก | หมายเหตุ |
|----|------|--------|-------|---------|
| - | - | - | - | ไม่มี blocker ปัจจุบัน |

## งานที่เสร็จแล้ว

| ID | Task | ปิดเมื่อ | หลักฐาน |
|----|------|---------|--------|
| T-000 | <ชื่องาน> | <DATE> | <หลักฐานการ validate> |
```

---

## ตัวอย่าง AI-CONTEXT ที่กรอกแล้ว

```
<!-- AI-CONTEXT
active: T-003(in_progress) T-004(todo) T-005(todo)
blocked: none
done: T-001 T-002
priority_next: T-003
src: v0.2
updated: 2026-04-28
-->
```
