# ADR (Architecture Decision Record) Template

เอกสารนี้กำหนดรูปแบบการบันทึก Architecture Decision Records สำหรับโปรเจ็กต์
ใช้เพื่อให้ session ถัดไป (ทั้งมนุษย์และ AI) เข้าใจว่า ทำไมถึงเลือก approach นั้น

---

## ส่วนที่ 1 — ADR Index (สำหรับ `doc/07-decisions/README.md`)

นำ template ด้านล่างไปสร้างเป็น `doc/07-decisions/README.md` ในโปรเจ็กต์

```markdown
# Decision Log — <PROJECT_NAME>

บันทึก architectural decisions ทั้งหมดของโปรเจ็กต์
ADR ที่ถูก accept แล้วถือเป็น source of truth สำหรับทิศทาง technical

## กฎการใช้งาน

- AI ทุก session ต้องอ่าน index นี้ก่อนทำการตัดสินใจเชิง architecture
- ห้ามลบ ADR — เปลี่ยนสถานะเป็น Deprecated หรือ Superseded แทน
- AI สามารถสร้าง ADR ในสถานะ Proposed ได้ — มนุษย์เป็นผู้ Approve

## Status ที่ใช้ได้

| Status | ความหมาย |
|--------|----------|
| Proposed | เสนอโดย AI หรือทีม รอการ approve |
| Accepted | ตัดสินใจแล้ว ใช้เป็นแนวทาง |
| Deprecated | ไม่ใช้แล้ว แต่ยังมีประวัติ |
| Superseded | ถูกแทนที่โดย ADR อื่น |

## Decision Log

| ID | Title | Status | Date | Supersedes |
|----|-------|--------|------|------------|
| [ADR-001](ADR-001-<title>.md) | <คำอธิบายสั้น> | Proposed | YYYY-MM-DD | — |
```

---

## ส่วนที่ 2 — ADR Individual File (สำหรับ `doc/07-decisions/ADR-NNN-<title>.md`)

นำ template ด้านล่างไปสร้างเป็นไฟล์ ADR แต่ละรายการ
ตั้งชื่อไฟล์: `ADR-001-<decision-title-in-kebab-case>.md`

```markdown
# ADR-NNN: <ชื่อการตัดสินใจ>

**วันที่:** YYYY-MM-DD
**สถานะ:** Proposed / Accepted / Deprecated / Superseded by ADR-XXX
**ผู้เสนอ:** <ชื่อมนุษย์> หรือ "AI session — YYYY-MM-DD"
**Source Reference:** `doc/00-source/versions/<VERSION>/<filename>.md`
**Related Tasks:** T-XXX, T-XXX

---

## Context

อธิบายสถานการณ์หรือปัญหาที่บังคับให้ต้องตัดสินใจ
มี constraint อะไรบ้าง? เกิดขึ้นในบริบทไหน?

## Options ที่พิจารณา

1. **Option A — <ชื่อ>**
   ข้อดี: ...
   ข้อเสีย: ...

2. **Option B — <ชื่อ>**
   ข้อดี: ...
   ข้อเสีย: ...

## การตัดสินใจ

เลือก **Option X** เพราะ...
(อธิบายเหตุผลหลักที่ทำให้เลือก option นี้)

## ผลที่ตามมา

- สิ่งที่ง่ายขึ้นเพราะการตัดสินใจนี้: ...
- สิ่งที่ยากขึ้นหรือมีข้อจำกัดเพิ่ม: ...
- สิ่งที่ต้องระวังต่อไป: ...

## Review Trigger (ถ้ามี)

ควรทบทวน ADR นี้ใหม่เมื่อ:
(เช่น "เมื่อ user base เกิน 10,000 คน", "เมื่อ migrate ไป microservices")
```

---

## กฎการใช้งาน ADR สำหรับ AI

**เมื่อใดต้องสร้าง ADR:**
- เลือก library หรือ framework ที่ไม่เคยใช้ในโปรเจ็กต์
- ตัดสินใจ architecture ที่ส่งผลต่อโครงสร้างใหญ่ (data model, API design, auth pattern)
- เลือก approach หนึ่งในสองทางที่มีเหตุผลทั้งคู่
- ตัดสินใจที่อาจถูก reverse ได้ง่ายหากไม่มีบันทึก

**เมื่อไม่ต้องสร้าง ADR:**
- การตัดสินใจระดับ implementation detail (ชื่อตัวแปร, formatting)
- งานที่ทำตามรูปแบบที่มี ADR อยู่แล้ว
- Bugfix ที่ไม่เปลี่ยน approach

**workflow:**
1. AI พบว่าต้องตัดสินใจเชิง architecture → สร้าง ADR ในสถานะ Proposed
2. เพิ่มรายการใน `doc/07-decisions/README.md`
3. บันทึกใน work-log ว่าสร้าง ADR-NNN
4. มนุษย์ review → เปลี่ยนสถานะเป็น Accepted หรือปรับ
5. Session ถัดไป: อ่าน ADR index ก่อนตัดสินใจ architecture
