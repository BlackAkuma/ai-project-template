# ADR-007: Dual-Authority Canonical Model

**Date:** 2026-06-05
**Status:** Proposed
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
- gate G0 ใน master-plan = การ commit ทิศนี้ (one-way door เมื่อ P1-P6 พึ่งพา)

## Review Trigger

ทบทวนถ้า: พบว่า narrative/structured เส้นแบ่งไม่ชัดในทางปฏิบัติ · no-Engine workflow สำคัญกว่าที่คิด · retrofit (A5) เผยว่า dual-authority ใช้จริงไม่ได้
