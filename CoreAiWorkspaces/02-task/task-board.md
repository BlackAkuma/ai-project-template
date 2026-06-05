<!-- AI-CONTEXT
total_tasks: 44
in_progress: []
blocked: []
done: [T-001,T-002,T-003,T-004,T-005,T-006,T-007,T-010,T-011,T-012,T-013,T-014,T-020,T-021,T-022,T-023,T-024,T-025,T-026,T-027,T-028,T-029,T-030,T-031,T-032,T-033,T-034,T-035,T-040]
todo: [T-041,T-042,T-043,T-044,T-045,T-046,T-047,T-048,T-049,T-050,T-051,T-052,T-053,T-054,T-055]
last_updated: 2026-06-05
priority_next: P0-A housekeeping (T-041..044, safe) — ADR-006..009 Accepted, unblocked
note: T-051..053 = carry-over กระทบ core ที่ ship แล้ว → รอ whole-project review round
-->

# Task Board — ai-project-template

## In Progress

*(ไม่มี)*

## Todo (unblocked — ADR-006..009 Accepted 2026-06-05)

### P0-A — Housekeeping (safe, reversible — ทำได้เลย)

| Task | Description | Source | Risk |
|------|-------------|--------|------|
| T-041 | แก้ core-count contradiction (docs บอก 00–18/21 จริง 00–22) | what-it-should-be §3 | L1 |
| T-042 | สร้าง `skills/game/04-compliance-codes.md` ที่หาย (อ้าง ~20×) | what-it-should-be §3 | L1 |
| T-043 | เพิ่ม `git_pipeline` เข้า core/06 work-status schema | what-it-should-be §3 | L1 |
| T-044 | define/rename C-15..C-19 (undefined + ชนกับ run-audit test ID) | what-it-should-be §3 | L1 |

### Stage A — Design & Validate Contract (paper-first, no code)

| Task | Description | Decision | Source |
|------|-------------|----------|--------|
| T-045 | A1 core schema (entities/fields/types) | ADR-009 | master-plan §2 |
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
