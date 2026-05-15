# ADR (Architecture Decision Record) Template

เอกสารนี้กำหนดรูปแบบการบันทึก Architecture Decision Records สำหรับโปรเจ็กต์
ใช้เพื่อให้ session ถัดไป (ทั้งมนุษย์และ AI) เข้าใจว่า ทำไมถึงเลือก approach นั้น

---

## ส่วนที่ 1 — ADR Index (สำหรับ `CoreAiWorkspaces/07-decisions/README.md`)

นำ template ด้านล่างไปสร้างเป็น `CoreAiWorkspaces/07-decisions/README.md` ในโปรเจ็กต์

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

## ส่วนที่ 2 — ADR Individual File (สำหรับ `CoreAiWorkspaces/07-decisions/ADR-NNN-<title>.md`)

นำ template ด้านล่างไปสร้างเป็นไฟล์ ADR แต่ละรายการ
ตั้งชื่อไฟล์: `ADR-001-<decision-title-in-kebab-case>.md`

```markdown
# ADR-NNN: <ชื่อการตัดสินใจ>

**วันที่:** YYYY-MM-DD
**สถานะ:** Proposed / Accepted / Deprecated / Superseded by ADR-XXX
**ผู้เสนอ:** <ชื่อมนุษย์> หรือ "AI session — YYYY-MM-DD"
**Source Reference:** `CoreAiWorkspaces/00-source/versions/<VERSION>/<filename>.md`
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
2. เพิ่มรายการใน `CoreAiWorkspaces/07-decisions/README.md`
3. บันทึกใน work-log ว่าสร้าง ADR-NNN
4. **⛔ STOP — ห้าม implement จนกว่าผู้ใช้จะ Approve**
   - แจ้งผู้ใช้ว่า ADR-NNN อยู่ใน Proposed — รอ review
   - ไม่มี ADR ใน Proposed ที่ถูก implement โดยที่ผู้ใช้ไม่ได้ Approve ก่อน
   - "ทำต่อ" หรือ "ได้เลย" ที่พูดก่อนเห็น ADR ไม่นับเป็น approval
5. มนุษย์ review → เปลี่ยนสถานะเป็น Accepted หรือแจ้ง reject
6. **เมื่อ ADR ถูก Accept** → อัปเดต `CoreAiWorkspaces/07-decisions/entity-register.md` ทันที
   - ถ้าเป็น tech/integration ใหม่: เพิ่ม row ใน Active Entities พร้อม ADR reference
   - ถ้าเป็นการ deprecate tech เก่า: ย้าย row ไป Deprecated พร้อม `until` date
   - อัปเดต AI-CONTEXT block ของ entity-register ด้วย
6. Session ถัดไป: อ่าน ADR index ก่อนตัดสินใจ architecture

**เมื่อ human reject ADR (Proposed → Rejected):**

```
human บอกว่า ADR-NNN ไม่ได้รับการ approve

→ เปลี่ยนสถานะ ADR เป็น Rejected (ไม่ลบ — เก็บไว้เป็นประวัติว่าเคยพิจารณาแล้ว)
→ เพิ่ม section "เหตุผลที่ Reject" ใน ADR file:

## เหตุผลที่ Reject (เพิ่มเมื่อ reject)

**Rejected by:** <ชื่อ> on YYYY-MM-DD
**เหตุผล:** <สรุปสั้นว่าทำไมถึงไม่เลือก approach นี้>
**ทิศทางที่จะทำแทน:** <approach ที่จะใช้จริง>

→ อัปเดต ADR index ใน README.md เปลี่ยน Status เป็น Rejected
→ บันทึกใน work-log ว่า ADR-NNN ถูก reject และทิศทางที่จะใช้แทน
→ ถ้าต้องการ approach ใหม่: สร้าง ADR-NNN+1 ใหม่สำหรับ approach ที่ตัดสินใจแทน
→ task ที่รอ ADR นั้นอยู่: อัปเดตให้ ref ADR ใหม่ หรือ unblock ถ้าตัดสินใจไม่ต้องการ ADR
```

**ตัวอย่าง ADR ที่ถูก reject:**

```md
# ADR-004: ใช้ GraphQL แทน REST สำหรับ API

**วันที่:** 2026-04-20
**สถานะ:** Rejected
**ผู้เสนอ:** AI session — Claude Code

## Context
ต้องการ API ที่ flexible สำหรับ mobile client ที่มี data requirements ต่างกัน

## Options ที่พิจารณา
1. GraphQL — ยืดหยุ่น แต่ทีมไม่มี experience
2. REST with field filtering — ทำได้ใน REST ปกติ

## การตัดสินใจ (Proposed)
เสนอ GraphQL เพราะ flexibility

## เหตุผลที่ Reject

**Rejected by:** Beam on 2026-04-21
**เหตุผล:** ทีมไม่มี GraphQL experience, timeline ไม่เอื้อให้เรียนใหม่,
           REST + field filtering ตอบโจทย์ได้เพียงพอในขนาด project นี้
**ทิศทางที่จะทำแทน:** REST API พร้อม ?fields= parameter สำหรับ partial response
                       → ดู ADR-005
```
