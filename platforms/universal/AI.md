# AI.md — Universal AI Session Protocol

> **สำหรับผู้ใช้:** ถ้าเปลี่ยน AI tool ให้บอก AI ใหม่ว่า:
> `"อ่าน AI.md แล้ว setup ตัวเองให้พร้อมทำงานในโปรเจ็กต์นี้"`
>
> **สำหรับ AI:** อ่านทีละขั้น ตัดสินใจเองได้ตามเงื่อนไขด้านล่าง

---

## ความเป็นเจ้าของไฟล์ — อ่านก่อน ห้ามข้าม

กฎนี้ป้องกันไม่ให้ AI tool ใดแก้ไฟล์ที่ไม่ใช่ของตัวเอง

### Shared Files — ทุก tool อ่านและเขียนได้

| ไฟล์/โฟลเดอร์ | หน้าที่ |
|--------------|--------|
| `CoreAiWorkspaces/01-plan/work-status.md` | สถานะโปรเจ็กต์ปัจจุบัน |
| `CoreAiWorkspaces/02-task/task-board.md` | task ทั้งหมด |
| `CoreAiWorkspaces/03-log/work-log-index.md` | log รวมทุก session |
| `CoreAiWorkspaces/07-decisions/` | ADR + entity register |
| `CoreAiWorkspaces/06-extensions/` | extension docs |

### Tool-Specific Files — เจ้าของเท่านั้นเขียนได้

| ไฟล์ | เจ้าของ | Tool อื่นทำได้ |
|------|--------|--------------|
| `CLAUDE.md` | Claude Code | อ่านได้ ห้ามแก้ |
| `.cursorrules` | Cursor | อ่านได้ ห้ามแก้ |
| `.windsurfrules` | Windsurf | อ่านได้ ห้ามแก้ |
| `.gemini/instructions.md` | Gemini CLI | อ่านได้ ห้ามแก้ |
| `.github/copilot-instructions.md` | GitHub Copilot | อ่านได้ ห้ามแก้ |
| `CoreAiWorkspaces/03-log/agents/[tool-name].md` | tool นั้นๆ | อ่านได้ ห้ามเขียนทับ |

### System Files — ห้ามแก้ไขหรือลบ

| ไฟล์ | เหตุผล |
|------|--------|
| `AI.md` | universal protocol — แก้โดย human เท่านั้น |
| `CoreAiWorkspaces/04-way-of-work/` | กฎโปรเจ็กต์ — แก้โดย human เท่านั้น |
| `CoreAiWorkspaces/00-source/` | source docs — ห้ามแก้โดยตรง |

---

## ขั้น 1 — ตรวจสอบตัวเอง

ตรวจไฟล์เหล่านี้ใน project root — มี config ของ tool ฉันอยู่แล้วไหม?

| ไฟล์ | Tool |
|------|------|
| `CLAUDE.md` | Claude Code / Claude Projects |
| `.cursorrules` | Cursor |
| `.windsurfrules` | Windsurf |
| `.gemini/instructions.md` | Gemini CLI |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `[tool-name]-setup.md` | tool อื่นๆ |

**พบไฟล์ของฉันแล้ว** → อ่านไฟล์นั้น แล้วไป **ขั้น 3**
**ยังไม่มีไฟล์ของฉัน** → ทำ **ขั้น 2** ก่อน

---

## ขั้น 2 — First-Time Setup (ทำครั้งเดียว)

### 2.1 อ่านบริบทโปรเจ็กต์

อ่านตามลำดับนี้ — **อ่าน AI-CONTEXT block ก่อนเสมอ** อ่าน body ถ้าต้องการ detail:

1. `CoreAiWorkspaces/01-plan/work-status.md` — phase + task ปัจจุบัน + next action
2. `CoreAiWorkspaces/03-log/work-log-index.md` — session ล่าสุดทำอะไร มีอะไรค้าง
3. `CoreAiWorkspaces/02-task/task-board.md` — tasks ทั้งหมด + priority + blocked
4. `CoreAiWorkspaces/04-way-of-work/way-of-work.md` — กฎการทำงาน + ภาษาที่ใช้
5. `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md` — เมื่อไหร่หยุด เมื่อไหร่ทำเองได้
6. `CoreAiWorkspaces/07-decisions/README.md` — decisions ที่ตัดสินใจไปแล้ว
7. `CoreAiWorkspaces/03-log/agents/` — ถ้ามีไฟล์ tool อื่นอยู่ → อ่าน AI-CONTEXT block เพื่อรู้ว่า tool นั้นทำอะไรไว้

### 2.2 สร้าง config ไฟล์ของตัวเอง

สร้างไฟล์ที่ tool ของคุณโหลดอัตโนมัติ โดยใช้ template เนื้อหาด้านล่าง:

```
# [Tool Name] — Session Protocol

อ่าน AI.md ทุกครั้งที่เริ่ม session

## Project Context
- work-status:       CoreAiWorkspaces/01-plan/work-status.md
- task-board:        CoreAiWorkspaces/02-task/task-board.md
- work-log:          CoreAiWorkspaces/03-log/work-log-index.md
- way-of-work:       CoreAiWorkspaces/04-way-of-work/way-of-work.md
- decision-protocol: CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md
- compliance:        CoreAiWorkspaces/04-way-of-work/compliance.md
- adr-index:         CoreAiWorkspaces/07-decisions/README.md

## Session Start → ดู AI.md ขั้น 3
## Session End   → ดู AI.md ขั้น 4

## Key Rules
- ห้าม implement โดยไม่รู้ source reference
- บอก plan ก่อนเขียน code — รอยืนยันก่อน implement
- ห้ามตัดสินใจ architecture โดยไม่สร้าง ADR draft
- ห้ามแก้ไฟล์ของ tool อื่น (ดู "ความเป็นเจ้าของไฟล์" ใน AI.md)
- ถ้าไม่แน่ใจ: Do less, document more
```

### 2.3 เขียน diary แนะนำตัว

สร้างไฟล์ `CoreAiWorkspaces/03-log/agents/[tool-name].md`:

```markdown
<!-- AI-CONTEXT
tool: [tool-name]
joined: [วันที่วันนี้]
status: onboarded
current_task: [อ่านจาก task-board]
-->

## [วันที่] — Onboarding

เข้ามาต่องานจาก: [tool ก่อนหน้า — อ่านจาก work-log หรือ "bootstrap" ถ้าเป็น tool แรก]
บริบทที่เข้าใจ: phase=[...] · active_task=[...] · next=[...]
พร้อมทำงานต่อจาก: [next_action จาก work-status]
```

---

## ขั้น 3 — Session Start (ทำทุก session)

อ่าน AI-CONTEXT block ของ 3 ไฟล์ตามลำดับ:

1. `CoreAiWorkspaces/01-plan/work-status.md`
2. `CoreAiWorkspaces/03-log/work-log-index.md`
3. `CoreAiWorkspaces/02-task/task-board.md`

แล้วรายงานผู้ใช้:
- phase ปัจจุบัน
- task ที่ active + status
- next action ที่ต้องทำก่อน
- blocked tasks (ถ้ามี) พร้อมสาเหตุ

---

## ขั้น 4 — Session End (ทำทุก session)

sync 3 ไฟล์ก่อนปิด session เสมอ:

1. **`work-status.md`** — อัปเดต body + AI-CONTEXT block (phase / active_task / next_action / last_updated)
2. **`work-log-index.md`** — เพิ่ม entry ใหม่ (ทำอะไร / task status / next)
3. **`task-board.md`** — อัปเดต status ของ task ที่เปลี่ยน
4. **diary ของตัวเอง** — `CoreAiWorkspaces/03-log/agents/[tool-name].md` เขียน summary session นี้

**กฎ:** AI-CONTEXT block ต้องสะท้อน body เสมอ — ถ้าไม่ตรงให้เชื่อ body แล้วอัปเดต block

---

## Handoff Protocol — ส่งต่องานให้ tool อื่น

### Tool ปัจจุบัน (ก่อนออก)

1. ทำ Session End ให้ครบ (ขั้น 4)
2. เพิ่ม handoff note ใน `work-log-index.md`:

```markdown
**[Handoff → tool ถัดไป]**
Checkpoint: [งานที่ทำไปถึงไหนแล้ว]
ยังค้าง: [สิ่งที่ยังไม่เสร็จ]
Next action: [สิ่งที่ tool ถัดไปต้องทำก่อนเลย]
```

3. อัปเดต `next_action` ใน work-status ให้ละเอียดที่สุดเท่าที่ทำได้

### Tool ใหม่ (ตอนเข้ามา)

บอก AI ใหม่ว่า: **"อ่าน AI.md แล้ว setup ตัวเองให้พร้อมทำงาน"**
→ AI จะทำขั้น 1-3 เองโดยอัตโนมัติ อ่าน handoff note แล้วทำงานต่อได้ทันที

### กลับมาใช้ tool เดิม (returning tool)

ถ้า config ไฟล์มีอยู่แล้ว → **ไม่ต้อง setup ใหม่**
แค่ทำขั้น 3 (Session Start) ตามปกติ — work-status จะบอกว่าค้างไว้ที่ไหน

---

## Clean Protocol — เมื่อต้องการใช้ tool เดียว

ถ้าตัดสินใจใช้ AI tool เจ้าเดียวและต้องการเคลียร์ tool อื่น:

### สิ่งที่ลบได้ (tool config ของ tool ที่ไม่ใช้แล้ว)

```
CLAUDE.md                          ← ถ้าไม่ใช้ Claude Code อีกต่อไป
.cursorrules                       ← ถ้าไม่ใช้ Cursor อีกต่อไป
.windsurfrules                     ← ถ้าไม่ใช้ Windsurf อีกต่อไป
.gemini/instructions.md            ← ถ้าไม่ใช้ Gemini CLI อีกต่อไป
.github/copilot-instructions.md    ← ถ้าไม่ใช้ Copilot อีกต่อไป
CoreAiWorkspaces/03-log/agents/[tool-name].md  ← diary ของ tool ที่ไม่ใช้
```

### สิ่งที่ห้ามลบเด็ดขาด

```
AI.md                              ← universal protocol — tool ใหม่ยังต้องใช้
CoreAiWorkspaces/                  ← ข้อมูลโปรเจ็กต์ทั้งหมด
```

### วิธี clean (ทำเองหรือบอก AI ให้ทำ)

1. ระบุว่าจะเก็บ tool ไหน: `"ฉันจะใช้แค่ [tool-name] ต่อจากนี้"`
2. AI แสดงรายการไฟล์ที่จะลบก่อน รอยืนยัน
3. ลบเฉพาะ tool config ของ tool ที่ไม่ใช้
4. `CoreAiWorkspaces/` และ `AI.md` ไม่ถูกแตะ

> Claude Code: รัน `/caw-tool-clean` เพื่อทำขั้นตอนนี้แบบ guided

---

*`CoreAiWorkspaces/` คือ single source of truth — tool ใดก็อ่าน/เขียนที่เดียวกัน*
*[ai-project-template](https://github.com/BlackAkuma/ai-project-template)*
