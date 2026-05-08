# Memory Architecture Overview

ระบบ memory เสริมเข้ากับ core workflow — ทำให้ AI จำได้ข้ามเวลาและข้ามโปรเจ็กต์
อ่านไฟล์นี้ก่อนเพื่อเข้าใจภาพรวม จากนั้นใช้ template แต่ละไฟล์ตามต้องการ

---

## ปัญหาที่ระบบนี้แก้

Core workflow แข็งแกร่งในด้าน "ทำอะไร และทำยังไง" — แต่ยังขาด:

| ปัญหา | ผลกระทบ |
|-------|---------|
| ไม่รู้ว่า tech ที่เลือกไว้ยังใช้อยู่ไหม | AI อาจ implement บน library ที่ deprecated แล้ว |
| อ่าน AI-CONTEXT แล้วไม่รู้ต้องอ่านไฟล์ไหนต่อ | อ่านเกิน (เปลือง token) หรืออ่านขาด (ทำงานผิด) |
| หลาย AI tool บนโปรเจ็กต์เดียว log ปนกัน | ไม่รู้ว่า decision ไหนมาจาก tool ไหน |
| แต่ละโปรเจ็กต์เริ่มจากศูนย์ทุกครั้ง | แก้ปัญหาเดิมซ้ำโดยไม่รู้ว่าเคยแก้แล้ว |

---

## เมื่อไหร่ที่ควรเปิดใช้ระบบนี้

**Phase 1–2 (Markdown only — เปิดใช้ได้ทันที ทุกโปรเจ็กต์):**
- โปรเจ็กต์ที่ใช้ tech หลายตัว และ tech เหล่านั้นอาจ deprecated ได้
- โปรเจ็กต์ที่ใช้ AI tool มากกว่า 1 ตัว (เช่น Claude Code + Claude.ai)
- โปรเจ็กต์ที่ต้องการ context routing ที่แม่นยำ
- ทีมที่ต้องการ pattern และ lesson สะสมข้ามโปรเจ็กต์

**Phase 3 (Optional — ต้องการ setup เพิ่ม):**
- โปรเจ็กต์ขนาดใหญ่ที่ CoreAiWorkspaces/ มีหลายสิบไฟล์และ routing hints ไม่พอ
- workspace ที่มีหลายโปรเจ็กต์และต้องการ semantic search ข้ามโปรเจ็กต์

---

## ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|------|--------|
| `core/19-memory-architecture-overview.md` | ภาพรวม (ไฟล์นี้) |
| `core/17-entity-register-template.md` | template สำหรับ `CoreAiWorkspaces/07-decisions/entity-register.md` |
| `core/18-cross-project-memory-template.md` | template สำหรับ `~/ai-workspace/cross-project-memory.md` |
| `core/06-work-status-template.md` | มี `read_more` field (Scoped Memory Map) |
| `core/08-log-and-summary-template.md` | มี Agent Diary format และ `deep_context` hint |
| `core/03-way-of-work-template.md` | มี Memory Scope Protocol (decision tree) |
| `core/11-ai-decision-protocol-template.md` | มี Scenario J (Entity Lifecycle Tags) และ Scenario K (Memory Scope) |
| `core/20-vector-memory-optional.md` | Phase 3 — local vector search setup และ decision protocol |
| `tools/vector-memory/README.md` | Quick reference: install, คำสั่งประจำวัน, token budget |

---

## สามชั้นของระบบ

### ชั้น 1 — Entity Memory (Phase 1)

**ปัญหา:** AI ไม่รู้ว่า entity (tech, integration, person, pattern) ยังมีสถานะอะไรอยู่

**วิธีแก้:** `CoreAiWorkspaces/07-decisions/entity-register.md` — ไฟล์เดียวที่ track entity ทั้งหมดพร้อม status และช่วงเวลา

```markdown
| Entity | Type | Status | Since | Until | ADR |
|--------|------|--------|-------|-------|-----|
| JWT    | auth | active | 2026-01 | — | ADR-001 |
| Redux  | state | deprecated | 2025-06 | 2026-03 | ADR-005 |
```

**Entity Lifecycle Tags** — เมื่อ entity เปลี่ยนสถานะ ใส่ tag ใน ADR และ task ที่อ้างถึง:

```
[ENTITY:deprecated:Redux]        ← อ่านเจอแล้วต้องตรวจ entity-register ก่อนใช้
[ENTITY:superseded:JWT→OAuth2]   ← entity ถูกแทนที่ด้วยอะไร
[ENTITY:proposed:GraphQL]        ← ยังไม่ได้ตัดสินใจ
```

**กฎ:** AI เจอ `[ENTITY:deprecated]` ในไฟล์ไหนก็ตาม → ตรวจ entity-register ก่อนใช้ข้อมูลนั้น (C-14)

---

### ชั้น 2 — Context Routing (Phase 1)

**ปัญหา:** AI อ่าน AI-CONTEXT 3 ไฟล์แล้วยังไม่รู้ว่าต้องอ่านอะไรเพิ่ม

**วิธีแก้:** `read_more` field ใน AI-CONTEXT block ของ work-status — บอกชัดว่าถ้าต้องการ context เรื่องอะไร ให้ไปอ่านที่ไหน

```
<!-- AI-CONTEXT
phase: implementation
focus: T-012 payment integration
read_more:
  architecture: CoreAiWorkspaces/07-decisions/README.md
  entities:     CoreAiWorkspaces/07-decisions/entity-register.md
  source:       CoreAiWorkspaces/00-source/versions/v1.2/
-->
```

**กฎ:** อ่าน `read_more` hints หลัง AI-CONTEXT block — load เฉพาะ section ที่ task ปัจจุบันต้องการ ไม่ต้อง scan ทั้งโปรเจ็กต์

---

### ชั้น 3 — Agent Isolation & Cross-Project Memory (Phase 2)

#### Agent Diary — แยก log ต่อ tool

**ปัญหา:** หลาย AI tool บนโปรเจ็กต์เดียวกัน — work-log ปนกัน ไม่รู้ว่า decision ไหนมาจากใคร

**วิธีแก้:**
```
CoreAiWorkspaces/03-log/
  work-log-index.md      ← master index รวมทุก tool (ไม่เปลี่ยน)
  agents/
    claude-code.md       ← diary เฉพาะ Claude Code
    claude-ai.md         ← diary เฉพาะ Claude.ai
```

**กฎ:**
- แต่ละ tool เขียน diary ของตัวเองเท่านั้น — ห้าม cross-write
- session เริ่ม: อ่าน diary ของ tool ที่ใช้ก่อนทำงาน
- ถ้าใช้ tool เดียว: ไม่ต้องสร้าง `agents/` folder

#### Cross-Project Memory — จำข้ามโปรเจ็กต์

**ปัญหา:** pattern และ lesson ที่เรียนรู้มาไม่ถูกนำมาใช้ในโปรเจ็กต์ต่อไป

**วิธีแก้:** `~/ai-workspace/cross-project-memory.md` — อยู่นอก git ระดับ user workspace

```markdown
## Patterns That Worked
- **JWT + refresh token rotation** — ป้องกัน token hijack (source: project-alpha, 2026-01)

## Lessons Learned
- **อย่าใช้ Redux กับ project ขนาดเล็ก** (source: project-alpha, 2026-01)

## Reusable Decisions (ADR Cross-Reference)
- **project-alpha/ADR-003**: Stripe integration pattern
```

**กฎ:**
- Bootstrap โปรเจ็กต์ใหม่: อ่านไฟล์นี้ก่อน ถ้ามี
- เขียนเพิ่มได้เฉพาะ pattern ที่ proven แล้ว — ไม่ใส่สิ่งที่ยังไม่ทดสอบ
- ห้ามเขียนโดยไม่ได้รับอนุญาตจากผู้ใช้

#### Memory Scope Protocol — ข้อมูลชิ้นหนึ่งเก็บที่ไหน

เมื่อพบข้อมูลใหม่ระหว่าง session ใช้ decision tree นี้:

```
ข้อมูลใหม่ที่ต้องเก็บ
├── เป็น architectural decision?       → ADR (CoreAiWorkspaces/07-decisions/)
├── เป็น entity ใหม่หรือ status เปลี่ยน? → entity-register.md
├── เป็น pattern ที่ใช้ได้ข้ามโปรเจ็กต์? → cross-project-memory.md (ถามผู้ใช้ก่อน)
├── เป็น progress/detail ของ session นี้? → agent diary + work-log-index
└── เป็น task หรือ status เปลี่ยน?      → task-board.md
```

**กฎ:** ข้อมูลหนึ่งชิ้นอาจต้องเก็บหลายที่ — ไม่ mutually exclusive
ถ้าไม่แน่ใจ: เก็บลง work-log ก่อน แล้วระบุว่า "ยังไม่แน่ใจว่าควรอยู่ที่ไหน"

---

### ชั้น 4 — Vector Search (Phase 3, Optional)

**ปัญหา:** CoreAiWorkspaces/ มีหลายสิบไฟล์ — `read_more` hints ไม่เพียงพอ ต้อง semantic search เพื่อหา context จาก session เก่า

**วิธีแก้:** local-first vector memory — ไม่ต้อง cloud API, ข้อมูลอยู่ในเครื่อง

```
Wing: <project-name>
  Room: decisions     ← CoreAiWorkspaces/07-decisions/
  Room: tasks         ← CoreAiWorkspaces/02-task/
  Room: plan          ← CoreAiWorkspaces/01-plan/
  Room: logs          ← CoreAiWorkspaces/03-log/
```

**กฎ:**
- search เฉพาะเมื่อ context window ไม่มีคำตอบ — ไม่ต้อง search ทุก query
- ผล search สูงสุด 5 chunks, ไม่เกิน 1,500 token รวม
- ดูรายละเอียดทั้งหมดใน `core/20-vector-memory-optional.md`

---

## การเปลี่ยนแปลงจาก Core Workflow

Memory system เพิ่มขั้นตอนต่อไปนี้บน core workflow:

### Start-of-Session (เพิ่มหลัง 3-file read)

```
4. ตรวจ read_more hints ใน work-status AI-CONTEXT
   → load เฉพาะ section ที่ task ปัจจุบันต้องการ
5. ถ้ามี agents/ folder → อ่าน diary ของ tool ที่ใช้อยู่
```

### End-of-Session (เพิ่มใน checklist)

```
□ entity-register — มี entity ใหม่หรือ status เปลี่ยนไหม? (deprecated, added, removed)
□ agent diary — เขียน diary ของ tool นี้ (ถ้าใช้ multi-tool workflow)
□ cross-project memory — มี pattern ที่ควร promote ข้ามโปรเจ็กต์ไหม? (ถามผู้ใช้ก่อน)
□ ถ้า vector_memory: enabled และ CoreAiWorkspaces/ เปลี่ยน → re-index: CoreAiWorkspaces/ --wing <vector_wing>
```

### เมื่อ ADR ถูก Accept

```
→ อัปเดต entity-register ทันที
   - เพิ่ม entity ใหม่ที่ตัดสินใจเลือก (status: active)
   - ย้าย entity ที่แทนที่ไป deprecated (status: deprecated, until: วันที่)
```

### เมื่อพบ deprecated entity ใน codebase

```
→ ใส่ tag [ENTITY:deprecated:ชื่อ] ในไฟล์ที่อ้างถึง
→ validate-commit.sh จะ warn อัตโนมัติถ้า commit มี reference ถึง deprecated entity
```

---

## สิ่งที่ไม่เปลี่ยนจาก Core

- Session Start/End Protocol — ใช้เหมือนเดิม memory system เป็นขั้นเพิ่มเติม
- ADR System — ใช้เหมือนเดิม entity-register เป็น downstream ของ ADR
- Compliance check — ใช้เหมือนเดิม พร้อม C-14 เพิ่มสำหรับ entity lifecycle
- work-status, task-board, work-log-index — ใช้เหมือนเดิม

---

## Compliance Rules ที่เกี่ยวข้อง

| Code | สิ่งที่ตรวจ |
|------|-----------|
| C-14 | AI เจอ `[ENTITY:deprecated]` ต้องตรวจ entity-register ก่อนใช้ข้อมูลนั้น |
| C-14 | เมื่อ ADR Accept → ต้องอัปเดต entity-register ทันที |
| C-20 | ถ้า `vector_memory: enabled` และ CoreAiWorkspaces/ เปลี่ยน → ต้อง re-mine ก่อนจบ session |
| C-21 | ผล search ที่ score ต่ำกว่า threshold ห้ามใส่ใน context (0.35 Thai/mixed, 0.50 English) |
| C-22 | ห้าม inject ผล search เกิน 1,500 token ต่อ session |

validate-commit.sh hook: warn เมื่อ commit file มี reference ถึง entity ที่อยู่ใน entity-register ด้วย status `deprecated`
