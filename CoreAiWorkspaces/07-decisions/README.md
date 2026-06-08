<!-- AI-CONTEXT
total_adrs: 13
accepted: [ADR-001,ADR-002,ADR-003,ADR-004,ADR-005,ADR-006,ADR-007,ADR-008,ADR-009,ADR-010,ADR-011,ADR-012,ADR-013]
proposed: []
last_updated: 2026-06-07
note: ADR-006..009 Accepted 2026-06-05 via 3-lens panel (2/3 rule); 008+009 revised per contrarian FAIL before accept
review_method: adr-review-panel workflow (see way-of-work)
-->

# Decision Log — ai-project-template

บันทึก architectural decisions ทั้งหมดของโปรเจ็กต์
ADR ที่ถูก accept แล้วถือเป็น source of truth สำหรับทิศทาง technical

## กฎการใช้งาน

- AI ทุก session ต้องอ่าน index นี้ก่อนทำการตัดสินใจเชิง architecture
- ห้ามลบ ADR — เปลี่ยนสถานะเป็น Deprecated หรือ Superseded แทน
- AI สามารถสร้าง ADR ในสถานะ Proposed ได้ — มนุษย์เป็นผู้ Approve

## Status ที่ใช้ได้

| Status | ความหมาย |
|--------|----------|
| Proposed | เสนอโดย AI หรือทีม รอการ approve |
| Accepted | ตัดสินใจแล้ว ใช้เป็นแนวทาง |
| Deprecated | ไม่ใช้แล้ว แต่ยังมีประวัติ |
| Superseded | ถูกแทนที่โดย ADR อื่น |

## Decision Log

| ID | Title | Status | Date | Supersedes |
|----|-------|--------|------|------------|
| ADR-001 | เลือก CoreAiWorkspaces/ เป็นชื่อ AI working folder (ไม่ใช่ doc/) | Accepted | 2026-05-07 | — |
| ADR-002 | MemPalace เป็น Phase 3 vector memory implementation | Accepted | 2026-05-07 | — |
| ADR-003 | docs/ web pages อยู่บน gh-pages branch เท่านั้น | Accepted | 2026-05-07 | — |
| ADR-004 | Versioning strategy — single release + layer separation | Accepted | 2026-05-08 | — |
| ADR-005 | Token-Aware Communication Protocol (TACP) | Accepted | 2026-05-08 | — |
| ADR-006 | Stage 2 direction — "Governed Project Memory" | Accepted | 2026-06-05 | — |
| ADR-007 | Dual-Authority Canonical Model | Accepted | 2026-06-05 | — |
| ADR-008 | Risk-Tiered Governance (not uniform gates) | Accepted | 2026-06-05 | — |
| ADR-009 | Schema Architecture — CORE + PROFILE | Accepted | 2026-06-05 | — |
| ADR-010 | BRD v1.0 Accepted (Governed Project Memory) | Accepted | 2026-06-05 | — |
| ADR-011 | G1 Decision — C-conservative (soft-ship + protect P3) | Accepted | 2026-06-06 | — |
| ADR-012 | G3 Decision — JSON-in-git canonical + deferred index | Accepted | 2026-06-07 | finalizes ADR-007 store |
| ADR-013 | G4 Decision — harvest demand first (gate Shell on WTP) | Accepted | 2026-06-07 | — |

## ✅ Stage 2 — Accepted 2026-06-05 (via 3-lens panel)

ADR-006..009 ผ่าน **adr-review-panel** (3 reviewer/ADR, กติกา 2/3):
- 006, 007 → 3/3 PASS (สะอาด)
- 008, 009 → 2/3 PASS (contrarian FAIL มีมูล → revise แก้ต้นเหตุก่อน Accept)
- ดู "Panel Review Record" ท้ายแต่ละ ADR (โหวต + dissent + การตัดสิน)

⚠️ **Carry-over tasks (กระทบ core ที่ ship แล้ว — รอ project review round):**
- T-051: re-publish Scenario A–N → new risk-Level mapping (core/11)
- T-052: rewrite CLAUDE.md uniform challenge-necessity → risk-tiered (ADR-008)
- T-053: invert C-07 resolution (block wins for enforceable-state) (ADR-007)

รายละเอียดเต็ม: `exploration/` (north-star-vision, what-it-should-be, master-plan)
