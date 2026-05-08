---
title: Advanced Setup — Existing Projects & Teams
---

# Advanced Setup

สำหรับ: เพิ่ม template เข้าโปรเจ็กต์ที่มีอยู่แล้ว, ทีม 2–5 คน, multi-AI tool workflow

→ [หน้าหลัก](index.md)

---

## Existing Project — เพิ่ม template เข้าโปรเจ็กต์ที่มีอยู่

ถ้ามีโปรเจ็กต์อยู่แล้วและต้องการเพิ่มระบบนี้เข้าไป

### ขั้น 1: ตรวจก่อน

```bash
# ตรวจว่า project มี git init แล้วหรือยัง
git status

# ตรวจว่ามี CoreAiWorkspaces/ อยู่แล้วหรือเปล่า (ถ้ามีต้องระวัง)
ls -la | grep "^d"
```

### ขั้น 2: Download template

```bash
# Download ZIP จาก GitHub แล้วแตกไฟล์
# copy เฉพาะ core/, platforms/, skills/, scripts/ เข้า _template/
mkdir _template
cp -r /path/to/ai-project-template-main/. _template/
```

### ขั้น 3: Bootstrap

```bash
# รัน new-project.sh — script จะไม่แตะ source code เดิม
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" .
```

Script นี้จะ:
- สร้าง `CoreAiWorkspaces/` พร้อมไฟล์ทั้งหมด
- **ไม่แตะ** source code, `.gitignore`, หรือไฟล์ที่มีอยู่แล้ว
- หยุดถ้าเจอ `CoreAiWorkspaces/` อยู่แล้ว (ป้องกัน overwrite)

### ขั้น 4: Populate source docs

เพิ่ม source documents ของโปรเจ็กต์เข้า `CoreAiWorkspaces/00-source/`:
```bash
# copy PRD, design docs, spec sheets ที่มีอยู่แล้วเข้าไป
cp docs/requirements.md CoreAiWorkspaces/00-source/
cp docs/design-spec.md CoreAiWorkspaces/00-source/
```

### ขั้น 5: ลบ _template/ และ commit

```bash
rm -rf _template/
cp platforms/claude-code/CLAUDE.md ./CLAUDE.md
git add CoreAiWorkspaces/ CLAUDE.md
git commit -m "chore: add AI collaboration system"
```

---

## Git Workflow — Branch Strategy

ระบบนี้ออกแบบมาสำหรับ branch-separated workflow:

```
master/main   ← production-ready code เท่านั้น
dev           ← งานประจำ, AI ทำงานที่นี่
feature/*     ← feature branches (optional สำหรับทีม)
```

### ตั้งค่าใน work-status.md

เปิด `CoreAiWorkspaces/01-plan/work-status.md` และตั้งค่า AI-CONTEXT block:

```yaml
<!-- AI-CONTEXT
git_mode: branch-separated
git_dev_branch: dev
git_prod_branch: master
-->
```

เมื่อตั้งค่านี้แล้ว Claude จะ:
- ตรวจ branch ทุก session start
- หยุดทันทีถ้าอยู่บน master โดยไม่ตั้งใจ
- Push ไป dev โดยอัตโนมัติตอน session end

### Merge to master

**ห้าม AI merge ไป master โดยไม่ได้รับอนุญาต** — ผู้ใช้ต้อง approve เสมอ:

```bash
# ผู้ใช้ทำเอง:
git checkout master
git merge dev
git push origin master
```

---

## Team Setup — ทีม 2–5 คน

### ใครทำอะไร

| บทบาท | หน้าที่ |
|-------|---------|
| **Project Lead** | approve ADR, merge to master, update source docs |
| **Developer + AI** | implement tasks, สร้าง ADR draft, update task-board |
| **AI (Claude)** | execute tasks, สร้าง ADR draft, compliance check, session tracking |

### กฎสำคัญสำหรับทีม

```
Requirements change → Human only (AI ไม่มีสิทธิ์เลย)
Architecture decision → AI สร้าง ADR draft, Human approve
Merge to master → Human only
Source doc update → Human อนุมัติก่อน AI เขียน
```

### Scenario: AI ต้องการตัดสินใจ architecture

แทนที่จะตัดสินใจเอง AI จะ:
1. สร้างไฟล์ `CoreAiWorkspaces/07-decisions/ADR-NNN-title.md` พร้อม status: **Proposed**
2. mark task เป็น `[BLOCKED: NEEDS ADR REVIEW]`
3. แจ้งใน work-status ว่าต้องการ human review

Project Lead อ่าน ADR draft → เปลี่ยน status เป็น **Accepted** หรือ **Rejected** → AI ทำงานต่อได้

### Multi-developer workflow

เมื่อหลายคนใช้ AI tool บนโปรเจ็กต์เดียว:

```bash
# Developer A จบ session
/caw-session-end  # sync ทุกไฟล์
git push origin dev

# Developer B เริ่ม session
git pull origin dev
claude .  # Claude อ่านไฟล์ที่ sync มาแล้ว
```

**สำคัญ:** ไม่ควรให้ AI tool สองตัวทำงานพร้อมกันบน branch เดียว — merge conflicts ใน `CoreAiWorkspaces/` ไฟล์แก้ยาก

---

## Multi-AI Tool Workflow

ถ้าใช้ทั้ง Claude Code (CLI) และ Claude.ai (web) บนโปรเจ็กต์เดียวกัน:

### ตั้งค่า Agent Diary

สร้าง `CoreAiWorkspaces/03-log/agents/` folder:

```bash
mkdir -p CoreAiWorkspaces/03-log/agents/
touch CoreAiWorkspaces/03-log/agents/claude-code.md
touch CoreAiWorkspaces/03-log/agents/claude-ai.md
```

รูปแบบของ diary:

```markdown
# Agent Diary — Claude Code

## [วันที่] Session N
**Task:** T-XXX
**ทำอะไร:** ...
**Decision:** ...
**ส่งต่อให้:** claude-ai.md ทำ [สิ่งที่ยังค้างอยู่]
```

### กฎ Agent Diary

- แต่ละ tool เขียนเฉพาะ diary ของตัวเอง — ห้าม cross-write
- เริ่ม session: อ่าน diary ของ tool ที่ใช้อยู่
- ถ้าใช้ tool เดียว: ไม่ต้องสร้าง `agents/` folder

---

## Game Project Setup

เพิ่ม `--game` flag ตอนรัน bootstrap:

```bash
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" . --game
```

หรือบอก AI ตอน First Run Bootstrap ว่าโปรเจ็กต์เป็น game — Claude จะโหลด `skills/game/` เพิ่มเติมเองและสร้าง:

```
CoreAiWorkspaces/
└── 08-design/          ← Game Design Documents
    ├── gdd-main.md
    ├── balance/
    └── levels/
```

Skill commands ที่จะได้เพิ่ม:
- `/caw-balance-check` — ตรวจ game balance
- `/caw-playtest-report` — สรุปผล playtesting

---

## ย้ายจาก doc/ (legacy) ไป CoreAiWorkspaces/

ถ้าเคยใช้ version เก่าที่ยังใช้ `doc/` folder:

```bash
# rename folder
mv doc/ CoreAiWorkspaces/

# update references ใน key files
# (ระบบมี migration script ใน scripts/migrate-doc-to-ai.sh ถ้ามี)
```

ตรวจ references ที่ต้องอัปเดต:
- `CLAUDE.md` — ทุก path ที่ชี้ไป `doc/`
- `CoreAiWorkspaces/04-way-of-work/compliance.md`
- `CoreAiWorkspaces/04-way-of-work/way-of-work.md`

---

→ ต่อไป: [ภาพรวมระบบ](architecture/overview.md) | [Claude Code Integration](integrations/claude-code.md)
