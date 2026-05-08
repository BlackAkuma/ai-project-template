---
title: สำหรับ Non-Developer — ใช้กับ Claude.ai Web
---

# สำหรับ Non-Developer

ใช้ระบบนี้ผ่าน Claude.ai web โดยไม่ต้องใช้ terminal หรือ CLI

→ [หน้าหลัก](index.md)

---

## ใครเหมาะกับคู่มือนี้

- ใช้ Claude.ai web ([claude.ai](https://claude.ai)) ไม่ใช่ Claude Code CLI
- ไม่คุ้นเคยกับ terminal หรือ bash commands
- ต้องการ AI ช่วยจัดการโปรเจ็กต์ผ่าน chat

ระบบยังทำงานได้เต็มรูปแบบ — เพียงแต่บางขั้นตอนทำด้วยมือแทนที่จะรัน command

---

## Setup ครั้งแรก

### ขั้น 1: ดาวน์โหลด template

ไปที่ [github.com/BlackAkuma/ai-project-template](https://github.com/BlackAkuma/ai-project-template)

คลิก **Code → Download ZIP** → แตกไฟล์

### ขั้น 2: สร้างโฟลเดอร์โปรเจ็กต์

สร้าง folder ใหม่สำหรับโปรเจ็กต์ของคุณ เช่น `C:\Projects\my-project\`

### ขั้น 3: Copy ไฟล์ที่จำเป็น

จาก ZIP ที่แตกแล้ว copy ไปที่ folder โปรเจ็กต์:
```
core/        → my-project/core/
platforms/   → my-project/platforms/
skills/      → my-project/skills/ (ถ้าต้องการ)
```

### ขั้น 4: เตรียม context สำหรับ Claude

Copy เนื้อหาของ `platforms/claude-code/CLAUDE.md` ทั้งหมด

---

## First Run Bootstrap — ผ่าน Claude.ai Chat

### เริ่ม conversation ใหม่

Paste prompt นี้:

```
ฉันต้องการ bootstrap โปรเจ็กต์ใหม่โดยใช้ ai-project-template

นี่คือ CLAUDE.md ของระบบ:
[Paste เนื้อหา CLAUDE.md ทั้งหมดที่นี่]

ช่วยทำ First Run Bootstrap ให้ฉันด้วย:
1. ถามว่าจะใช้ภาษาอะไร
2. บอกว่าต้องสร้างไฟล์อะไรบ้าง
3. แสดงเนื้อหาของแต่ละไฟล์ที่ต้องสร้าง
```

### Claude จะบอกให้สร้างไฟล์เหล่านี้

Claude จะ generate เนื้อหาของทุกไฟล์ใน `CoreAiWorkspaces/` ให้ คุณแค่ copy แล้วสร้างไฟล์ตาม:

```
CoreAiWorkspaces/
├── 00-source/README.md
├── 01-plan/work-status.md
├── 01-plan/project-plan.md
├── 02-task/task-board.md
├── 03-log/work-log-index.md
├── 04-way-of-work/way-of-work.md
├── 04-way-of-work/ai-decision-protocol.md
├── 04-way-of-work/compliance.md
├── 07-decisions/README.md
└── 07-decisions/entity-register.md
```

**เครื่องมือแนะนำ:** ใช้ VS Code, Notepad++, หรือ Obsidian สร้างและแก้ไขไฟล์ Markdown

---

## การทำงานทุก Session

### เริ่ม Session

สร้าง conversation ใหม่ใน Claude.ai แล้ว paste prompt นี้:

```
นี่คือสถานะโปรเจ็กต์ปัจจุบัน:

**work-status.md:**
[Paste เนื้อหา CoreAiWorkspaces/01-plan/work-status.md]

**work-log-index.md (5 entry ล่าสุด):**
[Paste ส่วน AI-CONTEXT block และ entries ล่าสุด]

**task-board.md:**
[Paste เนื้อหา CoreAiWorkspaces/02-task/task-board.md]

ช่วยสรุปสถานะและบอกว่าควรทำอะไรต่อ
```

### ระหว่าง Session

ทำงานตามปกติใน chat เดิม — Claude จะ track งาน, แจ้งถ้า scope creep, และแนะนำ ADR ถ้าจำเป็น

### จบ Session

ขอให้ Claude สรุปสิ่งที่ต้องอัปเดต:

```
session นี้จบแล้ว ช่วยบอกว่าต้องอัปเดตอะไรบ้าง:
1. work-status.md ควรเปลี่ยนอะไร
2. work-log-index.md ควรเพิ่ม entry อะไร
3. task-board.md ควรเปลี่ยน status อะไร
```

จากนั้น copy เนื้อหาที่ Claude generate มาอัปเดตไฟล์ด้วยมือ

---

## Template สำหรับ Session Start (เก็บไว้ใช้)

บันทึก template นี้ไว้เป็น text file — paste ทุกครั้งที่เริ่ม session:

```
## Session Context — [ชื่อโปรเจ็กต์]

### ระบบที่ใช้
ฉันใช้ ai-project-template — ระบบ AI collaboration
กฎสำคัญ: AI ต้องบอก plan ก่อนทำ, ห้ามแก้ requirement โดยตรง, ห้ามตัดสินใจ architecture โดยไม่สร้าง ADR

### work-status.md
[Paste ที่นี่]

### task-board.md (active tasks)
[Paste เฉพาะ tasks ที่ in-progress หรือ next]

### session ล่าสุดทำอะไร
[Paste work-log entry ล่าสุด 1-2 entry]

---
ช่วยสรุปสถานะและเสนอว่าควรทำอะไรก่อน
```

---

## ข้อจำกัดเมื่อใช้ผ่าน Claude.ai Web

| ฟีเจอร์ | Claude Code CLI | Claude.ai Web |
|---------|----------------|---------------|
| Auto-load CLAUDE.md | ✅ อัตโนมัติ | ❌ ต้อง paste เอง |
| /session-end command | ✅ อัตโนมัติ | ❌ ต้องขอให้ generate แล้ว copy |
| อ่าน/เขียนไฟล์โดยตรง | ✅ | ❌ ต้อง paste ใส่ chat |
| Git integration | ✅ | ❌ |
| Compliance hooks | ✅ | ❌ |
| Context ข้าม session | ✅ (อ่านไฟล์) | ❌ (ต้อง paste ทุกครั้ง) |

**ข้อดีของ Claude.ai Web:** ไม่ต้องติดตั้งอะไร, ใช้ได้ทุกอุปกรณ์

---

## Tips สำหรับ Non-Technical Users

**การจัดการไฟล์ Markdown:**
- ใช้ [Obsidian](https://obsidian.md) — ฟรี, เหมาะสำหรับ Markdown
- หรือ [VS Code](https://code.visualstudio.com) พร้อม Markdown Preview extension

**ถ้า Claude ตอบยาวเกินไปใน session:**
- เริ่ม conversation ใหม่
- Paste work-status + task-board อีกครั้ง
- Claude จะ continue ได้ทันที

**ถ้าไม่แน่ใจว่าต้องอัปเดตไฟล์ไหน:**
- ถามตรงๆ: "session นี้จบแล้ว ต้องอัปเดตไฟล์อะไรบ้าง ช่วย generate เนื้อหาให้ด้วย"

---

→ ต่อไป: [ภาพรวมระบบ](architecture/overview.md) | [Claude.ai Web Integration](integrations/claude-ai.md)
