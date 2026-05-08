# Changelog

## v1.4.0 — 2026-05-08

### Versioning System

- **`VERSION` file** — เก็บ version ที่ root — single source of truth สำหรับ template version
- **`new-project.sh`** — อ่าน VERSION และ embed ลง bootstrapped `CoreAiWorkspaces/README.md` — ทุกโปรเจ็กต์รู้ว่าใช้ template version อะไร
- **Bump rules** — PATCH/MINOR → `/caw-update` จัดการได้, MAJOR → re-bootstrap
- **ADR-004** — บันทึก versioning strategy: single release + layer separation

### Tests

- **46/46 tests** (เพิ่มจาก 44) — เพิ่ม A14: VERSION file exists, A15: version embedded in bootstrapped README

---

## v1.3.1 — 2026-05-08

### Update Commands Flow

- **`--update-commands` flag** — `new-project.sh --update-commands` อัปเดต `caw-*` commands และ `CLAUDE.md` เป็น version ใหม่ โดยไม่แตะ `CoreAiWorkspaces/`, source docs, หรือไฟล์โปรเจ็กต์ใดๆ
- **`/caw-update` slash command** — สั่ง update ได้โดยตรงจาก Claude Code ไม่ต้อง bootstrap ใหม่ทั้งหมด

### Documentation

- **Package Concept diagrams** — `docs/architecture/overview.md` เพิ่ม 3 diagrams แสดงโครงสร้าง template ก่อน/ระหว่าง/หลัง bootstrap
- **Merge workflow notes** — `docs/advanced-setup.md` อธิบาย `--no-commit` merge flow และ `merge=ours` bidirectionality กับ `CoreAiWorkspaces/` restore step

### Tests

- **44/44 tests** (เพิ่มจาก 43) — เพิ่ม `caw-update.md` ใน A13 slash commands check

---

## v1.3.0 — 2026-05-08

### Install Flow — Package Concept

- **`new-project.sh` upgrade** — Bootstrap script ติดตั้งทุกอย่างอัตโนมัติ: `CLAUDE.md` ที่ root, `.claude/commands/` พร้อม slash commands ทั้งหมด, `.git/hooks/validate-commit` สำหรับ commit validation — user ลบ `_template/` ได้ทันทีหลัง bootstrap
- **`verify-install.sh`** — Post-install verification script ตรวจ 6 sections: CoreAiWorkspaces/ structure, CLAUDE.md, .claude/commands/, .git/hooks/, no legacy ai/ folder

### Slash Commands — Namespace Isolation

- **`caw-` prefix** — Rename slash commands ทั้งหมดเพิ่ม `caw-` prefix (CoreAiWorkspaces abbreviation) เพื่อป้องกัน namespace collision กับ tools อื่นใน `.claude/commands/`: `/caw-session-end`, `/caw-adr-create`, `/caw-compliance-check`, `/caw-scope-check`, `/caw-fdd-create`, `/caw-launch-check`, `/caw-archive-logs`

### Documentation — Web Pages

- **docs/ (14 files)** — Web documentation site บน GitHub Pages: index, quick-start (Mac/Linux + Windows), advanced-setup, non-technical-setup, architecture overview, memory system, ADR system, Claude Code integration, Claude.ai integration, vector memory
- **Documentation overhaul** — อัปเดต QUICKSTART.md, README.md (EN+TH), platforms/claude-code/README.md ให้ reflect new install flow — ลบ manual copy steps ทั้งหมด
- **Fix broken URLs** — แก้ `claude.CoreAiWorkspaces/code` → `claude.ai/code` (regression จาก ai→CoreAiWorkspaces rename)

### Tests

- **43/43 tests** (เพิ่มจาก 35) — เพิ่ม A8–A13: ตรวจ CLAUDE.md auto-install, .claude/commands/ ครบ, slash command files ทั้งหมด

---

## v1.2.0 — 2026-05-08

### Structural Integrity

- **doc/ → CoreAiWorkspaces/ rename** — AI working folder เปลี่ยนชื่อจาก `doc/` เป็น `CoreAiWorkspaces/` ทั่วทั้งระบบ (101 files, 589 occurrences) เพื่อความชัดเจนและไม่ชนกับ `docs/` ที่ใช้สำหรับ GitHub Pages
- **Root CLAUDE.md** — สร้าง `CLAUDE.md` ที่ repo root เพื่อ fix clone flow — ก่อนหน้านี้ Claude Code ไม่โหลด CLAUDE.md เมื่อ user clone repo โดยตรง
- **gh-pages branch** — ย้าย web pages (`how-it-works.html`, `workflow-diagram.html`) ออกจาก dev/master ไปอยู่บน orphaned `gh-pages` branch — user ที่ clone repo จะไม่ได้รับ web pages เหล่านี้
- **Functional test suite** — `tests/functional/test-user-flows.sh` ทดสอบ 3 user flows: ZIP install (Flow A), git clone (Flow B), existing project (Flow C) พร้อม structural integrity checks รวม 35 tests

### Meta

- **Template bootstrap** — template project นี้เริ่มใช้ระบบตัวเอง: `CoreAiWorkspaces/` folder, ADRs, entity-register, work-status, task-board สำหรับ track การพัฒนา template

---

## v1.1.0 — 2026-05

### Memory Architecture (Phase 1–3)

- **Phase 1: Entity Register** (`core/17`) — track tech choices, integrations, และ dependencies พร้อม status และช่วงเวลา
- **Phase 1: Scoped Memory Map** (`core/06`) — `read_more` hints ใน AI-CONTEXT block สำหรับ context routing
- **Phase 1: Entity Lifecycle Tags** — `[ENTITY:deprecated:X]`, `[ENTITY:superseded:X→Y]` format + compliance rule C-14
- **Phase 2: Agent Diary Protocol** (`core/08`) — แยก log ต่อ AI tool ใน `CoreAiWorkspaces/03-log/agents/`
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
