# CLAUDE.md — Project Bootstrap (Claude Code)

ไฟล์นี้ถูกโหลดอัตโนมัติทุก session โดย Claude Code
Protocol หลักอยู่ใน `AI.md` — ไฟล์นี้เพิ่ม Claude-specific features เข้ามา

> **เปลี่ยนมาจาก AI tool อื่น?** → อ่าน `AI.md` แทน (universal protocol สำหรับทุก tool)

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
2. ตรวจว่ามี `~/ai-workspace/cross-project-memory.md` ไหม — ถ้ามีให้อ่านก่อน เพื่อดู pattern และ lesson จากโปรเจ็กต์เก่า
3. อ่านไฟล์ใน `core/` ทั้งหมดตามลำดับ (00 → 18)
4. ถ้าโปรเจ็กต์เป็น game หรือ web game → อ่าน `skills/game/` ต่อด้วย (00 → 06)
5. สร้างโครงสร้าง `CoreAiWorkspaces/` ตาม core/01 template
6. กรอกข้อมูลโปรเจ็กต์จาก context ที่มี — ใส่ placeholder ชัดเจนถ้าไม่พอ ห้ามเดา
   บันทึก `git_pipeline` ที่ได้จากข้อ 1 ใน work-status AI-CONTEXT block ด้วย
7. เพิ่มโปรเจ็กต์นี้ลงใน Project Registry ของ `~/ai-workspace/cross-project-memory.md` (ถ้ามีไฟล์นั้นอยู่)
8. ตรวจสอบกับ `core/10-bootstrap-checklist-template.md` ก่อนประกาศว่าเสร็จ

จากนั้น → ทำ Session Start Protocol ต่อ

---

## Session Start Protocol

ทำตามลำดับนี้ทุก session:

1. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/01-plan/work-status.md`
   - ถ้า `git_mode: branch-separated` → รัน `git branch --show-current` ทันที
   - ถ้า branch ปัจจุบัน == `git_prod_branch` → **หยุด** แจ้งผู้ใช้ก่อนดำเนินการต่อ: "คุณอยู่บน production branch ([branch]) แนะนำให้ switch ไป [git_dev_branch] ก่อน"
2. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/03-log/work-log-index.md`
3. อ่าน AI-CONTEXT block ของ `CoreAiWorkspaces/02-task/task-board.md`
4. ถ้า `CoreAiWorkspaces/03-log/agents/claude-code.md` มีอยู่ → อ่าน AI-CONTEXT block ของไฟล์นั้นด้วย เพื่อรับ checkpoint ที่ Claude Code session ก่อนหน้าบันทึกไว้ *(ไฟล์นี้มีเฉพาะโปรเจ็กต์ที่ใช้ AI tool มากกว่า 1 ตัว)*
5. ถ้า work-status มี `read_more` field → แสดงให้ผู้ใช้เห็นว่าอ่านเพิ่มได้ที่ไหนถ้าต้องการ context เจาะจง
6. ตรวจ gap ระหว่าง task board และ source docs (Scenario H ใน `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`)
7. รัน compliance scan อัตโนมัติ (ดู `CoreAiWorkspaces/04-way-of-work/compliance.md`)
8. รายงานสถานะ: phase ปัจจุบัน, task ที่ active, สิ่งที่ต้องทำก่อน

---

## Batch Checkpoint (ทำระหว่าง session)

**ทุกครั้งที่ commit feature สำคัญ** → หยุด 1 ครั้ง sync 3 ไฟล์ก่อนทำต่อ:

```
□ work-status.md   — body สะท้อนสิ่งที่เพิ่งทำ + AI-CONTEXT block ตรงกัน
□ task-board.md    — task ที่ทำเสร็จย้ายไป Done · task ใหม่ที่พบ register ไว้
□ work-log-index.md — มี entry บันทึก batch นี้
```

ไม่ต้องรอ session จบ — **commit code แล้ว commit docs ในครั้งถัดไปทันที**  
ถ้า user บอก "ทำต่อ" แต่ docs ยังค้าง → sync ก่อน แล้วค่อยทำต่อ

> กฎ: body ของไฟล์คือ source of truth — อ่าน body ก่อน แก้ body ก่อน แล้วค่อย sync AI-CONTEXT block  
> ห้าม reverse (อัปเดต block แต่ไม่แตะ body)

---

## Session End Protocol

ก่อนจบ session ทุกครั้ง — **บังคับ** รัน `/caw-session-end`:

1. อัปเดต `work-status` — body **และ** AI-CONTEXT block
2. เพิ่ม entry ใน `work-log-index` — body **และ** AI-CONTEXT block
3. อัปเดต `task-board` — status **และ** AI-CONTEXT block (ถ้ามี task เปลี่ยน)
4. task ที่ยัง in_progress → mark เป็น `[IN_PROGRESS: checkpoint saved — <สิ่งที่ทำไปแล้ว>]`
5. ถ้า `git_mode: branch-separated` → รัน `git push origin [git_dev_branch]` เพื่อป้องกัน data loss

**กฎ sync:** AI-CONTEXT block ต้องสะท้อน body เสมอ — ถ้าไม่ตรงให้เชื่อ body และอัปเดต block

---

## Context Window Management

**เมื่อ context ใกล้เต็ม — Pre-compact:**

1. บันทึก checkpoint ใน `work-log-index`: สรุปสิ่งที่ทำไปแล้วและหยุดตรงไหน
2. อัปเดต `work-status` ให้สะท้อนสถานะปัจจุบัน
3. mark task เป็น `[IN_PROGRESS: checkpoint saved — <สรุปสั้น>]`
4. บันทึก next action ที่ชัดเจน

**หลัง context ถูก compact — Post-compact:**

1. อ่าน AI-CONTEXT block ของ 3 ไฟล์หลัก + `CoreAiWorkspaces/07-decisions/README.md`
2. ยืนยันว่า task ที่กำลังทำตรงกับ checkpoint ที่บันทึกไว้
3. ถ้าพบความไม่สอดคล้อง → ทำตาม Scenario B ใน `ai-decision-protocol.md`

**หมายเหตุสำคัญ:** AI-CONTEXT block ใช้สำหรับ orient เท่านั้น — งานละเอียดอ่อน (เช่น architecture, security, requirement conflict) ให้อ่าน **body ของไฟล์ต้นฉบับเสมอ** อย่าตัดสินใจจาก AI-CONTEXT block เพียงอย่างเดียว

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

## Branching & Backup Policy

กฎ branching อยู่ใน `CoreAiWorkspaces/04-way-of-work/` (bootstrapped จาก `core/21-git-workflow-template.md`) — ใช้กับทุก AI tool เหมือนกัน

**ก่อนแตะโค้ดทุกครั้ง → รัน Scenario M** ใน `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`

---

## Key Rules

- ห้าม implement โดยไม่รู้ source reference
- **บอก plan ก่อนเขียน code เสมอ** — อธิบายว่าจะทำอะไร ทำไม แล้วรอยืนยันก่อน implement
- ห้ามแก้ requirement โดยตรง — ต้อง version ใหม่หรือ extension doc
- ห้ามตัดสินใจเรื่อง architecture โดยไม่สร้าง ADR draft
- ทุก session ต้องทำ Session End Protocol ก่อนจบ
- ถ้าไม่แน่ใจ: Do less, document more
- เมื่อพบข้อมูลใหม่ที่ต้องเก็บ → ใช้ Memory Scope decision tree (Scenario K ใน `ai-decision-protocol.md`) ตัดสินว่าเก็บที่ไหน
- ห้ามเขียนลง `~/ai-workspace/cross-project-memory.md` โดยไม่ถามผู้ใช้ก่อน
- เมื่อพบ `[ENTITY:deprecated]` หรือ `[ENTITY:superseded]` ในโค้ด task หรือ ADR → ตรวจ entity-register ก่อนเสมอ (Scenario J ใน `ai-decision-protocol.md`)

---

## Skill Pack Detection

ถ้าโปรเจ็กต์มี `CoreAiWorkspaces/08-design/` → โหลด game skill standards อัตโนมัติ (skills/game/ 00–11):
- ทุก feature ใหม่ต้องมี FDD ก่อน implement
- task lifecycle: todo → design_validate → in_progress → playtest → review → done
- compliance rules G-01 ถึง G-10, A-01 ถึง A-07, N-01 ถึง N-04, U-01 ถึง U-03, L-01 ถึง L-02 บังคับใช้

---

## Game Specialist Agents (Claude Code เท่านั้น)

สำหรับ game project สามารถ invoke specialist agents เพื่อ review เชิงลึก:

| Agent | ใช้เมื่อ |
|-------|---------|
| `game-designer` | ออกแบบ mechanic ใหม่, review FDD vs GDD, วิเคราะห์ degenerate strategies |
| `game-art-director` | review asset, ตรวจ color palette, gate review ด้าน visual |
| `game-narrative-director` | review dialogue, character voice, ludonarrative conflicts |
| `game-ux-designer` | ออกแบบ screen flow, review HUD, ตรวจ input mapping |
| `game-performance-analyst` | วิเคราะห์ bottleneck, review performance budget, frame timing |

ไฟล์ agent อยู่ที่ `platforms/claude-code/agents/` — Claude Code โหลดอัตโนมัติ

**Invoke ด้วย `/caw-game-review`** เพื่อรัน gate review จาก agent ที่เกี่ยวข้องทั้งหมด

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
/caw-tool-clean         ลบ config ของ AI tool ที่ไม่ใช้แล้ว เหลือเฉพาะ tool ที่ต้องการ
/caw-balance-check      รัน balance check สำหรับ game config (game projects)
/caw-playtest-report    สร้าง playtest report template (game projects)
/caw-game-review        รัน milestone gate review โดย specialist agents (game projects)
```
