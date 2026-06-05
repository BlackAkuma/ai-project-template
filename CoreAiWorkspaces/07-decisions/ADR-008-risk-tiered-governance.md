# ADR-008: Risk-Tiered Governance (not uniform gates)

**Date:** 2026-06-05
**Status:** Proposed
**Author:** AI session + User
**Related Tasks:** T-040 (Stage-2 exploration)
**Source Reference:** `exploration/what-it-should-be.md` (§2 correction #1), `core/11` escalation Level 0–3

## Context

`development-plan.md` เดิมวาง challenge-necessity (Scenario M step 0) + gate บังคับ *ทุก* code-touch

Market finding ขัดตรงๆ: **Gartner เตือน (2026-05-26) ว่า uniform governance across all AI agents = สาเหตุ enterprise AI agent failure** — approval fatigue สร้าง false safety; Gartner ยังทำนาย 40% agentic project ถูกยกเลิกภายใน 2027 ส่วนหนึ่งจาก weak/heavy risk controls

นั่นคือ posture "Scenario-M ทุก action" ของเรา = anti-pattern ที่ถูกชี้ตรงๆ

## Options Considered

**Option A: uniform mandatory gate (เดิม)** — เข้มสม่ำเสมอ; con: approval fatigue, Gartner failure mode

**Option B: no gate / advisory only** — ลื่นสุด; con: ไม่มี governance = ทั้ง premise พัง

**Option C (เลือก): risk-tiered — bind gate เข้า escalation Level 0–3** — gate หนักตามความเสี่ยง

## Decision

Governance **risk-tiered** เสมอ — bind ทุก gate/Scenario เข้า escalation Level (ซึ่ง `core/11 §3` มี mapping A–N → Level 0–3 อยู่แล้ว แต่ยังไม่ bind เข้า gate):

| Level | ลักษณะ | Effect |
|-------|--------|--------|
| 1 | reversible, low-stakes | auto log + continue (ไม่ prompt) |
| 2 | medium | → Decision Inbox (human approve) |
| 3 | irreversible/security/prod | hard stop |

challenge-necessity ยังอยู่ แต่ trigger ตาม risk ไม่ใช่ทุก action

## Consequences

- แก้ posture ใน `development-plan.md` (uniform → tiered) — งาน P0-B step 4 (bind risk tiers)
- ลด friction: งานเสี่ยงต่ำลื่น, gate เฉพาะที่สำคัญ → หลีกเลี่ยง approval fatigue
- Decision Inbox (Shell) รับเฉพาะ Level 2–3 → ไม่ท่วม
- ต้องนิยาม risk_level ต่อ task/action (อยู่ใน schema — ADR-009)

## Review Trigger

ทบทวนถ้า: พบว่า tier ที่ตั้งไว้ปล่อยงานเสี่ยงผ่านง่ายเกิน หรือยังหนักเกินจน friction · regulation เปลี่ยน (EU AI Act high-risk เลื่อนเป็น Dec 2027)
