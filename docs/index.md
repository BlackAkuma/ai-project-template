---
title: AI Project Template — คู่มือฉบับสมบูรณ์
---

# AI Project Template

> ระบบ AI collaboration สำหรับโปรเจ็กต์ทุกประเภท — ทำให้ AI รู้ว่าต้องทำอะไรทุก session โดยไม่ต้องอธิบายซ้ำ

---

## ปัญหาที่ระบบนี้แก้

| ปัญหาที่เจอ | สิ่งที่ระบบนี้ทำ |
|------------|----------------|
| AI เริ่มจากศูนย์ทุก session — ต้องอธิบายทุกอย่างใหม่ | AI อ่าน 3 ไฟล์ → รู้ phase, task active, และสิ่งที่รอทำทันที |
| Decision ที่เคยตัดสินใจถูกย้อนกลับโดยไม่รู้ตัว | ADR system บันทึก "ทำไม" ไว้ — AI ตรวจก่อนตัดสินใจทุกครั้ง |
| AI ตัดสินใจเรื่อง architecture เองโดยไม่แจ้ง | Decision protocol กำหนดชัดว่าอะไร AI ทำได้ อะไรต้องหยุดถาม |
| ทุก session ซ้ำงานกันเพราะไม่มี handoff | Session end protocol sync ทุกไฟล์ก่อนปิด — session ต่อไปเริ่มได้ทันที |
| Source doc เก่าขัดแย้งกับ code ปัจจุบัน | Traceability system — ทุก task อ้างอิง source reference |

---

## ประหยัด Token ~52% ทุก Session

ระบบนี้มีตัวช่วยประหยัด token ในตัว — **Token-Aware Communication Protocol (TACP)** ออกแบบมาสำหรับทั้งภาษาไทยและภาษาอังกฤษ

**ทำไมภาษาไทยถึงแพงกว่า:** AI ตัดภาษาไทยที่ 1–3 ตัวอักษร/token ขณะที่ภาษาอังกฤษ 4–5 ตัวอักษร/token ทำให้ข้อความภาษาไทยแพงกว่า 2–4 เท่าต่อความหมายเท่ากัน TACP แก้ปัญหานี้ด้วยการบังคับให้ส่วนที่ AI อ่าน (AI-CONTEXT blocks) เป็น English key-value เสมอ

| Operation | ก่อน TACP | หลัง TACP | ประหยัด |
|-----------|-----------|-----------|---------|
| Session start (อ่าน 4 ไฟล์) | ~2,030 tokens | ~135 tokens | **93%** |
| Simple confirm | ~90 tokens | ~10 tokens | **89%** |
| AI-CONTEXT block (ไทย→English) | ~89 tokens | ~28 tokens | **69%** |
| Design proposal | ~186 tokens | ~89 tokens | **52%** |
| **Session 100 messages รวม** | **~20,000 tokens** | **~9,600 tokens** | **~52%** |

→ [อ่านรายละเอียด TACP + benchmark เต็ม](architecture/tacp.md)

---

## 3 ชั้น — ใช้เท่าที่ต้องการ

```
core/                   ← ทุกคน ทุกโปรเจ็กต์ ทุก AI tool
├── Session Protocol
├── Task Board
├── ADR System
├── Memory Architecture (Phase 1–3)
└── Compliance Rules

+ skills/game/          ← เพิ่มสำหรับ game development
  ├── Game Design Standards
  ├── Balance Check System
  └── Playtesting Protocol

+ platforms/claude-code/ ← เพิ่มสำหรับ Claude Code CLI
  ├── CLAUDE.md (auto-load)
  ├── Slash Commands
  └── Git Hooks
```

---

## เริ่มต้นใช้งาน

### วิธีที่ 1: ZIP Download (แนะนำสำหรับโปรเจ็กต์ใหม่)

```bash
# ดาวน์โหลด ZIP จาก GitHub → แตกไฟล์ไปที่ _template/
# จากนั้น:
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" .
```

→ [คู่มือ Quick Start Mac/Linux](quick-start-mac-linux.md) | [Windows](quick-start-windows.md)

### วิธีที่ 2: Git Clone (สำหรับผู้ที่ต้องการ track template updates)

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git my-project
cd my-project
git checkout -b dev
# จากนั้นรัน First Run Bootstrap ใน CLAUDE.md
```

→ [คู่มือ Advanced Setup](advanced-setup.md)

---

## โครงสร้าง CoreAiWorkspaces/ ที่จะได้หลัง Bootstrap

```
CoreAiWorkspaces/
├── 00-source/          ← source documents ของโปรเจ็กต์ (versioned)
│   └── README.md
├── 01-plan/            ← work-status.md, project-plan.md
├── 02-task/            ← task-board.md
├── 03-log/             ← work-log-index.md (+ agents/ ถ้าใช้หลาย AI tool)
├── 04-way-of-work/     ← way-of-work.md, ai-decision-protocol.md, compliance.md
└── 07-decisions/       ← ADR index, entity-register.md, ADR-*.md files
```

---

## ทุก session ทำแค่นี้

**เริ่ม session:**
```
AI อ่าน 3 ไฟล์ → work-status + work-log-index + task-board
→ รู้ทันทีว่าอยู่ phase ไหน task ไหน active มีอะไรรอทำ
```

**จบ session:**
```
/caw-session-end → sync work-status + log + task-board ครั้งเดียว
```

---

## คู่มือทั้งหมด

### เริ่มต้น
- [Quick Start — Mac / Linux](quick-start-mac-linux.md)
- [Quick Start — Windows](quick-start-windows.md)
- [Existing Project Setup](advanced-setup.md)
- [สำหรับ Non-Developer (Claude.ai web)](non-technical-setup.md)

### สถาปัตยกรรม
- [ภาพรวมระบบ — Session Protocol + CoreAiWorkspaces/ Structure](architecture/overview.md)
- [TACP — Token Savings Protocol (~52% per session)](architecture/tacp.md)
- [Memory System — Phase 1–3](architecture/memory-system.md)
- [ADR System — บันทึก architectural decisions](architecture/adr-system.md)
- [How It Works (Visual)](architecture/how-it-works.html)
- [Workflow Diagram (Visual)](architecture/workflow-diagram.html)

### Integrations
- [Claude Code — CLAUDE.md, Slash Commands, Hooks](integrations/claude-code.md)
- [Claude.ai Web — Manual Workflow](integrations/claude-ai.md)
- [Vector Memory — Phase 3 Setup](integrations/vector-memory.md)

---

## สำหรับ Game Projects

ถ้าโปรเจ็กต์เป็น game ให้บอก AI ตอน bootstrap — ระบบจะโหลด `skills/game/` เพิ่มเติมอัตโนมัติ ซึ่งรวมถึง:

- Game Design Document (GDD) template
- Balance check system (`/caw-balance-check`)
- Playtesting report (`/caw-playtest-report`)
- Level design standards

---

*Repository: [github.com/BlackAkuma/ai-project-template](https://github.com/BlackAkuma/ai-project-template)*
