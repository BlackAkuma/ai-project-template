# ADR-008: Risk-Tiered Governance (not uniform gates)

**Date:** 2026-06-05
**Status:** Accepted (after panel-mandated revisions)
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

Governance **risk-tiered** เสมอ — bind ทุก gate/action เข้า escalation Level

**สำคัญ (แก้จาก panel review):** ADR นี้ **redefine** escalation level จากแกน *uncertainty* (เดิมใน core/11) → แกน *risk/reversibility* — ไม่ใช่ "แค่ bind ของที่มีอยู่" ต้อง re-publish mapping Scenario A–N → new-Level เต็มใน P0-B (งาน T-051)

| Level | ลักษณะ | Effect |
|-------|--------|--------|
| **0 Verify First** | triage เบาๆ — จัด risk tier ของ action | **รันเสมอ** (cheap, deterministic) → ตัดสินว่าต้องขึ้น gate ไหน |
| 1 | reversible, low-stakes | auto log + continue (ไม่ prompt) |
| 2 | medium / unknown | → Decision Inbox (human approve) |
| 3 | irreversible/security/prod **+ ขัด requirement ชัดเจน + data loss** | hard stop |

**แก้ chicken-and-egg (challenge-necessity):** Level 0 = triage เบา (รันทุก action), ส่วน challenge-necessity เต็ม (a/b/c + 3-lens) รันเฉพาะเมื่อ triage = Level 2–3; งานเสี่ยงต่ำ (Level 1) ข้าม challenge หนักได้

**กฎกันโกง (แก้ self-assessment):**
- risk classification = **Engine-determined** (constitutive, P3) ไม่ใช่ AI ประเมินตัวเอง → กัน AI downgrade เพื่อ bypass (pattern ที่ commit 08ba8a7 บล็อก)
- **conservative default:** unknown → Level 2 เสมอ (ไม่เคย auto-pass)
- **hard-stop ที่ห้ามลด:** core/11 Level-3 conditions ทั้งหมด (data loss, security/credentials, prod, ขัด requirement ชัดเจน) force Level 3 ไม่ว่า classifier จะว่ายังไง

## Consequences

- แก้ posture ใน `development-plan.md` (uniform → tiered) — งาน P0-B step 4 (bind risk tiers)
- ลด friction: งานเสี่ยงต่ำลื่น, gate เฉพาะที่สำคัญ → หลีกเลี่ยง approval fatigue
- Decision Inbox (Shell) รับเฉพาะ Level 2–3 → ไม่ท่วม
- `risk_level` field นิยามใน **ADR-009 CORE schema** (Task + Gate) — dependency แก้แล้ว
- ⚠️ **supersede กฎที่ ship แล้ว:** CLAUDE.md "Scenario M ทุกครั้ง ไม่ยกเว้น" + commit 08ba8a7/f9ee68a (uniform entry-point gate) → ADR นี้ทำให้ uniform-gate กลายเป็น tiered; ต้อง rewrite CLAUDE.md + entry-point enforcement (งาน **T-052**, รอบ project review — ไม่ทำเงียบ)
- silent auto-pass (Level 1) อาจสะสม drift → คุมด้วย whole-project review round + conservative default

## Review Trigger

ทบทวนถ้า: tier ปล่อยงานเสี่ยงผ่านง่ายเกิน หรือหนักเกินจน friction · classifier ตัดสิน Level ผิดบ่อย · regulation เปลี่ยน (EU AI Act high-risk เลื่อนเป็น Dec 2027)

## Panel Review Record (2026-06-05)

**โหวต: 2/3 PASS** (technical 0.72 PASS · strategic 0.82 PASS · contrarian 0.62 **FAIL**)
**Contrarian FAIL — มีมูลจริง (AI เห็นด้วย):**
- Level 0 "Verify First" หายจากตาราง (ทั้งที่ challenge-necessity อยู่ที่นั่น) → **แก้: เพิ่ม Level 0 + triage model**
- redefine แกน uncertainty→risk เงียบๆ → **แก้: ประกาศ redefine ชัด + task T-051 re-publish mapping**
- risk_level homeless (008 พึ่ง 009 แต่ 009 ไม่มี) → **แก้: เพิ่ม field ใน ADR-009**
- Level 3 แคบ ลด hard-stop (ขัด requirement) → **แก้: คง core/11 Level-3 conditions ทั้งหมด**
- self-assessment gameable → **แก้: Engine-determined + conservative default unknown→L2**
- reverse กฎ uniform ที่ ship → **แก้: ระบุ supersede + task T-052 (project review, ไม่ทำเงียบ)**
**การตัดสิน (AI):** contrarian ถูกทุกข้อ → revise แก้ครบก่อน Accept (ทางเลือก B). Accept หลัง revise. defect ที่กระทบ core ที่ ship แล้ว (T-052) lock เป็น task รอ project review ไม่แก้เงียบ
