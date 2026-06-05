<!-- AI-CONTEXT
last_session: 2026-06-05
tool: Claude Code
completed: [T-040]
checkpoint: none
next_from_last: human approve ADR-006 (Stage 2 direction) → P0-A housekeeping + A1 schema
notes: Odysseus analysis → Stage-2 vision "Governed Project Memory". 5 exploration docs + ADR-006..009 Proposed. Started dogfooding methodology (was bypassed since v1.5.0).
released_since_log: v1.6.0–v1.10.0 (HARD RULE, escape valve, challenge-necessity, task close gate, behavioral tests)
deep_context: exploration/master-plan.md
-->

# Work Log Index — ai-project-template

## Milestone Summary

| Milestone | Status | Completed |
|-----------|--------|-----------|
| M1: Core Template System (core/ 00–21, skills, platforms) | ✅ done | 2026-05 |
| M2: Structural Integrity (doc→ai, gh-pages, clone fix, tests) | ✅ done | 2026-05-07 |
| M3: Release Prep (ROADMAP, CHANGELOG, merge to master) | 🔄 todo | — |

## Recent Sessions

### 2026-06-05 — [Odysseus Analysis → Stage 2 Vision "Governed Project Memory"]

**สิ่งที่ทำ:**
- วิเคราะห์ Odysseus (52k-star self-hosted AI workspace) เชิงลึก — feasibility, differentiation, tech stack
- ตกผลึก vision 3-layer: Substrate (template/สมอง) → Engine (governance machine-enforced) → Shell (แอบ project-centric)
- thesis: "AI capability = context engineering ไม่ใช่ตัว model" — Odysseus พิสูจน์ว่า body = commodity
- gap audit ภายใน (อ่าน repo จริง): 3 รอยร้าวลึก — truth ใน prose, "done" เป็นคำพูด, ไม่มี concurrency; + housekeeping (core 00-22 vs docs, missing compliance-codes file, C-15..19)
- market research: four-way intersection (project-centric + enforced-governance + multi-agent + multi-repo) ยังว่าง; threats = Cursor/Factory/Cognition/MS
- 4 market corrections: governance risk-tiered (Gartner), multi-agent reframe (parallel เท่านั้น), อย่า out-index, compose underneath (LiteLLM/OPA), interoperate AGENTS.md
- master plan: 11 phase, critical path ~14-15 สัปดาห์ถึง ship (P6), bottleneck = P3 interception, 6 decision gates, 5 stop points
- schema architecture: CORE (process, invariant) + PROFILE (product, variant, compose ได้)
- **dogfood methodology กลับมาใช้** — สร้าง ADR-006..009 (Proposed), update work-status/task-board/log

**Artifacts:** `exploration/` 5 ไฟล์ (odysseus-analysis, north-star-vision, development-plan, what-it-should-be, master-plan) + ADR-006..009
**Decisions (Proposed):** ADR-006 Stage-2 direction · ADR-007 dual-authority · ADR-008 risk-tiered governance · ADR-009 schema CORE+PROFILE
**ผล:** vision + plan เป็น durable state แล้ว (ไม่ใช่แค่ในแชท)
**Next:** ⏳ human approve ADR-006 → P0-A housekeeping (T-041..044) + A1 schema (T-045)
**Branch:** explore/odysseus-analysis (pushed)

---

### 2026-05-08 — [TACP v1.5.0 — Token-Aware Communication Protocol]

**สิ่งที่ทำ:**
- วิเคราะห์ pordee Thai compression concepts → absorbed เป็น protocol rules (P-01 to P-06)
- ออกแบบ 3-layer model: L1 (machine), L2 (user), L3 (shared/dual-block)
- สร้าง `core/22-tacp-template.md` + `CoreAiWorkspaces/04-way-of-work/tacp.md`
- อัปเดต CLAUDE.md (root + platforms) เพิ่ม TACP section + verbosity scale V1-V5
- อัปเดต way-of-work.md เพิ่ม tacp config block (L2_LANG)
- convert caw-*.md ทั้ง 11 ไฟล์ → dual-block format (AI-CONTEXT L1 + HUMAN-CONTEXT L2)
- อัปเดต new-project.sh bootstrap tacp.md ไปยัง new projects
- สร้าง ADR-005, tests/token-savings/tacp-benchmark.md (15 test cases)
- tests: 46 → 67 (เพิ่ม T1-T10 TACP checks + A6 tacp.md required file)
- VERSION 1.4.0 → 1.5.0, commit b80cc35, push feat/savetoken

**ผล:** 67/67 tests passing. TACP complete. Estimated ~54% token savings typical session.
**Next:** รอ user อนุมัติ merge feat/savetoken → dev → master (v1.5.0)

---

### 2026-05-08 — [v1.3.0 Release + /caw-update]

**สิ่งที่ทำ:**
- Merge dev → master: v1.3.0 (caw- prefix, package install flow, docs)
- Merge docs: Package Concept diagrams + merge workflow notes → master → GitHub Pages live
- feat: `--update-commands` flag ใน new-project.sh — อัปเดต commands ไม่แตะ CoreAiWorkspaces/
- feat: `/caw-update` slash command — สั่งอัปเดตจาก AI ได้โดยตรง
- tests: 43 → 44 (เพิ่ม caw-update.md ใน SLASH_FILES check)
- อัปเดต platforms/claude-code/README.md + CLAUDE.md ให้รู้จัก /caw-update

**ผล:** 44/44 tests passing, dev pushed, ระบบ stable
**Next:** รอ feature request ถัดไป

---


### 2026-05-07 — [Structural Restructure + MemPalace + CoreAiWorkspaces/ Bootstrap]

**สิ่งที่ทำ:**
- ออกแบบและเขียน core/20-vector-memory-optional.md (MemPalace Phase 3 template)
- เขียน tools/vector-memory/README.md (quick reference)
- อัปเดต core/19-memory-architecture-overview.md (Layer 4 + compliance C-20/21/22)
- Rename doc/ → CoreAiWorkspaces/ ครบทุกไฟล์ (101 files, 589 occurrences) บน branch `restructure/doc-to-ai`
- ย้าย docs/ web pages ไป gh-pages branch (orphaned)
- สร้าง CLAUDE.md ที่ repo root — fix clone flow ที่ broken
- สร้าง tests/functional/test-user-flows.sh (35 tests, Flow A/B/C + Structural)
- Fix test S5 ให้ใช้ `git ls-files` แทน filesystem check
- Merge restructure/doc-to-ai → dev, push both dev + gh-pages
- Bootstrap CoreAiWorkspaces/ สำหรับ template project นี้เอง (meta-bootstrap)

**ผล:** 35/35 tests passing, dev branch clean + pushed

**Next:** T-023 (merge dev → master รอ permission)

---

### 2026-05-08 — [T-022: MemPalace Field Test + Doc Corrections]

**สิ่งที่ทำ:**
- ติดตั้ง mempalace 3.3.4 จริง และ test บน template project's CoreAiWorkspaces/ folder
- พบ 4 ข้อผิดพลาดในเอกสาร แก้ไขทั้งหมด:
  1. `init` command — เป็น interactive wizard ไม่ใช่ path command / ข้ามได้
  2. Palace location — `~/.mempalace/palace` (global) ไม่ใช่ `~/ai-workspace/mempalace/`
  3. `--wing` flag — ต้องระบุเสมอเมื่อ mine จาก `CoreAiWorkspaces/` subfolder (ไม่งั้น wing = 'ai')
  4. Threshold — 0.60 → 0.35 สำหรับ Thai/mixed (จาก actual cosine scores 0.31–0.53)
- ค้นพบ `mempalace wake-up`, `mempalace status` commands ที่ไม่ได้เขียนไว้
- Mine 22 files, 62 drawers สำเร็จ / Search ทำงานได้ถูกต้อง
- อัปเดต core/20, core/19, tools/vector-memory/README.md

**ผล:** T-022 complete — docs ถูกต้องแล้ว

---

### 2026-05-08 — [ROADMAP + CHANGELOG + Release Prep]

**สิ่งที่ทำ:**
- อัปเดต ROADMAP.md — Phase 3 Semantic Search Layer เปลี่ยนจาก "planned" เป็น "✅ template done"
- อัปเดต CHANGELOG.md — เพิ่ม v1.1.0 (memory architecture Phase 1–3) และ v1.2.0 (structural integrity)
- อัปเดต task-board.md — T-020/021 done, T-022 (field test) คือ next

**ผล:** ROADMAP ตรงกับ reality, CHANGELOG บันทึกครบ, งานเหลือ T-022 + T-023

---

### ก่อนหน้า 2026-05-07 — [Core Template Development]

**สรุป:** พัฒนา core/ templates 00–21 ทั้งหมด รวมถึง:
- Session protocol, task lifecycle, compliance, ADR system
- Memory architecture Phase 1–2 (entity register, cross-project memory, agent diary)
- Git workflow template (core/21)
- skills/game/ (00–11)
- Web pages (how-it-works.html, workflow-diagram.html) สำหรับ GitHub Pages
- Functional tests สำหรับ reader scripts

**Decisions:**
- เลือก MemPalace เป็น Phase 3 vector memory implementation (local-first, ไม่ต้อง cloud)
- เปลี่ยนชื่อ doc/ → CoreAiWorkspaces/ เพื่อความชัดเจน (ไม่ชน docs/ folder)
- แยก docs/ ไป gh-pages branch — user project ไม่ได้รับ web pages เมื่อ clone
