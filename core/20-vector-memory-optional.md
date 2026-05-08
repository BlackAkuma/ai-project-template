# Vector Memory — Optional Phase 3

ระบบนี้ใช้ **MemPalace** เป็น implementation — local-first, ไม่ต้อง cloud API, ไม่มีค่าใช้จ่ายรายเดือน
เปิดใช้เมื่อ `ai/` มีหลายสิบไฟล์และ `read_more` hints (Phase 2) ไม่เพียงพออีกต่อไป

อ่าน `core/19-memory-architecture-overview.md` ก่อนไฟล์นี้เพื่อเข้าใจบริบทของ Phase 1–2

---

## เมื่อไหร่ควรเปิดใช้

เปิดเมื่อ **อย่างน้อยหนึ่งข้อ** ต่อไปนี้เป็นจริง:

- `ai/` มีไฟล์มากกว่า 30 ไฟล์ และหา context ยากขึ้นทุก session
- โปรเจ็กต์ทำมานานกว่า 3 เดือน และ session เก่าๆ มี decision สำคัญที่ต้องค้นหา
- ต้องการ semantic search ข้ามโปรเจ็กต์ใน `~/ai-workspace/`
- `read_more` hints ต้องชี้ไฟล์มากกว่า 5 ไฟล์ต่อ query

**ไม่ต้องเปิด** ถ้า `read_more` + entity-register ยังรองรับได้ — อย่าเพิ่ม complexity โดยไม่จำเป็น

---

## MemPalace คืออะไร

MemPalace เป็น local AI memory system ที่:

- เก็บข้อมูลเป็น verbatim text (ไม่ summarize เอง — AI ยังคุมคุณภาพ)
- ค้นหาด้วย semantic search (ChromaDB backend, ~300 MB disk)
- จัดข้อมูลเป็น 3 ชั้น: **Wing → Room → Drawer**
- ทำงานได้ทั้ง CLI standalone และ MCP server สำหรับ Claude Code
- Recall แม่นยำ 96.6% R@5 โดยไม่ต้อง LLM call เพิ่ม

GitHub: https://github.com/MemPalace/mempalace

---

## การ Map โครงสร้าง ai/ กับ MemPalace

| โปรเจ็กต์ | MemPalace |
|-----------|-----------|
| ชื่อโปรเจ็กต์ | Wing |
| โฟลเดอร์ใน ai/ (01-plan, 07-decisions) | Room |
| ไฟล์ .md แต่ละไฟล์ | Drawer |
| `~/ai-workspace/` (cross-project) | Wing แยกต่างหาก |

ตัวอย่าง:
```
Wing: "hod-software"
  Room: "decisions"    ← ai/07-decisions/
  Room: "tasks"        ← ai/02-task/
  Room: "plan"         ← ai/01-plan/
  Room: "logs"         ← ai/03-log/
```

---

## Setup (ทำครั้งเดียวตอน bootstrap)

### ขั้น 1: ติดตั้ง

```bash
pip install mempalace
```

disk: ~300 MB สำหรับ embedding model (โหลดครั้งแรกอัตโนมัติ)
Palace location: `~/.mempalace/palace` (default — ทุกโปรเจ็กต์ใช้ palace เดียวกัน แยกด้วย wing)

### ขั้น 2: (Optional) Init wizard

```bash
mempalace init .
```

**หมายเหตุ:** `init` เป็น interactive wizard — ตรวจ git history และถามยืนยัน people/projects
**ข้ามขั้นนี้ได้** — `mine` ทำงานได้โดยไม่ต้อง init ก่อน

### ขั้น 3: Index ไฟล์ใน ai/

```bash
mempalace mine ai/ --wing <project-name>
```

**สำคัญ:** ต้องระบุ `--wing` เสมอเมื่อ mine จาก `ai/` subfolder
หากไม่ระบุ wing จะ default เป็น `ai` ซึ่งจะชนกันทุกโปรเจ็กต์ที่ใช้ template นี้

### ขั้น 4: ทดสอบ

```bash
mempalace search "authentication decisions" --wing <project-name>
mempalace status                              # ดู palace contents
mempalace wake-up --wing <project-name>       # L0+L1 context (~600-900 tokens)
```

ถ้า `search` คืนผลมีเนื้อหาจาก ADR หรือ work-log = setup สำเร็จ

---

## Zone 1 — AI Tool ทั่วไป (Manual Workflow)

ผู้ใช้รัน MemPalace CLI เอง แล้ว paste ผลเข้า chat

### ตอนเริ่ม session

```bash
# ถ้าต้องการ context เรื่อง X:
mempalace search "<คำที่อยากหา>" --wing <project-name>
# copy ผลลัพธ์ paste เข้า chat
```

### ตอนจบ session (ถ้า ai/ มีการเปลี่ยนแปลง)

```bash
mempalace mine ai/ --wing <project-name>
```

### ค้นหา cross-project

```bash
mempalace search "<query>" --wing ai-workspace
```

---

## Zone 2 — Claude Code CLI (Automatic Workflow)

Claude Code รัน MemPalace ได้โดยตรงผ่าน Bash tool และ MCP server

### Option A: Bash tool (ไม่ต้อง setup พิเศษ)

AI รัน `mempalace search` โดยตรงระหว่าง session:

```bash
# AI รันเองใน session
mempalace search "JWT token decisions" --wing <project-name>
```

### Option B: MCP Server (automatic, แนะนำ)

MemPalace มี MCP server 29 tools — AI ใช้ palace ได้โดยไม่ต้อง shell command

Setup: ดู https://mempalaceofficial.com/reference/mcp-tools

### Option C: Auto-save Hooks

MemPalace hooks สำหรับ Claude Code:
- **Periodic hook**: บันทึก session context ทุกช่วงเวลา
- **Pre-compact hook**: บันทึกก่อน context ถูก compress

Setup: ดู https://mempalaceofficial.com/guide/hooks

คำสั่ง sweep (index transcript ทั้งหมด):
```bash
mempalace sweep <transcript-dir> --wing <project-name>
```

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
- ยังไม่เคยรัน `mempalace mine` (ยังไม่มี index)
- query เหมือนกับ query ก่อนหน้ามาก (ใช้ผล search เดิมก่อน)

---

## Token Budget Rules

ผลลัพธ์จาก MemPalace search ต้องผ่าน filter ก่อนใส่ context:

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

| เมื่อ | คำสั่ง |
|-------|--------|
| จบ session (ถ้า ai/ เปลี่ยน) | `mempalace mine ai/ --wing <project-name>` |
| เพิ่มไฟล์ใหม่ใน ai/ | `mempalace mine ai/ --wing <project-name>` |
| Rebuild ทั้งหมด (index เสีย/เก่า) | ลบ palace แล้วรัน init + mine ใหม่ |

**กฎ:** mine command เป็น idempotent — รันซ้ำได้ไม่มีปัญหา, skip ไฟล์ที่ไม่เปลี่ยน

---

## บันทึกใน work-status AI-CONTEXT Block

เพิ่ม field เหล่านี้เมื่อเปิดใช้ vector memory:

```yaml
vector_memory: enabled          # enabled | later | disabled
vector_wing: <project-name>     # wing name ที่ใช้กับโปรเจ็กต์นี้
vector_palace: ~/ai-workspace/mempalace/<project-name>
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
□ ถ้า vector_memory: enabled และ ai/ มีการเปลี่ยนแปลงใน session นี้
  → รัน: mempalace mine ai/ --wing <vector_wing>
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
| C-20 | ถ้า `vector_memory: enabled` และ ai/ เปลี่ยน → ต้อง re-mine ก่อนจบ session |
| C-21 | ผล search ที่ score ต่ำกว่า threshold ห้ามใส่ใน context (0.35 สำหรับ Thai/mixed, 0.50 สำหรับ English) |
| C-22 | ห้าม inject ผล search เกิน 1,500 token ต่อ session |
