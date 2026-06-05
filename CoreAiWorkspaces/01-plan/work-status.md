<!-- AI-CONTEXT
phase: stage2-design (exploration → schema design)
active_task: T-040 done (Odysseus analysis + Stage-2 exploration); next T-045 (A1 core schema)
blocker: ADR-006 Proposed — await human approve before building Engine
last_updated: 2026-06-05
git_mode: branch-separated
git_dev_branch: dev
git_prod_branch: master
active_branch: explore/odysseus-analysis
released: v1.10.0 (challenge-necessity + task close gate + behavioral tests)
read_more:
  vision: exploration/north-star-vision.md
  market+gap: exploration/what-it-should-be.md
  plan: exploration/master-plan.md
  decisions: CoreAiWorkspaces/07-decisions/README.md (ADR-006..009 Proposed)
next_action: human approve ADR-006 (Stage 2 direction) → เริ่ม P0-A housekeeping + A1 schema
-->

# Work Status — ai-project-template

อัปเดตล่าสุด: 2026-06-05

## สถานะปัจจุบัน

**Phase:** Stage-2 design — exploration เสร็จ กำลังเข้าสู่ schema design
**Active branch:** `explore/odysseus-analysis`
**Released:** v1.10.0 (challenge-necessity + task close gate + behavioral tests) — merged master
**Blocker:** ⏳ ADR-006 (Stage 2 direction) = Proposed → รอ human approve ก่อนเริ่ม build Engine

## สิ่งที่เสร็จ session นี้ (2026-06-05 — Odysseus → Stage 2)

- วิเคราะห์ Odysseus เชิงลึก (feasibility + differentiation + stack) → `exploration/odysseus-analysis.md`
- ตกผลึก vision 3-layer (Substrate→Engine→Shell) → `exploration/north-star-vision.md`
- gap audit (internal, อ่าน repo จริง) + market research (competitors + trends) → `exploration/what-it-should-be.md`
- positioning refined: **"Governed Project Memory"** (4 market corrections: risk-tiered, multi-agent reframe, อย่า out-index, compose underneath)
- master plan: 11 phase, critical path ~14-15 สัปดาห์ถึง ship, 6 decision gates, 5 stop points → `exploration/master-plan.md`
- schema architecture ตกผลึก: CORE (process) + PROFILE (product), compose ได้
- บันทึก decision เป็น ADR-006..009 (Proposed) + dogfood methodology (งานนี้)

## Next Actions

1. ⏳ **human approve ADR-006** (Stage 2 direction) — gate ก่อนทุกอย่าง
2. P0-A housekeeping (safe, reversible): T-041 core-count, T-042 missing compliance-codes, T-043 git_pipeline, T-044 C-15..19
3. เคาะ G0 (canonical inversion → dual-authority ADR-007)
4. A1 core schema (T-045) — ร่าง entities/fields/types เป็นเอกสารจริง
5. A5 retrofit schema กับ repo นี้ + เคสเกม → validate ก่อน build

## Stage 2 Roadmap (สรุป)

```
P0 Substrate Fixes ← เริ่มหลัง ADR-006 approve
P1 config-driven validator → P2 CLI evaluator ← MVW (governance linter)
P3 tool-call interception ← bottleneck → P4 canonical store
P5 read-only Cockpit → P6 governed agent + Decision Inbox ← SHIP / MVP
P7-P10 model-agnostic → specialists → multi-repo → vector
```

## Note: Dogfooding gap ที่พบ

methodology (CoreAiWorkspaces) ถูก bypass ตั้งแต่ v1.5.0 — work-status/task-board ค้างที่ 2026-05-08 ไม่สะท้อน v1.6-1.10 หรือ exploration นี้ → เริ่มใช้จริงอีกครั้ง session นี้ (= บททดสอบว่า substrate พร้อมเป็นฐาน Engine มั้ย)
