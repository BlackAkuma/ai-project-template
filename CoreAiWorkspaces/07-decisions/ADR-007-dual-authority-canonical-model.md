# ADR-007: Dual-Authority Canonical Model

**Date:** 2026-06-05
**Status:** Accepted
**Author:** AI session + User
**Related Tasks:** T-050 (A6 dual-authority contract)
**Source Reference:** `exploration/what-it-should-be.md` (§3, Critical gap #1), `exploration/master-plan.md` (G0)

## Context

contract ปัจจุบัน: *"body ของไฟล์คือ source of truth — AI-CONTEXT block เป็นแค่ orientation ถ้าไม่ตรงเชื่อ body"*

ปัญหาสำหรับ Engine: Engine จะ enforce gate ได้ก็ต่อเมื่อ parse state ได้แน่นอน แต่ truth อยู่ใน free-form Thai prose (parse ไม่ได้) ส่วนครึ่งที่ parse ได้ (block) ถูกประกาศว่า non-authoritative → premise ของ Engine (evidence-based, ไม่เชื่อคำพูด) พังทันที

ผู้ใช้ยืนยัน: pain หลักคือ "ให้ AI อ่าน markdown เสมอ แต่มันหลุดบ่อย" — คือ tool-universality แบบ advisory ที่ไม่เสถียร ไม่ใช่สิ่งที่หวง

## Options Considered

**Option A: คงไว้ (body = truth)** — universal markdown; con: Engine enforce ไม่ได้, drift บ่อย (ปัญหาปัจจุบัน)

**Option B: invert เต็มตัว (structured = truth, prose = generated render ทั้งหมด)** — Engine แข็งสุด; con: เสีย human-authoring + nuage + Layer-1 tool-universality เต็มที่

**Option C (เลือก): dual-authority** — structured = truth สำหรับ *enforceable state* (status, evidence, IDs, lifecycle); prose = truth สำหรับ *narrative* (reasoning, caveats) แต่ละอันเป็นเจ้าของ domain ตัวเอง

## Decision

ใช้ **dual-authority** — ลากเส้นที่ "enforceable state vs narrative"

- **enforceable state** → structured (Engine ตรวจได้ deterministic)
- **reasoning/narrative** → prose (คนอ่าน Engine ไม่ enforce)

แยกความหมาย "universal": **model-agnostic (เสียบ model ไหนก็ได้) คงไว้เต็ม** ส่วนที่ยอมแลกคือ tool เปล่าๆ แก้ markdown แล้วเป็น truth ได้ (= สิ่งที่ทำให้หลุดอยู่แล้ว)

**Sequencing:** P0 แค่ *ประกาศ* intent; enforce จริง (prose = generated view) รอ P4 ตอน store generate; จนถึง P4 ใช้ C-07 (block-body sync) เป็นสะพานให้ทั้งคู่เท่ากัน → ไม่จ่ายต้นทุนทันที

## Consequences

- enforceable state บันทึกเป็น prose ลอยๆ ไม่ authoritative อีก ("done" ต้องเป็นหลักฐาน ไม่ใช่ความรู้สึก)
- prose ยังเป็น first-class generated view → git-diffable, human-readable, no-Engine session อ่านได้
- nuance ที่ใส่ schema ไม่ได้ → อยู่ใน narrative prose (linked กับ structured record)
- ⚠️ **C-07 ต้อง invert (panel จับ):** ปัจจุบัน C-07 (core/03 L125, core/15 L65) นิยาม "block≠body → เชื่อ body" = ตรงข้าม dual-authority → ใช้เป็น "สะพานเท่ากัน" ไม่ได้จริง ต้อง rewrite ที่ P0-B step 5: enforceable-state fields → block (structured) ชนะ (งาน **T-053**, รอบ project review)
- **determinism narrow:** Engine ตรวจ deterministic เฉพาะ machine-verifiable evidence; human-attested = ตรวจแค่ presence (สอดคล้อง ADR-009 D2 + "enforce presence ไม่ใช่ quality")
- gate G0 = commit ทิศนี้ — **"high-cost-to-reverse" ไม่ใช่ absolute one-way door**; A5 retrofit (Review Trigger) ยัง rollback ได้ก่อน P1-P6 พึ่งพา
- enforceable-state fields = field ที่ถูก gate predicate อ้าง (= ที่อยู่ใน ADR-009 CORE schema marked machine-verifiable); ที่เหลือ = narrative prose

## Review Trigger

ทบทวนถ้า: พบว่า narrative/structured เส้นแบ่งไม่ชัดในทางปฏิบัติ · no-Engine workflow สำคัญกว่าที่คิด · retrofit (A5) เผยว่า dual-authority ใช้จริงไม่ได้

## Panel Review Record (2026-06-05)

**โหวต: 3/3 PASS** (technical 0.82 · strategic 0.82 · contrarian 0.60 — confidence สูงสุดในชุด)
**Dissent ที่บันทึก + แก้แล้ว:**
- contrarian: C-07 ขัดตัวเอง (นิยามว่า "เชื่อ body" ใช้เป็นสะพานไม่ได้) → **เพิ่ม Consequence: C-07 ต้อง invert ที่ P0-B step5 (task T-053)**
- contrarian/technical: "evidence-based" oversell (human-attested ตรวจได้แค่ presence) → **narrow determinism claim แล้ว**
- contrarian: "one-way door" ขัดกับ rollback ใน Review Trigger → **softened เป็น "high-cost-to-reverse"**
- technical: boundary straddling fields ไม่มี tie-breaker → **เพิ่มกฎ: field ที่ gate predicate อ้าง = structured-authoritative**
**การตัดสิน (AI):** Accept หลังเพิ่ม 4 ข้อข้างบน — contrarian ถูกทุกข้อ แก้ที่ต้นเหตุแล้ว
