# Flow Plan — Granular Execution + Gate Policy

**Date:** 2026-06-05
**Branch:** `explore/odysseus-analysis`
**Status:** ✅ Refines `master-plan.md` (execution view) — แก้ปัญหา "หยุดบ่อย/phase ใหญ่เกิน"
**Trigger:** feedback — plan ใหญ่เกิน + AI gate ระแวงเกิน → loop ไม่ลื่น

> master-plan = WHAT (phases/strategy) · flow-plan = HOW to flow (micro-tasks + gate policy)

---

## 1. วิเคราะห์: ทำไม loop ไม่ลื่น (root cause)

| อาการ | สาเหตุจริง | แก้ |
|-------|-----------|-----|
| ผมหยุดที่ "build threshold" ทุกที | **phase ใหญ่เกิน** — P1 = 3-5 วันเป็นก้อนเดียว ดูเหมือน commitment ใหญ่ | decompose เป็น micro-task (≤0.5 วัน/ชิ้น) ที่ chain กัน |
| รู้สึกต้องขออนุมัติบ่อย | **gate ระแวงเกิน** — เหมา "safe/reversible work" = "ต้อง gate" | flow-gate policy 3 tier ชัด (ด้านล่าง) |
| ไม่ครอบคลุม | loose ends กระจาย (T-044b, T-051..053, T-057 apply, T-058) ไม่อยู่ใน flow เดียว | รวมเข้า backlog เดียว เรียงลำดับ |
| ไม่รู้เมื่อไหร่ flow เมื่อไหร่หยุด | gate ไม่มีนิยาม operational | นิยาม STOP ให้แคบและชัด |

**หลักใหม่:** *default = FLOW* — หยุดเฉพาะเมื่อเข้าเงื่อนไข STOP ที่นิยามไว้เท่านั้น

---

## 2. Flow-Gate Policy (3 tier — นิยาม operational)

### 🟢 FLOW — ทำต่อเนื่อง ไม่หยุด ไม่ถาม
- design docs / spec / schema (paper)
- ไฟล์ใหม่ (additive)
- code ที่ไม่กระทบ prod behavior (validator, CLI, predicate, test) — dogfood บน repo นี้
- แก้ tracking (CoreAiWorkspaces)
- → **ทำ + log ใน work-log เท่านั้น**

### 🟡 LOG-ONLY — ทำเอง + log ชัด ไม่หยุด (แต่บันทึกการตัดสิน)
- แก้ shipped template ที่เป็น *correction* (ไม่ใช่ reversal) — เช่น typo, count, missing ref, additive field
- decision เล็กที่มี default ชัด → เลือก default + log เหตุผล

### 🔴 STOP — หยุด รอ human (gate จริงเท่านั้น)
- **irreversible** ที่ rollback แพง (G3: SQLite vs JSON store)
- **reverse shipped behavior** — แก้กฎ/พฤติกรรมที่ ship แล้ว (T-052 uniform-gate, T-053 C-07)
- **strategic fork** — G1 (หยุดที่ Engine-CLI?), G4 (build Shell?)
- security / prod / destructive / requirement change
- ADR ใหม่ → Scenario O panel (auto, ไม่ใช่ human ก่อน)

> ที่ผ่านมาผมหยุดผิดที่: P1 (generalize hook) = 🟢 FLOW ไม่ใช่กำแพง · T-057 apply = 🟡 LOG-ONLY (additive field)

---

## 3. Granular Backlog → MVW (P2 governance linter)

decompose เป็น micro-task ที่ chain ลื่น (แต่ละชิ้น ≤0.5 วัน, มี done-criteria, dogfood ได้ทันที)

### Stage A — ปิดให้จบ (🟢 FLOW)
| ID | task | done เมื่อ |
|----|------|-----------|
| T-049 | retrofit schema กับ domain ห่าง (research + industrial) | mapping ผ่าน/เจอ gap → log |
| T-058 | game playtest → sub-gate (เลือกแบบแกนคงที่) ใน A1 + note | A1 + game profile spec ตรงกัน |

### T-057 apply — unified work-status schema (🟡 LOG-ONLY, additive)
| ID | task | done |
|----|------|------|
| T-057a | apply unified field set → `core/06` template (additive + rename ใน template) | core/06 ตรง A1 §3 |
| T-057b | apply → live `work-status.md` (rename field) | ไฟล์จริงตรง schema |
| T-057c | normalize list delimiter `[a, b]` ทุก state file | ไม่มี space-list |

### P1 — config-driven validator (🟢 FLOW, dogfood)
| ID | task | done |
|----|------|------|
| P1-1 | นิยาม gate YAML grammar (`gates/*.yaml`: trigger/predicate/effect/risk) | schema + 1 ตัวอย่าง |
| P1-2 | predicate resolver lib (Python) — 4 ตัวแรก: `file_exists`, `git_diff_contains`, `placeholder_absent`, `secret_absent` | unit test ผ่าน |
| P1-3 | wire `validate-commit.sh` → อ่าน gate YAML (1 check) | hook รัน YAML check ได้ |
| P1-4 | migrate check เดิม → YAML (placeholder, secret, doc-sync, prototype) | hook เก่า logic = YAML |
| P1-5 | snapshot test parity (good/bad staged diff) | parity ผ่าน → ลบ inline เก่า |

### P2 — CLI evaluator + risk-tier (🟢 FLOW, → MVW)
| ID | task | done |
|----|------|------|
| P2-1 | `engine check <gate>` CLI skeleton (อ่าน gate, return verdict) | รันได้ exit code |
| P2-2 | predicate vocabulary +4: `field_in_block`, `evidence_count_gte`, `status_equals`, `block_matches_body` | test ผ่าน |
| P2-3 | challenge-necessity JSON-schema validator (presence-only) | broken challenge ถูกจับ |
| P2-4 | risk-tier routing — verdict carry Level 0-3 → effect | tier ถูกใน output |
| P2-5 | CI integration — `engine check` ทุก PR repo นี้ | CI จับ broken state |
| **G1** 🔴 | **STOP: หยุดที่ Engine-CLI (ship linter) หรือไป P3?** | human decide |

→ **ถึง P2-5 = MVW (governance linter ship ได้)** โดย FLOW ตลอด ไม่หยุดจน G1

### Carry-over (🔴 STOP — whole-project review batch)
T-051 (mapping), T-052 (CLAUDE.md uniform→tiered), T-053 (C-07 invert), T-044b (run-audit rename) — รวมทำรอบเดียวใน review (กระทบ shipped)

---

## 4. ผลของ re-plan

- **default FLOW** → loop ไหลจาก T-049 → T-058 → T-057a/b/c → P1-1..5 → P2-1..5 โดยไม่หยุด
- หยุดจริงแค่ **G1** (หลัง MVW) + carry-over batch (review)
- ทุก micro-task dogfood + log → ตรวจสอบซ้ำได้ระหว่างทาง
- master-plan coarse phase ยังใช้เป็น strategy map; flow-plan = execution

---

*refines master-plan.md · แก้ root cause: phase ใหญ่ + gate ระแวง → micro-task + flow-first policy*
