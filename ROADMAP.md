# AI Project Template — Roadmap

> แผนพัฒนานี้ใช้ MemPalace เป็นแรงบันดาลใจในการวิเคราะห์ช่องว่าง
> ไม่ได้ integrate MemPalace โดยตรง แต่นำ concept มาพัฒนาให้เหมาะกับระบบของเรา

---

## 1. Vision & เป้าหมาย

**template นี้คืออะไร และกำลังไปทิศทางไหน**

AI Project Template เป็นระบบ structured workflow สำหรับการทำงานร่วมกันระหว่างมนุษย์และ AI
ปัจจุบันแข็งแกร่งในด้าน workflow discipline — session protocol, task lifecycle, compliance, source doc versioning
แต่ยังขาดด้าน memory — AI รู้ว่าต้องทำอะไร แต่จำไม่ได้ว่าเคยตัดสินใจอะไรไป และไม่รู้ว่า entity ในระบบยังมีสถานะเดิมอยู่ไหม

**ปัญหาที่การวิเคราะห์ MemPalace ช่วยให้เห็น**

| ช่องว่าง | ผลกระทบ |
|---------|---------|
| ไม่มี entity tracking ตามเวลา | AI ไม่รู้ว่า tech choice หรือ integration ยังใช้งานอยู่ไหม |
| AI-CONTEXT ไม่มี scoped routing | AI ต้องเดาว่าต้องอ่านไฟล์ไหนเพิ่มเมื่อต้องการ context เจาะจง |
| ไม่มี cross-project memory | แต่ละโปรเจ็กต์เริ่มจากศูนย์ ไม่เรียนรู้จากโปรเจ็กต์ก่อน |
| agent แต่ละตัวไม่มี log แยก | เมื่อใช้หลาย AI tool บนโปรเจ็กต์เดียว context ปนกัน |

**เป้าหมายปลายทาง**

```
ปัจจุบัน:  structured workflow  +  manual memory
เป้าหมาย:  structured workflow  +  persistent memory  +  cross-project learning
```

AI ที่ทำงานถูกต้อง (workflow) AND จำได้ (memory) AND เรียนรู้สะสม (learning)
โดยไม่ต้องพึ่ง cloud service หรือ external API

**หลักการพัฒนา**

- **Backward compatible** — ทุก phase ใช้กับโปรเจ็กต์ที่มีอยู่แล้วได้เลย ไม่รื้อโครงสร้าง core/
- **Progressive** — แต่ละ phase เสริมของเดิม ไม่แทนที่
- **Markdown-first** — phase แรกไม่มี dependency ใหม่ ทำได้ทันที
- **Optional layers** — feature ขั้นสูง (vector DB) เป็น opt-in ไม่บังคับ

**ภาพรวม Features ทั้งหมด**

| Phase | Feature | สถานะ |
|-------|---------|--------|
| **Phase 1** | Project Entity Register | planned |
| **Phase 1** | Scoped Memory Map | planned |
| **Phase 1** | Entity Lifecycle Tags | planned |
| **Phase 2** | Agent Diary Protocol | planned |
| **Phase 2** | Cross-Project Memory Bridge | planned |
| **Phase 2** | Memory Scope Protocol | planned |
| **Phase 3** | Semantic Search Layer | planned |
| **Phase 3** | Cross-Project Learning Engine | planned |

---

## 2. สิ่งที่มีอยู่แล้ว (Baseline)

สิ่งเหล่านี้ถูกต้องและไม่ต้องแก้ไข — Phase ต่อไปเสริมขึ้นมาบนฐานนี้

**Workflow & Session**
- Session Start/End Protocol — 3-file read, AI-CONTEXT blocks, checkpoint saving
- Pre/Post-compact Protocol — บันทึก state ก่อน context หาย ต่อได้หลัง compact
- Two-tier Log System — Milestone Summary (ถาวร) + Recent Sessions (rotating 20 entries)
- Compliance System — C-01 to C-13, G-01 to G-07, A-01 to A-04, N-01 to N-04

**Task & Planning**
- Task Lifecycle — todo → design_validate → in_progress → review → done
- Definition of Ready / Definition of Done — checklist ก่อนเลื่อน status
- Source Doc Versioning — immutable, versioned, ห้ามแก้ retroactive

**Decision & Architecture**
- ADR System — บันทึกเหตุผลการตัดสินใจ, Proposed → Accepted, ไม่ลบ
- AI Decision Protocol — 9 scenarios, 3 escalation levels, responsibility boundary

**Claude Code Platform Layer**
- CLAUDE.md — auto-load bootstrap, First Run detection, session protocols
- Hooks — session-start/stop, pre-compact, validate-commit, detect-gaps
- Rules — path-scoped coding standards (src/, doc/, tests/, src/game/)
- Skills — /compliance-check, /session-end, /fdd-create, /adr-create, /scope-check, /launch-check, /archive-logs

**Game Skill Pack**
- FDD System — Feature Design Documents พร้อม section-by-section approval
- Balance & Playtest templates
- Narrative Standards + N-01 to N-04

---

## 3. Phase 1 — Quick Wins

ทำได้ทันที — ไม่มี dependency ใหม่ ไม่รื้อโครงสร้าง core/
ทุก feature ในระยะนี้เป็น markdown ล้วน

---

### Feature 1: Project Entity Register

**ปัญหาที่แก้**
ปัจจุบัน AI ไม่รู้ว่า tech choice, integration, หรือ dependency ที่ตัดสินใจไว้ยังใช้งานอยู่ไหม
ต้องอ่าน ADR และ source doc ทั้งหมดเพื่อหาคำตอบ — แพง และพลาดได้

**หลักการ**
ไฟล์เดียวที่ track "entity สำคัญ" ของโปรเจ็กต์พร้อม status และช่วงเวลาที่ใช้งาน
แรงบันดาลใจจาก MemPalace Knowledge Graph แต่เป็น markdown ไม่ต้องมี vector DB

**ที่อยู่ในโปรเจ็กต์**
`doc/06-entities/entity-register.md`

**โครงสร้างตัวอย่าง**
```markdown
| Entity | Type | Status | Since | Until | ADR | Notes |
|--------|------|--------|-------|-------|-----|-------|
| JWT | auth-method | active | 2026-01 | — | ADR-001 | ใช้กับ /api/* |
| Redux | state-mgmt | deprecated | 2025-06 | 2026-03 | ADR-005 | แทนด้วย Zustand |
| Stripe | payment | active | 2026-02 | — | ADR-003 | sandbox mode |
```

**fields:**
- `Type` — tech / integration / person / pattern / decision
- `Status` — active / deprecated / proposed / removed
- `Since / Until` — temporal window (Until ว่างเปล่า = ยังใช้อยู่)
- `ADR` — link ไปที่เหตุผลการตัดสินใจ

**สิ่งที่ต้องสร้าง**
- template ไฟล์ใน `core/` สำหรับ entity-register.md
- เพิ่มใน core/01 folder structure
- เพิ่ม C-XX compliance rule: task ที่ deprecated tech ต้องอัปเดต entity-register

---

### Feature 2: Scoped Memory Map

**ปัญหาที่แก้**
AI อ่าน AI-CONTEXT block 3 ไฟล์แล้วรู้ state ปัจจุบัน แต่ถ้าต้องการ context เพิ่ม ต้องเดาเองว่าต้องอ่านไฟล์ไหน
ทำให้บางครั้งอ่านเกิน (เปลือง token) หรืออ่านขาด (ทำงานผิด)

**หลักการ**
เพิ่ม routing hints ลงใน AI-CONTEXT block ของ work-status — บอกชัดว่า "ถ้าต้องการข้อมูลเรื่อง X ให้อ่านที่ Y"
แรงบันดาลใจจาก MemPalace scoped search ที่ค้นเฉพาะ wing/room แทนการ scan ทั้งหมด

**รูปแบบที่เพิ่มใน AI-CONTEXT**
```
<!-- AI-CONTEXT
phase: implementation
focus: T-012 payment integration
...
read_more:
  architecture: doc/07-decisions/README.md
  entities: doc/06-entities/entity-register.md
  game_design: doc/08-design/fdd-index.md
  source_current: doc/00-source/versions/v1.2/
-->
```

**สิ่งที่ต้องสร้าง**
- อัปเดต core/06 (work-status template) เพิ่ม `read_more` field
- อัปเดต core/08 (log template) ให้ AI-CONTEXT ของ work-log-index มี `deep_context` hint ด้วย
- อัปเดต CLAUDE.md ให้ Session Start Protocol อ่าน `read_more` แล้ว suggest ว่าควรอ่านอะไรเพิ่ม

---

### Feature 3: Entity Lifecycle Tags

**ปัญหาที่แก้**
เมื่อ tech หรือ pattern ถูก deprecated ข้อมูลเก่ายังอยู่ใน ADR, task, และ source doc
AI อาจหยิบข้อมูลเก่ามาใช้โดยไม่รู้ว่า outdated แล้ว

**หลักการ**
Tag มาตรฐานที่ใส่ใน ADR และ task เพื่อ signal ว่า entity นี้มีสถานะเปลี่ยนแล้ว
AI ที่อ่านเจอ tag นี้ต้องตรวจ entity-register ก่อนใช้ข้อมูล

**Tag format**
```
[ENTITY:deprecated:Redux]       ← ใน ADR หรือ task ที่อ้างถึง Redux
[ENTITY:superseded:JWT→OAuth2]  ← เมื่อ entity ถูกแทนที่
[ENTITY:proposed:GraphQL]       ← entity ที่ยังไม่ได้ตัดสินใจ
```

**สิ่งที่ต้องสร้าง**
- เพิ่ม tag format ใน core/11 (ai-decision-protocol) เป็น Scenario ใหม่
- เพิ่ม compliance rule: AI เจอ `[ENTITY:deprecated]` ต้องตรวจ entity-register ก่อนใช้
- เพิ่ม validate-commit.sh hook ให้ warn เมื่อ commit มี reference ถึง deprecated entity

---

## 4. Phase 2 — Deeper Integration

ต่อยอดจาก Phase 1 — เพิ่มความสามารถด้าน multi-agent และ cross-project
บางส่วนอาจต้องการ tooling เพิ่มแต่ยังไม่ถึงขั้น vector DB

---

### Feature 4: Agent Diary Protocol

**ปัญหาที่แก้**
เมื่อใช้หลาย AI tool บนโปรเจ็กต์เดียวกัน (Claude Code สำหรับ implementation, Claude.ai สำหรับ design review)
work-log ปนกันหมด — ไม่รู้ว่า decision ไหนมาจาก tool ไหน context ของแต่ละ tool ก็ต่างกัน

**หลักการ**
แยก log section ต่อ agent อย่างเป็นระบบ แต่ละ agent มี "diary" ของตัวเองภายใน work-log-index
แรงบันดาลใจจาก MemPalace dedicated wings + AAAK diary per agent

**โครงสร้าง**
```
doc/03-log/
  work-log-index.md         ← master index (ไม่เปลี่ยน)
  agents/
    claude-code.md          ← diary เฉพาะ Claude Code sessions
    claude-ai.md            ← diary เฉพาะ Claude.ai sessions
    [tool-name].md          ← เพิ่มตาม tool ที่ใช้
```

**diary format ต่อ agent**
```markdown
<!-- AI-CONTEXT
agent: Claude Code
last_session: 2026-04-29
focus: T-012
checkpoint: finished payment hook, pending webhook test
-->

### 2026-04-29
- implement: Stripe webhook handler
- decision: ใช้ idempotency key แทน deduplication table (เบากว่า)
- blocked: ยังไม่ได้ test กับ Stripe sandbox
```

**สิ่งที่ต้องสร้าง**
- template ไฟล์ `doc/03-log/agents/[tool].md` ใน core/08
- อัปเดต core/03 way-of-work ให้ระบุว่า tool ไหนรับผิดชอบ section ไหน
- อัปเดต CLAUDE.md Session Start Protocol: ถ้ามี agents/ folder ให้อ่าน diary ของ tool นั้นก่อน
- อัปเดต /session-end skill ให้ write ลง agent diary ด้วย

---

### Feature 5: Cross-Project Memory Bridge

**ปัญหาที่แก้**
แต่ละโปรเจ็กต์เริ่มจากศูนย์ทุกครั้ง — AI ไม่รู้ว่าโปรเจ็กต์ก่อนแก้ปัญหาคล้ายกันยังไง
ไม่มีการสะสม pattern หรือ lesson learned ข้ามโปรเจ็กต์

**หลักการ**
ไฟล์ "bridge" ที่วางนอกโปรเจ็กต์ (ระดับ workspace/user) สรุป pattern และ lesson ที่ควรรู้ก่อนเริ่มโปรเจ็กต์ใหม่
AI อ่านไฟล์นี้ตอน bootstrap ใหม่แทนการเริ่มจากศูนย์

**โครงสร้าง**
```
~/ai-workspace/                      ← นอกโปรเจ็กต์ ระดับ user
  cross-project-memory.md            ← pattern และ lesson สะสม
  entity-registry.md                 ← entity ที่ใช้ข้ามโปรเจ็กต์ (เช่น shared lib, team members)
```

**cross-project-memory format**
```markdown
## Patterns That Worked
- JWT + refresh token rotation — ใช้ได้ดีใน project-A, project-B
- Stripe webhook idempotency key — แก้ปัญหา duplicate event

## Lessons Learned
- อย่าใช้ Redux กับ project ขนาดเล็ก — overhead เกิน (project-A)
- ต้อง rate-limit ก่อน deploy เสมอ — เจอปัญหาใน project-C

## Reusable Decisions (ADR cross-reference)
- project-A/ADR-003: Stripe integration pattern
```

**สิ่งที่ต้องสร้าง**
- template ไฟล์ cross-project-memory.md ใน core/ หรือ platforms/claude-code/
- อัปเดต CLAUDE.md First Run Bootstrap: ถ้ามี `~/ai-workspace/cross-project-memory.md` ให้อ่านก่อน bootstrap
- /session-end skill เพิ่ม optional step: "มี pattern ที่ควรบันทึกข้ามโปรเจ็กต์ไหม?"

---

### Feature 6: Memory Scope Protocol

**ปัญหาที่แก้**
ยังไม่มีกฎชัดเจนว่า "ข้อมูลแบบไหนควรอยู่ที่ไหน" — AI ต้องเดาว่าควรเก็บลง work-log, ADR, entity-register, หรือ cross-project memory

**หลักการ**
กำหนด decision tree ชัดเจนว่าข้อมูลแต่ละประเภทควรอยู่ที่ไหน
ทำให้ AI ทุก session เก็บข้อมูลในที่เดิมเสมอ — ค้นหาได้ predictable

**Decision Tree**
```
ข้อมูลใหม่ที่ต้องเก็บ
├── เป็น architectural decision?
│   └── → ADR (doc/07-decisions/)
├── เป็น entity ใหม่หรือ status เปลี่ยน?
│   └── → Entity Register (doc/06-entities/)
├── เป็น pattern ที่ใช้ได้ข้ามโปรเจ็กต์?
│   └── → Cross-Project Memory (~/ai-workspace/)
├── เป็น progress/detail ของ session นี้?
│   └── → Agent Diary + work-log-index (doc/03-log/)
└── เป็น task หรือ status?
    └── → Task Board (doc/02-task/)
```

**สิ่งที่ต้องสร้าง**
- เพิ่ม Memory Scope section ใน core/03 way-of-work template
- เพิ่ม Scenario J ใน core/11 ai-decision-protocol: "ไม่รู้ว่าควรเก็บข้อมูลที่ไหน → ใช้ decision tree"
- อัปเดต CLAUDE.md Key Rules ให้ reference memory scope protocol

---

## 5. Phase 3 — Long-term Vision

ระยะนี้ต้องการ dependency เพิ่ม และ setup ที่หนักกว่า
เป็น opt-in — ไม่ทำก็ใช้ Phase 1–2 ได้ครบ
เป้าหมายคือให้ระบบ markdown ของเราเชื่อมกับ semantic search ได้

---

### Feature 7: Semantic Search Layer

**ปัญหาที่แก้**
Phase 1–2 ค้นหาด้วยการอ่าน — AI ต้องรู้ว่าต้องอ่านไฟล์ไหน
ถ้าโปรเจ็กต์ใหญ่ขึ้น จำนวนไฟล์มากขึ้น การ navigate ด้วย routing hints อาจไม่พอ
ต้องการ "ค้นหาด้วยความหมาย" แทนการค้นหาด้วย path

**หลักการ**
เพิ่ม semantic search เป็น optional layer บน doc/ ที่มีอยู่แล้ว
ไม่ย้ายข้อมูลออกจาก markdown — แค่ index มันเพิ่มเติม
ใช้ MemPalace หรือ ChromaDB โดยตรงก็ได้ เพราะโครงสร้าง doc/ ของเราเป็น "wings/rooms" อยู่แล้ว

**การ map โครงสร้าง**
```
doc/ folder          →   MemPalace concept
doc/00-source/       →   "source" wing
doc/01-plan/         →   "plan" wing
doc/02-task/         →   "tasks" wing
doc/03-log/          →   "log" wing
doc/07-decisions/    →   "decisions" wing
doc/06-entities/     →   "entities" wing  (Phase 1)
```

**วิธี integrate**
- `mempalace sweep` หรือ script ที่คล้ายกัน index doc/ เข้า vector store
- เพิ่ม MCP tool ใน Claude Code: `search_project_docs "query"` → ค้นหาข้าม doc/ ทั้งหมด
- ยัง write ลง markdown ตามปกติ — vector store เป็น read-only index เท่านั้น

**สิ่งที่ต้องสร้าง**
- script `tools/index-docs.sh` — index doc/ เข้า vector store ที่เลือก (MemPalace / ChromaDB / อื่น)
- MCP server wrapper หรือ skill `/search-docs` สำหรับ Claude Code
- documentation วิธี setup พร้อม option หลายแบบ (MemPalace, bare ChromaDB, อื่น)
- ระบุชัดว่า markdown ยังเป็น source of truth — vector store เป็นแค่ index

---

### Feature 8: Cross-Project Learning Engine

**ปัญหาที่แก้**
Phase 2 ทำให้เก็บ pattern ข้ามโปรเจ็กต์ได้ แต่ยังต้อง curate manual
ถ้ามีหลายโปรเจ็กต์ cross-project-memory.md จะโตขึ้นและหาคำตอบยากขึ้น
ต้องการให้ AI ค้นหา pattern จากโปรเจ็กต์เก่าได้โดยตรง

**หลักการ**
แต่ละโปรเจ็กต์ที่ใช้ template นี้กลายเป็น "wing" ใน shared palace
AI สามารถถามว่า "โปรเจ็กต์ไหนเคยทำ auth แบบ JWT มาก่อน" และได้คำตอบโดยไม่ต้องเปิดโปรเจ็กต์นั้น

**โครงสร้าง**
```
~/ai-workspace/
  palace/                        ← shared vector store
    project-alpha/               ← wing ต่อโปรเจ็กต์
    project-beta/
    project-gamma/
  cross-project-memory.md        ← Phase 2 ยังอยู่ เป็น curated summary
```

**workflow**
```
1. โปรเจ็กต์ใหม่ bootstrap → auto-index doc/ เข้า palace เป็น wing ใหม่
2. AI session เริ่ม → ค้น palace ก่อน: "โปรเจ็กต์ไหนเคยแก้ปัญหาคล้ายนี้"
3. พบ match → แสดง pattern + link ไปโปรเจ็กต์ต้นทาง
4. session end → sync doc/ ที่เปลี่ยนกลับเข้า palace
```

**ความสัมพันธ์กับ MemPalace**
ณ จุดนี้ระบบเราและ MemPalace ทำงานบนแนวคิดเดียวกัน
ความแตกต่างคือเรามี structured workflow layer (compliance, task lifecycle, source doc versioning)
ที่ MemPalace ไม่มี — ทำให้ cross-project learning ของเราเชื่อถือได้กว่า
เพราะรู้ว่า pattern ที่เรียนรู้มาผ่าน workflow ที่ถูกต้องมาแล้ว

**สิ่งที่ต้องสร้าง**
- `tools/sync-palace.sh` — sync doc/ เข้า shared palace หลัง session end
- Bootstrap hook: ค้น palace ก่อน bootstrap โปรเจ็กต์ใหม่
- `/search-projects "query"` skill สำหรับ Claude Code
- Privacy boundary: ระบุชัดว่า palace อยู่ที่ไหน และอยู่นอก git เสมอ

---

## 6. Non-Goals (Scope ที่จงใจไม่ทำ)

สิ่งเหล่านี้ไม่ใช่ทิศทางของ template นี้ — มีเหตุผลชัดเจนที่ไม่ทำ

| สิ่งที่ไม่ทำ | เหตุผล |
|-------------|--------|
| **Cloud storage / sync** | template นี้ออกแบบมาให้ทำงาน local-first ข้อมูลต้องอยู่ในมือผู้ใช้ |
| **Replace markdown ด้วย database** | markdown อ่านได้โดยตรง ไม่ต้องการ tool พิเศษ human-readable เสมอ |
| **Build AI agent framework** | เราทำ workflow layer ไม่ใช่ agent framework — ใช้ร่วมกับ tool ใดก็ได้ |
| **Lock-in กับ Claude** | core/ ต้องทำงานกับ AI tool ใดก็ได้ platform layer เป็นแค่ enhancement |
| **Auto-implement feature แทนมนุษย์** | AI เสนอและ draft ได้ แต่มนุษย์ต้อง approve ทุก architectural decision |
| **Replace MemPalace** | Phase 3 ใช้ร่วมกับ MemPalace ได้ ไม่ได้แข่ง — จุดแข็งต่างกัน |
| **Manage production infrastructure** | template ดูแล doc และ workflow เท่านั้น ไม่ยุ่งกับ deploy หรือ ops |
