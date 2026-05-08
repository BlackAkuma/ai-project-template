# Claude Code Platform Layer

Layer เพิ่มเติมสำหรับคนที่ใช้ **Claude Code CLI** โดยเฉพาะ
ใช้ร่วมกับ `core/` และ `skills/` — ไม่ใช่การแทนที่

---

## สิ่งที่ layer นี้เพิ่มให้

| Feature | โดยไม่มี layer นี้ | โดยมี layer นี้ |
|---------|------------------|----------------|
| Session start | Copy prompt ให้ AI | `CLAUDE.md` โหลดอัตโนมัติ |
| Compliance check | สั่งด้วยตัวเอง | Hook รันก่อน commit อัตโนมัติ |
| Session log | AI เขียนเอง | Hook เตือนอัตโนมัติก่อนจบ |
| Gap detection | ต้องนึกถึงเอง | Hook ตรวจทุก session start |
| Coding standards | AI อ่าน doc | Rules โหลดตาม file path อัตโนมัติ |
| Pre-compact | AI ต้องจำเอง | Hook บังคับ checkpoint ก่อน compact |

---

## โครงสร้าง

```
platforms/claude-code/
  CLAUDE.md           ← copy ไปวางที่ root ของโปรเจ็กต์
  hooks/
    session-start.sh  ← PreToolUse (session แรก)
    session-stop.sh   ← PostToolUse (session สุดท้าย)
    pre-compact.sh    ← PreCompact
    validate-commit.sh← PreToolUse (git commit)
    detect-gaps.sh    ← PreToolUse (session start)
  rules/
    core-standards.md ← src/**
    design-docs.md    ← CoreAiWorkspaces/**
    gameplay-code.md  ← src/game/** (game projects)
    test-standards.md ← tests/**
  skills/
    /caw-compliance-check
    /caw-session-end
    /caw-fdd-create
    /caw-adr-create
    /caw-scope-check
    /caw-launch-check
```

---

## Template ที่ layer นี้อ้างอิง

- **core/ 00–18** — universal templates (19 ไฟล์) — ทุกโปรเจ็กต์ใช้
- **skills/game/ 00–06** — game skill pack (7 ไฟล์) — โหลดเมื่อ CoreAiWorkspaces/08-design/ มีอยู่

---

## วิธี Setup

**ใช้ bootstrap script — ไม่ต้อง copy ไฟล์เองเลย:**

```bash
bash _template/scripts/new-project.sh "ชื่อโปรเจ็กต์" /path/to/your-project
```

Script ติดตั้งให้อัตโนมัติ:

| สิ่งที่ติดตั้ง | ที่ไหน | หมายเหตุ |
|--------------|--------|---------|
| `CLAUDE.md` | project root | Claude Code โหลดทุก session |
| slash commands | `.claude/commands/` | `/caw-*` ทั้งหมด |
| `validate-commit` | `.git/hooks/` | ถ้ามี `.git` อยู่ |
| `CoreAiWorkspaces/` | project root | AI working folder |

### ไฟล์ที่ติดตั้งใน `.claude/commands/`

```
caw-session-end.md       sync work-status + log + task-board
caw-compliance-check.md  ตรวจ compliance violations
caw-adr-create.md        สร้าง architectural decision record
caw-scope-check.md       ตรวจ scope ของ task ปัจจุบัน
caw-fdd-create.md        สร้าง feature design document
caw-launch-check.md      checklist ก่อน deploy
caw-archive-logs.md      compress session logs เก่า
```

ชื่อขึ้นต้นด้วย `caw-` (**C**ore**A**i**W**orkspaces) เพื่อป้องกันชนกับ commands ของ tools อื่น

---

## หมายเหตุ

- `validate-commit` hook ต้องการ bash และ git
- ถ้าโปรเจ็กต์ไม่มี `.git` — hook จะข้ามการติดตั้งโดยอัตโนมัติ
- ปรับ `CoreAiWorkspaces/04-way-of-work/way-of-work.md` เพื่อ customize language policy และ project rules
