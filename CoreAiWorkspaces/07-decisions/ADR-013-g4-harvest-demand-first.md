# ADR-013: G4 Decision — Harvest demand first, gate Shell on willingness-to-pay (B)

**Date:** 2026-06-07
**Status:** Accepted
**Author:** User decision + G4 panel (technical/strategic/contrarian + marketing/revenue)
**Related:** BRD OD-3/OD-4/G4, ADR-011 (G1 C-conservative — OD-3 gate), ADR-006
**Resolves:** partial OD-3 (revenue hypothesis + gate criteria); defers full Shell

## Context

Engine-side สมบูรณ์ + tested headless (45 tests/6 suites): governance linter, tamper-evidence, gated mutation, JSON-in-git canonical store (drift=0), Decision Inbox data layer. ที่เหลือของผลิตภัณฑ์ = Shell UI. G4 = build Shell หรือไม่

## G4 Panel (2/3 + marketing/revenue)

| lens | vote | conf | core |
|------|------|------|------|
| technical | C | .68 | harvest WTP จาก invisible CLI ไม่ได้ → read-only Cockpit เป็น instrument |
| **strategic** | **B** | .72 | Shell=commodity; ADR-011 ล็อก gate-on-demand แล้ว; อย่า override |
| **contrarian** | **B** | .68 | build Shell = R5 ร้อนรน trap; B least-fatal + optionality |
| marketing | B | — | revenue hypothesis ชัด; harvest ก่อน build |

**tally A0 B2 C1 → B** · **A ตัดเอกฉันท์** (commodity + no demand + ขัด ADR-011 OD-3 gate + R5)

## Decision

**B — harvest demand first** (เลือกโดย user):
- **ไม่ build Shell ตอนนี้** · soft-ship OSS + hero-demo (DEMO.md, มีแล้ว) เป็น demand funnel
- **outreach 8-12 ราย** ถาม WTP แบบ falsifiable (ไม่ใช่ pitch)
- **Shell-go signal (นิยามชัด กัน infinite deferral):** ≥1 signed design-partner หรือ paid LOI · **timebox 4-6 สัปดาห์** → ถ้าไม่ถึง auto-escalate เป็น build/no-build review
- **C (read-only Cockpit) = pre-committed fallback** ถ้า 0 design-partner หลัง outreach cycle (disambiguate "no demand" vs "demo too thin"); strict scope: read-only, ≤1wk, ห้ามโตเป็น full Shell
- **A (full Shell) deferred** จนมี signal

## Revenue Hypothesis (OD-3, marketing)
- **ฟรี:** OSS linter (bottom-up wedge สู้ install-base คู่แข่ง)
- **จ่าย (governance-of-record):** hosted durable Decision Inbox + team ACLs + **tamper-evident compliance/audit export** (per-run ของคู่แข่งทำไม่ได้เชิงโครงสร้าง) — per-seat บนคนที่ approve
- **ใคร:** ทีม dev/ops 2-10 (self-hosted) · **เมื่อ:** คนที่ 2 ต้องเชื่อ output ของ agent คนแรก · **trigger:** "agent แกล้ง done / ship ของไม่ review แล้วมีคนเจ็บ"

## Consequences

- **autonomous build terminus:** สิ่งที่ build headless ได้เสร็จหมด (Engine moat); next = **real-world GTM ของ user** (publish hero-demo + category flag, outreach) — ไม่ใช่ autonomous coding
- category flag (publish hero-demo + adversarial-bypass result) ทำ NOW ภายใต้ soft-ship (decoupled จาก Shell build) — กัน Cursor fast-follow
- **contrarian/technical-C dissent (บันทึก):** invisible-CLI harvest อาจ under-convert → mitigation = hero-demo asset + C-fallback pre-committed; ถ้า Cursor ปักธง category ก่อน → flip C ทันที (ADR-011 review trigger)

## Review Trigger
reopen ถ้า: ≥1 design-partner/WTP signal ได้ (→ build Shell, likely C→A) · timebox 4-6wk หมดโดยไม่มี signal (→ build/no-build review) · Cursor ปักธง category ก่อน (→ flip C)
