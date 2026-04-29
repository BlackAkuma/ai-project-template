# AI Project Template

**A structured collaboration system for developers and AI — across every session, every tool, every team size.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/BlackAkuma?style=flat&logo=github&color=pink)](https://github.com/sponsors/BlackAkuma)

📖 **[See How It Works →](https://blackakuma.github.io/ai-project-template/how-it-works.html)**

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
| **`+ skills/game/`** | Game developers | FDD before every feature · Balance check · Asset registry · Playtest report · Narrative standards |
| **`+ platforms/claude-code/`** | Claude Code CLI users | CLAUDE.md auto-loaded · Commit hooks · Path-scoped rules · /session-end · /adr-create |

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
3. If the project is a game or web game, also read skills/game/ (00 → 06)
4. Create the doc/ structure at the path above
5. Fill in available info — use clear placeholders where missing, never guess
6. Verify against core/10-bootstrap-checklist-template.md before declaring done
```

**Future sessions:** paste the session-start block from `core/03-way-of-work-template.md` each time.

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
| Setup + game skill pack | ~23,000 |
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

📖 **[ดู User Guide →](https://blackakuma.github.io/ai-project-template/how-it-works.html)**

---

## ปัญหาที่แก้

- AI เริ่มจากศูนย์ทุก session — ไม่รู้ว่าทำอะไรไปแล้ว
- ตัดสินใจซ้ำ — เลือก TypeScript ไปแล้วแต่ session ใหม่ AI เสนอ JavaScript อีก
- AI ตัดสินใจเองเงียบ ๆ หรือหยุดในสิ่งที่ควรทำได้เอง
- ทีมทำงานไม่ไปทิศทางเดียวกัน

## วิธีแก้

**19 template files** ที่ AI อ่านครั้งเดียวแล้วทำตามได้ตลอดโปรเจ็กต์

AI อ่าน 3 ไฟล์ตอนเริ่ม session → รู้ว่าต้องทำอะไรทันที ไม่ต้องอธิบายซ้ำ ไม่มีการตัดสินใจซ้ำ ไม่มี scope creep เงียบ ๆ

---

## 3 ระดับการใช้งาน

| ระดับ | ใครใช้ | ได้อะไร |
|-------|-------|---------|
| **`core/`** | ทุกคน · ทุก AI tool | Session ต่อกันได้ · Requirements ไม่หาย · Task traceable · AI รู้ขอบเขตตัวเอง · บันทึก ADR |
| **`+ skills/game/`** | นักพัฒนาเกม | FDD ก่อน code · Balance check · Asset registry · Playtest report |
| **`+ platforms/claude-code/`** | Claude Code users | CLAUDE.md โหลดอัตโนมัติ · Hooks · Rules ตาม path · /session-end |

---

## วิธีใช้

### ตัวเลือก A — Claude Code (แนะนำ)

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
cp ai-project-template/platforms/claude-code/CLAUDE.md ./your-project/CLAUDE.md
```

พิมพ์ใน Claude Code ครั้งเดียว:

```
Setup doc/ system for this project.
- Name: [PROJECT_NAME]
- Type: [app / web / game / mobile]
- Source docs: [แนบไฟล์ / none yet]
- Goal: [PROJECT_GOAL_SUMMARY]
```

Session ถัดไปไม่ต้องส่ง prompt อีก — `CLAUDE.md` โหลดเองทุกครั้ง

### ตัวเลือก B — AI tool อื่น

Copy `core/` ไปโปรเจ็กต์แล้วส่ง prompt จาก template ด้านบน (ภาษาอังกฤษ) ให้ AI อ่าน core/ ลำดับ 00 → 18

---

## License

MIT
