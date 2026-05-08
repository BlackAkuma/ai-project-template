---
title: ADR System — บันทึก Architectural Decisions
---

# ADR System

Architecture Decision Records (ADR) — ระบบบันทึก "ทำไม" ของทุก architectural decision เพื่อให้ session ต่อไปไม่ย้อนกลับมาถกเถียงเรื่องเดิม

→ [หน้าหลัก](../index.md)

---

## ปัญหาที่ ADR แก้

ทีมและ AI มักเผชิญกับ:

- **"ทำไมถึงเลือก X?"** — ไม่มีใครจำได้ว่าทำไม ถกเถียงกันใหม่ทุกครั้ง
- **"Option Y ดีกว่าไหม?"** — ไม่รู้ว่า Y เคยถูกพิจารณาและ reject ไปแล้ว
- **AI เปลี่ยน approach โดยไม่มีเหตุผล** — เพราะไม่เห็น decision ที่เคยทำไว้
- **Technical debt ที่ไม่มีเหตุผล** — ไม่รู้ว่า constraint ที่มีอยู่มาจากไหน

ADR แก้ทุกปัญหานี้ด้วยการบันทึก: **Context → Options → Decision → Consequences**

---

## ไฟล์ที่เกี่ยวข้อง

```
CoreAiWorkspaces/07-decisions/
├── README.md               ← ADR Index — ดู status ทุก decision
├── entity-register.md      ← track entities ที่เกิดจาก ADRs
├── ADR-001-title.md        ← individual ADR files
├── ADR-002-title.md
└── ADR-003-title.md
```

---

## ADR Index — CoreAiWorkspaces/07-decisions/README.md

ไฟล์นี้เป็น entry point สำหรับทุก ADR — AI อ่านก่อนตัดสินใจ architecture เสมอ

```markdown
# Decision Log

| ID | Title | Status | Date | Supersedes |
|----|-------|--------|------|------------|
| ADR-001 | เลือก PostgreSQL เป็น database หลัก | Accepted | 2026-01-15 | — |
| ADR-002 | Auth Strategy: JWT + refresh rotation | Accepted | 2026-02-01 | — |
| ADR-003 | State management: Zustand แทน Redux | Accepted | 2026-03-10 | ADR-008 |
| ADR-004 | Payment: Stripe integration pattern | Accepted | 2026-03-20 | — |
| ADR-005 | API versioning strategy | Proposed | 2026-05-01 | — |
```

**Statuses:**
- `Proposed` — สร้างโดย AI, รอ human review
- `Accepted` — Human approve แล้ว, ใช้ได้
- `Deprecated` — ยังไม่แทนที่ แต่ไม่ใช้แล้ว
- `Superseded by ADR-XXX` — ถูกแทนที่โดย ADR ใหม่

**กฎ:** ADR ไม่ถูกลบ — มีแต่ deprecated หรือ superseded เพื่อ preserve history

---

## Individual ADR — รูปแบบ

```markdown
# ADR-001: เลือก PostgreSQL เป็น Database หลัก

**Date:** 2026-01-15
**Status:** Accepted
**Author:** John Doe + AI session 2026-01-15
**Source Reference:** CoreAiWorkspaces/00-source/versions/v1.0/technical-requirements.md §4.2
**Related Tasks:** T-003, T-004

## Context

โปรเจ็กต์ต้องการ database ที่รองรับ:
- Relational data ที่มี complex joins
- ACID transactions สำหรับ payment operations
- JSON fields สำหรับ flexible metadata
- Scale ถึง ~100k users ในปีแรก

ข้อจำกัด: ทีมมีประสบการณ์ SQL มากกว่า NoSQL

## Options Considered

1. **PostgreSQL**
   - Pro: ACID, JSON support, ทีมคุ้นเคย, ecosystem ดี
   - Con: ต้อง manage schema migrations

2. **MongoDB**
   - Pro: flexible schema, JSON-native
   - Con: ทีมไม่คุ้นเคย, ACID ซับซ้อนกว่า

3. **MySQL**
   - Pro: ทีมคุ้นเคย
   - Con: JSON support ด้อยกว่า PostgreSQL

## Decision

เลือก PostgreSQL เพราะ:
- ทีมมี expertise อยู่แล้ว → ลด onboarding time
- JSONB สำหรับ metadata fields ตอบโจทย์
- Transaction support แข็งแกร่งสำหรับ payment

## Consequences

✅ ง่ายขึ้น: Schema migrations ชัดเจน, query optimization ตรงไปตรงมา
⚠️ ยากขึ้น: ต้อง manage schema changes ทุกครั้งที่ add field
📝 ต้องจำ: ถ้า document structure เปลี่ยนมาก ให้ revisit decision นี้

## Review Trigger

ถ้า user base เกิน 1M rows หรือ query performance ตกให้ review sharding strategy
```

---

## เมื่อไหร่ที่ AI ต้องสร้าง ADR

AI ต้องสร้าง ADR draft เสมอเมื่อ:

- เลือก library หรือ framework ใหม่
- เปลี่ยน architecture pattern ที่ใช้อยู่
- ตัดสินใจ trade-off ที่มีผลระยะยาว
- เปลี่ยน tech stack component ใดก็ตาม
- ตัดสินใจ security หรือ authentication approach

**AI ไม่ตัดสินใจ architecture เอง** — สร้าง draft แล้วรอ human approve เสมอ

### กระบวนการ

```
1. AI เจอ architectural decision ที่ต้องทำ
   ↓
2. AI สร้าง ADR-NNN-title.md ด้วย status: Proposed
   ↓
3. AI mark task เป็น [BLOCKED: NEEDS ADR REVIEW — ADR-NNN]
   ↓
4. Human อ่าน ADR draft → เปลี่ยน status เป็น Accepted/Rejected + เหตุผล
   ↓
5. AI update entity-register.md ทันที
   ↓
6. AI ทำงานต่อตาม decision ที่ accepted
```

---

## สร้าง ADR ด้วย Slash Command

ถ้าใช้ Claude Code:

```
/adr-create
```

Claude จะถาม:
1. Decision นี้เกี่ยวกับอะไร?
2. Options ที่พิจารณา?
3. Context และ constraints?

แล้วสร้าง ADR file พร้อม ID ถัดไปให้อัตโนมัติ

---

## Entity Register Integration

ทุกครั้งที่ ADR ถูก Accept → อัปเดต entity-register ทันที

```markdown
# หลัง ADR-003 accepted (Zustand แทน Redux):

| Entity | Type | Status | Since | Until | ADR |
|--------|------|--------|-------|-------|-----|
| Redux  | state | deprecated | 2025-06 | 2026-03 | ADR-003 |
| Zustand | state | active | 2026-03 | — | ADR-003 |
```

และใส่ tag ในไฟล์ที่ยังอ้างถึง Redux:
```
[ENTITY:deprecated:Redux][ENTITY:superseded:Redux→Zustand]
```

---

## ตัวอย่าง: ADR Workflow จริงในโปรเจ็กต์

**Scenario:** AI กำลัง implement auth และต้องเลือก approach

```
Session 5:
  T-010: Implement authentication
  
  AI: "ต้องตัดสินใจระหว่าง JWT stateless vs Session-based
       สร้าง ADR-002-auth-strategy.md (Proposed)
       T-010 → [BLOCKED: NEEDS ADR REVIEW — ADR-002]"