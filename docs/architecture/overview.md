---
title: ภาพรวมระบบ — Session Protocol & CoreAiWorkspaces/ Structure
---

# ภาพรวมระบบ

ระบบนี้แก้ปัญหาหลักของการทำงานกับ AI: **AI ไม่มี memory ข้าม session**

แทนที่จะพึ่ง AI memory ระบบนี้เก็บ state ทุกอย่างไว้ใน `CoreAiWorkspaces/` folder บน filesystem — AI แค่อ่านไฟล์แล้วรู้ทันทีว่าอยู่ที่ไหน ต้องทำอะไร และตัดสินใจอะไรไปแล้ว

→ [How It Works (Visual)](how-it-works.html) | [Workflow Diagram](workflow-diagram.html)

---

## โครงสร้าง CoreAiWorkspaces/ — ทุกอย่างอยู่ที่นี่

```
CoreAiWorkspaces/
├── 00-source/              ← source of truth ของโปรเจ็กต์
│   ├── README.md           ← index ของ source docs ทั้งหมด
│   └── versions/           ← version history ของ docs (ถ้ามี)
│
├── 01-plan/                ← สถานะและแผนงาน
│   ├── work-status.md      ← *** ไฟล์สำคัญที่สุด — อ่านทุก session ***
│   └── project-plan.md     ← milestones และ timeline
│
├── 02-task/                ← งานที่ต้องทำ
│   └── task-board.md       ← task list พร้อม status, priority, reference
│
├── 03-log/                 ← บันทึกทุก session
│   ├── work-log-index.md   ← master log รวมทุก session
│   └── agents/             ← (optional) แยก diary ต่อ AI tool
│       ├── claude-code.md
│       └── claude-ai.md
│
├── 04-way-of-work/         ← กฎและ protocol ของโปรเจ็กต์
│   ├── way-of-work.md      ← communication rules, git workflow
│   ├── ai-decision-protocol.md ← AI ทำอะไรได้ / ต้องหยุดเมื่อไหร่
│   ├── compliance.md       ← ข้อกำหนด C-01 ถึง C-22
│   └── tacp.md             ← Token-Aware Communication Protocol (TACP)
│
└── 07-decisions/           ← บันทึก architectural decisions
    ├── README.md            ← ADR index (ดู status ทุก decision)
    ├── entity-register.md   ← track tech choices และ dependencies
    └── ADR-NNN-title.md    ← decision records แต่ละรายการ
```

**หมายเหตุ:** `08-design/` จะถูกสร้างเพิ่มสำหรับ game projects โดยอัตโนมัติ

---

## Package Concept — Template ติดตั้งแล้วลบทิ้งได้

Template ทำงานแบบ "package" — ติดตั้งครั้งเดียวแล้วแจกจ่ายไปยังตำแหน่งที่ถูกต้อง จากนั้นลบได้เลย

### โครงสร้าง Template Package (สิ่งที่ดาวน์โหลด)

```
_template/
├── core/                       ← 22 AI reading templates
│   ├── 00-ai-bootstrap-master-template.md
│   ├── 01-folder-structure-template.md
│   └── ... (00–21)
│
├── platforms/claude-code/
│   ├── CLAUDE.md               ← จะถูก install → project root
│   └── skills/
│       ├── caw-session-end.md  ┐
│       ├── caw-adr-create.md   │ จะถูก install →
│       ├── caw-compliance-check.md  │ .claude/commands/
│       └── ... (10 commands)   ┘
│
├── scripts/
│   ├── new-project.sh          ← bootstrap script
│   └── validate-commit.sh      ← จะถูก install → .git/hooks/
│
└── skills/game/                ← optional game skill pack
```

### สิ่งที่ `new-project.sh` แจกจ่ายไปยังโปรเจ็กต์

```
new-project.sh อ่านจาก _template/ แล้วติดตั้ง:

CLAUDE.md           → [project root]/CLAUDE.md
                       (Claude Code โหลดอัตโนมัติทุก session)

skills/caw-*.md     → [project root]/.claude/commands/
                       (slash commands พร้อมใช้ทันที)

validate-commit.sh  → [project root]/.git/hooks/validate-commit
                       (ตรวจ deprecated entities ก่อน commit)

[templates]         → [project root]/CoreAiWorkspaces/
                       (สร้าง workspace structure ใหม่)
```

### โครงสร้างโปรเจ็กต์หลัง Bootstrap + ลบ _template/

```
my-project/
│
├── CLAUDE.md                       ← Claude Code อ่านทุก session
│
├── .claude/
│   └── commands/                   ← slash commands ของระบบนี้
│       ├── caw-session-end.md      /caw-session-end
│       ├── caw-adr-create.md       /caw-adr-create
│       ├── caw-compliance-check.md /caw-compliance-check
│       ├── caw-scope-check.md      /caw-scope-check
│       ├── caw-fdd-create.md       /caw-fdd-create
│       ├── caw-launch-check.md     /caw-launch-check
│       ├── caw-archive-logs.md     /caw-archive-logs
│       └── caw-update.md           /caw-update
│
├── .git/hooks/
│   └── validate-commit             ← ตรวจก่อน commit อัตโนมัติ
│
├── CoreAiWorkspaces/               ← AI working folder
│   ├── 00-source/                  source of truth documents
│   ├── 01-plan/
│   │   └── work-status.md          *** อ่านทุก session ***
│   ├── 02-task/
│   │   └── task-board.md
│   ├── 03-log/
│   │   └── work-log-index.md
│   ├── 04-way-of-work/
│   │   ├── way-of-work.md
│   │   ├── ai-decision-protocol.md
│   │   └── compliance.md
│   └── 07-decisions/
│       ├── README.md               ADR index
│       └── entity-register.md
│
└── [source code ของโปรเจ็กต์]     ← ไม่ถูกแตะโดย template
```

**หลักการ:** `_template/` ทำหน้าที่แล้วหายไป — `CoreAiWorkspaces/` ที่สร้างอยู่ด้วยตัวเองได้โดยไม่ต้องพึ่ง template อีกต่อไป

---

## AI-CONTEXT Block — หัวใจของระบบ

ทุกไฟล์หลักมี AI-CONTEXT block ที่ด้านบน — เป็น YAML comment ที่ AI อ่านเพื่อรู้สถานะล่าสุดโดยไม่ต้องอ่านทั้งไฟล์

```yaml
<!-- AI-CONTEXT
phase: implementation
milestone: M2 - Core Features
active_task: T-012 - Payment Integration
last_session: 2026-05-08
status: in_progress
next_action: เชื่อม Stripe webhook กับ order confirmation
git_mode: branch-separated
git_dev_branch: dev
git_prod_branch: master
read_more:
  architecture: CoreAiWorkspaces/07-decisions/README.md
  entities:     CoreAiWorkspaces/07-decisions/entity-register.md
-->
```

**กฎ:** AI-CONTEXT block ต้องเป็นข้อมูลจริงเสมอ — ไม่ใช่ template placeholder

---

## Session Start Protocol

ทำตามลำดับนี้ทุก session โดยไม่มีข้อยกเว้น:

### ขั้น 1: อ่าน work-status.md

```
อ่าน AI-CONTEXT block ของ CoreAiWorkspaces/01-plan/work-status.md

ตรวจ:
- ถ้า git_mode: branch-separated → รัน git branch --show-current
- ถ้า branch == git_prod_branch (master) → หยุดทันที แจ้งผู้ใช้
- ถ้า read_more มี hints → แสดงให้ผู้ใช้เห็น
```

### ขั้น 2: อ่าน work-log-index.md

```
อ่าน AI-CONTEXT block ของ CoreAiWorkspaces/03-log/work-log-index.md
→ รู้ว่า session ล่าสุดทำอะไร, มีอะไรที่ยังค้างอยู่
```

### ขั้น 3: อ่าน task-board.md

```
อ่าน AI-CONTEXT block ของ CoreAiWorkspaces/02-task/task-board.md
→ รู้ว่า task ไหน active, priority อะไร, blocked ไหม
```

### ขั้น 4: อ่าน agent diary (ถ้ามี)

```
ถ้า CoreAiWorkspaces/03-log/agents/[tool].md มีอยู่ → อ่าน AI-CONTEXT block
→ รู้ว่า tool นี้ทำอะไรไปแล้วใน sessions ที่ผ่านมา
```

### ขั้น 5: ตรวจ compliance

รัน compliance scan ดู gaps และ violations ก่อนเริ่มทำงาน

### ขั้น 6: รายงานสถานะ

AI รายงาน:
- phase ปัจจุบัน
- task ที่ active และ status
- สิ่งที่ต้องทำก่อนตามลำดับ
- ถ้ามี blocked tasks → ระบุว่าบล็อคอยู่เพราะอะไร

**ใช้เวลา:** ~1–2 นาที ได้ context ครบ

---

## Session End Protocol

ก่อนจบ session ทุกครั้ง — รัน `/caw-session-end` หรือทำด้วยมือ:

### 1. อัปเดต work-status.md

```markdown
<!-- ต้องอัปเดตทั้ง body และ AI-CONTEXT block -->

**สิ่งที่อัปเดต:**
- phase (ถ้าเปลี่ยน)
- active_task (task ปัจจุบัน)
- last_session (วันที่วันนี้)
- next_action (สิ่งที่ต้องทำ session ต่อไป)
```

### 2. เพิ่ม entry ใน work-log-index.md

```markdown
## [วันที่] Session N — [หัวข้อหลัก]

**ทำอะไร:** สรุปย่อ 2–3 บรรทัด
**Task:** T-XXX → [status ใหม่]
**Decision:** ถ้ามี decision สำคัญ
**Next:** สิ่งที่ต้องทำ session ต่อไป
```

### 3. อัปเดต task-board.md

```markdown
- เปลี่ยน status ของ tasks ที่เสร็จหรือเปลี่ยนแปลง
- tasks ที่ยัง in-progress → mark เป็น:
  [IN_PROGRESS: checkpoint saved — <สิ่งที่ทำไปแล้ว>]
```

### 4. Push (ถ้า git_mode: branch-separated)

```bash
git push origin dev
```

---

## Task Board — รูปแบบและ Status

```markdown
## Active Tasks

| ID | Task | Status | Priority | Source Ref |
|----|------|--------|----------|-----------|
| T-001 | Setup database schema | ✅ done | P1 | PRD v1.2 §3 |
| T-002 | Implement auth flow | 🔄 in_progress | P1 | PRD v1.2 §4 |
| T-003 | Build dashboard UI | ⏳ next | P2 | Design spec §2 |
| T-004 | Payment integration | 🚫 blocked | P1 | Waiting ADR-003 |
```

**Status tags:**
- `✅ done` — เสร็จสมบูรณ์
- `🔄 in_progress` — กำลังทำ
- `⏳ next` — รอทำถัดไป
- `🚫 blocked` — รอบางอย่าง
- `[IN_PROGRESS: checkpoint saved — ...]` — ค้างไว้ระหว่าง session

---

## Decision Protocol — AI ทำอะไรได้ / ต้องหยุดเมื่อไหร่

ดูรายละเอียดทั้งหมดใน `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`

**สรุปสั้น:**

| Scenario | AI ทำอะไร |
|---------|----------|
| Task คลุมเครือ | STOP — เขียน [BLOCKED], อธิบายว่าต้องการข้อมูลอะไร |
| Source doc ขัดแย้งกับ code | Flag ทั้งคู่ — ไม่แก้เงียบ |
| Scope creep เจอระหว่างทำ | ทำเฉพาะ scope เดิม — log งานใหม่เป็น task ใหม่ |
| Bug นอก scope | อย่าแก้ — log เป็น T-XXX [FOUND-IN-PASSING] |
| ต้องตัดสินใจ architecture | สร้าง ADR draft — ไม่ตัดสินใจเอง |
| ไม่มีข้อมูลเพียงพอ | Placeholder `<NEEDS_CLARIFICATION: ...>` — ไม่เดา |

**กฎทอง:** Do less, document more — การหยุดที่มีการบันทึกดีกว่าการตัดสินใจผิดที่เงียบงัน

---

## Compliance System

`CoreAiWorkspaces/04-way-of-work/compliance.md` มี rules C-01 ถึง C-22

Rules หลักที่ AI ตรวจทุก session:
- **C-01:** ไม่ implement โดยไม่มี source reference
- **C-02:** บอก plan ก่อนเขียน code — รอยืนยัน
- **C-03:** ห้ามแก้ requirements โดยตรง
- **C-04:** ทุก architecture decision ต้องมี ADR draft
- **C-14:** เจอ `[ENTITY:deprecated]` → ตรวจ entity-register ก่อนใช้
- **C-20:** ถ้า vector_memory: enabled และ CoreAiWorkspaces/ เปลี่ยน → re-index ก่อนจบ

รัน compliance scan ด้วย: `/caw-compliance-check`

---

→ ต่อไป: [TACP — Token Savings](tacp.md) | [Memory System](memory-system.md) | [ADR System](adr-system.md) | [Visual: How It Works](how-it-works.html)
