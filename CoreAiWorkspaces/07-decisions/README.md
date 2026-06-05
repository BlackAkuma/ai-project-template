<!-- AI-CONTEXT
total_adrs: 9
accepted: [ADR-001,ADR-002,ADR-003,ADR-004,ADR-005]
proposed: [ADR-006,ADR-007,ADR-008,ADR-009]
last_updated: 2026-06-05
note: ADR-006..009 = Stage-2 direction, await human approval (ADR Proposed → STOP per protocol)
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
| ADR-006 | Stage 2 direction — "Governed Project Memory" | Proposed | 2026-06-05 | — |
| ADR-007 | Dual-Authority Canonical Model | Proposed | 2026-06-05 | — |
| ADR-008 | Risk-Tiered Governance (not uniform gates) | Proposed | 2026-06-05 | — |
| ADR-009 | Schema Architecture — CORE + PROFILE | Proposed | 2026-06-05 | — |

## ⏳ Proposed — รอ human approve (Stage 2)

ADR-006..009 เป็นทิศทาง Stage 2 ตกผลึกจาก session วิเคราะห์ Odysseus (2026-06-05)
ตาม protocol: **ADR Proposed → STOP รอ human Approve ก่อน implement** — ห้ามเริ่ม Engine/Shell จนกว่า ADR-006 ถูก Accept
รายละเอียดเต็ม: `exploration/` (north-star-vision, what-it-should-be, master-plan)
