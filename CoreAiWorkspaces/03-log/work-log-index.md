<!-- AI-CONTEXT
last_session: 2026-06-05
tool: Claude Code
completed: [T-040]
checkpoint: GOAL full-build. DONE: F1 model-agnostic+role-floor, F2 agent-dispatch, F3 multi-repo, F4 vector-memory, F5 cockpit-renderer. 98 tests/11 suites, CI all. Panels: F1 3/3 (role-binding dissent→fixed F2), F2 3/3 + F3 3/3 (F2 risk-axis/fail-closed dissent→FIXED in agent.py: dangerous-intent force-L3, normalize_risk, lane_for fail-closed code-author). ALL FEATURES F1-F8 BUILT (105 tests/12 suites, CI). F6 migrate (7/7). F7 carry-over DONE (CLAUDE.md risk-tiered, C-07 dual-authority invert, core/11 risk-Level binding — closes BRD §12, implements ADR-007/008). F8 done (run-audit→AUD, playtest→sub-gate ×5, Scenario O→core/11). Panels: F1/F2/F3/F4/F5 all 3/3 (dissents fixed inline). final full-system audit running.
next_from_last: T-049 full retrofit + T-056/057 (A1 findings); then P1 validator
notes: ADR-006..009 Accepted (panel 2/3). Scenario O codified. P0-A done. A1 core schema drafted (exploration/a1-core-schema.md) — retrofit เจอ 2 gap จริง (spike source_ref, work-status field reconcile).
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

### 2026-06-07 — [Engine moat complete (P3-P6 data) + G3/G4 decided → autonomous-build terminus]

**สิ่งที่ทำ:**
- P3-1 tamper-evidence (hash chain) · P3-2 gated mutation + faked-done detection · P4-1/2 JSON-in-git canonical store + generated views (drift=0) · P6-1 Decision Inbox data layer — รวม **45 tests/6 suites** ผ่านหมด, CI รันครบ
- G3 panel → **C-deferred** (ADR-012): JSON-in-git canonical, NFR-2 git-native FINAL
- G4 panel → **B harvest-demand-first** (ADR-013): Shell gated บน ≥1 design-partner WTP; revenue hypothesis (OSS free + paid governance-of-record)
- ทุก gate: panel 2/3 + dissent + marketing → user ตัดสิน → lock (G1✅ G3✅ G4✅)

**ผล:** Engine (moat) สมบูรณ์+พิสูจน์แล้ว headless; thesis "context>model" = ระบบที่รัน+test ได้จริง · **autonomous build ถึง terminus** — next คือ GTM จริงของ user (harvest demand) ไม่ใช่ autonomous coding
**Decisions:** ADR-012 (G3), ADR-013 (G4)
**Next (USER):** publish hero-demo + category flag, outreach WTP, gate Shell บน signal (timebox 4-6wk)
**Branch:** explore/odysseus-analysis

---

### 2026-06-06 — [MVW reached + G1 decided (C-conservative) + engine build P1-P2]

**สิ่งที่ทำ:**
- build engine/ ครบ MVW: P1 (5→6 gates as data, 8→9 resolvers, smoke tests, wired hook) + P2 (CLI, risk-tier, challenge-necessity validator, CI workflow) — รัน+verify จริงทุกขั้น
- fixed 2 hook bugs ระหว่างทาง (BOM shebang, grep-c integer error)
- **G1 decision panel** (3-lens vote + marketing): C2/B1 → C; user เลือก **C-conservative** → ADR-011
- contrarian (B) dissent บันทึกครบ: solo focus risk → mitigation (timebox launch, P3 single-threaded, internal go/no-go)

**Decisions:** G1=C-conservative (ADR-011) — soft-ship OSS + protect P3 + เลื่อน loud launch
**ผล:** governance linter (MVW) ship-able + dogfooded; engine ชั้น 2 มีชีวิต
**Next:** P3 interception (constitutive, moat — protected critical path) + soft-ship prep timeboxed
**Branch:** explore/odysseus-analysis

---

### 2026-06-05 — [BRD v1.0 ACCEPTED via 3-iteration panel (+ marketing)]

**สิ่งที่ทำ:**
- ร่าง BRD (00-source) = source-of-truth requirements ของ "Governed Project Memory"
- รัน brd-review-panel 3 รอบ (3 voting lens 2/3 + marketing advisory), log ทุกรอบ:
  - iter1 v0.1 → 3/3 PASS (contra .60 borderline) → consensus gaps (acceptance criteria/metrics/Plan/GTM ฯลฯ)
  - iter2 v0.2 → 2/3 PASS (contra FAIL .66, defect จริง: scope/MoSCoW, X placeholder, OD-1 dep) → แก้
  - iter3 v0.3/v0.4 → 2/3 PASS (contra FAIL .63 บน named-deferrals) → **CONVERGED → LOCK**
- เคารพ contrarian: iterate ไม่ override; lock เมื่อ contrarian self-acknowledged "named-deferral != incompleteness"
- marketing ทุกรอบ = viable (thesis/trend แรง, ต้อง GTM/hero-demo/monetization)
- lock BRD v1.0 = ADR-010 (โปร่งใส, reopenable); OD-1..4 ผูก gate รอ panel เมื่อถึง phase

**Decisions:** BRD v1.0 Accepted (ADR-010) · all reviews logged ใน BRD §13 (อ่านย้อนได้)
**ผล:** governing requirements doc พร้อม — ขับ build P1+ ได้
**Next:** P1-3 wire engine→hook (build) + OD panels at gates
**Branch:** explore/odysseus-analysis

---

### 2026-06-05 — [ADR Review Panel → Accept ADR-006..009 + codify Scenario O]

**สิ่งที่ทำ:**
- รัน **adr-review-panel** workflow: 3-lens reviewer (technical/strategic/contrarian) × 4 ADR = 12 agent, กติกา 2/3
- ผล: 006/007 = 3/3 PASS · 008/009 = 2/3 PASS (contrarian FAIL มีมูลจริง)
- ทางเลือก B: **revise 008/009 แก้ต้นเหตุก่อน accept** (contrarian ถูกทุกข้อ):
  - 008: เพิ่ม Level 0 triage, redefine แกน uncertainty→risk ชัด, Engine-determined classification + conservative default, คง hard-stop conditions, ระบุ supersede กฎ uniform
  - 009: เพิ่ม Task/Gate.risk_level, คง design_validate, fix source cite §5→§3, reconcile D2 กับ ADR-007
  - 007: เพิ่ม C-07 invert mandate, narrow determinism, soften one-way-door
- Accept ทั้ง 4 + Panel Review Record (log โหวต+dissent+การตัดสิน) ท้ายแต่ละ ADR
- **codify Scenario O** (ADR Review Panel) เข้า ai-decision-protocol §7 — institutionalize loop
- carry-over tasks ที่กระทบ core ที่ ship แล้ว → lock เป็น T-051/052/053 รอ project review (ไม่แก้เงียบ)

**Decisions:** ADR-006..009 Accepted · Scenario O = standing protocol (every ADR → panel → 2/3 → log)
**AI autonomy used:** revise เรื่องเล็ก/safe เอง + log; เรื่องใหญ่ (core ที่ ship) → task รอ review
**ผล:** governance pattern จาก product vision = ใช้จริงด้วยมือแล้ว (dogfood ขั้นสุด)

**P0-A housekeeping (ทำต่อในรอบเดียวกัน — delegated small tasks):**
- T-041 ✅ core-count: root+platforms CLAUDE.md → core 00–22, skills 00–12
- T-042 ✅ สร้าง `skills/game/12-compliance-codes.md` (consolidated G/A/N/U/L index); เจอ bonus gap: 00-overview table แถว 04/05 ผิด (อ้าง compliance-codes/game-session-end ที่ไม่มี) → sync ให้ตรงไฟล์จริง (playtest-report/balance-check). หมายเหตุ: เดิมตั้งชื่อ 04 ชนกับ playtest-report → rename เป็น 12
- T-043 ✅ git_pipeline เข้า core/06 (field table + template block)
- T-044 ✅ core/15 note C-15–C-19 reserved + flag run-audit collision (T-044b ตามมา)

**T-045 ✅ A1 core schema (Stage A, paper-first):**
- ร่าง CORE 11 entities (Project/Requirement/Task/Evidence/Decision/TeamMember/Gate/Repo/Entity/Event) + fields/types
- lifecycle (D1), evidence model machine vs attested (D2), AI-CONTEXT schema เดียว (Critical gap #2), profile hook + game (D3, defer compose engine ตาม panel guidance)
- schema_version 0.1, additive-only
- **A5 lite retrofit กับ state จริง → เจอ 2 gap (paper-first ได้ผล):** #1 source_ref บังคับไม่ได้กับ spike/exploration (T-056) · #2 work-status field จริง ≠ core/06 template = Critical gap #2 ตัวจริง (T-057)
- → `exploration/a1-core-schema.md`
**Next:** T-049 full retrofit (domain ห่าง) + T-056/057 → P1 validator
**Branch:** explore/odysseus-analysis

**ตรวจสอบซ้ำ — independent verification pass (2026-06-05):**
- spawn verification agent อิสระ audit ทั้งสาย (ADR + A1 schema + housekeeping + tracking)
- เจอ + แก้ 5 defect: [HIGH] total_tasks 45→48 (math ผิด) · [MED] stale "00–11" ใน CLAUDE.md Skill Pack Detection ×2 (T-041 พลาด) · [LOW] Done table lag (เพิ่ม T-041..045) · [LOW] work-status body stale (ADR Proposed→Accepted) · [LOW] playtest state vs sub-gate (T-058)
- confirmed correct: cross-ADR consistency, risk_level dependency, carry-over tasks, source cites, A1 soundness, Scenario O
- T-056 resolved (spike source_ref), T-057 design done (unified work-status schema A1 §3, apply=P0-B)
- → ตรวจสอบซ้ำได้ผล: paper + verify จับ error ก่อน propagate

---

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
- แยก docs/ ไป gh-pages branch — user projec