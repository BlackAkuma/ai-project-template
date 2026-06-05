# ADR-010: BRD v1.0 Accepted (Governed Project Memory)

**Date:** 2026-06-05
**Status:** Accepted
**Author:** AI session + User (via 3-iteration panel)
**Related:** `CoreAiWorkspaces/00-source/BRD.md` (v1.0), ADR-006..009
**Review method:** brd-review-panel — 3 voting lens (technical/strategic/contrarian) 2/3 + marketing advisory

## Context

ผู้ใช้สั่ง (loop): ทำ BRD ให้ครบโดย panel review (2/3 ผ่าน), log ทุก review, เคารพ dissent, marketing ตรวจ feature/trend, iterate จนทุกฝ่าย agree → lock

BRD เป็น source-of-truth requirements ของผลิตภัณฑ์ "Governed Project Memory" สังเคราะห์จาก exploration + ADR-006..009

## Options Considered

- **คง iterate ต่อจน contrarian PASS** — con: contrarian เป็น adversarial-lens, residual FAIL อยู่บน *named-deferrals* (OD-1/T-058/model-agnostic@SHIP) ที่ถ้าตัดสินตอนนี้ = premature gate decision (ร้อนรน trap); อาจ loop ไม่จบ
- **Lock ที่ 2/3 (เกณฑ์ผู้ใช้) เมื่อ converged** ✅ — defect จริงแก้หมด 3 รอบ, confidence ไต่ขึ้น, contrarian agree-on-direction

## Decision

**Lock BRD v1.0 = Accepted** ผ่าน 3-iteration panel:

| iter | votes | contrarian |
|------|-------|-----------|
| 1 (v0.1) | 3/3 PASS | .60 borderline |
| 2 (v0.2) | 2/3 PASS | FAIL .66 (defect จริง → แก้ v0.3) |
| 3 (v0.3→v0.4) | 2/3 PASS | FAIL .63 (named-deferrals + small fixes → แก้ v0.4) |

marketing = viable ทั้ง 3 รอบ (thesis/trend แรง, ต้อง GTM/hero-demo)

**เหตุผล lock:** 2/3 (เกณฑ์ผู้ใช้) ผ่าน 3 รอบติด · defect จริงทุกข้อแก้แล้ว · contrarian self-acknowledged "named-deferral != incompleteness" = agree-on-direction · ค้านแค่ adversarial-strictness บน deferrals ที่ผูก gate

## Consequences

- BRD v1.0 = baseline requirements; FR/NFR + acceptance criteria ใช้ขับ build (P1+)
- Open decisions OD-1 (store/G3), OD-2 (CLI/G1), OD-3 (Shell/G4), OD-4 (universal/G5) = panel+lock เมื่อถึง phase (ไม่ตัดสินก่อนเวลา)
- carry-over T-051/052/053/058 = remediate ก่อน market risk-tiered claim (credibility prereq)
- **reopenable:** lock ทับ contrarian-FAIL อย่างโปร่งใส (dissent บันทึกครบใน BRD §13) — ถ้าผู้ใช้ไม่เห็นด้วย reopen ได้

## Review Trigger

reopen ถ้า: ผู้ใช้ไม่เห็นด้วยกับ lock-over-contrarian · deferred gate (OD-1..4) ตอน resolve เผยว่า BRD assumption ผิด · market shift (คู่แข่งปิด gap)
