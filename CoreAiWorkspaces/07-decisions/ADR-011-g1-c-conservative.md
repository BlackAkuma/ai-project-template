# ADR-011: G1 Decision — C-conservative (soft-ship OSS + protect P3)

**Date:** 2026-06-06
**Status:** Accepted
**Author:** User decision + G1 panel (technical/strategic/contrarian + marketing)
**Related:** BRD OD-2/G1, ADR-006, master-plan §7 (stop-points)
**Resolves:** Open Decision OD-2 (G1: ship Engine-CLI vs proceed P3)

## Context

MVW reached = governance linter (engine/check.py: 6 gates-as-data, 9 resolvers, 14/14 tests, CI, wired pre-commit hook, dogfooded). G1 gate = ตัดสินว่าที่ MVW จะ (A) ship+pause / (B) moat-first P3 / (C) hybrid

## G1 Panel (2/3 rule + marketing)

| lens | vote | conf | core |
|------|------|------|------|
| technical | C | .66 | linter เสร็จ cost~0; P2/P3 decoupled → parallel ไม่เพิ่ม risk; ไม่ ship = value ค้าง |
| strategic | C | .72 | moat=P3 แต่ต้องปักธง category ก่อน window ปิด (R9); A/B เสีย timing ครึ่ง |
| **contrarian** | **B** | .60 | solo: hybrid แตก focus ที่ P3 (bottleneck/R5); linter=commodity; ship เร็ว=เปิดไพ่ก่อนมี moat; R9 แค่ M/M |
| marketing | C | — | "C แต่ sequencing เข้มงวด ≈ A-then-B": soft-ship ปักธง, เลื่อน loud launch จนมี hero demo |

**tally: A0 B1 C2 → C majority**

## Decision

**C-conservative** (เลือกโดย user — จุด converge ของทุกฝ่าย):
- **soft-ship OSS linter เงียบๆ** (repo + README + adversarial-bypass note; cost~0 เพราะมีอยู่แล้ว) — ปักธง category "Governed Project Memory"
- **protect P3 = single-threaded critical path** (non-negotiable focus); launch ops = timeboxed discrete milestone ไม่ใช่ parallel track ต่อเนื่อง
- **เลื่อน loud launch (HN/Show) + hero demo จนหลัง P3** (gate launch บน adversarial-bypass result + live block-demo)
- ห้าม headline feature ที่ยังไม่ ship (model-agnostic/multi-repo) — BRD §9 proves-vs-defers
- เลือก C-conservative = **commit G2 (build runtime/P3)** ด้วย

## Consequences

- next build = **P3 interception** (constitutive enforcement, moat) เป็น critical path
- soft-ship prep = task แยก timeboxed (README + adversarial note) — ไม่กิน P3 focus
- harvest OD-3 signal (design-partner/willingness-to-pay) จาก soft-ship — feed G4 ภายหลัง
- **contrarian dissent บันทึก (ไม่ override เงียบ):** ถ้า founder focus หลุด → B กลายเป็น infinite deferral / hybrid = "ทำทั้งคู่ห่วย"; mitigation = timebox launch, P3 single-threaded, P3 internal go/no-go (ถ้า sandbox-escape ไม่ผ่านใน 2.5-4wk → fall back A)

## Review Trigger

reopen ถ้า: P3 บานเกิน box (→ tilt A/C) · คู่แข่งปักธง category ก่อน (→ B no-flag กลายเป็น fatal) · soft-ship launch ops เริ่มกิน P3 focus
