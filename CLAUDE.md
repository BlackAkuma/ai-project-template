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

# 3b. (ทางเลือก) ถ้าต้องการเฉพาะ TEMPLATE ไม่เอา governance engine:
rm -rf engine/ exploration/ start-cockpit.cmd
# ปลอดภัย 100% — hooks ตรวจเองว่าไม่มี engine/ แล้วทำงานแบบ template-only อัตโนมัติ
# (ถ้าเก็บ engine/ ไว้ = ได้ governance ที่บังคับจริง + Cockpit dashboard เพิ่ม — ดู engine/README.md)
```

→ ทำตาม First Run Bootstrap ด้านล่าง

---

## Protocol เต็ม → `platforms/claude-code/CLAUDE.md`

> **RD-1 (dedup):** เดิมไฟล์นี้ duplicate protocol ~80% กับ `platforms/claude-code/CLAUDE.md`
> ทำให้ AI อ่านซ้ำทุก session (compliance-decay). ตอนนี้ **canonical อยู่ที่
> `platforms/claude-code/CLAUDE.md`** (Claude Code auto-load ทั้งสองไฟล์ + เป็น deploy source ของ
> `scripts/new-project.sh`) — ไฟล์นี้เก็บเฉพาะ Case 1/2 ที่ unique แล้วชี้ไปที่นั่น.

อ่าน **`platforms/claude-code/CLAUDE.md`** สำหรับ:
- First Run Bootstrap · Session Start / End Protocol · Batch Checkpoint · Context Window Management
- Project Context · TACP · Language Policy · Branching & Backup
- **Key Rules ครบทุกข้อ** (challenge-necessity risk-tiered, plan-before-code, "ทำต่อ"=task เดียว, scope-change, ADR-Proposed STOP, Memory Scope, entity-register ฯลฯ)
- Skill Pack Detection · Game Specialist Agents · Available Slash Commands (`/caw-*`)

AI tool อื่น (Cursor/Windsurf/claude.ai) → `platforms/universal/AI.md` · มีอะไรขัดกัน → เชื่อ `platforms/claude-code/CLAUDE.md`
