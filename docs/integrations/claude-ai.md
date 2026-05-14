---
title: Claude.ai Web Integration
---

# Claude.ai Web Integration

การใช้ ai-project-template ผ่าน [claude.ai](https://claude.ai) web interface

→ [หน้าหลัก](../index.md) | [Claude Code CLI](claude-code.md) | [สำหรับ Non-Developer](../non-technical-setup.md)

---

## ภาพรวม

Claude.ai web ทำงานกับระบบนี้ได้เต็มรูปแบบ — เพียงแต่บางขั้นตอนต้องทำด้วยมือแทนที่จะรัน command

**เหมาะสำหรับ:**
- งาน design, planning, review ที่ไม่ต้องการ file access โดยตรง
- ใช้คู่กับ Claude Code (Claude.ai ทำ high-level, Claude Code ทำ implementation)
- ทีมที่สมาชิกบางคนไม่มี Claude Code license

---

## วิธีเริ่ม Session ผ่าน Claude.ai Web

### Template สำหรับ Session Start

Copy และ fill template นี้ทุกครั้งที่เริ่ม session:

```
## AI Project Session — [ชื่อโปรเจ็กต์]

**ระบบ:** ai-project-template (Session Protocol)

**กฎสำคัญ:**
- บอก plan ก่อนทำทุกครั้ง รอยืนยัน
- ห้ามแก้ requirements โดยตรง
- ห้ามตัดสินใจ architecture โดยไม่สร้าง ADR
- Do less, document more

---

### work-status.md
[paste เนื้อหาทั้งหมดที่นี่]

---

### work-log-index.md (5 entries ล่าสุด)
[paste AI-CONTEXT block + entries ล่าสุด]

---

### task-board.md
[paste เนื้อหาทั้งหมด หรือเฉพาะ active tasks]

---

ช่วยสรุปสถานะปัจจุบัน และแนะนำว่าควรทำอะไรก่อน
```

---

## Multi-Tool Workflow — Claude Code + Claude.ai

วิธีใช้ทั้งสองร่วมกันในโปรเจ็กต์เดียว:

### แบ่งหน้าที่

| งาน | Claude Code | Claude.ai Web |
|-----|------------|---------------|
| Implementation (เขียน code) | ✅ | — |
| Design review | — | ✅ |
| ADR drafting (ต้องการ file access) | ✅ | — |
| ADR review (อ่านและให้ feedback) | — | ✅ |
| Session tracking | ✅ (auto) | — (manual) |
| Architecture discussion | — | ✅ |
| Brainstorming | — | ✅ |

### ตั้งค่า Agent Diary

เมื่อใช้ทั้งสอง tool ต้องตั้งค่า diary แยกกัน:

```bash
mkdir -p CoreAiWorkspaces/03-log/agents/
```

**`CoreAiWorkspaces/03-log/agents/claude-code.md`** — Claude Code เขียน
**`CoreAiWorkspaces/03-log/agents/claude-ai.md`** — Claude.ai web เขียน (ด้วยมือหลัง session)

### Handoff Pattern

**Claude Code → Claude.ai:**

```
# เมื่อจบ Claude Code session
/caw-session-end

# เปิด Claude.ai แล้ว paste:
"ฉันเพิ่งจบ Claude Code session ที่ทำ [สรุปสิ่งที่ทำ]
ต้องการ review decision ต่อไปนี้: [ADR draft]
ช่วย review และให้ feedback ก่อนที่จะ accept"
```

**Claude.ai → Claude Code:**

```
# หลัง Claude.ai review เสร็จ
# save feedback ลงไฟล์ด้วยมือ หรือ note ไว้

# เปิด Claude Code แล้วบอก:
"Claude.ai review ADR-005 แล้ว accept ด้วยเงื่อนไข [เงื่อนไข]
ทำ T-015 ต่อตาม decision นั้น"
```

---

## Projects Feature (Claude.ai Pro)

ถ้ามี Claude.ai Pro — ใช้ **Projects** feature เพื่อ persist context:

### ตั้งค่า Project

1. สร้าง Project ใหม่ ตั้งชื่อตามโปรเจ็กต์
2. เพิ่ม **Project Instructions:**

```
ฉันใช้ ai-project-template สำหรับโปรเจ็กต์นี้

กฎ:
- บอก plan ก่อนทำทุกครั้ง รอยืนยัน
- ห้ามตัดสินใจ architecture โดยไม่สร้าง ADR draft
- ถ้าไม่แน่ใจ: Do less, document more

ทุกครั้งที่เริ่ม session ให้ถามว่า:
"ต้องการ paste context ไหม หรือ continue จาก session ก่อน?"
```

3. Upload ไฟล์ `CoreAiWorkspaces/` ที่สำคัญเข้า Project Knowledge:
   - `CoreAiWorkspaces/01-plan/work-status.md`
   - `CoreAiWorkspaces/02-task/task-board.md`
   - `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`

**หมายเหตุ:** Project Knowledge ไม่อัปเดตอัตโนมัติ — ต้อง re-upload เมื่อไฟล์เปลี่ยน

---

## Session End — ทำด้วยมือ

เมื่อจบ session ผ่าน Claude.ai web ขอให้ Claude สรุปสิ่งที่ต้องอัปเดต:

```
session นี้จบแล้ว ช่วย generate เนื้อหาที่ต้องอัปเดต:

1. work-status.md — AI-CONTEXT block ใหม่ที่ควรเป็น
2. work-log-index.md — entry ใหม่สำหรับ session นี้
3. task-board.md — tasks ที่เปลี่ยน status
4. ถ้าทำ architectural decision — ADR draft

(format แบบที่ copy วางได้เลย)
```

จากนั้น copy เนื้อหาไปวางในไฟล์ด้วยมือ

---

## Tips สำหรับ Claude.ai Web

**Context window ใกล้เต็ม:**
```
เริ่ม conversation ใหม่
Paste session start template อีกครั้ง
Claude จะ continue ได้ทันที
```

**ต้องการ review ADR:**
```
paste เนื้อหา ADR-NNN.md ทั้งหมดเข้าไปใน chat
แล้วถามว่า "มีจุดไหนที่ควรพิจารณาเพิ่มเติมไหม?"
```

**ต้องการ brainstorm แต่ไม่ให้ commit:**
```
เริ่มด้วย: "นี่คือ exploration ยังไม่ใช่ decision
อยากได้ความเห็นเรื่อง [topic] โดยไม่ต้องสร้าง ADR"
```

**ต้องการ review compliance:**
```
paste CoreAiWorkspaces/04-way-of-work/compliance.md
paste work-status.md และ task-board.md
ถามว่า "มี compliance issues อะไรบ้างจากสถานะนี้"
```

---

→ ต่อไป: [Vector Memory](vector-memory.md) | [ภาพรวมระบบ](../architecture/overview.md)
