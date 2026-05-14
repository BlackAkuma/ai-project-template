# CLAUDE.md — ai-project-template

ไฟล์นี้ถูกโหลดอัตโนมัติโดย Claude Code
ใช้ได้ทั้งสองกรณี: **พัฒนา template นี้เอง** และ **clone เป็นฐานโปรเจ็กต์ใหม่**

---

## กรณีที่ 1 — คุณกำลังพัฒนา template นี้

ถ้าคุณเป็นผู้พัฒนาที่กำลังแก้ไข core/, platforms/, skills/ หรือ tests/:

- `CoreAiWorkspaces/` ในโฟลเดอร์นี้ = AI working folder สำหรับ template project เอง
- ทำงานบน `dev` branch เสมอ — ห้าม commit ตรงไปที่ `master`
- อ่าน `CoreAiWorkspaces/01-plan/work-status.md` เพื่อดูสถานะปัจจุบัน

→ ทำตาม Session Protocol ด้านล่างได้เลย

---

## กรณีที่ 2 — คุณ clone repo นี้เป็นโปรเจ็กต์ใหม่

ถ้าคุณใช้ repo นี้เป็นจุดเริ่มต้นของโปรเจ็กต์ตัวเอง:

**ขั้นตอนหลัง clone:**

```bash
# 1. สร้าง dev branch สำหรับโปรเจ็กต์ตัวเอง
git checkout -b dev

# 2. AI จะ bootstrap และสร้าง CoreAiWorkspaces/ ให้
# (ทำตาม First Run Bootstrap ด้านล่าง)

# 3. หลัง bootstrap เสร็จ ลบไฟล์ที่ไม่ต้องการออก
rm -rf CoreAiWorkspaces/ docs/ tests/ CHANGELOG.md ROADMAP.md
# CoreAiWorkspaces/     — tracking ของ template project เอง (ไม่ใช่ของโปรเจ็กต์คุณ)
# docs/   — web pages ของ template (อยู่บน gh-pages branch)
# (core/, platforms/, skills/ ยังต้องเก็บไว้ — AI อ่านทุก session)
```

→ ทำตาม First Run Bootstrap ด้านล่าง

---

## เริ่มต้น Session

**ก่อนทำอะไร** ตรวจว่า `CoreAiWorkspaces/` มีอยู่ไหม:

- **ยังไม่มี** → ทำ **First Run Bootstrap** (ด้านล่าง)
- **มีแล้ว** → ทำ **Session Start Protocol** (ด้านล่าง)

---

## First Run Bootstrap

ทำครั้งเดียวตอนสร้างโปรเจ็กต์ใหม่:

1. ถามผู้ใช้ 2 เรื่องพร้อมกัน รอคำตอบก่อน:
   - ภาษาที่จะสื่อสารกัน
   - Promotion pipeline: `dev→main` / `dev→sit→uat→main` / อื่นๆ (ให้ระบุ)
2. ตรวจว่ามี `~/ai-workspace/cross-project-memory.md` ไหม — ถ้ามีให้อ่านก่อน
3. อ่านไฟล์ใน `core/` ทั้งหมดตามลำดับ (00 → 21)
4. ถ้าโปรเจ็กต์เป็น game หรือ web game → อ่าน `skills/game/` ต่อด้วย (00 → 11)
5. สร้างโครงสร้าง `CoreAiWorkspaces/` ตาม core/01 template
6. กรอกข้อมูลโปรเจ็กต์จาก context ที่มี — ใส่ placeholder ชัดเจนถ้าไม่พอ ห้ามเดา
   บันทึก `git_pipeline` ที่ได้จากข้อ 1 ใน work-status AI-CONTEXT block ด้วย
7. เพิ่มโปรเจ็กต์นี้ลงใน `~/ai-workspace/cross-project-memory.md` (ถ้ามีไฟล์นั้นอยู่)
8. ตรวจสอบกับ `core/10-bootstrap-checklist-template.md` ก่อนประกาศว่าเสร็จ

จากนั้น → ทำ Session Start Protocol ต่อ

---

## Session Start Protocol

ทำตามลำดับนี้ทุก session:

1. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/01-plan/work-status.md`
   - ถ้า `git_mode: branch-separated` → รัน `git branch --show-current` ทันที
   - ถ้า branch ปัจจุบัน == `git_prod_branch` → **หยุด** แจ้งผู้ใช้ก่อน
2. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/03-log/work-log-index.md`
3. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/02-task/task-board.md`
4. ถ้า `CoreAiWorkspaces/03-log/agents/claude-code.md` มีอยู่ → อ่าน AI-CONTEXT block ด้วย
5. ถ้า work-status มี `read_more` field → แสดงให้ผู้ใช้เห็น
6. ตรวจ gap ระหว่าง task board และ source docs (Scenario H ใน `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`)
7. รัน compliance scan อัตโนมัติ (ดู `CoreAiWorkspaces/04-way-of-work/compliance.md`)
8. รายงานสถานะ: phase ปัจจุบัน, task ที่ active, สิ่งที่ต้องทำก่อน

---

## Session End Protocol

ก่อนจบ session ทุกครั้ง — รัน `/caw-session-end` หรือทำตามลำดับ:

1. อัปเดต `work-status` — body **และ** AI-CONTEXT block
2. เพิ่ม entry ใน `work-log-index` — body **และ** AI-CONTEXT block
3. อัปเดต `task-board` — status **และ** AI-CONTEXT block (ถ้ามี task เปลี่ยน)
4. task ที่ยัง in_progress → mark เป็น `[IN_PROGRESS: checkpoint saved — <สิ่งที่ทำไปแล้ว>]`
5. ถ้า `git_mode: branch-separated` → รัน `git push origin [git_dev_branch]`

---

## Project Context

- Source docs: `CoreAiWorkspaces/00-source/`
- Work status: `CoreAiWorkspaces/01-plan/work-status.md`
- Task board: `CoreAiWorkspaces/02-task/task-board.md`
- Way of work: `CoreAiWorkspaces/04-way-of-work/way-of-work.md`
- Decision protocol: `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`
- Compliance rules: `CoreAiWorkspaces/04-way-of-work/compliance.md`
- ADR index: `CoreAiWorkspaces/07-decisions/README.md`

---

## Token-Aware Communication Protocol (TACP)

AI ใช้ 3-layer model — destination กำหนด format อัตโนมัติ:

| Layer | Destination | Language | Format |
|-------|-------------|----------|--------|
| **L1** | AI-CONTEXT blocks, internal logic | English only | Dense key-value, no prose |
| **L2** | Chat output to user | L2_LANG (`th`) | Compressed Thai, verbosity V1–V5 |
| **L3** | Shared files (caw-*.md, templates) | Dual-block | AI-CONTEXT (L1) + HUMAN-CONTEXT (L2) |

**Verbosity scale:** V1=ยืนยัน · V2=รายการสั้น · V3=อธิบาย · V4=เสนอ design · V5=warning/destructive

**Thai compression (L2):** one polite anchor per message block · drop redundant particles · noun phrases in lists · English for tech terms

อ้างอิง protocol เต็ม: `CoreAiWorkspaces/04-way-of-work/tacp.md`

---

## Language Policy

- AI-internal reasoning: English
- Output to user: ตาม `tacp.L2_LANG` ใน `CoreAiWorkspaces/04-way-of-work/way-of-work.md` (default: `th`)
- AI-CONTEXT blocks: English เสมอ (L1)
- Code / identifiers: English เสมอ

---

## Key Rules

- ห้าม implement โดยไม่รู้ source reference
- **บอก plan ก่อนเขียน code เสมอ** — อธิบายว่าจะทำอะไร ทำไม แล้วรอยืนยันก่อน implement
- ห้ามแก้ requirement โดยตรง — ต้อง version ใหม่หรือ extension doc
- ห้ามตัดสินใจเรื่อง architecture โดยไม่สร้าง ADR draft
- ทุก session ต้องทำ Session End Protocol ก่อนจบ
- ถ้าไม่แน่ใจ: Do less, document more

---

## Skill Pack Detection

ถ้าโปรเจ็กต์มี `CoreAiWorkspaces/08-design/` → โหลด game skill standards อัตโนมัติ (skills/game/ 00–11)

---

## Available Slash Commands

```
/caw-compliance-check   รัน compliance scan ทันที
/caw-fdd-create         สร้าง FDD template สำหรับ feature ใหม่
/caw-adr-create         สร้าง ADR สำหรับ architectural decision
/caw-session-end        sync work-status + log + task-board ครบในคำสั่งเดียว
/caw-scope-check        ตรวจ scope ของ task ปัจจุบัน
/caw-launch-check       รัน launch checklist ก่อน deploy
/caw-archive-logs       compress session เก่าเป็น monthly archive
/caw-update             อัปเดต caw-* commands และ CLAUDE.md เป็น version ใหม่
```
