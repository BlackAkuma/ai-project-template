# Changelog

## v1.10.0 — 2026-05-22 (dev — ยังไม่ merge master)

### Challenge-Necessity Protocol

ระบบใหม่ที่ป้องกัน AI implement โดยไม่ตั้งคำถามว่า "ควรทำหรือเปล่า" — แก้ failure pattern หลัก: momentum override และ blanket approval

- **Scenario M step 0** (`core/11`) — ⛔ challenge necessity: AI ต้องตอบ 3 ข้อก่อน code ทุกครั้ง:
  (a) task ทำเพื่ออะไร, (b) cite source requirement, (c) มีทางที่ง่ายกว่าไหม
- **3-Lens Internal Challenge** — รัน Expert / Technical / Contrarian lenses เป็น single-instance structured challenge (ไม่ต้อง spawn agents จริง)
  - 🔍 Expert lens: มี pattern คล้ายกันอยู่แล้วไหม?
  - ⚙️ Technical lens: complexity, reversibility, dependencies
  - 🔴 Contrarian lens: เหตุผลที่แข็งแกร่งที่สุดที่ไม่ควรทำ (ห้ามตอบว่าไม่มี)
- **Entry-point enforcement** (`CLAUDE.md`, `platforms/claude-code/CLAUDE.md`) — เพิ่ม ⛔ rule ที่ Key Rules ระดับ entry point ว่า "ทำต่อ" / task ที่ดูชัดเจน ไม่ยกเว้น challenge-necessity

### Task Close Gate

- **`core/15`** — ⛔ prerequisite gate ก่อน mark task เป็น DONE:
  1. work-log มี entry สำหรับ task นี้
  2. task-board อัปเดต status แล้ว
  3. validation evidence ระบุไว้ (code tasks)
  → ขาดข้อใด: ห้ามปิด — mark `[IN_PROGRESS: pending close — ระบุว่าขาดอะไร]`

### Behavioral Test Suite

- **`tests/reader/test-challenge-necessity.md`** — 6 scenarios ทดสอบ AI behavior จริง:
  - CN-1: "ทำต่อ" ต้องไม่ bypass challenge-necessity
  - CN-2: task ที่ซ้ำของที่มีอยู่แล้ว Expert lens ต้องจับได้
  - CN-3: 3-lens ต้องผลิต objection จริง ไม่ใช่ performance
  - TCG-1/2: Task Close Gate บล็อกและเปิดได้ถูกเงื่อนไข
  - HARD-1: HARD RULE ไม่ถูก override ด้วย momentum

### Tests

- **96/96 tests** (เพิ่มจาก 92) — P14: root CLAUDE.md มี challenge-necessity guard, P15: platforms CLAUDE.md มีด้วย

---

## v1.9.0 — 2026-05-22

### HARD RULE Classification

- **`core/03`** — เพิ่ม Rule Classification table: ⛔ HARD RULE vs Guideline
  - HARD RULE: ห้ามข้าม ห้ามต่อรอง ไม่มี exception แม้แต่ momentum / "ทำต่อ"
  - Guideline: แนวปฏิบัติที่ดี มี context ที่ยืดหยุ่นได้
  - body-first rule marked ⛔: body คือ source of truth เสมอ — ห้าม reverse

### Escape Valve Audit Trail

- **`validate-commit.sh`** — `SKIP_DOC_SYNC=1` escape valve:
  - อนุญาตให้ข้าม doc-sync warning ได้ แต่ต้อง log entry ลง `CoreAiWorkspaces/03-log/work-log-index.md` อัตโนมัติ
  - ถ้าหา work-log ไม่เจอ: warn ว่า audit trail หายไป (ไม่ silent)
  - warning ปกติแจ้ง user ด้วยว่า escape valve มีและใช้งานอย่างไร

### Tests

- **92/92 tests** (เพิ่มจาก 90) — P11: HARD RULE marker อยู่ใน core/03, H7: escape valve log ถึง work-log-index.md

---

## v1.8.0 — 2026-05-22

### Approval Discipline

- **Scenario N** (`core/11`) — "ทำต่อ" = approve task ปัจจุบันเท่านั้น ไม่ใช่ arc ทั้งหมด
  - ก่อน implement milestone ถัดไปต้องตรวจ 4 ข้อ: scope approved?, scope change?, milestone ใหม่โดยไม่เห็น plan?, ADR Proposed?
  - เพิ่มใน Escalation Level 2 table
- **ADR blocking gate** (`core/12`) — ⛔ STOP ระหว่าง Proposed → implement
  - "ทำต่อ" ที่พูดก่อนเห็น ADR ไม่นับเป็น approval

### Doc Sync Enforcement

- **Batch Checkpoint** (`CLAUDE.md`, `core/03`) — sync 3 ไฟล์ (work-status, task-board, work-log-index) ทุกครั้งที่ commit feature สำคัญ ไม่ต้องรอ session จบ
- **`session-stop.sh`** — ตรวจ uncommitted changes ใน CoreAiWorkspaces/ (ไม่ใช่แค่วันที่), ตรวจ task-board, อ้างอิง /caw-session-end ถูกต้อง
- **`validate-commit.sh`** — เพิ่ม doc-sync warning: ถ้า code staged แต่ CoreAiWorkspaces/ dirty → warn พร้อมบอก /caw-session-end

### Architecture Clarification

- **`core/00`** — เพิ่ม architecture diagram: `core/` = กฎกลางทุก tool, `platforms/` = tool-specific wiring เท่านั้น (ห้าม duplicate กฎ)
- **`CLAUDE.md` + `platforms/claude-code/CLAUDE.md`** — ลบ branching rules ซ้ำซ้อน เหลือแค่ reference ไปยัง core/21
- **Scenario M** (`core/11`) — เพิ่ม step 7: scope check ก่อนทุก task

### Tests

- **90/90 tests** (เพิ่มจาก 46) — เพิ่ม P1–P10 (protocol), H1–H6 (hooks), U1–U4 (AI.md)

---

## v1.7.1 — 2026-05-22

### Fixes

- **`platforms/claude-code/CLAUDE.md`** — ลบ branching policy table ซ้ำซ้อน (9 กฎ) ที่ copy มาจาก core/21 แล้ว — เหลือแค่ 2-line reference
- Architecture diagram เพิ่มใน core/00 ชัดเจนว่า platforms/ = wiring only

---

## v1.7.0 — 2026-05-14

### Feature Branch Workflow

- **`core/21`** — git workflow template: branch strategy สมบูรณ์ (main/master, dev, feature/*, fix/*), One feature at a time rule, promotion pipeline (dev→main หรือ dev→sit→uat→main)
- **Scenario M** (`core/11`) — Pre-Code Checklist 6 ขั้น: git status, branch check, feature branch ซ้อน, task size, task ID, source reference

### Universal AI Protocol

- **`platforms/universal/AI.md`** — Universal entry point สำหรับทุก AI tool: session start protocol, file ownership table (Shared/Tool-Specific/System Files), Scenario M reference
- **`/caw-tool-clean`** — slash command สำหรับลบ config ของ AI tool ที่ไม่ใช้แล้ว เหลือเฉพาะ tool ที่ต้องการ
- **File ownership rules** (`core/03`) — กฎว่าไฟล์ไหน AI tool ไหนแตะได้

---

## v1.6.0 — 2026-05-11

### Multi-Tool Handoff

- **`platforms/universal/AI.md`** — AI tool ใดก็ตามอ่านไฟล์นี้แล้วเริ่ม contribute ได้ทันทีโดยไม่ต้อง re-explain context
- **Agent Diary** (`core/08`) — `CoreAiWorkspaces/03-log/agents/[tool-name].md` แยก checkpoint ต่อ AI tool สำหรับ multi-tool projects

---

## v1.5.1 — 2026-05-08

### Fixes

- **`docs/`** — แก้ web docs: `ai/` → `CoreAiWorkspaces/` naming, เพิ่ม TACP section ใน how-it-works.html และ workflow-diagram.html

---

## v1.5.0 — 2026-05-08

### Token-Aware Communication Protocol (TACP)

- **`CoreAiWorkspaces/04-way-of-work/tacp.md`** — Protocol anchor: 3-layer model (L1/L2/L3), verbosity scale V1–V5, Thai compression rules P-01 to P-06
- **`CLAUDE.md` + `platforms/claude-code/CLAUDE.md`** — TACP section เพิ่ม: layer table, verbosity scale, compression summary, L2_LANG reference
- **`way-of-work.md`** — เพิ่ม TACP configuration block (`tacp.L2_LANG`, `verbosity_default`, `politeness_level`)
- **Dual-block format** — caw-*.md ทั้ง 11 ไฟล์ migrate เป็น AI-CONTEXT (L1) + HUMAN-CONTEXT (L2) format ทำให้ AI อ่าน L1 block เท่านั้นแทน Thai full text
- **ADR-005** — บันทึก TACP architectural decision: 3-layer model vs alternatives

#### Layer Summary

| Layer | Destination | Before | After | Savings |
|-------|-------------|--------|-------|---------|
| L1 | AI-CONTEXT blocks | Thai prose | English key-value | 65–70% |
| L2 | Chat output | Verbose Thai | Compressed + V1–V5 | 30–90% by type |
| L3 | caw-*.md | Thai only | Dual-block | 86% AI read path |

### Benchmark

- **`tests/token-savings/tacp-benchmark.md`** — 15 test cases พร้อมตัวเลขก่อน/หลัง:
  - Session orientation reads: 93.4% savings
  - Simple ack (V1): 88.8% savings
  - Design proposal (V4): 52.2% savings  
  - Warning (V5): 0% (correct — no compression on warnings)
  - **Typical session weighted average: ~54% savings**

---

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
