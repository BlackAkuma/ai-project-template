---
title: Memory System — Phase 1–3
---

# Memory System

ระบบ memory 3 ชั้นที่ทำให้ AI จำข้อมูลสำคัญได้ข้ามเวลาและข้ามโปรเจ็กต์ — โดยไม่พึ่ง context window

→ [Visual: Memory Diagram](workflow-diagram.html#sec-memory) | [หน้าหลัก](../index.md)

---

## ทำไมต้องมี Memory System

Core workflow (session start → work → session end) แก้ปัญหา "AI ลืมระหว่าง session" ได้แล้ว

แต่ยังเหลือปัญหาที่ core workflow ไม่ครอบคลุม:

| ปัญหา | ผลกระทบ |
|-------|---------|
| ไม่รู้ว่า tech ที่เลือกไว้ยัง active ไหม | AI อาจ implement บน library ที่ deprecated แล้ว |
| อ่าน AI-CONTEXT แล้วไม่รู้ต้องอ่านไฟล์ไหนต่อ | อ่านเกิน (เปลือง token) หรืออ่านขาด (ทำงานผิด) |
| หลาย AI tool บนโปรเจ็กต์เดียว log ปนกัน | ไม่รู้ว่า decision ไหนมาจาก tool ไหน |
| แต่ละโปรเจ็กต์เริ่มจากศูนย์ทุกครั้ง | แก้ปัญหาเดิมซ้ำโดยไม่รู้ว่าเคยแก้แล้ว |

Memory system แก้ปัญหาเหล่านี้เป็น **layer เพิ่มเติม** บน core workflow — ไม่แทนที่ core

---

## เมื่อไหร่ควรเปิดใช้แต่ละ Phase

```
Phase 1 (Entity Memory + Context Routing)
→ เปิดใช้ได้ทันที ทุกโปรเจ็กต์ — ไม่มี setup เพิ่ม

Phase 2 (Agent Diary + Cross-Project Memory)
→ เปิดเมื่อใช้ AI tool มากกว่า 1 ตัว หรือทำโปรเจ็กต์หลายโปรเจ็กต์

Phase 3 (Vector Search)
→ เปิดเมื่อ ai/ มีไฟล์มากกว่า 30 ไฟล์ หรือโปรเจ็กต์ทำมานานกว่า 3 เดือน
→ ต้องการ setup เพิ่ม — ดู integrations/vector-memory.md
```

---

## Phase 1: Entity Memory

### Entity Register

**ไฟล์:** `ai/07-decisions/entity-register.md`

Track tech choices, integrations, และ dependencies ทั้งหมดพร้อม status และช่วงเวลา

```markdown
| Entity | Type | Status | Since | Until | ADR |
|--------|------|--------|-------|-------|-----|
| PostgreSQL | database | active | 2026-01 | — | ADR-001 |
| Stripe | payment | active | 2026-03 | — | ADR-005 |
| Redux | state | deprecated | 2025-06 | 2026-03 | ADR-008 |
| Zustand | state | active | 2026-03 | — | ADR-008 |
```

**กฎ:** เมื่อ ADR ถูก Accept → อัปเดต entity-register ทันที

### Entity Lifecycle Tags

เมื่อ entity เปลี่ยนสถานะ ใส่ tag ในไฟล์ที่อ้างถึง:

```
[ENTITY:deprecated:Redux]         ← เจอแล้วต้องตรวจ entity-register ก่อนใช้
[ENTITY:superseded:JWT→OAuth2]    ← entity ถูกแทนที่ด้วยอะไร
[ENTITY:proposed:GraphQL]         ← ยังไม่ได้ตัดสินใจ
```

**Compliance C-14:** AI เจอ `[ENTITY:deprecated]` ในไฟล์ไหนก็ตาม → ต้องตรวจ entity-register ก่อนใช้ข้อมูลนั้น

### Validate Commit Hook

`scripts/validate-commit.sh` จะ warn อัตโนมัติถ้า commit มี reference ถึง entity ที่อยู่ใน entity-register ด้วย status `deprecated`

---

## Phase 1: Context Routing

**ปัญหา:** AI อ่าน AI-CONTEXT 3 ไฟล์แล้วยังไม่รู้ว่าต้องอ่านอะไรเพิ่ม

**วิธีแก้:** `read_more` field ใน AI-CONTEXT block ของ work-status

```yaml
<!-- AI-CONTEXT
phase: implementation
focus: T-012 payment integration
read_more:
  architecture: ai/07-decisions/README.md
  entities:     ai/07-decisions/entity-register.md
  source:       ai/00-source/versions/v1.2/
-->
```

**กฎ:** AI อ่าน `read_more` hints → load เฉพาะ section ที่ task ปัจจุบันต้องการ ไม่ต้อง scan ทั้งโปรเจ็กต์

**ผลลัพธ์:** ลด token ที่ใช้ต่อ session ลงได้ ~40–60% ในโปรเจ็กต์ที่มีไฟล์มาก

---

## Phase 2: Agent Diary

**ปัญหา:** หลาย AI tool บนโปรเจ็กต์เดียว — log ปนกัน ไม่รู้ว่า decision ไหนมาจาก tool ไหน

**โครงสร้าง:**

```
ai/03-log/
├── work-log-index.md       ← master index (ไม่เปลี่ยน)
└── agents/
    ├── claude-code.md      ← diary เฉพาะ Claude Code
    └── claude-ai.md        ← diary เฉพาะ Claude.ai
```

**รูปแบบ diary:**

```markdown
# Agent Diary — Claude Code

## 2026-05-08 Session 12

**Task:** T-015 - Database migration
**ทำอะไร:**
- สร้าง migration script สำหรับ user table
- เพิ่ม index บน email column

**Decision:**
- ใช้ soft delete แทน hard delete (C-14 compliance)

**ส่งต่อ:**
- claude-ai: review migration strategy ก่อน run
```

**กฎ:**
- แต่ละ tool เขียน diary ของตัวเองเท่านั้น — ห้าม cross-write
- เริ่ม session: อ่าน diary ของ tool ที่ใช้ก่อน
- ถ้าใช้ tool เดียว: ไม่ต้องสร้าง `agents/` folder

---

## Phase 2: Cross-Project Memory

**ปัญหา:** pattern และ lesson ที่เรียนรู้มาไม่ถูกนำมาใช้ในโปรเจ็กต์ต่อไป

**ที่เก็บ:** `~/ai-workspace/cross-project-memory.md` — อยู่นอก git ระดับ user workspace

```markdown
# Cross-Project Memory

## Patterns That Worked
- **JWT + refresh token rotation** — ป้องกัน token hijack
  (source: project-alpha, 2026-01)

## Lessons Learned
- **อย่าใช้ Redux กับโปรเจ็กต์ขนาดเล็ก** — overhead สูง, Zustand เพียงพอ
  (source: project-alpha, 2026-03)

## Reusable Decisions (ADR Cross-Reference)
- **project-alpha/ADR-003**: Stripe integration pattern — ใช้ซ้ำได้ทันที
```

**กฎ:**
- Bootstrap โปรเจ็กต์ใหม่: อ่านไฟล์นี้ก่อน ถ้ามี
- เพิ่มได้เฉพาะ pattern ที่ proven แล้ว
- AI ต้องถามผู้ใช้ก่อนเพิ่มข้อมูลใหม่

---

## Phase 2: Memory Scope Protocol

เมื่อพบข้อมูลใหม่ระหว่าง session ใช้ decision tree นี้:

```
ข้อมูลใหม่ที่ต้องเก็บ
├── เป็น architectural decision?         → ADR (ai/07-decisions/)
├── เป็น entity ใหม่หรือ status เปลี่ยน? → entity-register.md
├── เป็น pattern ข้ามโปรเจ็กต์?          → cross-project-memory.md (ถามก่อน)
├── เป็น progress ของ session นี้?        → agent diary + work-log
└── เป็น task หรือ status เปลี่ยน?        → task-board.md
```

ข้อมูลหนึ่งชิ้นอาจต้องเก็บหลายที่ — ไม่ mutually exclusive

---

## Phase 3: Vector Search (Optional)

เปิดใช้เมื่อ **อย่างน้อยหนึ่งข้อ** ต่อไปนี้เป็นจริง:

- `ai/` มีไฟล์มากกว่า 30 ไฟล์ และหา context ยากขึ้น
- โปรเจ็กต์ทำมานานกว่า 3 เดือน และ session เก่ามี decision สำคัญ
- `read_more` hints ต้องชี้ไฟล์มากกว่า 5 ไฟล์ต่อ query

**อย่าเปิด** ถ้า read_more + entity-register ยังรองรับได้ — อย่าเพิ่ม complexity โดยไม่จำเป็น

### หลักการ Wing / Room / Drawer

Vector store จัดข้อมูลเป็น 3 ชั้น:

```
Wing: "my-project"           ← ชื่อโปรเจ็กต์ (แยก project ออกจากกัน)
├── Room: "decisions"        ← ai/07-decisions/
├── Room: "tasks"            ← ai/02-task/
├── Room: "plan"             ← ai/01-plan/
└── Room: "logs"             ← ai/03-log/
```

**สำคัญ:** ต้องระบุ Wing name เสมอเมื่อ index — ไม่งั้น projects ต่างๆ ที่ใช้ template เดียวกันจะ clash กัน

### Token Budget

| กฎ | ค่า |
|----|-----|
| จำนวน chunk สูงสุด | 5 chunks |
| token รวมสูงสุด | 1,500 token |
| Similarity threshold (Thai/mixed) | 0.35 |
| Similarity threshold (English-only) | 0.50 |

ผลลัพธ์ที่ score ต่ำกว่า threshold → ไม่ inject เข้า context (Compliance C-21)

### ตั้งค่าใน work-status.md

```yaml
<!-- AI-CONTEXT
vector_memory: enabled
vector_wing: my-project-name
-->
```

→ รายละเอียดการ setup: [integrations/vector-memory.md](../integrations/vector-memory.md)

---

## Session Checklist ที่เพิ่มจาก Memory System

**Session Start (เพิ่มหลัง 3-file read):**
```
4. ตรวจ read_more hints ใน work-status → load เฉพาะส่วนที่ต้องการ
5. ถ้ามี agents/ → อ่าน diary ของ tool ที่ใช้อยู่
6. ถ้า vector_memory: enabled → ตรวจว่า task ต้องการ context จาก session เก่าไหม
```

**Session End (เพิ่มใน checklist):**
```
□ entity-register — มี entity ใหม่หรือ status เปลี่ยนไหม?
□ agent diary — เขียน diary สำหรับ tool นี้ (ถ้าใช้ multi-tool)
□ cross-project memory — มี pattern ที่ควร promote? (ถามก่อน)
□ vector_memory: enabled + ai/ เปลี่ยน → re-index
```

---

→ ต่อไป: [ADR System](adr-system.md) | [Vector Memory Setup](../integrations/vector-memory.md)
