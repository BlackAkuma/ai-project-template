# AI Project Template

ชุด template สำหรับวางโครงสร้างการทำงานร่วมกันระหว่าง **นักพัฒนา** และ **AI** ในโปรเจ็กต์ซอฟต์แวร์

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
- **ใช้ได้กับทุกประเภทโปรเจ็กต์** — app, web, game, mobile ใช้ได้หมด ไม่ผูกกับ stack ใด

---

## วิธีใช้งานเบื้องต้น

### 1. Clone โฟลเดอร์นี้

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
```

### 2. เตรียมข้อมูลโปรเจ็กต์ใหม่

| ข้อมูล | ตัวอย่าง |
|--------|---------|
| ชื่อโปรเจ็กต์ | `my-app` |
| path ที่จะสร้าง `doc/` | `/projects/my-app` |
| source docs | ไฟล์ PRD / spec (ถ้ายังไม่มีพิมพ์ว่า "ยังไม่มี") |
| เป้าหมายสั้น ๆ | "แอปจองคิวออนไลน์" |

### 3. Copy prompt นี้ให้ AI

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ใหม่

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [PROJECT_ROOT_PATH]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ข้อกำหนด:
- ถามฉันก่อนว่าจะสื่อสารกันเป็นภาษาอะไร
- กระบวนการคิดภายใน: ใช้ภาษาอังกฤษเพื่อประหยัด token
- AI-CONTEXT block ในไฟล์: ใช้ภาษาอังกฤษเสมอ
- output และเอกสาร: ใช้ภาษาที่ตกลงกัน

ขั้นตอน:
1. ถามภาษาที่จะใช้สื่อสาร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ในโฟลเดอร์ template นี้ตามลำดับใน README.md
3. สร้างโครงสร้าง doc/ ที่ path ด้านบน
4. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอให้ใส่ placeholder ชัดเจน ห้ามเดา
5. ตรวจสอบกับ 10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

### 4. รอ AI ทำงาน แล้วลบโฟลเดอร์ template นี้ทิ้ง

เมื่อ AI รายงานว่าผ่าน checklist แล้ว โฟลเดอร์นี้ลบทิ้งได้เลย — `doc/` ในโปรเจ็กต์ของคุณคือสิ่งที่เหลือไว้

> ดูรายละเอียดเพิ่มเติมใน [QUICKSTART.md](QUICKSTART.md)

---

## โครงสร้าง Template

```
core/        ← ทุกโปรเจ็กต์ใช้
skills/
  game/      ← โปรเจ็กต์เกมและ web game
```

### core/ — Universal Templates

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Bootstrap Master | ภาพรวม rules ขั้นตอน setup และ skill detection |
| `01` Folder Structure | โครงสร้างโฟลเดอร์มาตรฐาน |
| `02` Source Doc Versioning | การจัดการ requirements แบบ versioned |
| `03` Way of Work | กติกา session protocol และ language policy |
| `04` Coding Standards | มาตรฐาน code และ workflow |
| `05` Project Plan | template แผนโปรเจ็กต์ + quality gates (PASS/CONCERNS/FAIL) |
| `06` Work Status | สถานะโปรเจ็กต์ พร้อม AI-CONTEXT block |
| `07` Task Board | จัดการ task lifecycle (design_validate → in_progress → review → done) |
| `08` Log & Summary | บันทึก session และ summary รายวัน/เดือน |
| `09` Extension Doc | เอกสารขยายที่ไม่ใช่ source doc |
| `10` Bootstrap Checklist | ตรวจสอบว่า setup ครบก่อน deploy |
| `11` AI Decision Protocol | กฎว่า AI ตัดสินใจอะไรได้เอง อะไรต้องถาม |
| `12` ADR | บันทึก architectural decisions |
| `13` Retrospective | ทบทวนการทำงานรายช่วง |
| `14` Anti-Patterns | สิ่งที่ไม่ควรทำ |
| `15` Compliance Check | ตรวจ code quality อัตโนมัติทุก session |

### skills/game/ — Game Development Skill Pack

เปิดใช้งานอัตโนมัติเมื่อโปรเจ็กต์เป็น game หรือ web game

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Game Skill Overview | ภาพรวม เมื่อไหร่ใช้ และสิ่งที่เพิ่มจาก core |
| `01` FDD Template | Feature Design Document — ออกแบบก่อนโค้ด |
| `02` Game Coding Standards | Config-driven, delta time, logic/render separation |
| `03` Asset Protocol | Naming convention, folder structure, registry |

---

## หลักการออกแบบ

- **Source docs คือ source of truth** — ห้ามแก้ requirement โดยตรง ต้อง version ใหม่เท่านั้น
- **AI อ่าน AI-CONTEXT block ก่อน** — 3 ไฟล์หลักมี compact block ด้านบนเพื่อประหยัด token
- **ทุก task มี traceability** — trace กลับถึง requirement ได้ทุก task
- **Do less, document more** — AI หยุดพร้อมบันทึกชัดเจน ดีกว่าตัดสินใจเงียบ ๆ แล้วผิด
- **ใช้ได้กับทุก AI tool** — Claude, ChatGPT, Gemini หรือ tool ใดก็ตามที่ทีมใช้

---

---

# AI Project Template

A template pack for structuring collaboration between **developers** and **AI** on software projects.

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
- **Works for any project type** — app, web, game, mobile — not tied to any specific stack

---

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
```

### 2. Prepare your project details

| Info | Example |
|------|---------|
| Project name | `my-app` |
| Path to create `doc/` | `/projects/my-app` |
| Source docs | PRD / spec files (type "none yet" if unavailable) |
| Short goal | "Online queue booking app for restaurants" |

### 3. Copy this prompt to your AI

```
You are about to set up a documentation system for a new software project.

Project details:
- Name: [PROJECT_NAME]
- Path to create doc/ at: [PROJECT_ROOT_PATH]
- Source docs: [attach files / none yet]
- Goal: [PROJECT_GOAL_SUMMARY]

Requirements:
- First ask what language we should communicate in
- Internal reasoning: use English to save tokens
- AI-CONTEXT blocks in files: always English
- Output and documents: use the agreed language

Steps:
1. Ask what language to use for communication — wait for answer before proceeding
2. Read all files in this template folder in the order listed in README.md
3. Create the doc/ structure at the path above
4. Fill in available project info — use clear placeholders where info is missing, never guess
5. Verify against 10-bootstrap-checklist-template.md before declaring setup complete
```

### 4. Wait for AI to finish, then delete this template folder

Once AI confirms the checklist passes — delete this folder. The `doc/` directory in your project is what remains.

> See [QUICKSTART.md](QUICKSTART.md) for a step-by-step walkthrough.

---

## Structure

```
core/        ← used by every project
skills/
  game/      ← activated for game and web game projects
```

### core/ — Universal Templates

| File | Purpose |
|------|---------|
| `00` Bootstrap Master | Rules overview, setup steps, and skill detection |
| `01` Folder Structure | Standard directory layout |
| `02` Source Doc Versioning | Versioned requirements management |
| `03` Way of Work | Session protocol and language policy |
| `04` Coding Standards | Code and workflow standards |
| `05` Project Plan | Project plan template + quality gates (PASS/CONCERNS/FAIL) |
| `06` Work Status | Project status with AI-CONTEXT block |
| `07` Task Board | Task lifecycle (design_validate → in_progress → review → done) |
| `08` Log & Summary | Session logs and daily/monthly summaries |
| `09` Extension Doc | Non-source supplemental documents |
| `10` Bootstrap Checklist | Verify setup is complete before starting |
| `11` AI Decision Protocol | Rules for what AI decides vs. escalates |
| `12` ADR | Architecture Decision Records |
| `13` Retrospective | Periodic collaboration review |
| `14` Anti-Patterns | What not to do |
| `15` Compliance Check | Automatic code quality scan every session |

### skills/game/ — Game Development Skill Pack

Auto-activated when the project is a game or web game.

| File | Purpose |
|------|---------|
| `00` Game Skill Overview | When to use and what it adds on top of core |
| `01` FDD Template | Feature Design Document — design before code |
| `02` Game Coding Standards | Config-driven values, delta time, logic/render separation |
| `03` Asset Protocol | Naming convention, folder structure, asset registry |

---

## Design Principles

- **Source docs are the source of truth** — requirements are never edited directly; changes create a new version
- **AI reads AI-CONTEXT blocks first** — 3 key files have compact blocks at the top to minimize token usage
- **Every task has traceability** — every task can be traced back to a requirement
- **Do less, document more** — a well-documented stop is better than a silent wrong decision
- **Works with any AI tool** — Claude, ChatGPT, Gemini, or whatever tool your team uses

---

## License

MIT
