# AI Project Template

ชุด template สำหรับวางโครงสร้างการทำงานร่วมกันระหว่าง **นักพัฒนา** และ **AI** ในโปรเจ็กต์ซอฟต์แวร์ทุกประเภท

---

## ทำไมถึงสร้างสิ่งนี้ขึ้นมา

การทำงานกับ AI หลาย session บนโปรเจ็กต์เดียวกันมักเจอปัญหาเหล่านี้:

- **AI ไม่รู้ว่าทำอะไรไปแล้ว** — ทุก session เริ่มใหม่จากศูนย์ ทำงานซ้ำหรือข้ามสิ่งสำคัญ
- **Requirement เปลี่ยนโดยไม่มีร่องรอย** — ไม่รู้ว่าเปลี่ยนเมื่อไหร่ ทำไม และใครตัดสินใจ
- **AI ตัดสินใจเองในสิ่งที่ไม่ควร** — หรือหยุดชะงักในสิ่งที่ควรตัดสินใจได้เอง
- **หลายคนทำงานไม่ไปทิศทางเดียวกัน** — แต่ละคนใช้ AI คนละแบบ ได้ผลลัพธ์ไม่สอดคล้องกัน

Template ชุดนี้แก้ปัญหาเหล่านั้นด้วยโครงสร้างที่ชัดเจนและ protocol ที่ AI ทุกตัวสามารถทำตามได้

---

## ข้อดีที่ได้จากการใช้

- **Session ต่อกันได้ไม่สะดุด** — AI ใหม่อ่าน status แล้วรู้ทันทีว่าต้องทำอะไรต่อ
- **Requirements ไม่สูญหาย** — source docs เป็น versioned immutable records
- **ทุก task มีที่มา** — traceability จาก task กลับไปถึง requirement จริง
- **AI รู้ขอบเขตตัวเอง** — protocol ชัดเจนว่าตัดสินใจอะไรได้เอง อะไรต้องรอมนุษย์
- **ทีมหลายคนทำงานไปทิศทางเดียวกัน** — ทุกคนยึด template เดียวกัน AI ทุกตัวทำงานตาม standard เดียวกัน
- **ตรวจสอบ code quality อัตโนมัติ** — compliance check ทำงานทุก session จับ violation ก่อนสะสม
- **รองรับโปรเจ็กต์เกม** — skill pack เพิ่ม FDD, game coding standards, asset protocol, playtest, balance check
- **ใช้ได้กับทุก AI tool** — Claude, ChatGPT, Gemini หรือ tool ใดก็ตามที่ทีมใช้
- **Claude Code power layer** — ถ้าใช้ Claude Code ให้ hooks + rules + slash commands ทำงานอัตโนมัติ

---

## โครงสร้าง Template

```
core/           ← ทุกโปรเจ็กต์ใช้ได้ ทุก AI tool
skills/
  game/         ← เปิดใช้อัตโนมัติสำหรับ game / web game
platforms/
  claude-code/  ← สำหรับคนที่ใช้ Claude Code CLI โดยเฉพาะ
```

### ระดับการใช้งาน (Progressive Enhancement)

| ระดับ | ใครใช้ | สิ่งที่ได้ |
|-------|-------|-----------|
| **core/** | ทุกคน ทุก AI tool | session ต่อกันได้ ไม่หลุด ไม่ซ้ำ |
| **+ skills/game/** | นักพัฒนาเกม | FDD, playtest, balance, narrative standards |
| **+ platforms/claude-code/** | Claude Code users | hooks อัตโนมัติ, rules ตาม path, slash commands |

---

## วิธีใช้งานเบื้องต้น

### 1. Clone โฟลเดอร์นี้

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
```

### 2. เตรียมข้อมูลโปรเจ็กต์ใหม่

| ข้อมูล | ตัวอย่าง |
|--------|---------|
| ชื่อโปรเจ็กต์ | `my-game` |
| path ที่จะสร้าง `doc/` | `/projects/my-game` |
| ประเภทโปรเจ็กต์ | app / web / game / mobile |
| source docs | ไฟล์ PRD / spec (ถ้ายังไม่มีพิมพ์ว่า "ยังไม่มี") |

### 3. Copy prompt นี้ให้ AI

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ใหม่

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [PROJECT_ROOT_PATH]
- ประเภท: [app / web / game / mobile]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ขั้นตอน:
1. ถามว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ใน core/ ตามลำดับ (00 → 16)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน skills/game/ ต่อด้วย (00 → 06)
4. สร้างโครงสร้าง doc/ ที่ path ด้านบน
5. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอให้ใส่ placeholder ชัดเจน ห้ามเดา
6. ตรวจสอบกับ core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

### 4. รอ AI ทำงาน แล้วลบโฟลเดอร์ template นี้ทิ้ง

เมื่อ AI รายงานว่าผ่าน checklist แล้ว โฟลเดอร์นี้ลบทิ้งได้เลย

**ถ้าใช้ Claude Code:** setup เพิ่มได้จาก `platforms/claude-code/README.md`

> ดูรายละเอียดเพิ่มเติมใน [QUICKSTART.md](QUICKSTART.md)

---

## core/ — Universal Templates

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Bootstrap Master | ภาพรวม rules ขั้นตอน setup และ skill detection |
| `01` Folder Structure | โครงสร้างโฟลเดอร์มาตรฐานของ `doc/` |
| `02` Source Doc Versioning | การจัดการ requirements แบบ versioned immutable |
| `03` Way of Work | กติกา session protocol, start/stop checklist, pre/post-compact |
| `04` Coding Standards | มาตรฐาน code และ workflow |
| `05` Project Plan | template แผนโปรเจ็กต์ + quality gates (PASS / CONCERNS / FAIL) |
| `06` Work Status | สถานะโปรเจ็กต์ พร้อม AI-CONTEXT block |
| `07` Task Board | task lifecycle + Definition of Ready/Done |
| `08` Log & Summary | บันทึก session และ summary รายวัน/เดือน |
| `09` Extension Doc | extension doc + reverse-document protocol |
| `10` Bootstrap Checklist | ตรวจสอบว่า setup ครบก่อนเริ่มทำงาน |
| `11` AI Decision Protocol | 9 scenarios + responsibility matrix |
| `12` ADR | Architecture Decision Records |
| `13` Retrospective | ทบทวนการทำงานรายช่วง |
| `14` Anti-Patterns | สิ่งที่ไม่ควรทำและเหตุผล |
| `15` Compliance Check | C-01–C-11 + tech debt register |
| `16` Launch Checklist | Pre-release checklist ก่อน deploy จริง |

## skills/game/ — Game Development Skill Pack

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Game Skill Overview | ภาพรวม สิ่งที่เพิ่มจาก core |
| `01` FDD Template | Feature Design Document (FDD-NNN) — เขียนทีละ section รอ approve |
| `02` Game Coding Standards | Config-driven, delta time, logic/render, prototype vs production + G-01–G-07 |
| `03` Asset Protocol | Naming, folder structure, registry (AST-XXX) + A-01–A-04 |
| `04` Playtest Report | template รายงาน playtest พร้อม criteria |
| `05` Balance Check | ตรวจ config values อยู่ใน FDD range + G-07 |
| `06` Narrative Standards | dialogue, localization-ready, character registry + N-01–N-04 |

## platforms/claude-code/ — Claude Code Power Layer

| ส่วน | เนื้อหา |
|-----|--------|
| `CLAUDE.md` | bootstrap อัตโนมัติ ไม่ต้อง copy prompt |
| `hooks/` | session-start, session-stop, pre-compact, validate-commit, detect-gaps |
| `rules/` | core-standards, design-docs, gameplay-code, test-standards (path-scoped) |
| `skills/` | /compliance-check, /session-end, /fdd-create, /adr-create, /scope-check, /launch-check |

---

## ค่าใช้จ่าย Token โดยประมาณ

> ตัวเลขนี้เป็นการประมาณ ขึ้นอยู่กับ AI tool และขนาดโปรเจ็กต์

| สถานการณ์ | Input tokens | Output tokens | รวม |
|----------|-------------|--------------|-----|
| **Setup ครั้งแรก** (core 17 ไฟล์ + สร้าง doc/) | ~12,000 | ~6,000 | **~18,000** |
| **Setup + game skill pack** (+ อีก 7 ไฟล์) | ~15,000 | ~8,000 | **~23,000** |
| **Session ปกติ** (อ่าน AI-CONTEXT + ทำงาน) | ~2,000–5,000 | ~2,000–5,000 | **~4,000–10,000** |
| **Session เบา** (อ่าน block อย่างเดียว orient) | ~500–1,000 | ~500 | **~1,000–1,500** |
| **Archive** (compress log เก่า) | ~3,000–5,000 | ~2,000 | **~5,000–7,000** |

**Setup จ่ายแค่ครั้งเดียว** — session ถัดไปใช้แค่ AI-CONTEXT block ซึ่งถูกกว่าอ่านเอกสารเต็มมาก

สำหรับ Claude Sonnet (ราคาประมาณ):
- Setup ครั้งแรก: **< $0.10 USD**
- Session ปกติ: **$0.01–0.05 USD** ต่อ session

---

## การบริหาร Token ระยะยาว

ไฟล์เอกสารโตขึ้นตามเวลา ถ้าไม่จัดการจะทำให้แต่ละ session ใช้ token มากขึ้นเรื่อย ๆ — ระบบนี้มีกลไกจัดการในตัว:

### AI-CONTEXT Block — อ่านน้อย รู้มาก

ไฟล์หลัก 3 ไฟล์ (work-status, task-board, work-log-index) มี compact English block ด้านบน AI อ่าน block เดียวได้ context ทันทีโดยไม่ต้องอ่าน body ทั้งไฟล์

### Two-Tier Log System — ไม่ทำซ้ำ ไม่บวม

```
Tier 1: Milestone Summary  ← ถาวร ย่อเสมอ AI อ่านเพื่อรู้ว่าทำอะไรไปแล้ว
Tier 2: Recent Sessions    ← เก็บแค่ 20 session ล่าสุด ที่เก่ากว่า archive ไป
```

session เก่าถูก compress เป็น monthly summary ใน `doc/03-log/archive/` — ยังอ่านได้ถ้าต้องการรายละเอียด แต่ไม่โหลดเข้า context ทุก session

### Archive — AI แจ้ง ผู้ใช้ตัดสินใจ

เมื่อไฟล์ถึง threshold (work-log-index > 300 บรรทัด หรือ done tasks > 15 รายการ) AI จะแจ้งเตือนก่อนทำงาน:

```
[INFO] C-12: work-log-index มี 340 บรรทัด
       พิมพ์ "archive logs" หรือ /archive-logs เพื่อ compress session เก่า
```

AI ไม่ archive เองโดยไม่ถาม — ผู้ใช้ตัดสินใจเสมอ

---

## แนวคิดหลัก

| แนวคิด | ความหมาย |
|--------|---------|
| **Source docs = source of truth** | ห้ามแก้ requirement โดยตรง ต้อง version ใหม่เท่านั้น |
| **AI-CONTEXT block** | compact English block ด้านบนไฟล์หลัก AI อ่านก่อนเสมอ ประหยัด token |
| **Two-tier log** | Milestone Summary ถาวร + Recent Sessions หมุนเวียน ป้องกันทำซ้ำและไฟล์บวม |
| **Do less, document more** | หยุดพร้อมบันทึกชัดเจน ดีกว่าตัดสินใจเงียบ ๆ แล้วผิด |
| **Progressive enhancement** | core ใช้ได้กับทุก AI — ยิ่งใช้ platform ลึกขึ้น ยิ่งอัตโนมัติมากขึ้น |
| **Template ใช้ครั้งเดียว** | AI อ่าน → สร้าง `doc/` → ลบโฟลเดอร์ template ทิ้ง |

---

---

# AI Project Template

A template pack for structuring collaboration between **developers** and **AI** on software projects of any type.

---

## Why This Exists

Working with AI across multiple sessions on the same project often leads to these problems:

- **AI doesn't know what was already done** — every session starts from scratch
- **Requirements change without a trace** — no record of when, why, or who decided
- **AI makes decisions it shouldn't** — or stalls on decisions it should handle independently
- **Team members work in different directions** — each person uses AI differently

This template pack solves these problems with a clear structure and a protocol that any AI tool can follow.

---

## Benefits

- **Seamless session continuity** — a new AI session reads the status and immediately knows what to do next
- **Requirements never get lost** — source docs are versioned, immutable records
- **Every task is traceable** — every task traces back to a real requirement
- **AI knows its boundaries** — 9 decision scenarios with explicit protocols
- **Teams stay aligned** — everyone follows the same template; every AI follows the same standards
- **Automatic code quality checks** — compliance checks run every session
- **Game development support** — FDD, playtest, balance check, narrative standards
- **Claude Code power layer** — hooks, rules, and slash commands for full automation

---

## Structure

```
core/           ← used by every project, any AI tool
skills/
  game/         ← auto-activated for game and web game projects
platforms/
  claude-code/  ← for Claude Code CLI users only
```

### Progressive Enhancement

| Layer | Who uses it | What you get |
|-------|-------------|--------------|
| **core/** | Everyone, any AI tool | Sessions stay connected, no drift, full traceability |
| **+ skills/game/** | Game developers | FDD, playtest, balance check, narrative standards |
| **+ platforms/claude-code/** | Claude Code users | Automatic hooks, path-scoped rules, slash commands |

---

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
```

### 2. Copy this prompt to your AI

```
You are about to set up a documentation system for a new software project.

Project details:
- Name: [PROJECT_NAME]
- Path to create doc/ at: [PROJECT_ROOT_PATH]
- Type: [app / web / game / mobile]
- Source docs: [attach files / none yet]
- Goal: [PROJECT_GOAL_SUMMARY]

Steps:
1. Ask what language to use for communication — wait for answer before proceeding
2. Read all files in core/ in order (00 → 16)
3. If the project is a game or web game, also read skills/game/ (00 → 06)
4. Create the doc/ structure at the path above
5. Fill in available project info — use clear placeholders where info is missing, never guess
6. Verify against core/10-bootstrap-checklist-template.md before declaring setup complete
```

### 3. Wait for AI to finish, then delete this template folder

Once AI confirms the checklist passes — delete this folder. The `doc/` directory in your project is what remains.

**If using Claude Code:** see `platforms/claude-code/README.md` for additional setup.

---

## core/ — Universal Templates

| File | Purpose |
|------|---------|
| `00` Bootstrap Master | Rules overview, setup steps, skill detection |
| `01` Folder Structure | Standard `doc/` directory layout |
| `02` Source Doc Versioning | Versioned, immutable requirements management |
| `03` Way of Work | Session protocol, start/stop checklists, pre/post-compact |
| `04` Coding Standards | Code and workflow standards |
| `05` Project Plan | Project plan + quality gates (PASS / CONCERNS / FAIL) |
| `06` Work Status | Project status with AI-CONTEXT block |
| `07` Task Board | Task lifecycle + Definition of Ready/Done |
| `08` Log & Summary | Session logs and daily/monthly summaries |
| `09` Extension Doc | Extension docs + reverse-document protocol |
| `10` Bootstrap Checklist | Verify setup is complete before starting work |
| `11` AI Decision Protocol | 9 ambiguous scenarios with explicit if/then guidance |
| `12` ADR | Architecture Decision Records — never deleted, only superseded |
| `13` Retrospective | Periodic collaboration review |
| `14` Anti-Patterns | What not to do, and why |
| `15` Compliance Check | C-01–C-11 + tech debt register |
| `16` Launch Checklist | Pre-release checklist before deploying |

## skills/game/ — Game Development Skill Pack

| File | Purpose |
|------|---------|
| `00` Game Skill Overview | When to activate, what changes from core |
| `01` FDD Template | Feature Design Document (FDD-NNN) — one section at a time |
| `02` Game Coding Standards | Config-driven, delta time, logic/render, prototype vs production + G-01–G-07 |
| `03` Asset Protocol | Naming, folder structure, registry (AST-XXX) + A-01–A-04 |
| `04` Playtest Report | Structured playtest findings template |
| `05` Balance Check | Validate config values against FDD ranges + G-07 |
| `06` Narrative Standards | Dialogue, localization-ready strings, character registry + N-01–N-04 |

## platforms/claude-code/ — Claude Code Power Layer

| Section | Content |
|---------|---------|
| `CLAUDE.md` | Auto-loaded bootstrap — no copy-paste prompt needed |
| `hooks/` | session-start, session-stop, pre-compact, validate-commit, detect-gaps |
| `rules/` | core-standards, design-docs, gameplay-code, test-standards (path-scoped) |
| `skills/` | /compliance-check, /session-end, /fdd-create, /adr-create, /scope-check, /launch-check |

---

## Token Management Over Time

Documentation files grow with every session. Without management, each session consumes more tokens over time — this system has built-in mechanisms to prevent that.

### AI-CONTEXT Block — Read less, know more

The 3 key files (work-status, task-board, work-log-index) have a compact English block at the top. AI reads this block alone to get full context without reading the entire file body.

### Two-Tier Log System — No repetition, no bloat

```
Tier 1: Milestone Summary  ← permanent, always compact — AI reads this to know what's been done
Tier 2: Recent Sessions    ← keeps only last 20 sessions — older ones are archived
```

Old sessions are compressed into monthly summaries in `doc/03-log/archive/` — still readable if detail is needed, but not loaded into context every session.

### Archive — AI alerts, user decides

When files reach threshold (work-log-index > 300 lines or done tasks > 15 items), AI notifies before starting work:

```
[INFO] C-12: work-log-index has 340 lines
       Type "archive logs" or /archive-logs to compress old sessions
```

AI never archives without being asked — the user always decides.

---

## Key Concepts

| Concept | Meaning |
|---------|---------|
| **Source docs = source of truth** | Requirements are never edited directly — changes create a new version |
| **AI-CONTEXT block** | Compact English block at the top of key files — AI reads this first to minimize token usage |
| **Two-tier log** | Permanent Milestone Summary + rotating Recent Sessions — prevents repetition and file bloat |
| **Do less, document more** | A well-documented stop is better than a silent wrong decision |
| **Progressive enhancement** | core works standalone — deeper platform layers add automation |
| **One-time-use template** | AI reads → creates `doc/` → template folder is deleted |

---

## License

MIT
