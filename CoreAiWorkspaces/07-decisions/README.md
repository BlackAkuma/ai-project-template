<!-- AI-CONTEXT
total_adrs: 3
accepted: [ADR-001,ADR-002,ADR-003]
proposed: []
last_updated: 2026-05-07
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
