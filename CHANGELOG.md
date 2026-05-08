# Changelog

## v1.2.0 — 2026-05-08

### Structural Integrity

- **doc/ → ai/ rename** — AI working folder เปลี่ยนชื่อจาก `doc/` เป็น `ai/` ทั่วทั้งระบบ (101 files, 589 occurrences) เพื่อความชัดเจนและไม่ชนกับ `docs/` ที่ใช้สำหรับ GitHub Pages
- **Root CLAUDE.md** — สร้าง `CLAUDE.md` ที่ repo root เพื่อ fix clone flow — ก่อนหน้านี้ Claude Code ไม่โหลด CLAUDE.md เมื่อ user clone repo โดยตรง
- **gh-pages branch** — ย้าย web pages (`how-it-works.html`, `workflow-diagram.html`) ออกจาก dev/master ไปอยู่บน orphaned `gh-pages` branch — user ที่ clone repo จะไม่ได้รับ web pages เหล่านี้
- **Functional test suite** — `tests/functional/test-user-flows.sh` ทดสอบ 3 user flows: ZIP install (Flow A), git clone (Flow B), existing project (Flow C) พร้อม structural integrity checks รวม 35 tests

### Meta

- **Template bootstrap** — template project นี้เริ่มใช้ระบบตัวเอง: `ai/` folder, ADRs, entity-register, work-status, task-board สำหรับ track การพัฒนา template

---

## v1.1.0 — 2026-05

### Memory Architecture (Phase 1–3)

- **Phase 1: Entity Register** (`core/17`) — track tech choices, integrations, และ dependencies พร้อม status และช่วงเวลา
- **Phase 1: Scoped Memory Map** (`core/06`) — `read_more` hints ใน AI-CONTEXT block สำหรับ context routing
- **Phase 1: Entity Lifecycle Tags** — `[ENTITY:deprecated:X]`, `[ENTITY:superseded:X→Y]` format + compliance rule C-14
- **Phase 2: Agent Diary Protocol** (`core/08`) — แยก log ต่อ AI tool ใน `ai/03-log/agents/`
- **Phase 2: Cross-Project Memory Bridge** (`core/18`) — `~/ai-workspace/cross-project-memory.md` สำหรับ lesson learned ข้ามโปรเจ็กต์
- **Phase 2: Memory Scope Protocol** (`core/03`, `core/11`) — decision tree ว่าข้อมูลแต่ละแบบควรเก็บที่ไหน
- **Phase 3: Vector Memory** (`core/20`, `tools/vector-memory/`) — optional local semantic search layer, ไม่ต้อง cloud
- **Memory Architecture Overview** (`core/19`) — ภาพรวม Phase 1–3, compliance rules C-20/21/22

### Git Workflow

- **core/21** — git workflow template: branch strategy, commit format, dev/master separation

---

## v1.0.0 — 2026-04-30

First release. Bootstrap script ready, 108-check audit suite passing.

- `scripts/new-project.sh` — one-command project bootstrap (`--game` flag for game projects)
- `/balance-check` + `/playtest-report` slash commands for Claude Code game projects
- Audit suite: 108 automated checks including functional bootstrap tests
