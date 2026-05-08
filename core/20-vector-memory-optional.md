# Vector Memory — Optional Phase 3

ระบบ local-first vector search เป็น layer เสริมบน Phase 1–2
เปิดใช้เมื่อ `CoreAiWorkspaces/` มีหลายสิบไฟล์และ `read_more` hints ไม่เพียงพออีกต่อไป

อ่าน `core/19-memory-architecture-overview.md` ก่อนไฟล์นี้เพื่อเข้าใจบริบทของ Phase 1–2

สำหรับ CLI setup และคำสั่งเฉพาะ → ดู `tools/vector-memory/`

---

## เมื่อไหร่ควรเปิดใช้

เปิดเมื่อ **อย่างน้อยหนึ่งข้อ** ต่อไปนี้เป็นจริง:

- `CoreAiWorkspaces/` มีไฟล์มากกว่า 30 ไฟล์ และหา context ยากขึ้นทุก session
- โปรเจ็กต์ทำมานานกว่า 3 เดือน และ session เก่าๆ มี decision สำคัญที่ต้องค้นหา
- ต้องการ semantic search ข้ามโปรเจ็กต์ใน `~/ai-workspace/`
- `read_more` hints ต้องชี้ไฟล์มากกว่า 5 ไฟล์ต่อ query

**ไม่ต้องเปิด** ถ้า `read_more` + entity-register ยังรองรับได้ — อย่าเพิ่ม complexity โดยไม่จำเป็น

---

## หลักการ

Vector memory layer ที่เราใช้:

- เก็บข้อมูลเป็น verbatim text — ไม่ summarize เอง AI ยังคุมคุณภาพ
- ค้นหาด้วย semantic search (local embedding, ไม่ต้อง cloud API)
- จัดข้อมูลเป็น 3 ชั้น: **Wing → Room → Drawer**
- ทำงานได้ทั้ง CLI standalone และ MCP server สำหรับ Claude Code

---

## การ Map โครงสร้าง CoreAiWorkspaces/ เข้า Vector Store

| โปรเจ็กต์ | Vector Store |
|-----------|--------------|
| ชื่อโปรเจ็กต์ | Wing |
| โฟลเดอร์ใน CoreAiWorkspaces/ (01-plan, 07-decisions) | Room |
| ไฟล์ .md แต่ละไฟล์ | Drawer |
| `~/ai-workspace/` (cross-project) | Wing แยกต่างหาก |

ตัวอย่าง:
```
Wing: "hod-software"
  Room: "decisions"    ← CoreAiWorkspaces/07-decisions/
  Room: "tasks"        ← CoreAiWorkspaces/02-task/
  Room: "plan"         ← CoreAiWorkspaces/01-plan/
  Room: "logs"         ← CoreAiWorkspaces/03-log/
```

---

## Setup

→ ดูคำสั่งติดตั้งและ setup ที่ `tools/vector-memory/`

**หลักการทั่วไป:**

1. ติดตั้ง tool
2. Index ไฟล์ใน `CoreAiWorkspaces/` โดยระบุ wing name = ชื่อโปรเจ็กต์
3. ทดสอบด้วย query เกี่ยวกับ ADR หรือ decision ในโปรเจ็กต์

**สำคัญ:** ต้องระบุ wing name เสมอเมื่อ index จาก `CoreAiWorkspaces/` subfolder
เพื่อป้องกัน wing name ชนกันระหว่างโปรเจ็กต์ที่ใช้ template เดียวกัน

---

## Zone 1 — AI Tool ทั่วไป (Manual Workflow)

ผู้ใช้รัน CLI เอง แล้ว paste ผลเข้า chat

### ตอนเริ่ม session

```
ถ้าต้องการ context เรื่อง X:
→ รัน: search "<คำที่อยากหา>" --wing <project-name>
→ copy ผลลัพธ์ paste เข้า chat
```

### ตอนจบ session (ถ้า CoreAiWorkspaces/ มีการเปลี่ยนแปลง)

```
→ รัน: index CoreAiWorkspaces/ --wing <project-name>
```

### ค้นหา cross-project

```
→ รัน: search "<query>"  # ไม่ระบุ wing = ค้นข้ามทุกโปรเจ็กต์
```

---

## Zone 2 — Claude Code CLI (Automatic Workflow)

Claude Code รัน vector search ได้โดยตรงผ่าน Bash tool และ MCP server

### Option A: Bash tool (ไม่ต้อง setup พิเศษ)

AI รันคำสั่ง search โดยตรงระหว่าง session ผ่าน Bash tool

### Option B: MCP Server (automatic, แนะนำ)

เชื่อม Claude Code กับ vector store ผ่าน MCP — AI ใช้ search ได้โดยไม่ต้อง shell command
→ ดูวิธี setup ใน `tools/vector-memory/`

### Option C: Auto-save Hooks

hooks สำหรับ Claude Code:
- **Periodic hook**: index session context ทุกช่วงเวลา
- **Pre-compact hook**: index ก่อน context ถูก compress

คำสั่ง sweep — index transcript ทั้งหมด:
```
sweep <transcript-dir> --wing <project-name>
```

→ ดูวิธี setup ใน `tools/vector-memory/`

---

## Decision Protocol: เมื่อไหร่ควร Search

### ✅ ค้น เมื่อ:

- ถามเรื่อง ADR หรือ architectural decision จาก session เก่า
- ถามเรื่อง task ที่เสร็จไปแล้วหลาย session
- ต้องการ context เฉพาะที่ไม่อยู่ใน context window ปัจจุบัน
- query มี keyword เฉพาะโปรเจ็กต์ (ชื่อ feature, ชื่อ tech, ชื่อ entity)

### ❌ ไม่ต้องค้น เมื่อ:

- เรื่องที่เพิ่งทำหรือพูดถึงใน session นี้ (อยู่ใน context แล้ว)
- คำถาม general ที่ไม่เกี่ยวกับโปรเจ็กต์นี้
- ยังไม่เคยรัน index (ยังไม่มี vector index)
- query เหมือนกับ query ก่อนหน้ามาก (ใช้ผล search เดิมก่อน)

---

## Token Budget Rules

ผลลัพธ์จาก vector search ต้องผ่าน filter ก่อนใส่ context:

| กฎ | ค่า |
|----|-----|
| จำนวน chunk สูงสุด | 5 chunks |
| token รวมสูงสุด | 1,500 token (~6,000 ตัวอักษร) |
| similarity ต่ำสุดที่ใช้ได้ | 0.35 (Thai/mixed content) หรือ 0.50 (English-only) |
| ทิ้ง chunk ที่ score ต่ำที่สุดก่อน ถ้าเกิน budget | เสมอ |

**วิธีนับ token แบบเร็ว:** ตัวอักษรไทย ÷ 2 + ตัวอักษรอังกฤษ ÷ 4

**หมายเหตุ threshold:** content ภาษาไทย + อังกฤษ mixed จะได้ cosine score ต่ำกว่า pure-English
ค่า 0.35 เหมาะกับโปรเจ็กต์ Thai/mixed — ถ้าโปรเจ็กต์เป็น English ล้วนใช้ 0.50 ได้

ถ้าผลลัพธ์ดูไม่เกี่ยวกับ query → อย่าใช้ และ note ว่า "search ไม่เจอ context ที่ต้องการ"

---

## เมื่อไหร่ควร Re-index

| เมื่อ | action |
|-------|--------|
| จบ session (ถ้า CoreAiWorkspaces/ เปลี่ยน) | index CoreAiWorkspaces/ --wing <project-name> |
| เพิ่มไฟล์ใหม่ใน CoreAiWorkspaces/ | index CoreAiWorkspaces/ --wing <project-name> |
| Index เสีย/ผลผิดพลาด | ดู tools/vector-memory/ troubleshooting |

**กฎ:** index command เป็น idempotent — รันซ้ำได้ไม่มีปัญหา, skip ไฟล์ที่ไม่เปลี่ยน

---

## บันทึกใน work-status AI-CONTEXT Block

เพิ่ม field เหล่านี้เมื่อเปิดใช้ vector memory:

```yaml
vector_memory: enabled          # enabled | later | disabled
vector_wing: <project-name>     # wing name ที่ใช้กับโปรเจ็กต์นี้
```

---

## Session Protocol Integration

### เพิ่มใน Session Start (หลัง read AI-CONTEXT blocks)

```
ถ้า vector_memory: enabled
→ ตรวจว่า task ปัจจุบันต้องการ context จาก session เก่าไหม
→ ถ้าใช่: search ด้วย keyword ของ task นั้น
→ ถ้าไม่: ข้ามได้ ไม่ต้อง search ทุกครั้ง
```

### เพิ่มใน Session End Checklist

```
□ ถ้า vector_memory: enabled และ CoreAiWorkspaces/ มีการเปลี่ยนแปลงใน session นี้
  → re-index: index CoreAiWorkspaces/ --wing <vector_wing>
```

---

## สิ่งที่ไม่เปลี่ยน

- Phase 1 (entity-register) และ Phase 2 (read_more, agent diary) ยังทำงานเหมือนเดิม
- Vector memory เป็น Layer เพิ่มเติม ไม่แทนที่ระบบเดิม
- ถ้า `vector_memory: disabled` — ไม่ต้องทำอะไรเพิ่มจาก core workflow

---

## Compliance Rules เพิ่มเติม

| Code | สิ่งที่ตรวจ |
|------|-----------|
| C-20 | ถ้า `vector_memory: enabled` และ CoreAiWorkspaces/ เปลี่ยน → ต้อง re-index ก่อนจบ session |
| C-21 | ผล search ที่ score ต่ำกว่า threshold ห้ามใส่ใน context (0.35 Thai/mixed, 0.50 English) |
| C-22 | ห้าม inject ผล search เกิน 1,500 token ต่อ session |
