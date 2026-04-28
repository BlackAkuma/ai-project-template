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
- **รองรับโปรเจ็กต์เกม** — skill pack เพิ่ม FDD, game coding standards, asset protocol โดยเฉพาะ
- **ใช้ได้กับทุก AI tool** — Claude, ChatGPT, Gemini หรือ tool ใดก็ตามที่ทีมใช้

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
| เป้าหมายสั้น ๆ | "เกม puzzle บน browser" |

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
2. อ่านไฟล์ทุกไฟล์ใน core/ ตามลำดับ (00 → 15)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน skills/game/ ต่อด้วย (00 → 03)
4. สร้างโครงสร้าง doc/ ที่ path ด้านบน
5. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอให้ใส่ placeholder ชัดเจน ห้ามเดา
6. ตรวจสอบกับ core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

### 4. รอ AI ทำงาน แล้วลบโฟลเดอร์ template นี้ทิ้ง

เมื่อ AI รายงานว่าผ่าน checklist แล้ว โฟลเดอร์นี้ลบทิ้งได้เลย — `doc/` ในโปรเจ็กต์ของคุณคือสิ่งที่เหลือไว้

> ดูรายละเอียดเพิ่มเติมใน [QUICKSTART.md](QUICKSTART.md)

---

## โครงสร้าง Template

```
core/        ← ทุกโปรเจ็กต์ใช้ (app, web, game, mobile)
skills/
  game/      ← เปิดใช้อัตโนมัติเมื่อโปรเจ็กต์เป็น game หรือ web game
```

### core/ — Universal Templates

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Bootstrap Master | ภาพรวม rules ขั้นตอน setup และ skill detection |
| `01` Folder Structure | โครงสร้างโฟลเดอร์มาตรฐานของ `doc/` |
| `02` Source Doc Versioning | การจัดการ requirements แบบ versioned immutable |
| `03` Way of Work | กติกา session protocol และ language policy |
| `04` Coding Standards | มาตรฐาน code และ workflow |
| `05` Project Plan | template แผนโปรเจ็กต์ + quality gates (PASS / CONCERNS / FAIL) |
| `06` Work Status | สถานะโปรเจ็กต์ พร้อม AI-CONTEXT block |
| `07` Task Board | จัดการ task lifecycle (todo → design_validate → in_progress → review → done) |
| `08` Log & Summary | บันทึก session และ summary รายวัน/เดือน |
| `09` Extension Doc | เอกสารขยายที่ไม่ใช่ source doc |
| `10` Bootstrap Checklist | ตรวจสอบว่า setup ครบก่อนเริ่มทำงาน |
| `11` AI Decision Protocol | กฎว่า AI ตัดสินใจอะไรได้เอง อะไรต้องถาม + 7 scenarios |
| `12` ADR | บันทึก architectural decisions — ห้ามลบ แก้ได้แค่ supersede |
| `13` Retrospective | ทบทวนการทำงานรายช่วง |
| `14` Anti-Patterns | สิ่งที่ไม่ควรทำและเหตุผล |
| `15` Compliance Check | ตรวจ code quality อัตโนมัติทุก session (C-01 ถึง C-10) |

### skills/game/ — Game Development Skill Pack

เปิดใช้งานอัตโนมัติเมื่อโปรเจ็กต์เป็น game หรือ web game

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Game Skill Overview | ภาพรวม สิ่งที่เพิ่มจาก core และ task lifecycle ที่ปรับสำหรับ game |
| `01` FDD Template | Feature Design Document (FDD-NNN) — ออกแบบทีละ section รอ approve ก่อนโค้ด |
| `02` Game Coding Standards | Config-driven values, delta time, logic/render separation + G-01 ถึง G-05 |
| `03` Asset Protocol | Naming convention, folder structure, asset registry (AST-XXX) + A-01 ถึง A-04 |

---

## แนวคิดหลัก

| แนวคิด | ความหมาย |
|--------|---------|
| **Source docs = source of truth** | ห้ามแก้ requirement โดยตรง ต้อง version ใหม่เท่านั้น |
| **AI-CONTEXT block** | ทุกไฟล์หลักมี compact English block ด้านบน AI อ่านก่อนเสมอ ประหยัด token |
| **Do less, document more** | หยุดพร้อมบันทึกชัดเจน ดีกว่าตัดสินใจเงียบ ๆ แล้วผิด |
| **Traceability ทุก task** | trace กลับถึง requirement ได้ทุก task ผ่าน T-XXX → source doc |
| **Template ใช้ครั้งเดียว** | AI อ่าน → สร้าง `doc/` → ลบโฟลเดอร์ template ทิ้ง |

---

---

# AI Project Template

A template pack for structuring collaboration between **developers** and **AI** on software projects of any type.

---

## Why This Exists

Working with AI across multiple sessions on the same project often leads to these problems:

- **AI doesn't know what was already done** — every session starts from scratch, repeating work or skipping important steps
- **Requirements change without a trace** — no record of when, why, or who decided
- **AI makes decisions it shouldn't** — or stalls on decisions it should handle independently
- **Team members work in different directions** — each person uses AI differently, producing inconsistent results

This template pack solves these problems with a clear structure and a protocol that any AI tool can follow.

---

## Benefits

- **Seamless session continuity** — a new AI session reads the status and immediately knows what to do next
- **Requirements never get lost** — source docs are versioned, immutable records
- **Every task is traceable** — every task traces back to a real requirement
- **AI knows its boundaries** — clear protocol for what it can decide independently vs. what requires human input
- **Teams stay aligned** — everyone follows the same template; every AI tool follows the same standards
- **Automatic code quality checks** — compliance checks run every session, catching violations before they accumulate
- **Game development support** — skill pack adds FDD, game coding standards, and asset protocol
- **Works with any AI tool** — Claude, ChatGPT, Gemini, or whatever tool your team uses

---

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
```

### 2. Prepare your project details

| Info | Example |
|------|---------|
| Project name | `my-game` |
| Path to create `doc/` | `/projects/my-game` |
| Project type | app / web / game / mobile |
| Source docs | PRD / spec files (type "none yet" if unavailable) |
| Short goal | "Browser-based puzzle game" |

### 3. Copy this prompt to your AI

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
2. Read all files in core/ in order (00 → 15)
3. If the project is a game or web game, also read skills/game/ (00 → 03)
4. Create the doc/ structure at the path above
5. Fill in available project info — use clear placeholders where info is missing, never guess
6. Verify against core/10-bootstrap-checklist-template.md before declaring setup complete
```

### 4. Wait for AI to finish, then delete this template folder

Once AI confirms the checklist passes — delete this folder. The `doc/` directory in your project is what remains.

> See [QUICKSTART.md](QUICKSTART.md) for a step-by-step walkthrough.

---

## Structure

```
core/        ← used by every project (app, web, game, mobile)
skills/
  game/      ← auto-activated for game and web game projects
```

### core/ — Universal Templates

| File | Purpose |
|------|---------|
| `00` Bootstrap Master | Rules overview, setup steps, and skill detection |
| `01` Folder Structure | Standard `doc/` directory layout |
| `02` Source Doc Versioning | Versioned, immutable requirements management |
| `03` Way of Work | Session protocol and language policy |
| `04` Coding Standards | Code and workflow standards |
| `05` Project Plan | Project plan template + quality gates (PASS / CONCERNS / FAIL) |
| `06` Work Status | Project status with AI-CONTEXT block |
| `07` Task Board | Task lifecycle (todo → design_validate → in_progress → review → done) |
| `08` Log & Summary | Session logs and daily/monthly summaries |
| `09` Extension Doc | Non-source supplemental documents |
| `10` Bootstrap Checklist | Verify setup is complete before starting work |
| `11` AI Decision Protocol | What AI decides vs. escalates — 7 ambiguous scenarios covered |
| `12` ADR | Architecture Decision Records — never deleted, only superseded |
| `13` Retrospective | Periodic collaboration review |
| `14` Anti-Patterns | What not to do, and why |
| `15` Compliance Check | Automatic code quality scan every session (C-01 to C-10) |

### skills/game/ — Game Development Skill Pack

Auto-activated when the project is identified as a game or web game.

| File | Purpose |
|------|---------|
| `00` Game Skill Overview | When to activate, what changes from core, adjusted task lifecycle |
| `01` FDD Template | Feature Design Document (FDD-NNN) — write one section at a time, approve before coding |
| `02` Game Coding Standards | Config-driven values, delta time, logic/render separation + G-01 to G-05 |
| `03` Asset Protocol | Naming convention, folder structure, asset registry (AST-XXX) + A-01 to A-04 |

---

## Key Concepts

| Concept | Meaning |
|---------|---------|
| **Source docs = source of truth** | Requirements are never edited directly — changes create a new version |
| **AI-CONTEXT block** | Compact English block at the top of key files — AI reads this first to minimize token usage |
| **Do less, document more** | A well-documented stop is better than a silent wrong decision |
| **Full traceability** | Every task traces back to a requirement via T-XXX → source doc |
| **One-time-use template** | AI reads → creates `doc/` → template folder is deleted |

---

## License

MIT
