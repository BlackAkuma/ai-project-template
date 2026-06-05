# ADR-006: Stage 2 Product Direction — "Governed Project Memory"

**Date:** 2026-06-05
**Status:** Accepted
**Author:** AI session + User
**Related Tasks:** T-040 (Odysseus analysis + Stage-2 exploration)
**Source Reference:** `exploration/north-star-vision.md`, `exploration/what-it-should-be.md`, `exploration/master-plan.md`

## Context

วิเคราะห์ Odysseus (self-hosted AI workspace, 52k stars) → ตกผลึกว่า "หน้าจอ + เสียบ model + ต่อ model serving" เป็น commodity (ใครก็ fork ได้) สิ่งที่ Odysseus ไม่มีคือ **project/structural governance** ซึ่งคือจุดแข็งของ ai-project-template

เกิดคำถามเชิงทิศทาง: โปรเจ็กต์นี้ควรขยายจาก "template/methodology" ไปเป็น product จริงหรือไม่ และแบบไหนถึงไม่หลุดคอนเซปต์

Vision เดิมที่ถอดมา (จากผู้ใช้): เว็บ control การทำงานพัฒนาซอฟต์แวร์ ข้าม multi-repo ให้ AI เข้าใจทั้งโครงการ ทำงานกับทีมคน/AI โดยเสียบ model ไหนก็ได้ — "ความเก่งของ AI = context engineering ไม่ใช่ตัว model"

## Options Considered

**Option A: เก็บเป็น methodology อย่างเดียว + skill pack** — on-concept 100%, effort ต่ำ; con: ไม่ตอบ vision product ของผู้ใช้

**Option B: สร้างแอปแยก repo ที่ใช้ template** — เป็น product จริง; con: undertaking ใหญ่, อาจหลุดเป็น "Odysseus clone"

**Option C (เลือก): 3-layer bottom-up — Substrate → Engine → Shell** — substrate (template) = สมอง, Engine = governance machine-enforced, Shell = แอปแบบ Odysseus ที่ project-centric; สร้างจากล่างขึ้นบน Shell มาสุดท้าย

## Decision

เดินทาง **Option C** ภายใต้ positioning **"Governed Project Memory"**:

> ระบบ governance + project memory ที่ AI ตัวไหนก็ทำงานเชิงโครงการได้น่าเชื่อถือ เพราะกฎถูก *บังคับเป็น state จริง* รันบนเครื่องตัวเอง เสียบ model ไหนก็ได้

5 เสา: Governed (risk-tiered, evidence-based) · Project Memory (structured/durable/evolving) · Decision Inbox (human-gate first-class) · Model-agnostic + Self-hosted · Multi-repo orchestration

Market validation: context engineering = mainstream (ACE paper); project memory = ช่องว่างที่ vendor (mem0/Letta/Zep) ยังไม่แก้; governance demand จริง (88% เจอ AI-agent incident); four-way intersection (project-centric + enforced-governance + multi-agent + multi-repo) ยังไม่มีใครถือครบ

## Consequences

- ลำดับ fixed: Substrate → Engine → Shell (ห้ามกลับ — Shell value = Substrate)
- substrate (core/) ต้องแก้ให้ machine-ready ก่อน (ดู ADR-007, ADR-009)
- governance ต้อง risk-tiered ไม่ใช่ uniform (ดู ADR-008)
- ของที่ "ไม่" ทำ: ไม่ out-index Sourcegraph, ไม่ out-orchestrate LangGraph, ไม่ headline swarm, ไม่ reinvent AGENTS.md (interoperate)
- Stop points มี standalone value: หลัง P2 (governance linter), หลัง P6 (SHIP)

## Review Trigger

ทบทวนถ้า: คู่แข่ง (Cursor/Factory) ปิด gap four-way · ผู้ใช้ตัดสินหยุดที่ Engine-CLI (G1) · เจอว่า substrate รับ Stage 2 ไม่ไหวหลัง dogfood

## Panel Review Record (2026-06-05)

**โหวต: 3/3 PASS** (technical 0.72 · strategic 0.72 · contrarian 0.60)
**Dissent ที่บันทึก:**
- contrarian: live contradiction กับกฎ uniform ที่ ship แล้ว (08ba8a7) → **จัดการใน ADR-008 + task T-052**
- contrarian: directional drift ไปฝั่ง Shell-product ทั้งที่ G5 (universal-vs-own) ยัง defer → **คงไว้ defer, ไม่ resolve ตอนนี้**
**การตัดสิน (AI):** Accept — direction ผ่านสะอาด; soften wording "evidence-based" → "presence/structure-verifiable" (ใน ADR-007/009 แล้ว); market figures = directional/non-authoritative (รับทราบ)
