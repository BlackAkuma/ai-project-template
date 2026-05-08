---
title: Claude Code Integration
---

# Claude Code Integration

คู่มือการใช้ ai-project-template กับ Claude Code CLI — รูปแบบที่ได้ automation เต็มรูปแบบ

→ [หน้าหลัก](../index.md) | [Claude.ai Web](claude-ai.md)

---

## ทำไม Claude Code ถึงแนะนำ

| ฟีเจอร์ | Claude Code | Claude.ai Web |
|---------|------------|---------------|
| Auto-load CLAUDE.md | ✅ ทุก session | ❌ ต้อง paste เอง |
| อ่าน/เขียนไฟล์โดยตรง | ✅ | ❌ |
| Slash commands | ✅ | ❌ |
| Git integration | ✅ | ❌ |
| Compliance hooks | ✅ | ❌ |
| Session continuity | ✅ อ่านจากไฟล์ | ❌ ต้อง paste context |

---

## Setup

### ขั้น 1: ติดตั้ง Claude Code

```bash
# ดูคำสั่งติดตั้งล่าสุดที่ claude.CoreAiWorkspaces/code
npm install -g @anthropic-ai/claude-code
# หรือดูวิธีติดตั้งอื่นๆ ที่ official docs
```

### ขั้น 2: วาง CLAUDE.md ที่ root

```bash
cp platforms/claude-code/CLAUDE.md ./CLAUDE.md
```

Claude Code โหลด `CLAUDE.md` อัตโนมัติทุกครั้งที่เปิดโปรเจ็กต์ — ไม่ต้อง paste ด้วยมือ

### ขั้น 3: เปิดโปรเจ็กต์

```bash
claude .
# หรือเปิด VS Code แล้วใช้ Claude Code extension
```

---

## CLAUDE.md — โครงสร้างและการทำงาน

`CLAUDE.md` ที่ root บอก Claude ว่าต้องทำอะไรทุก session:

```markdown
## Session Start Protocol
1. อ่าน CoreAiWorkspaces/01-plan/work-status.md
2. อ่าน CoreAiWorkspaces/03-log/work-log-index.md
3. อ่าน CoreAiWorkspaces/02-task/task-board.md
→ รายงานสถานะ

## Session End Protocol
/caw-session-end → sync ทุกไฟล์
```

**อย่าแก้ไข CLAUDE.md โดยตรง** ถ้าต้องการ customize ให้แก้ที่ `CoreAiWorkspaces/04-way-of-work/way-of-work.md` แทน — CLAUDE.md load มาจาก platforms/ และอาจถูก update จาก template ได้

---

## Slash Commands

คำสั่งทั้งหมดที่ใช้ได้ใน Claude Code:

### `/caw-session-end`

Sync ทุกไฟล์ก่อนจบ session ในคำสั่งเดียว

ทำ:
1. อัปเดต `work-status.md` — body + AI-CONTEXT block
2. เพิ่ม entry ใน `work-log-index.md`
3. อัปเดต status ใน `task-board.md`
4. Mark tasks ที่ยัง in-progress ด้วย checkpoint note
5. Push ถ้า `git_mode: branch-separated`

**ใช้ทุกครั้งก่อนปิด Claude Code**

---

### `/caw-compliance-check`

รัน compliance scan ทันที — ตรวจว่า:

- มี tasks ที่ไม่มี source reference ไหม (C-01)
- มี decisions ที่ไม่มี ADR ไหม (C-04)
- มี deprecated entities ในไฟล์ที่กำลังทำงานไหม (C-14)
- ถ้า vector_memory: enabled — CoreAiWorkspaces/ เปลี่ยนแล้ว re-index หรือยัง (C-20)
- มี tasks ที่ BLOCKED นานเกินไปไหม

ผลลัพธ์: รายการ violations + warnings + ข้อแนะนำ

---

### `/caw-adr-create`

สร้าง ADR สำหรับ architectural decision ใหม่

Claude จะถาม:
1. Decision นี้เกี่ยวกับอะไร?
2. Options ที่พิจารณา (อย่างน้อย 2 option)
3. Context และ constraints?
4. Source reference ที่เกี่ยวข้อง?

แล้วสร้าง:
- `CoreAiWorkspaces/07-decisions/ADR-NNN-title.md` พร้อม ID ถัดไปอัตโนมัติ
- อัปเดต ADR index ใน `CoreAiWorkspaces/07-decisions/README.md`
- Mark task ที่รอ decision นี้เป็น `[BLOCKED: NEEDS ADR REVIEW]`

---

### `/caw-fdd-create`

สร้าง Feature Design Document template สำหรับ feature ใหม่

Output: ไฟล์ `CoreAiWorkspaces/00-source/features/FDD-[name].md` พร้อมโครงสร้าง:
- Feature Overview + Acceptance Criteria
- Technical Approach
- Edge Cases
- Dependencies
- Test Plan

---

### `/caw-scope-check`

ตรวจ scope ของ task ปัจจุบัน

Claude จะ:
- อ่าน task ปัจจุบันจาก task-board
- ตรวจ source reference ที่อ้างถึง
- ระบุว่า สิ่งที่กำลังทำอยู่นอก scope ไหม
- แสดง out-of-scope items ที่ควร log เป็น task ใหม่

---

### `/caw-launch-check`

รัน launch checklist ก่อน deploy ไป production

ตรวจ:
- Tasks ทั้งหมด done แล้วหรือยัง
- มี BLOCKED tasks ที่ยังค้างอยู่ไหม
- ADR ทุกตัว reviewed แล้วหรือยัง
- มี compliance violations ไหม
- Entity register อัปเดตแล้วหรือยัง

---

### `/caw-archive-logs`

Compress session logs เก่าเป็น monthly archive

ทำ:
- รวม entries เก่ากว่า 30 วันจาก `work-log-index.md`
- สร้าง `CoreAiWorkspaces/03-log/archives/YYYY-MM.md`
- อัปเดต work-log-index เก็บแค่ entries ล่าสุด

ช่วยลด context ที่ต้องโหลดทุก session

---

### `/caw-balance-check` (Game Projects เท่านั้น)

ตรวจ game balance ตาม design standards ใน `skills/game/`

---

### `/caw-playtest-report` (Game Projects เท่านั้น)

สรุปและ format ผล playtesting เป็น structured report

---

## Git Hooks

### validate-commit.sh

Hook ที่รันก่อนทุก commit — ตรวจ:

```bash
# ติดตั้ง hook:
cp scripts/validate-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

ตรวจ:
- ไฟล์ที่ commit มี reference ถึง `[ENTITY:deprecated]` ไหม
- ถ้ามี → warn และแสดงว่า entity ไหนที่ deprecated
- ไม่ block commit — แค่ warn เพื่อให้ human ตัดสินใจ

---

## Settings และ Configuration

### ตั้งค่า git mode

ใน `CoreAiWorkspaces/01-plan/work-status.md` AI-CONTEXT block:

```yaml
git_mode: branch-separated     # หรือ single-branch
git_dev_branch: dev
git_prod_branch: master
```

`branch-separated` → Claude ตรวจ branch ทุก session start + push อัตโนมัติตอน session end

### ตั้งค่า vector memory

```yaml
vector_memory: enabled         # enabled | later | disabled
vector_wing: my-project-name
```

### ตั้งค่า language

ใน `CoreAiWorkspaces/04-way-of-work/way-of-work.md`:
```
สื่อสารกัน: ภาษาไทย
Code และ identifiers: English
AI-CONTEXT blocks: English เสมอ
```

---

## Tips การใช้งาน

**เริ่ม session ให้เร็ว:**
```
แค่พิมพ์: "เริ่ม session"
Claude จะอ่าน 3 ไฟล์และรายงานสถานะเอง ไม่ต้องบอกอะไรเพิ่ม
```

**ถ้า Claude ลืม context ระหว่าง session:**
```
พิมพ์: "อ่าน work-status.md อีกครั้ง"
```

**ถ้าต้องการดู compliance status:**
```
/caw-compliance-check
```

**ก่อนปิด Claude Code ทุกครั้ง:**
```
/caw-session-end
```

---

→ ต่อไป: [Claude.ai Web](claude-ai.md) | [Vector Memory](vector-memory.md)
