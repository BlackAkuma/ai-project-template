<!-- AI-CONTEXT
total_adrs: 0
accepted: []
proposed: []
last_updated: 2026-04-30
-->

# Decision Log — ShopFlow

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
| *(ยังไม่มี ADR — สร้างด้วย /adr-create)* | | | | |
