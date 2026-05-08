---
title: Quick Start — Windows
---

# Quick Start — Windows

คู่มือเริ่มต้นสำหรับ Windows — มีความแตกต่างจาก Mac/Linux บางจุด

→ [Mac / Linux version](quick-start-mac-linux.md) | [หน้าหลัก](index.md)

---

## Prerequisites

### ตัวเลือก Shell (เลือกอย่างใดอย่างหนึ่ง)

**ตัวเลือก A: Git Bash (แนะนำ — ง่ายที่สุด)**
- ดาวน์โหลด Git for Windows จาก [git-scm.com](https://git-scm.com)
- ติดตั้ง → ใช้ **Git Bash** เป็น terminal หลัก
- รันคำสั่งทั้งหมดใน Git Bash

**ตัวเลือก B: WSL2 (แนะนำถ้าต้องการ Linux environment เต็มรูปแบบ)**
- เปิด PowerShell as Administrator: `wsl --install`
- Restart เครื่อง
- เปิด Ubuntu จาก Start Menu

**ตัวเลือก C: PowerShell (จำกัด)**
- bash scripts บางตัวอาจไม่รัน
- ใช้ได้เฉพาะถ้า Claude Code จัดการ bootstrap ให้

| | Git Bash | WSL2 | PowerShell |
|--|---------|------|------------|
| ง่ายต่อการตั้ง | ✅ | ⚠️ | ✅ |
| รัน bash scripts ได้ | ✅ | ✅ | ❌ |
| Path separator | `/c/Users/...` | `/mnt/c/Users/...` | `C:\Users\...` |

---

## หมายเหตุเรื่อง Path บน Windows

Windows ใช้ `\` แต่ Git Bash และ WSL ใช้ `/` — ระบบนี้ใช้ Unix-style paths ตลอด

| สิ่งที่เห็น | Git Bash | WSL2 |
|-----------|---------|------|
| C:\Users\you\project | `/c/Users/you/project` | `/mnt/c/Users/you/project` |
| Home directory | `~` = `/c/Users/you` | `~` = `/home/you` |

**คำแนะนำ:** เก็บ project files ใน path ที่ไม่มีช่องว่าง เช่น `C:\Projects\my-project` แทน `C:\Users\My Name\Documents\My Project\`

---

## Flow A: ZIP Download

### ขั้น 1: ดาวน์โหลด

ไปที่ [github.com/BlackAkuma/ai-project-template](https://github.com/BlackAkuma/ai-project-template)

คลิก **Code → Download ZIP** → แตกไฟล์ด้วย Windows Explorer หรือ 7-Zip

### ขั้น 2: เปิด Git Bash ในโฟลเดอร์โปรเจ็กต์

```bash
# ใน Git Bash:
mkdir /c/Projects/my-project
cd /c/Projects/my-project
```

หรือคลิกขวาในโฟลเดอร์ → **Git Bash Here**

### ขั้น 3: วาง template

```bash
mkdir _template
# copy ไฟล์จาก ZIP ที่แตกแล้วไปที่ _template/
cp -r /c/Users/YourName/Downloads/ai-project-template-main/. _template/
```

### ขั้น 4: รัน Bootstrap Script

```bash
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" .
```

Script จะทำทุกอย่างอัตโนมัติ:
- สร้าง `CoreAiWorkspaces/` folder พร้อมไฟล์ทั้งหมด
- ติดตั้ง `CLAUDE.md` ที่ root
- ติดตั้ง slash commands ไว้ที่ `.claude/commands/`
- ติดตั้ง git hook (ถ้ามี `.git`)

### ขั้น 5: ลบ _template/

```bash
rm -rf _template/
```

---

## Slash Commands หลัง Bootstrap

หลัง bootstrap เสร็จ script จะติดตั้ง slash commands ไว้ที่ `.claude/commands/` อัตโนมัติ

คำสั่งที่ใช้บ่อย (ชื่อขึ้นต้นด้วย `caw-` เพื่อป้องกันชนกับ tools อื่น):

```
/caw-session-end       ← sync work-status + log + task-board ก่อนปิด Claude
/caw-compliance-check  ← ตรวจ compliance violations
/caw-adr-create        ← สร้าง architectural decision record
/caw-scope-check       ← ตรวจว่างานปัจจุบันอยู่ใน scope ไหม
/caw-fdd-create        ← สร้าง feature design document
/caw-update            ← อัปเดต commands และ CLAUDE.md เป็น version ใหม่
```

> `caw-` ย่อมาจาก **C**ore**A**i**W**orkspaces — ชื่อของระบบนี้

---

## Flow B: Git Clone

```bash
# ใน Git Bash:
cd /c/Projects
git clone https://github.com/BlackAkuma/ai-project-template.git my-project
cd my-project
git checkout -b dev

# ลบไฟล์ที่ไม่ต้องการ
rm -rf CoreAiWorkspaces/ tests/ CHANGELOG.md ROADMAP.md
git add -A && git commit -m "chore: clean template files before bootstrap"
```

---

## เปิด Claude Code บน Windows

**ถ้าติดตั้ง Claude Code แล้ว:**

```bash
# ใน Git Bash:
claude /c/Projects/my-project
```

หรือเปิด VS Code ในโฟลเดอร์ → Claude Code extension จะโหลด CLAUDE.md อัตโนมัติ

**ถ้าใช้ Claude.ai web:**

1. เปิด [claude.ai](https://claude.ai)
2. Paste เนื้อหา `CLAUDE.md` เข้าไปใน chat แรก
3. ทำตาม [คู่มือ Claude.ai web](integrations/claude-ai.md)

---

## Windows-Specific Gotchas

### Line endings (CRLF vs LF)

Windows Git อาจแปลง line endings โดยอัตโนมัติ ซึ่งอาจทำให้ bash scripts ผิดพลาด

ตรวจและแก้:
```bash
git config core.autocrlf input
```

หรือสร้าง `.gitattributes` ที่ root:
```
*.sh text eol=lf
*.md text eol=lf
```

### Script permission error

ถ้ารัน `.sh` แล้วขึ้น `permission denied`:
```bash
chmod +x _template/scripts/new-project.sh
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" .
```

### Unicode ใน terminal

ถ้า emoji หรือ unicode แสดงผลผิด ใน Git Bash:
```bash
export LANG=en_US.UTF-8
```

### WSL2: เข้าถึงไฟล์ Windows

```bash
# ใน WSL2 terminal:
cd /mnt/c/Projects/my-project
```

---

## First Run Bootstrap

เหมือนกับ Mac/Linux — ดูรายละเอียดที่ [Quick Start Mac/Linux](quick-start-mac-linux.md#first-run-bootstrap---สิ่งที่จะเกิดขึ้น)

---

## ปัญหาที่พบบ่อยบน Windows

**`bash: _template/scripts/new-project.sh: No such file or directory`**
- ตรวจ path separator — ใช้ `/` ไม่ใช่ `\` ใน Git Bash

**Claude Code ไม่เห็น `CLAUDE.md`**
- ตรวจว่าเปิด Claude Code ใน folder ที่ถูกต้อง (ที่มี `CLAUDE.md`)
- ใน VS Code: File → Open Folder → เลือก project folder

**Git Bash ช้าใน Windows**
- เปิด Git Bash ด้วย "Run as Administrator" ครั้งแรก
- หรือ switch ไปใช้ WSL2 สำหรับงานหนัก

---

→ ต่อไป: [ภาพรวมระบบ — Session Protocol](architecture/overview.md)
