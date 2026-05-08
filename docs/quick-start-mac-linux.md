---
title: Quick Start — Mac / Linux
---

# Quick Start — Mac / Linux

คู่มือเริ่มต้นแบบ step-by-step สำหรับ macOS และ Linux

→ [Windows version](quick-start-windows.md) | [หน้าหลัก](index.md)

---

## Prerequisites

| สิ่งที่ต้องมี | ตรวจสอบ |
|-------------|---------|
| Git | `git --version` |
| Bash (มีใน macOS/Linux อยู่แล้ว) | `bash --version` |
| Claude Code CLI **หรือ** Claude.ai web account | เลือกอย่างใดอย่างหนึ่ง |

ถ้าใช้ Claude Code CLI: ติดตั้งจาก [claude.ai/code](https://claude.ai/code)

---

## Flow A: ZIP Download (แนะนำ — เหมาะสำหรับโปรเจ็กต์ใหม่)

วิธีนี้ได้รับเฉพาะ template files เท่านั้น — ไม่มี `.git` history ของ template ปนมา

### ขั้น 1: ดาวน์โหลด

ไปที่ [github.com/BlackAkuma/ai-project-template](https://github.com/BlackAkuma/ai-project-template)

คลิก **Code → Download ZIP** → แตกไฟล์

### ขั้น 2: วาง template ลงโปรเจ็กต์

```bash
# สร้างหรือเข้าโฟลเดอร์โปรเจ็กต์ของคุณ
mkdir my-project && cd my-project

# สร้าง _template/ แล้ว copy ไฟล์จาก ZIP ที่แตกแล้วไว้ใน _template/
mkdir _template
cp -r /path/to/ai-project-template-main/. _template/
```

โครงสร้างที่ได้:
```
my-project/
└── _template/
    ├── core/
    ├── platforms/
    ├── skills/
    └── scripts/
```

### ขั้น 3: รัน Bootstrap Script

```bash
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" .
```

Script จะสร้าง `ai/` folder พร้อมไฟล์ทั้งหมดให้อัตโนมัติ

### ขั้น 4: Copy CLAUDE.md (ถ้าใช้ Claude Code)

```bash
cp _template/platforms/claude-code/CLAUDE.md ./CLAUDE.md
```

### ขั้น 5: ลบ _template/

```bash
rm -rf _template/
```

`_template/` ไม่จำเป็นอีกต่อไปหลัง bootstrap — `ai/` ที่สร้างมาอยู่ด้วยตัวเองได้แล้ว

---

## Flow B: Git Clone (สำหรับผู้ที่ต้องการ sync กับ template updates)

### ขั้น 1: Clone

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git my-project
cd my-project
```

### ขั้น 2: สร้าง branch ของตัวเอง

```bash
git checkout -b dev
```

### ขั้น 3: ลบไฟล์ที่ไม่ต้องการ

```bash
# ลบไฟล์ที่เป็นของ template project เอง ไม่ใช่ของโปรเจ็กต์คุณ
rm -rf ai/ tests/ CHANGELOG.md ROADMAP.md
git add -A && git commit -m "chore: clean template files before bootstrap"
```

### ขั้น 4: เปิด Claude Code แล้วรัน First Run Bootstrap

เปิด Claude Code ใน folder นั้น:
```bash
claude .
```

Claude จะอ่าน `CLAUDE.md` และเริ่ม **First Run Bootstrap** อัตโนมัติ

---

## First Run Bootstrap — สิ่งที่จะเกิดขึ้น

เมื่อ Claude เห็นว่าไม่มี `ai/` folder Claude จะ:

1. ถามภาษาที่จะใช้สื่อสาร (ไทย/อังกฤษ/อื่นๆ)
2. ตรวจว่ามี `~/ai-workspace/cross-project-memory.md` ไหม — ถ้ามีจะอ่านก่อน
3. อ่านไฟล์ใน `core/` ทั้งหมด (00 → 21) เพื่อเข้าใจระบบ
4. ถ้าโปรเจ็กต์เป็น game → อ่าน `skills/game/` ด้วย
5. สร้างโครงสร้าง `ai/` พร้อมกรอก placeholder ในแต่ละไฟล์
6. ถามข้อมูลโปรเจ็กต์ที่ยังขาด
7. ตรวจ bootstrap checklist ก่อนประกาศเสร็จ

**ใช้เวลา:** 5–10 นาทีครั้งแรก

---

## Session แรกหลัง Bootstrap

หลัง bootstrap เสร็จ ทุก session ต่อจากนี้จะเร็วมาก:

**Session Start (~1 นาที):**
```
Claude อ่าน 3 ไฟล์:
  1. ai/01-plan/work-status.md     ← phase ปัจจุบัน
  2. ai/03-log/work-log-index.md   ← session ล่าสุดทำอะไร
  3. ai/02-task/task-board.md      ← task ที่ active อยู่
→ รายงานสถานะและถามว่าจะเริ่มต้นที่ไหน
```

**ระหว่าง session:**
```
ทำงานตามปกติ — Claude จะจัดการ task tracking, compliance, ADR เอง
```

**Session End (~2 นาที):**
```
พิมพ์: /session-end
Claude จะ sync work-status + work-log + task-board ให้ครบ
```

---

## โครงสร้างที่จะได้

```
my-project/
├── CLAUDE.md               ← Claude Code อ่านอัตโนมัติ
├── core/                   ← template engine (อย่าแก้ไข)
├── platforms/              ← platform-specific configs
├── skills/                 ← optional skill packs
├── ai/                     ← AI working folder ของโปรเจ็กต์คุณ
│   ├── 00-source/          ← source documents
│   ├── 01-plan/            ← work-status, project-plan
│   ├── 02-task/            ← task-board
│   ├── 03-log/             ← work-log
│   ├── 04-way-of-work/     ← rules และ protocols
│   └── 07-decisions/       ← ADRs และ entity-register
└── [source code ของคุณ]
```

---

## ปัญหาที่พบบ่อย

**Claude ไม่ขึ้น First Run Bootstrap เอง:**
- ตรวจว่า `CLAUDE.md` อยู่ที่ root ของโปรเจ็กต์
- ตรวจว่าไม่มี `ai/` folder อยู่แล้ว (ถ้ามีให้ลบก่อน)
- ลอง prompt: `"อ่าน CLAUDE.md และทำ First Run Bootstrap"`

**new-project.sh error "ai/ already exists":**
- มี `ai/` จาก clone ค้างอยู่ → `rm -rf ai/` แล้วรันใหม่

**ไม่รู้จะใส่ข้อมูลอะไรตอน bootstrap:**
- ใส่ placeholder `<NEEDS_CLARIFICATION: ...>` ได้เลย — เติมทีหลัง
- ห้ามเดา ระบบออกแบบมาให้ทำงานแม้ข้อมูลยังไม่ครบ

---

→ ต่อไป: [ภาพรวมระบบ — Session Protocol](architecture/overview.md)
