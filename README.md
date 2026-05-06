# AI Project Template

**A structured collaboration system for developers and AI — across every session, every tool, every team size.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/BlackAkuma?style=flat&logo=github&color=pink)](https://github.com/sponsors/BlackAkuma)

📖 **[See How It Works →](https://blackakuma.github.io/ai-project-template/how-it-works.html)**

---

## What's New

- **49 game specialist agents** (Claude Code) — full game studio in your terminal: Creative/Technical Directors, all programmer roles (lead, gameplay, engine, AI, network, UI, tools, devops, security), all design disciplines, QA, Audio, Narrative, and 15 engine specialists (5× Godot · 5× Unity · 5× Unreal). Invoke `/game-review` for milestone gate review across all specialist agents.
- **33 Thinking Frames** — specialist reasoning embedded in `skills/game/00` for **any AI tool** (ChatGPT, Gemini, Copilot): structured analysis from Game Designer, Narrative Director, GAS Specialist, UMG Specialist, and 29 more roles — no Claude Code required
- **`scripts/new-project.sh`** — one-command bootstrap: creates a complete `doc/` structure from templates in seconds (`--game` flag for game projects)
- **`/balance-check` + `/playtest-report`** — two new Claude Code slash commands for game projects (verify balance config against FDD ranges · generate playtest report from FDD section 8)
- **FDD section 2** now includes an MDA framework table (Mechanics / Dynamics / Aesthetics) — forces player-experience thinking before design
- **CLAUDE.md** — two new enforced rules: plan-before-code gate, and auto-check entity register on deprecated entity detection

---

## The Problem

Working with AI across multiple sessions breaks down fast:

- AI starts from zero every session — no memory of what was done
- Decisions get reversed silently — TypeScript chosen last week, JavaScript suggested today
- AI either guesses (and goes wrong) or freezes (and does nothing)
- Teams drift — different people, different tools, different directions

## The Solution

A set of **19 template files** that any AI can read once and follow forever.

```
doc/
  00-source/      ← versioned requirements (never edited directly)
  01-plan/        ← work-status with AI-CONTEXT block
  02-task/        ← task board with full traceability
  03-log/         ← session history + agent diary
  04-way-of-work/ ← session protocol + decision rules
  07-decisions/   ← ADR index + entity register
```

AI reads 3 files at the start of every session → knows exactly what to do. No re-explaining. No repeated decisions. No silent scope creep.

---

## Three Tiers — Use What You Need

| Tier | For | What you get |
|------|-----|--------------|
| **`core/`** | Everyone · Any AI tool | Sessions connect seamlessly · Requirements never lost · Every task traceable · AI knows its own boundaries · Architecture decisions recorded |
| **`+ skills/game/`** | Game developers | FDD before every feature · Balance check · Asset registry · Playtest report · Narrative standards · **33 Thinking Frames** (any AI tool) · **49 specialist agents** + `/game-review` (Claude Code) |
| **`+ platforms/claude-code/`** | Claude Code CLI users | CLAUDE.md auto-loaded · Commit hooks · Path-scoped rules · /session-end · /adr-create · /balance-check · /playtest-report *(game)* |

---

## Quick Start


### Option A — Claude Code (recommended)

```bash
# 1. Clone and copy CLAUDE.md to your project root
git clone https://github.com/BlackAkuma/ai-project-template.git
cp ai-project-template/platforms/claude-code/CLAUDE.md ./your-project/CLAUDE.md

# 2. Optional: install hooks, rules, and skills
mkdir -p your-project/.claude/{hooks,rules,skills}
cp ai-project-template/platforms/claude-code/hooks/*.sh your-project/.claude/hooks/
cp ai-project-template/platforms/claude-code/rules/*.md  your-project/.claude/rules/
cp ai-project-template/platforms/claude-code/skills/*.md your-project/.claude/skills/
chmod +x your-project/.claude/hooks/*.sh
```

Open Claude Code in your project and type — **once only**:

```
Setup doc/ system for this project.
- Name: [PROJECT_NAME]
- Type: [app / web / game / mobile]
- Source docs: [attach files / none yet]
- Goal: [PROJECT_GOAL_SUMMARY]
```

Claude Code reads `CLAUDE.md` + all of `core/` + `skills/game/` (if game) and builds `doc/` for you.
**Every future session loads automatically** — no prompts needed.

---

### Option B — Any AI Tool (ChatGPT, Gemini, Cursor, etc.)

Copy `core/` to your project root, then send this prompt to your AI:

```
You are setting up a documentation system for a new software project.

Project details:
- Name: [PROJECT_NAME]
- Path to create doc/ at: [PROJECT_ROOT_PATH]
- Type: [app / web / game / mobile]
- Source docs: [attach files / none yet]
- Goal: [PROJECT_GOAL_SUMMARY]

Steps:
1. Ask what language to use for communication — wait before proceeding
2. Read all files in core/ in order (00 → 18)
3. If the project is a game or web game, also read skills/game/ (00 → 11)
4. Create the doc/ structure at the path above
5. Fill in available info — use clear placeholders where missing, never guess
6. Verify against core/10-bootstrap-checklist-template.md before declaring done
```

**Future sessions:** paste the session-start block from `core/03-way-of-work-template.md` each time.

---

### Option C — Bootstrap Script (fastest, Claude Code)

If you already have the template repo cloned, use the bootstrap script to generate `doc/` in one command:

```bash
# Software project
bash scripts/new-project.sh "MyApp" "../my-app"

# Game project (creates doc/08-design/ + asset-registry)
bash scripts/new-project.sh "MyGame" "../my-game" --game
```

The script reads directly from `core/` and `skills/game/`, strips template meta-headers, and produces clean project files with your project name substituted throughout. Output is verified against a 305-check audit suite.

---

### After Setup

Once AI confirms the bootstrap checklist passes — delete the template folder. What remains is `doc/` in your project (and `.claude/` if using Claude Code).

> Full walkthrough: [QUICKSTART.md](QUICKSTART.md) · Visual guide: [How It Works](https://blackakuma.github.io/ai-project-template/how-it-works.html)

---

## What's in `core/`

| File | Purpose |
|------|---------|
| `00` Bootstrap Master | Full setup rules, steps, and skill detection |
| `01` Folder Structure | Standard `doc/` directory layout |
| `02` Source Doc Versioning | Versioned, immutable requirements |
| `03` Way of Work | Session protocol · start/stop checklists · pre/post-compact |
| `04` Coding Standards | Code and workflow standards |
| `05` Project Plan | Plan template + quality gates |
| `06` Work Status | Live project status with AI-CONTEXT block |
| `07` Task Board | Task lifecycle + Definition of Ready/Done |
| `08` Log & Summary | Session logs · daily/monthly summaries · agent diary |
| `09` Extension Doc | Extension docs + reverse-document protocol |
| `10` Bootstrap Checklist | Verify setup before starting work |
| `11` AI Decision Protocol | 11 scenarios (A–K) · responsibility matrix |
| `12` ADR | Architecture Decision Records — never deleted |
| `13` Retrospective | Periodic collaboration review |
| `14` Anti-Patterns | What not to do, and why |
| `15` Compliance Check | C-01–C-14 + tech debt register |
| `16` Launch Checklist | Pre-release checklist |
| `17` Entity Register | Track active/deprecated entities across the project |
| `18` Cross-Project Memory | Patterns and lessons across multiple projects |

---

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **AI-CONTEXT block** | Compact block at top of key files — AI reads this first, under 500 tokens, full context |
| **Source docs = source of truth** | Requirements are never edited directly — changes create a new version |
| **Do less, document more** | A well-documented stop beats a silent wrong decision |
| **Progressive enhancement** | `core/` works alone — add tiers only when you need them |
| **Memory Scope Protocol** | 5-step rule for where to store new information (task board / log / ADR / entity register / cross-project memory) |

---

## Token Cost (approximate)

| Scenario | Total tokens |
|----------|-------------|
| First setup (core 19 files + build doc/) | ~18,000 |
| Setup + game skill pack (12 files) | ~26,000 |
| Normal session (AI-CONTEXT + work) | ~4,000–10,000 |
| Light session (orient only) | ~1,000–1,500 |

Setup is paid once. Every session after that uses only the AI-CONTEXT blocks — a fraction of the cost.

---

## Support

If this saves you time, consider sponsoring:

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/BlackAkuma)

---

---

# AI Project Template — ภาษาไทย

**ชุด template สำหรับวางโครงสร้างการทำงานร่วมกันระหว่างนักพัฒนาและ AI — ทุก session ทุก tool ทุกขนาดทีม**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/BlackAkuma?style=flat&logo=github&color=pink)](https://github.com/sponsors/BlackAkuma)

📖 **[ดู User Guide →](https://blackakuma.github.io/ai-project-template/how-it-works.html)**

---

## อัปเดตใหม่

- **49 game specialist agents** (Claude Code) — game studio เต็มรูปแบบในเทอร์มินัล: Creative/Technical Directors, programmer ทุกบทบาท (lead, gameplay, engine, AI, network, UI, tools, devops, security), design ทุกสาย, QA, Audio, Narrative และ engine specialist 15 คน (5× Godot · 5× Unity · 5× Unreal) เรียก `/game-review` เพื่อทำ milestone gate review ผ่าน specialist agents ทั้งหมด
- **33 Thinking Frames** — reasoning แบบ specialist ฝังอยู่ใน `skills/game/00` สำหรับ **ทุก AI tool** (ChatGPT, Gemini, Copilot): วิเคราะห์เชิงโครงสร้างจาก Game Designer, Narrative Director, GAS Specialist, UMG Specialist และอีก 29 บทบาท — ไม่ต้องใช้ Claude Code
- **`scripts/new-project.sh`** — bootstrap ด้วยคำสั่งเดียว: สร้างโครงสร้าง `doc/` จาก template ภายในไม่กี่วินาที (ใส่ `--game` สำหรับ game project)
- **`/balance-check` + `/playtest-report`** — slash command ใหม่สำหรับ Claude Code ใน game project (ตรวจค่า balance config เทียบกับ FDD · สร้าง playtest report จาก FDD ส่วนที่ 8)
- **FDD ส่วนที่ 2** เพิ่มตาราง MDA framework (Mechanics / Dynamics / Aesthetics) — บังคับคิดจากมุมผู้เล่นก่อนออกแบบ
- **CLAUDE.md** — กฎใหม่ 2 ข้อ: plan-before-code gate และ auto-check entity register เมื่อเจอ deprecated entity

---

## ปัญหา

ทำงานกับ AI ข้ามหลาย session พังเร็วมาก:

- AI เริ่มจากศูนย์ทุก session — ไม่รู้ว่าทำอะไรไปแล้ว
- ตัดสินใจซ้ำเงียบ ๆ — เลือก TypeScript ไปแล้วแต่ session ใหม่ AI เสนอ JavaScript อีก
- AI เดา (แล้วผิด) หรือหยุดชะงัก (แล้วทำอะไรไม่ได้)
- ทีมทำงานไม่ไปทิศทางเดียวกัน — คนละคน คนละ tool คนละทิศ

## วิธีแก้

**19 template files** ที่ AI อ่านครั้งเดียวแล้วทำตามได้ตลอดโปรเจ็กต์

```
doc/
  00-source/      ← requirements แบบ versioned (ห้ามแก้โดยตรง)
  01-plan/        ← work-status พร้อม AI-CONTEXT block
  02-task/        ← task board พร้อม traceability เต็มรูปแบบ
  03-log/         ← ประวัติ session + agent diary
  04-way-of-work/ ← session protocol + decision rules
  07-decisions/   ← ADR index + entity register
```

AI อ่าน 3 ไฟล์ตอนเริ่ม session → รู้ว่าต้องทำอะไรทันที ไม่ต้องอธิบายซ้ำ ไม่มีการตัดสินใจซ้ำ ไม่มี scope creep เงียบ ๆ

---

## 3 ระดับการใช้งาน — ใช้เท่าที่ต้องการ

| ระดับ | ใครใช้ | ได้อะไร |
|-------|-------|---------|
| **`core/`** | ทุกคน · ทุก AI tool | Session ต่อกันได้ · Requirements ไม่หาย · Task traceable · AI รู้ขอบเขตตัวเอง · บันทึก ADR |
| **`+ skills/game/`** | นักพัฒนาเกม | FDD ก่อน code · Balance check · Asset registry · Playtest report · Narrative standards · **33 Thinking Frames** (ทุก AI tool) · **49 specialist agents** + `/game-review` (Claude Code) |
| **`+ platforms/claude-code/`** | Claude Code CLI users | CLAUDE.md โหลดอัตโนมัติ · Commit hooks · Rules ตาม path · /session-end · /adr-create · /balance-check · /playtest-report *(game)* |

---

## เริ่มต้นใช้งาน

### ตัวเลือก A — Claude Code (แนะนำ)

```bash
# 1. Clone แล้ว copy CLAUDE.md ไปที่ root โปรเจ็กต์
git clone https://github.com/BlackAkuma/ai-project-template.git
cp ai-project-template/platforms/claude-code/CLAUDE.md ./your-project/CLAUDE.md

# 2. ไม่บังคับ: ติดตั้ง hooks, rules, และ skills
mkdir -p your-project/.claude/{hooks,rules,skills}
cp ai-project-template/platforms/claude-code/hooks/*.sh your-project/.claude/hooks/
cp ai-project-template/platforms/claude-code/rules/*.md  your-project/.claude/rules/
cp ai-project-template/platforms/claude-code/skills/*.md your-project/.claude/skills/
chmod +x your-project/.claude/hooks/*.sh
```

เปิด Claude Code แล้วพิมพ์ — **ครั้งเดียวเท่านั้น**:

```
Setup doc/ system for this project.
- Name: [ชื่อโปรเจ็กต์]
- Type: [app / web / game / mobile]
- Source docs: [แนบไฟล์ / none yet]
- Goal: [สรุปเป้าหมายโปรเจ็กต์]
```

Claude Code อ่าน `CLAUDE.md` + `core/` ทั้งหมด + `skills/game/` (ถ้าเป็นเกม) แล้วสร้าง `doc/` ให้
**Session ถัดไปโหลดอัตโนมัติ** — ไม่ต้อง prompt ซ้ำ

---

### ตัวเลือก B — AI tool อื่น (ChatGPT, Gemini, Cursor ฯลฯ)

Copy `core/` ไปที่ root โปรเจ็กต์ แล้วส่ง prompt นี้ให้ AI:

```
คุณกำลัง setup ระบบเอกสารสำหรับโปรเจ็กต์ซอฟต์แวร์ใหม่

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [PROJECT_ROOT_PATH]
- ประเภท: [app / web / game / mobile]
- Source docs: [แนบไฟล์ / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ขั้นตอน:
1. ถามว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ใน core/ ตามลำดับ (00 → 18)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน skills/game/ ต่อด้วย (00 → 11)
4. สร้างโครงสร้าง doc/ ที่ path ด้านบน
5. กรอกข้อมูลที่มี — ใส่ placeholder ชัดเจนถ้าไม่พอ ห้ามเดา
6. ตรวจสอบกับ core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

**Session ถัดไป:** วาง session-start block จาก `core/03-way-of-work-template.md` ทุกครั้ง

---

### ตัวเลือก C — Bootstrap Script (เร็วที่สุด, Claude Code)

ถ้า clone template repo ไว้แล้ว ใช้ script สร้าง `doc/` ด้วยคำสั่งเดียว:

```bash
# Software project
bash scripts/new-project.sh "MyApp" "../my-app"

# Game project (สร้าง doc/08-design/ + asset-registry)
bash scripts/new-project.sh "MyGame" "../my-game" --game
```

Script อ่านจาก `core/` และ `skills/game/` โดยตรง ตัด template header ออก และแทนที่ชื่อโปรเจ็กต์ทั่วทุกไฟล์ ผ่านการตรวจ 305 จุดด้วย audit suite

---

### หลัง Setup

เมื่อ AI ยืนยันว่า bootstrap checklist ผ่านแล้ว — ลบ template folder ทิ้ง เหลือแค่ `doc/` ในโปรเจ็กต์ (และ `.claude/` ถ้าใช้ Claude Code)

> คู่มือเต็ม: [QUICKSTART.md](QUICKSTART.md) · Visual guide: [How It Works](https://blackakuma.github.io/ai-project-template/how-it-works.html)

---

## อยู่ใน `core/` มีอะไรบ้าง

| ไฟล์ | หน้าที่ |
|------|---------|
| `00` Bootstrap Master | กฎ setup ทั้งหมด ขั้นตอน และการตรวจ skill |
| `01` Folder Structure | โครงสร้าง `doc/` มาตรฐาน |
| `02` Source Doc Versioning | Requirements แบบ versioned ห้ามแก้ย้อนหลัง |
| `03` Way of Work | Session protocol · checklist เริ่ม/หยุด · pre/post-compact |
| `04` Coding Standards | มาตรฐาน code และ workflow |
| `05` Project Plan | Plan template + quality gates |
| `06` Work Status | สถานะโปรเจ็กต์แบบ live พร้อม AI-CONTEXT block |
| `07` Task Board | Task lifecycle + Definition of Ready/Done |
| `08` Log & Summary | Session log · daily/monthly summary · agent diary |
| `09` Extension Doc | Extension docs + reverse-document protocol |
| `10` Bootstrap Checklist | ตรวจ setup ก่อนเริ่มทำงานจริง |
| `11` AI Decision Protocol | 11 scenarios (A–K) · responsibility matrix |
| `12` ADR | Architecture Decision Records — ห้ามลบ |
| `13` Retrospective | ทบทวนการทำงานร่วมกันเป็นระยะ |
| `14` Anti-Patterns | สิ่งที่ไม่ควรทำ และเหตุผล |
| `15` Compliance Check | C-01–C-14 + tech debt register |
| `16` Launch Checklist | Checklist ก่อน release |
| `17` Entity Register | ติดตาม entity ที่ active/deprecated ทั่วโปรเจ็กต์ |
| `18` Cross-Project Memory | Pattern และ lesson ข้ามหลายโปรเจ็กต์ |

---

## แนวคิดสำคัญ

| แนวคิด | ความหมาย |
|--------|----------|
| **AI-CONTEXT block** | block ย่อที่ไฟล์สำคัญ — AI อ่านตรงนี้ก่อน ไม่เกิน 500 tokens แต่ได้ context ครบ |
| **Source docs = source of truth** | Requirements ห้ามแก้โดยตรง — การเปลี่ยนแปลงต้องสร้าง version ใหม่ |
| **Do less, document more** | หยุดพร้อมบันทึกชัดเจน ดีกว่าตัดสินใจเงียบ ๆ แล้วผิดพลาด |
| **Progressive enhancement** | `core/` ใช้คนเดียวได้เลย — เพิ่ม tier เมื่อต้องการ |
| **Memory Scope Protocol** | กฎ 5 ขั้นสำหรับตัดสินใจว่าข้อมูลใหม่ควรเก็บที่ไหน |

---

## ต้นทุน Token (ประมาณการ)

| สถานการณ์ | Token ทั้งหมด |
|-----------|-------------|
| Setup ครั้งแรก (core 19 ไฟล์ + สร้าง doc/) | ~18,000 |
| Setup + game skill pack (12 ไฟล์) | ~26,000 |
| Session ปกติ (AI-CONTEXT + งาน) | ~4,000–10,000 |
| Session เบา (orient only) | ~1,000–1,500 |

จ่ายต้นทุน setup ครั้งเดียว Session ถัดไปอ่านแค่ AI-CONTEXT block — ถูกกว่ามาก

---

## สนับสนุน

ถ้า template นี้ช่วยประหยัดเวลาคุณได้ ลองพิจารณา sponsor ดูนะครับ:

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github)](https://github.com/sponsors/BlackAkuma)

---

## License

MIT
