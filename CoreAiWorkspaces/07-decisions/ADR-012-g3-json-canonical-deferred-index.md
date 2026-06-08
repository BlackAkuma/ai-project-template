# ADR-012: G3 Decision — JSON-in-git canonical + deferred SQLite index (C-deferred)

**Date:** 2026-06-07
**Status:** Accepted
**Author:** User decision + G3 panel (technical/strategic/contrarian + marketing)
**Related:** BRD OD-1/G3, NFR-2, NFR-4, ADR-007 (dual-authority)
**Resolves:** Open Decision OD-1 (canonical store: SQLite vs JSON-in-git)
**Supersedes/finalizes:** ADR-007 store-side ("structured=truth" → truth lives as JSON-in-git)

## Context

P4 ต้องการ canonical store ที่ prose-views generate จาก (ADR-007 dual-authority). G3 = fork สถาปัตยกรรมที่ลึกสุด (master-plan). ตัวเลือก: A SQLite / B JSON-in-git / C hybrid

## G3 Panel (2/3 + marketing)

| lens | vote | conf | core |
|------|------|------|------|
| technical | C | .74 | A ตัดทิ้ง (binary ทำลาย sovereignty); single-writer Engine ทำ SQLite lock ไร้ค่า; index=CQRS read-only rebuildable |
| strategic | C | .68 | moat=git-native diffable truth; C ได้ sovereign+fast |
| **contrarian** | **B** | .72 | C=premature complexity (2-store drift = ปัญหาที่โปรเจ็กต์เกิดมาเพื่อกำจัด); B=least fatal, defer index |
| marketing | C | — | "C target, B=de-risked MVP ไม่เสีย positioning; index เพิ่มทีหลังไม่ต้อง reposition" |

**tally A0 B1 C2 → C** · **converge เอกฉันท์:** A ตัดทิ้ง · JSON-in-git=truth ship now · SQLite index defer

## Decision

**C-deferred** (เลือกโดย user — จุด converge ของทุกฝ่าย):
- **JSON-in-git = canonical truth, FINAL** — ship ที่ P4 (= B's substrate); match events.py (append-only JSONL hash-chain ที่ proven)
- **SQLite derived read-index = documented future-target, DEFERRED** — build เฉพาะเมื่อ query pain จริง (P8/P9 เกิน NFR-8 ≤200ms บน JSONL scan); ถ้าไม่เกิดเลย → collapse เป็น B ที่ cost 0
- **NFR-2 git-native diffable = FINAL** (เลิก provisional)

## Consequences

- next build = **P4 JSON-in-git canonical store** + render prose views (ADR-007); reuse events.py shape
- **invariants (lock):** gate/enforcement predicate อ่าน JSON/log truth เท่านั้น ไม่อ่าน index · index (เมื่อ build) = strictly read-only, rebuildable-from-git, keyed กับ event hash · CI test "wipe+rebuild from git = identical state" · JSON มี schema_version (NFR-7 additive-only)
- **escape hatch:** re-open G3 → graduate เป็น C-full (add index) ถ้า JSONL scan เกิน 200ms หรือ P8 เกิด concurrent writer (breach NFR-4)
- **contrarian-B dissent (บันทึก, ไม่ override เงียบ):** 2-store drift = correctness trap → mitigated โดย defer (ไม่ build ตอนนี้) + read-only + CI rebuild test + predicate อ่าน truth เท่านั้น

## Review Trigger

reopen ถ้า: JSONL scan เกิน NFR-8 (→ build index) · P8 ต้องการ concurrent writer (NFR-4 breach) · JSON blob churny ทำลาย diffability (→ A competitive)
