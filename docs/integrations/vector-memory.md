---
title: Vector Memory — Phase 3 Setup
---

# Vector Memory (Phase 3)

Local-first semantic search สำหรับโปรเจ็กต์ขนาดใหญ่ — ค้นหา context จาก session เก่าได้โดยไม่ต้อง load ทุกไฟล์

→ [Memory System Overview](../architecture/memory-system.md) | [หน้าหลัก](../index.md)

---

## เมื่อไหร่ควรเปิดใช้

**เปิดเมื่อ อย่างน้อยหนึ่งข้อต่อไปนี้เป็นจริง:**

- `ai/` มีไฟล์มากกว่า 30 ไฟล์ และหา context ยากขึ้นทุก session
- โปรเจ็กต์ทำมานานกว่า 3 เดือน และ session เก่ามี decision สำคัญที่ต้องค้นหา
- `read_more` hints ต้องชี้ไปมากกว่า 5 ไฟล์ต่อ query
- ต้องการ semantic search ข้ามโปรเจ็กต์

**อย่าเปิด** ถ้า Phase 1–2 (entity-register + read_more hints) ยังรองรับได้ดีอยู่ — อย่าเพิ่ม complexity โดยไม่จำเป็น

---

## หลักการ: Wing / Room / Drawer

Vector store จัดโครงสร้างข้อมูลเป็น 3 ชั้น:

```
Wing (ระดับ Project)
└── Room (ระดับ Folder)
    └── Drawer (ระดับ File)
```

**ตัวอย่าง:**

```
Wing: "my-project"
├── Room: "decisions"    ← ai/07-decisions/
│   ├── Drawer: README.md
│   ├── Drawer: entity-register.md
│   └── Drawer: ADR-001-database.md
├── Room: "tasks"        ← ai/02-task/
├── Room: "plan"         ← ai/01-plan/
└── Room: "logs"         ← ai/03-log/
```

**สำคัญมาก:** ต้องระบุ Wing name ทุกครั้งที่ index — ถ้าไม่ระบุ wing จะ default เป็นชื่อ directory (`ai`) ซึ่งจะ clash กับทุกโปรเจ็กต์ที่ใช้ template เดียวกัน

---

## เลือก Tool

ระบบนี้ **tool-agnostic** — ใช้ได้กับ vector search tool ใดก็ได้ที่รองรับ:
- Local embedding (ไม่ต้อง cloud API)
- Wing/namespace separation
- Markdown indexing
- CLI สำหรับ index และ search

→ ดูคำสั่งเฉพาะของ tool ที่เลือกใช้ใน `tools/vector-memory/README.md` ในโปรเจ็กต์

---

## Setup ทั่วไป

### ขั้น 1: ติดตั้ง tool ที่เลือก

ดูคำสั่งใน `tools/vector-memory/README.md`

### ขั้น 2: Index ไฟล์ใน ai/

```bash
# รูปแบบทั่วไป:
[tool] index ai/ --wing <project-name>

# ตัวอย่าง (แทน [tool] ด้วย tool จริงที่ใช้):
[tool] index ai/ --wing my-ecommerce-project
```

**Wing name แนะนำ:** ใช้ชื่อโปรเจ็กต์ที่ unique — เช่น `my-ecommerce-project` ไม่ใช่ `project` หรือ `ai`

### ขั้น 3: ทดสอบ

```bash
# ค้นหา decision เกี่ยวกับ database
[tool] search "database choice" --wing my-ecommerce-project

# ค้นข้ามทุกโปรเจ็กต์
[tool] search "stripe integration pattern"
```

### ขั้น 4: ตั้งค่าใน work-status.md

```yaml
<!-- AI-CONTEXT
vector_memory: enabled
vector_wing: my-ecommerce-project
-->
```

---

## Zone 1: Manual Workflow (ทุก AI tool)

สำหรับผู้ใช้ Claude.ai web หรือ AI tool ที่ไม่มี file access โดยตรง

### เริ่ม session — ถ้าต้องการ context เรื่อง X

```bash
# ผู้ใช้รันเอง:
[tool] search "<สิ่งที่ต้องการหา>" --wing <project-name>

# copy ผลลัพธ์ paste เข้า chat
```

### จบ session — ถ้า ai/ มีการเปลี่ยนแปลง

```bash
[tool] index ai/ --wing <project-name>
```

---

## Zone 2: Claude Code (Automatic)

Claude Code รัน vector search ได้โดยตรงผ่าน Bash tool

### Option A: Bash tool

Claude รันคำสั่ง search โดยตรงระหว่าง session — ไม่ต้อง setup พิเศษ

Claude จะ search เมื่อ:
- ถามเรื่อง ADR หรือ decision จาก session เก่า
- Task ต้องการ context ที่ไม่อยู่ใน context window ปัจจุบัน
- Query มี keyword เฉพาะโปรเจ็กต์

### Option B: MCP Server

เชื่อม Claude Code กับ vector store ผ่าน MCP — AI ใช้ search ได้โดยไม่ต้อง shell command

ดูวิธี setup MCP ใน `tools/vector-memory/README.md`

### Option C: Auto-index Hooks

ตั้ง hooks สำหรับ Claude Code:

```bash
# Pre-compact hook: index ก่อน context ถูก compress
# ดูวิธี setup ใน tools/vector-memory/README.md
```

---

## เมื่อไหร่ควร Search / ไม่ควร Search

### ✅ ค้น เมื่อ:

- ถามเรื่อง ADR หรือ architectural decision จาก session เก่า
- ถามเรื่อง task ที่เสร็จไปแล้วหลาย session
- ต้องการ context เฉพาะที่ไม่อยู่ใน context window ปัจจุบัน
- Query มี keyword เฉพาะโปรเจ็กต์ (ชื่อ feature, ชื่อ entity)

### ❌ ไม่ต้องค้น เมื่อ:

- เรื่องที่เพิ่งทำหรือพูดถึงใน session นี้ (อยู่ใน context แล้ว)
- คำถาม general ที่ไม่เกี่ยวกับโปรเจ็กต์
- ยังไม่เคยรัน index
- Query เหมือนกับ query ก่อนหน้า (ใช้ผลเดิมก่อน)

---

## Token Budget — กฎที่ต้องทำตาม

| กฎ | ค่า | เหตุผล |
|----|-----|--------|
| จำนวน chunk สูงสุด | 5 chunks | ป้องกัน context overflow |
| Token รวมสูงสุด | 1,500 token | ~6,000 ตัวอักษร |
| Similarity threshold (Thai/mixed) | 0.35 | Thai cosine score ต่ำกว่า English โดยธรรมชาติ |
| Similarity threshold (English-only) | 0.50 | standard threshold สำหรับ pure English |

**วิธีนับ token แบบเร็ว:** ตัวอักษรไทย ÷ 2 + ตัวอักษรอังกฤษ ÷ 4

**Compliance C-21:** ผล search ที่ score ต่ำกว่า threshold → ห้าม inject เข้า context
**Compliance C-22:** ห้าม inject ผล search เกิน 1,500 token ต่อ session

ถ้าผลลัพธ์ดูไม่เกี่ยว → อย่าใช้ และ note ว่า "search ไม่เจอ context ที่ต้องการ"

---

## หมายเหตุเรื่อง Threshold สำหรับ Thai Content

Content ภาษาไทยผสมอังกฤษ (Thai/mixed) จะได้ cosine similarity score ต่ำกว่า pure-English content โดยธรรมชาติ — เพราะ embedding models ส่วนใหญ่ optimize สำหรับ English

**ตัวอย่างจาก field test:**
- Thai/mixed content → score range ประมาณ 0.31–0.53
- ถ้าใช้ threshold 0.60 (English standard) → ผลลัพธ์ดีๆ จะถูก filter ออกหมด
- Threshold 0.35 เหมาะสมสำหรับ Thai/mixed projects

ถ้าโปรเจ็กต์เป็น English ล้วน → ใช้ threshold 0.50 ได้

---

## เมื่อไหร่ควร Re-index

| เมื่อ | Action |
|-------|--------|
| จบ session (ถ้า ai/ เปลี่ยน) | `[tool] index ai/ --wing <project-name>` |
| เพิ่มไฟล์ใหม่ใน ai/ | `[tool] index ai/ --wing <project-name>` |
| Index เสีย/ผลผิดพลาด | ดู troubleshooting ใน tools/vector-memory/ |

**Index command เป็น idempotent** — รันซ้ำได้ไม่มีปัญหา, skip ไฟล์ที่ไม่เปลี่ยน

---

## Cross-Project Search

ค้นหาข้ามทุกโปรเจ็กต์ที่ index ไว้:

```bash
# ไม่ระบุ --wing = ค้นทุกโปรเจ็กต์
[tool] search "stripe integration pattern"

# ค้นเฉพาะโปรเจ็กต์เดียว
[tool] search "stripe integration" --wing my-ecommerce-project
```

ใช้กับ `~/ai-workspace/cross-project-memory.md` เพื่อ find patterns ข้ามโปรเจ็กต์

---

→ ต่อไป: [Memory System Architecture](../architecture/memory-system.md) | [Claude Code Setup](claude-code.md)
