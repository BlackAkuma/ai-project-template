# Way of Work Template

คัดลอกและปรับไฟล์นี้เป็น `CoreAiWorkspaces/04-way-of-work/way-of-work.md`

## Purpose

เอกสารนี้กำหนดวิธีทำงานร่วมกันของโปรเจ็กต์ `<PROJECT_NAME>` เพื่อให้ทุก session รู้ว่า:

- ต้องเริ่มอ่านจากไหน
- งานล่าสุดไปถึงไหน
- อะไรเสร็จ อะไรค้าง
- ต้องอัปเดต status, log, summary อย่างไร
- ต้องอ้างอิง source docs เวอร์ชันใด

## Files That Must Be Read First

อ่านตามลำดับนี้ทุก session — 3 ไฟล์แรกมี `AI-CONTEXT` block ด้านบน อ่าน block นั้นก่อนเพื่อ orient อย่างรวดเร็ว จากนั้นอ่าน body เฉพาะส่วนที่ต้องการรายละเอียดเพิ่ม

1. `CoreAiWorkspaces/01-plan/work-status.md` — อ่าน AI-CONTEXT block ก่อน
2. `CoreAiWorkspaces/03-log/work-log-index.md` — อ่าน AI-CONTEXT block ก่อน
3. `CoreAiWorkspaces/02-task/task-board.md` — อ่าน AI-CONTEXT block ก่อน
4. `CoreAiWorkspaces/01-plan/project-plan.md`
5. `CoreAiWorkspaces/04-way-of-work/coding-standards.md`
6. source doc index ใน `CoreAiWorkspaces/00-source/`
7. source docs เวอร์ชันปัจจุบันใน `CoreAiWorkspaces/00-source/versions/`

## AI-CONTEXT Block Format

ไฟล์ operating 3 ไฟล์ข้างต้นมี block นี้อยู่ด้านบนสุด:

```
<!-- AI-CONTEXT
key: value
...
-->
```

Block นี้คือ snapshot ที่อัปเดตทุก session — AI อ่าน block เดียวได้ context ทันทีโดยไม่ต้องอ่าน body ทั้งไฟล์
หลังอ่าน block ครบทั้ง 3 ไฟล์ ถ้าต้องการรายละเอียดค่อยอ่าน body เพิ่ม

## Source of Truth by Purpose

- business/product source docs: `CoreAiWorkspaces/00-source/versions/<CURRENT_SOURCE_VERSION>/...`
- แผนหลัก: `CoreAiWorkspaces/01-plan/project-plan.md`
- สถานะล่าสุด: `CoreAiWorkspaces/01-plan/work-status.md`
- งานและ ticket: `CoreAiWorkspaces/02-task/task-board.md`
- handoff summary: `CoreAiWorkspaces/03-log/work-log-index.md`

## Language Policy

| บริบท | ภาษาที่ใช้ | เหตุผล |
|-------|-----------|--------|
| กระบวนการคิด / reasoning ภายใน | English | token-efficient, AI ประมวลผลได้เร็วกว่า |
| output ที่สื่อสารกับผู้ใช้ | `<PROJECT_LANGUAGE>` | ผู้ใช้อ่านได้สะดวก |
| เนื้อหาในไฟล์เอกสาร (work-status, task-board, log ฯลฯ) | `<PROJECT_LANGUAGE>` | มนุษย์ต้องอ่านและ maintain |
| AI-CONTEXT block | English | AI อ่าน ไม่ใช่มนุษย์ |
| code, variable names, technical identifiers | English | convention สากล |

`<PROJECT_LANGUAGE>` = ภาษาที่ตกลงกับผู้ใช้ตอน setup
ค่าที่ใช้ได้: `Thai` | `English` | `Japanese` | ฯลฯ — ใช้ให้สอดคล้องกันทุกไฟล์
ตัวอย่าง: `<PROJECT_LANGUAGE>` = `Thai`

**กฎ:** AI ห้าม output ภาษาอื่นกับผู้ใช้โดยไม่ได้รับอนุญาต แม้จะคิดภายในเป็นภาษาอะไรก็ตาม

## Rule Classification

กฎในระบบนี้แบ่งเป็น 2 ระดับ — AI ต้องแยกแยะให้ออก:

| ระดับ | Marker | ความหมาย |
|-------|--------|----------|
| **⛔ HARD RULE** | `⛔` นำหน้า | ห้ามข้าม ห้ามต่อรอง ไม่มี exception ใด ๆ ทั้งสิ้น momentum / "ทำต่อ" / "ได้เลย" ไม่ใช่ข้ออ้าง |
| Guideline | ไม่มี marker | แนวปฏิบัติที่ดี มี context ที่ยืดหยุ่นได้ |

**กฎที่ mark `⛔` ต้องทำก่อนทุกอย่างเสมอ — รวมถึงตอนที่ user บอกให้ทำต่อ**

## Core Working Rules

- ห้ามเริ่ม implement โดยไม่รู้ source docs ที่ใช้อ้างอิง
- ห้ามเขียนทับ source docs revision เดิม
- ถ้ามี scope ใหม่เกินต้นฉบับ ให้สร้าง extension doc หรือ source version ใหม่
- ทุก session ต้องอัปเดต status และ log index
- ⛔ **body ของไฟล์คือ source of truth** — อ่าน body ก่อน แก้ body ก่อน แล้ว sync AI-CONTEXT block ตาม ห้าม reverse

## Batch Checkpoint Rule

ทุก feature commit → ต้องตามด้วย doc sync ทันที (**ไม่รอ session จบ**):

```
□ work-status.md    — body สะท้อนสิ่งที่เพิ่งทำ · AI-CONTEXT block ตรงกับ body
□ task-board.md     — task เสร็จย้ายไป Done · task ใหม่ที่พบ register ไว้
□ work-log-index.md — มี entry บันทึก batch นี้
```

ถ้า user บอก "ทำต่อ" แต่ docs ยังค้าง → **sync ก่อน แล้วค่อยทำต่อ**

## Logging Rule

- daily log ใช้เก็บรายละเอียดรายวัน
- work-log-index ใช้เป็น summary สำหรับ handoff
- ถ้า repo ต้องเบา ให้เก็บเฉพาะ summary ระดับเดือนขึ้นไปใน git

## Start-of-Session Checklist

ทำตามลำดับนี้ทุกครั้งที่เริ่ม session ใหม่:

- [ ] อ่าน AI-CONTEXT block ของ `work-status.md` — รู้ phase/focus/blocked ปัจจุบัน
- [ ] ถ้า `git_mode: branch-separated` → ตรวจ branch ปัจจุบัน: `git branch --show-current` — ถ้าอยู่บน `git_prod_branch` ให้หยุดและแจ้งผู้ใช้ก่อนดำเนินการต่อ
- [ ] อ่าน AI-CONTEXT block ของ `work-log-index.md` — รู้ว่า session ก่อนทำอะไรไปแล้ว
- [ ] อ่าน AI-CONTEXT block ของ `task-board.md` — รู้ว่า task ไหน active/blocked
- [ ] ตรวจ gap: task ที่ `in_progress` ใน board มี source reference ครบไหม?
- [ ] ถ้าพบ gap หรือ inconsistency → ทำตาม Scenario H ใน `ai-decision-protocol.md`
- [ ] รัน compliance scan อัตโนมัติ (ถ้าไม่ได้ pause)

## End-of-Session Checklist

ก่อนจบงานทุกครั้งอย่างน้อยต้องทำครบทุกข้อ:

- [ ] `work-status` — อัปเดต body **และ** AI-CONTEXT block
- [ ] `work-log-index` — เพิ่ม entry ใหม่ **และ** อัปเดต AI-CONTEXT block
- [ ] `task-board` — เปลี่ยน status **และ** AI-CONTEXT block ถ้ามี task เปลี่ยน
- [ ] daily log / daily summary ใน local workspace
- [ ] task ที่ทำค้างอยู่ต้องมี `[IN_PROGRESS: checkpoint saved]` พร้อมสรุปสิ่งที่ทำไปแล้ว
- [ ] ถ้า `git_mode: branch-separated` → `git push origin [git_dev_branch]` ป้องกัน data loss

**กฎ sync:** AI-CONTEXT block และ body ต้องสะท้อนข้อมูลเดียวกันเสมอ ถ้า block กับ body ไม่ตรงกัน ให้เชื่อ body และอัปเดต block ทันที

## Branching Policy

**ก่อนเริ่มทุก task** → รัน Scenario M checklist ใน `ai-decision-protocol.md`

| สถานการณ์ | ทำอะไร |
|-----------|--------|
| งาน ≤2 ไฟล์ | ทำบน dev ได้ |
| งานใหญ่ / feature / ADR-level / ≥3 ไฟล์ | `git checkout -b feature/<task-id>-<name>` ก่อนแตะโค้ด |
| มี feature branch ค้างอยู่ | ห้ามแตก branch ใหม่ — จัดการ branch ค้างก่อน |
| Promotion dev→SIT/UAT/main | รอ user สั่งเท่านั้น |
| Session End | push เสมอ (WIP OK) |

รายละเอียดเต็ม → `CLAUDE.md ## Branching & Backup Policy` หรือ `core/21-git-workflow-template.md`

## Context Window Management

เมื่อ context ใกล้เต็มกลางคัน (สังเกตจากการตอบสนองช้าลง หรือ AI ขอสรุป context ใหม่):

**Minimal Context Set** — 4 ไฟล์ที่ให้ข้อมูลมากที่สุดในเวลาน้อยที่สุด:
1. `CoreAiWorkspaces/01-plan/work-status.md` — สถานะปัจจุบัน
2. `CoreAiWorkspaces/02-task/task-board.md` — งานที่กำลังทำ
3. `CoreAiWorkspaces/03-log/work-log-index.md` — สิ่งที่ทำไปแล้ว (entry ล่าสุด)
4. `CoreAiWorkspaces/07-decisions/README.md` — ADR index (ป้องกัน reverse decisions)

**Pre-compact protocol** — ทำก่อน context ถูกบีบ:
1. บันทึก checkpoint ใน work-log: สรุปสิ่งที่ทำไปแล้วและหยุดตรงไหน
2. อัปเดต work-status ให้สะท้อนสถานะปัจจุบัน
3. mark task เป็น `[IN_PROGRESS: checkpoint saved — <สรุปสั้น>]`
4. บันทึก next action ที่ชัดเจนว่า session ใหม่ต้องทำอะไรก่อน

**Post-compact protocol** — หลัง context ถูกบีบแล้ว:
1. อ่าน minimal context set ทั้ง 4 ไฟล์ก่อนทำงานต่อ
2. ยืนยันว่า task ที่กำลังทำยังตรงกับ checkpoint ที่บันทึกไว้
3. ถ้าพบความไม่สอดคล้อง → ทำตาม Scenario B ใน `ai-decision-protocol.md`

## Multi-AI / Multi-Tool Coordination

เมื่อใช้หลาย AI tool บนโปรเจ็กต์เดียวกัน (เช่น Claude Code สำหรับ implementation, Claude.ai สำหรับ design review):

**กฎเดียวกันใช้กับทุก AI tool:**
- ทุก session ไม่ว่าจะเป็น tool ใด ต้องอ่าน startup files และอัปเดต log ตาม protocol นี้
- ระบุ tool identity ใน work-log entry: `[Claude Code]`, `[Claude.ai]`, `[ChatGPT]` เป็นต้น
- ห้ามให้ AI tool ใด overwrite งานของ AI tool อื่นโดยไม่อ่าน log ก่อน

**Source of truth ไม่เปลี่ยน:**
- tool ที่ใช้อยู่ไม่มีผลต่อ hierarchy — source docs ยังคงเป็น source of truth เสมอ
- ถ้า AI tool ต่างกันให้ output ที่ขัดแย้งกัน ให้ทำตาม Scenario E ใน `ai-decision-protocol.md`

**Agent Diary — log แยกต่อ tool:**
- ถ้าโปรเจ็กต์ใช้ AI tool มากกว่า 1 ตัว ให้สร้าง `CoreAiWorkspaces/03-log/agents/<tool-name>.md` ต่อ tool
- แต่ละ tool เขียน diary ของตัวเองเท่านั้น — ห้าม cross-write
- ตัวอย่างไฟล์: `CoreAiWorkspaces/03-log/agents/claude-code.md`, `CoreAiWorkspaces/03-log/agents/claude-ai.md`
- รูปแบบและกฎการใช้งาน: ดู `core/08-log-and-summary-template.md` ส่วน "Agent Diary Template"
- `work-log-index.md` ยังคงเป็น master index รวมทุก tool — diary เป็นรายละเอียดเพิ่มเติม
- ถ้าใช้ tool เดียว ไม่ต้องสร้าง `agents/` folder

**แนะนำ:** ถ้าใช้หลาย tool ให้ระบุไว้ใน `way-of-work.md` ของโปรเจ็กต์ว่า tool ไหนรับผิดชอบส่วนใด

**ตัวอย่าง multi-AI scenario — session ที่ใช้ 2 tool:**

```
สถานการณ์: Claude Code ทำ implementation, Claude.ai ทำ design review

วันที่ 1 — Claude Code session:
  - อ่าน work-log-index → เห็น entry [Claude.ai] เมื่อวาน: "design review T-016 เสร็จ, แนะนำ pattern X"
  - อ่าน agents/claude-ai.md → เห็น checkpoint: "เสนอ Stripe checkout pattern, รอ implement"
  - ดำเนินการ implement T-016 ตาม pattern ที่ Claude.ai เสนอ
  - จบ session: เขียนลง agents/claude-code.md + อัปเดต work-log-index [Claude Code]

วันที่ 2 — Claude.ai session (design review รอบ 2):
  - อ่าน work-log-index → เห็น entry [Claude Code] เมื่อวาน: "implement T-016 เสร็จ, รอ review"
  - อ่าน agents/claude-code.md → เห็น: "implement ตาม pattern X แต่ edge case Y ยังไม่ handle"
  - review code T-016 เฉพาะ scope ที่ตัวเองรับผิดชอบ (design/architecture)
  - จบ session: เขียนลง agents/claude-ai.md + อัปเดต work-log-index [Claude.ai]

สิ่งที่ไม่เกิดขึ้น:
  ✗ Claude.ai ไม่เขียนทับ agents/claude-code.md
  ✗ Claude Code ไม่ implement โดยไม่อ่าน Claude.ai diary ก่อน
  ✗ ไม่มี session ไหนที่เริ่มโดยไม่รู้ว่า session ก่อนหน้าหยุดตรงไหน
```

## Memory Scope Protocol

เมื่อพบข้อมูลใหม่ระหว่าง session — ใช้ decision tree นี้เพื่อตัดสินว่าควรเก็บที่ไหน:

| ประเภทข้อมูล | ที่เก็บ |
|-------------|--------|
| Architectural decision | `CoreAiWorkspaces/07-decisions/ADR-NNN-*.md` |
| Entity ใหม่ หรือ status เปลี่ยน | `CoreAiWorkspaces/07-decisions/entity-register.md` |
| Pattern / lesson ข้ามโปรเจ็กต์ | `~/ai-workspace/cross-project-memory.md` (ถามผู้ใช้ก่อน) |
| Progress / detail / decisions ใน session | `CoreAiWorkspaces/03-log/agents/<tool>.md` + `work-log-index.md` |
| Task ใหม่ หรือ status เปลี่ยน | `CoreAiWorkspaces/02-task/task-board.md` |

**กฎ:**
- ข้อมูลหนึ่งชิ้นอาจต้องเก็บในหลายที่ — ไม่ mutually exclusive
- ถ้าไม่แน่ใจ: เก็บลง work-log ก่อน และระบุว่า "ยังไม่แน่ใจว่าควรอยู่ที่ไหน"
- ห้ามเขียนลง cross-project memory โดยไม่ได้รับอนุญาตจากผู้ใช้
- รายละเอียดเพิ่มเติม: ดู Scenario K ใน `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md`
