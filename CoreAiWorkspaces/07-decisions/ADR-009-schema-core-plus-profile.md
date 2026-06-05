# ADR-009: Schema Architecture — CORE + PROFILE

**Date:** 2026-06-05
**Status:** Proposed
**Author:** AI session + User
**Related Tasks:** T-045 (A1 core schema), T-046/047/048 (D1/D2/D3)
**Source Reference:** `exploration/what-it-should-be.md` (§5), บทสนทนา schema design 2026-06-05

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
- **PROFILE** = product-specific เสียบ 5 อย่างเข้า core: `lifecycle+, evidence+, roles+, quality+, toolchain, doc-types`
- **classify ด้วยมิติที่ทำให้ management ต่าง** (build/verify target, artifact type, quality dims, toolchain, specialists) ไม่ใช่ surface (web/mobile)
- **profile compose ได้** (web-game = web + game) — additive merge + priority

สร้างจริง: CORE schema (ครั้งเดียว) + extension mechanism + profile เริ่มต้น 2 ตัว (`generic-software` default, `game` ลงลึก) domain อื่น = เขียน pack ทีหลัง ไม่รื้อ core

## Open sub-decisions (เคาะใน Stage A)

- **D1 (T-046) — task lifecycle + profile stage:** เสนอ core lifecycle เป็นแกนคงที่ (`todo→in_progress→review→done`), profile เพิ่ม *sub-gate* ภายใน stage (เกม: review ต้องผ่าน playtest) ไม่เพิ่ม state ใหม่ในแกน
- **D2 (T-047) — evidence model:** เสนอแยก `machine-verifiable` (Engine ตรวจ) vs `human-attested` (sign-off ผ่าน Decision Inbox) — ตรง "enforce presence ไม่ใช่ quality"
- **D3 (T-048) — profile compose conflict:** เสนอ additive merge + priority order; toolchain ซ้อนได้

## Consequences

- core entities = ร่างแรกของ AI-CONTEXT schema (P0-B step 1)
- domain ใหม่ขยายได้ไม่จบ โดย core ไม่แตะ → scale ไป vision multi-tool
- ความเฉพาะทางเกมช่วย: ถ้า profile เกมเสียบสวย profile อื่นก็เสียบได้ (stress-test extension mechanism)
- ต้อง validate ด้วย retrofit (A5) ก่อน build

## Review Trigger

ทบทวนถ้า: retrofit (A5) เผยว่า core/profile เส้นแบ่งผิด · มี domain ที่ใส่กรอบ process ไม่ได้ · D1/D2/D3 ตอนเคาะออกมาขัด architecture นี้
