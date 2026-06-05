# ADR-009: Schema Architecture — CORE + PROFILE

**Date:** 2026-06-05
**Status:** Accepted (after panel-mandated revisions)
**Author:** AI session + User
**Related Tasks:** T-045 (A1 core schema), T-046/047/048 (D1/D2/D3)
**Source Reference:** `exploration/what-it-should-be.md` (§3 substrate fixes + "ลำดับ" item #2/#5), บทสนทนา schema design 2026-06-05

## Context

"ซอฟต์แวร์" มีหลายสาขา (web/desktop/mobile/game/web-game/console/industrial/research...) scope ใหญ่มาก แต่ **แกนของงานคือ business/การบริหารโครงการ** ผู้ใช้ต้องการครอบทั้งหมดที่เป็น software engineering แต่โฟกัสเกม (ต่อ Godot/Unreal)

ต้องออกแบบ schema ให้ครอบ domain กว้าง โดยไม่บวมและ machine-enforceable ข้าม domain

## Options Considered

**Option A: schema เดียวครอบทุก domain** — ง่ายตอนแรก; con: บวม, field เกมปนกับ field web

**Option B: schema แยกต่อ domain** — เฉพาะเจาะจง; con: ไม่ universal, core ซ้ำ, compose ไม่ได้ (web-game?)

**Option C (เลือก): CORE (invariant) + PROFILE (variant) เสียบเข้า core, compose ได้**

## Decision

แยก 2 ชั้นด้วยเส้น **Process (universal) vs Product (variant)**:

- **CORE** = process ของทุกซอฟต์แวร์ (เข้าใจ→วิเคราะห์→แผน→ทำตามแผน→verify→ทีมคน/AI): `Project, Requirement, Plan, Task, Evidence, Decision(ADR), TeamMember, Gate, Repo, Entity, Event`
  - **`Task.risk_level` + `Gate.risk_level`** (enum Level 0–3) — field ที่ ADR-008 delegate มา (dependency แก้แล้ว); Engine-determined ไม่ใช่ AI self-assess; default unknown→Level 2
  - **core lifecycle** = `todo → design_validate → in_progress → review → done` (+ `blocked`) — **คง design_validate ไว้** ตรงกับ state machine จริงใน core/07 (panel จับว่าร่างแรกตัดทิ้งผิด); profile เพิ่ม *sub-gate* ภายใน stage ไม่เพิ่ม state ใหม่
- **PROFILE** = product-specific เสียบ 5 อย่างเข้า core: `lifecycle+, evidence+, roles+, quality+, toolchain, doc-types`
- **classify ด้วยมิติที่ทำให้ management ต่าง** (build/verify target, artifact type, quality dims, toolchain, specialists) ไม่ใช่ surface (web/mobile)
- **profile compose ได้** (web-game = web + game) — additive merge + priority

สร้างจริง: CORE schema (ครั้งเดียว) + extension mechanism + profile เริ่มต้น 2 ตัว (`generic-software` default, `game` ลงลึก) domain อื่น = เขียน pack ทีหลัง ไม่รื้อ core

## Open sub-decisions (เคาะใน Stage A)

- **D1 (T-046) — task lifecycle + profile stage:** core lifecycle = `todo→design_validate→in_progress→review→done` (คง design_validate), profile เพิ่ม *sub-gate* ภายใน stage (เกม: review ต้องผ่าน playtest) ไม่เพิ่ม state ใหม่ในแกน
- **D2 (T-047) — evidence model:** แยก `machine-verifiable` (Engine ตรวจ deterministic) vs `human-attested` (sign-off ผ่าน Decision Inbox, Engine ตรวจแค่ presence) — ตรง "enforce presence ไม่ใช่ quality" · **reconcile กับ ADR-007:** เส้น machine/attested = subset ของ "enforceable state" ของ 007; human-attested ยังเป็น structured record แต่ value เป็น trust-based (007 framing ปรับเป็น "presence/structure-verifiable" แล้ว)
- **D3 (T-048) — profile compose conflict:** เสนอ additive merge + priority order; toolchain ซ้อนได้

## Consequences

- core entities = ร่างแรกของ AI-CONTEXT schema (P0-B step 1)
- domain ใหม่ขยายได้ไม่จบ โดย core ไม่แตะ → scale ไป vision multi-tool
- ความเฉพาะทางเกมช่วย: ถ้า profile เกมเสียบสวย profile อื่นก็เสียบได้ (stress-test extension mechanism)
- ต้อง validate ด้วย retrofit (A5) ก่อน build

## Review Trigger

ทบทวนถ้า: retrofit (A5) เผยว่า core/profile เส้นแบ่งผิด · มี domain ที่ใส่กรอบ process ไม่ได้ · D1/D2/D3 ตอนเคาะออกมาขัด architecture นี้

## Panel Review Record (2026-06-05)

**โหวต: 2/3 PASS** (technical 0.68 PASS · strategic 0.72 PASS · contrarian 0.60 **FAIL**)
**Contrarian FAIL — มีมูลจริง (AI เห็นด้วย):**
- risk_level homeless (สัญญา ADR-008 ไม่ถูกทำ) → **แก้: เพิ่ม Task.risk_level + Gate.risk_level**
- source cite ผิด (§5 → ต้อง §3) → **แก้แล้ว**
- design_validate หายจาก lifecycle จริง → **แก้: คง design_validate ไว้**
- D2 อาจ diverge กับ ADR-007 → **แก้: เพิ่มประโยค reconcile**
**Strategic suggestion ที่รับเป็น guidance (log ไว้สำหรับ Stage A):**
- descope substrate phase → 1 profile (game) + extension *hook* เท่านั้น, defer compose-engine (D3) ไป post-SHIP → **บันทึก: ไม่ build compose engine ใน substrate phase**
- retrofit (A5) ต้อง validate กับ domain ที่ห่างจริง (research/industrial) ไม่ใช่แค่ generic+game
**การตัดสิน (AI):** contrarian ถูก → revise แก้ครบก่อน Accept (B). compose-engine descope = guidance สำหรับ Stage A (เรื่อง design ไม่ใช่ blocker → ทำต่อได้)
