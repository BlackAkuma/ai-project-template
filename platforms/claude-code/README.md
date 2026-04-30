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
    design-docs.md    ← doc/**
    gameplay-code.md  ← src/game/** (game projects)
    test-standards.md ← tests/**
  skills/
    /compliance-check
    /session-end
    /fdd-create
    /adr-create
    /scope-check
    /launch-check
```

---

## Template ที่ layer นี้อ้างอิง

- **core/ 00–18** — universal templates (19 ไฟล์) — ทุกโปรเจ็กต์ใช้
- **skills/game/ 00–06** — game skill pack (7 ไฟล์) — โหลดเมื่อ doc/08-design/ มีอยู่

---

## วิธี Setup

### 1. Copy CLAUDE.md

```bash
cp platforms/claude-code/CLAUDE.md ./CLAUDE.md
```

ปรับ language policy และ project-specific notes ตามโปรเจ็กต์

### 2. Setup Hooks

สร้าง `.claude/hooks/` ในโปรเจ็กต์แล้ว copy hooks ที่ต้องการ:

```bash
mkdir -p .claude/hooks
cp platforms/claude-code/hooks/session-start.sh .claude/hooks/
cp platforms/claude-code/hooks/session-stop.sh .claude/hooks/
cp platforms/claude-code/hooks/pre-compact.sh .claude/hooks/
cp platforms/claude-code/hooks/validate-commit.sh .claude/hooks/
cp platforms/claude-code/hooks/detect-gaps.sh .claude/hooks/
chmod +x .claude/hooks/*.sh
```

### 3. Setup Rules

```bash
mkdir -p .claude/rules

# ทุกโปรเจ็กต์:
cp platforms/claude-code/rules/core-standards.md .claude/rules/
cp platforms/claude-code/rules/design-docs.md .claude/rules/
cp platforms/claude-code/rules/test-standards.md .claude/rules/

# game projects เท่านั้น:
cp platforms/claude-code/rules/gameplay-code.md .claude/rules/
```

### 4. Setup Skills

```bash
mkdir -p .claude/skills
cp platforms/claude-code/skills/* .claude/skills/
```

---

## หมายเหตุ

- Hook scripts ต้องการ bash และ git
- `PROJECT_ROOT` environment variable ควรตั้งค่าให้ตรงกับ root ของโปรเจ็กต์
- ปรับ glob patterns ใน rules ให้ตรงกับโครงสร้าง folder ของโปรเจ็กต์
