<!-- AI-CONTEXT
total_tasks: 48
in_progress: []
blocked: []
done: [T-001,T-002,T-003,T-004,T-005,T-006,T-007,T-010,T-011,T-012,T-013,T-014,T-020,T-021,T-022,T-023,T-024,T-025,T-026,T-027,T-028,T-029,T-030,T-031,T-032,T-033,T-034,T-035,T-040,T-041,T-042,T-043,T-044,T-045,T-049,T-056,T-058]
done_features: [F1,F2,F3,F4,F5,F6,F7,F8]   # ALL features built (105 tests/12 suites + carry-over + loose ends)
todo: [BL-1,BL-2,BL-3,BL-4,BL-5,BL-6,BL-7,BL-8,BL-9,BL-10,BL-11,BL-12]   # see 02-task/backlog-v2.md
last_updated: 2026-06-10
priority_next: backlog-v2 (4-lens panel): P0 = close see-decide-remember loop on LIVE repo (BL-1 cockpit-live, BL-2 memory-autoload, BL-3 writeback, BL-4 one-click, BL-5 dogfood-start). A1/A2/A4 done+verified. B* locked until M-A3 (R3)
status: M-A1 done (A1 local AI + A2 real-action hooks). M-A2 in progress via backlog-v2 P0
backlog: exploration/flow-plan.md §3 (granular micro-tasks + flow-gate policy)
note: P3-1 done (events.py hash-chain tamper-evidence, 3/3 tests; DEMO.md soft-ship). MVW done. G1=C-conservative (ADR-011)
note: T-051..053 = carry-over กระทบ core ที่ ship แล้ว → รอ whole-project review round
-->

# Task Board — ai-project-template

## In Progress

*(ไม่มี)*

## Todo (unblocked — ADR-006..009 Accepted 2026-06-05)

### ✅ P0-A — Housekeeping (DONE 2026-06-05)

| Task | Description | ผล |
|------|-------------|-----|
| T-041 | แก้ core-count (root+platforms CLAUDE.md → core 00–22, skills 00–12) | ✅ |
| T-042 | สร้าง `skills/game/12-compliance-codes.md` (consolidated index) + sync 00-overview table (04/05 ผิด) | ✅ |
| T-043 | เพิ่ม `git_pipeline` เข้า core/06 schema (field table + template block) | ✅ |
| T-044 | core/15: note C-15–C-19 reserved + flag run-audit collision | ✅ |
| T-044b | rename run-audit.sh test-ID "C-15".."C-19" → prefix อื่น (กัน namespace ชน) | todo |

### Stage A — Design & Validate Contract (paper-first, no code)

| Task | Description | Decision | Source |
|------|-------------|----------|--------|
| T-045 | ✅ A1 core schema (entities/fields/types) → `exploration/a1-core-schema.md` | ADR-009 | master-plan §2 |
| T-056 | ✅ source_ref สำหรับ spike/exploration (`source_ref: spike:<note>`) | — | a1-core-schema §1 |
| T-057 | unified work-status schema — **design done (A1 §3)**, apply กับ core/06 + ไฟล์จริง = P0-B step1 (pending) | ADR-007 | a1-core-schema §3 |
| T-058 | reconcile game playtest: state vs sub-gate (verification finding) — เลือก sub-gate | ADR-009 | a1-core-schema §2 |
| T-046 | A2 task lifecycle + profile stage extension | D1 (ADR-009) | master-plan |
| T-047 | A3 evidence model (machine-verifiable vs human-attested) | D2 (ADR-009) | master-plan |
| T-048 | A4 profile/extension mechanism + compose | D3 (ADR-009) | master-plan |
| T-049 | A5 retrofit schema กับ repo นี้ + เคสเกม (+ domain ห่าง: research/industrial) → iterate | — | master-plan |
| T-050 | A6 dual-authority contract spec | ADR-007 | master-plan |

### Carry-over จาก ADR panel — ⚠️ กระทบ core ที่ ship แล้ว (รอ whole-project review round)

| Task | Description | Source | หมายเหตุ |
|------|-------------|--------|---------|
| T-051 | re-publish Scenario A–N → new risk-Level mapping (core/11) | ADR-008 | redefine แกน uncertainty→risk |
| T-052 | rewrite CLAUDE.md uniform challenge-necessity → risk-tiered + entry-point enforcement | ADR-008 | supersede commit 08ba8a7 |
| T-053 | invert C-07 resolution (block wins for enforceable-state fields) core/03+core/15 | ADR-007 | แก้ contradiction กับ dual-authority |

### Protocol institutionalization

| Task | Description | Source |
|------|-------------|--------|
| T-054 | สร้าง `/caw-adr-review` slash command (wrap adr-review-panel workflow) | Scenario O |
| T-055 | promote ADR-review-panel เข้า core template (core/11 + core/12) | Scenario O |

## Todo (ภายหลัง)

*(หลัง Stage A: P1 validator → P2 CLI → P3+ ตาม master-plan)*

## Done

| Task | Description | Completed |
|------|-------------|-----------|
| T-001–007 | core/ templates ครบ (00–21) + skills/game/ + platforms/ | 2026-05 |
| T-010 | doc/ → CoreAiWorkspaces/ rename ครบ 101 files | 2026-05-07 |
| T-011 | docs/ web pages ย้ายไป gh-pages → ย้ายมา master/docs/ | 2026-05-07 |
| T-012 | Root CLAUDE.md สร้างแล้ว — fix clone flow | 2026-05-07 |
| T-013 | Functional test suite (43/43 passing) | 2026-05-08 |
| T-014 | new-project.sh สร้าง CoreAiWorkspaces/ + auto-install CLAUDE.md, commands, hooks | 2026-05-08 |
| T-020 | Update ROADMAP.md — Phase 3 MemPalace template done | 2026-05-08 |
| T-021 | Update CHANGELOG.md — v1.1.0 + v1.2.0 | 2026-05-08 |
| T-022 | Field test MemPalace: install + mine + search, fix 4 doc errors | 2026-05-08 |
| T-024 | Sync task-board + work-status | 2026-05-08 |
| T-026 | docs/ web pages: 14 files, index + quickstarts + architecture + integrations | 2026-05-08 |
| T-027 | verify-install.sh: post-install verification script (6 sections) | 2026-05-08 |
| T-028 | new-project.sh upgrade: auto-install CLAUDE.md + .claude/commands/ + .git/hooks/ | 2026-05-08 |
| T-029 | rename slash commands: add caw- prefix (CoreAiWorkspaces abbreviation) | 2026-05-08 |
| T-030 | docs update: fix claude.ai URLs, remove manual copy steps, add caw- explanation | 2026-05-08 |
| T-031 | tests update: 35 → 43 tests, add A8–A13 (CLAUDE.md + commands), update B2/S5/C6 | 2026-05-08 |
| T-023 | merge dev → master: v1.3.0 release | 2026-05-08 |
| T-025 | .gitattributes: CoreAiWorkspaces/ merge=ours + line endings | 2026-05-08 |
| T-032 | docs: Package Concept diagrams + merge workflow notes → master | 2026-05-08 |
| T-033 | feat: --update-commands flag + /caw-update slash command | 2026-05-08 |
| T-034 | feat: versioning system — VERSION file + embed in bootstrap + ADR-004 | 2026-05-08 |
| T-035 | feat: TACP — 3-layer model, dual-block caw-*.md, benchmark, 67 tests | 2026-05-08 |
| T-040 | Odysseus analysis + Stage-2 exploration (5 exploration docs + ADR-006..009) | 2026-06-05 |
| T-041 | P0-A: core-count fix (core 00–22, skills 00–12) root+platforms CLAUDE.md | 2026-06-05 |
| T-042 | P0-A: สร้าง skills/game/12-compliance-codes.md + sync 00-overview table | 2026-06-05 |
| T-043 | P0-A: git_pipeline เข้า core/06 schema | 2026-06-05 |
| T-044 | P0-A: core/15 C-15–C-19 reserved note | 2026-06-05 |
| T-045 | A1 core schema draft + retrofit (exploration/a1-core-schema.md) | 2026-06-05 |
