# Entity Register Template

คัดลอกและปรับไฟล์นี้เป็น `doc/07-decisions/entity-register.md`

Entity Register คือ snapshot ของ "สิ่งสำคัญ" ในโปรเจ็กต์ — tech choices, integrations, patterns, people —
พร้อม status ปัจจุบันและช่วงเวลาที่ใช้งาน
ช่วยให้ AI ทุก session รู้ว่า entity ไหน active ไหน deprecated โดยไม่ต้องอ่าน ADR ทั้งหมด

**กฎสำคัญ:**
- เมื่อเพิ่ม tech ใหม่ → เพิ่ม entity พร้อม ADR reference
- เมื่อเลิกใช้ tech → อัปเดต status เป็น `deprecated` + ใส่ `until` date
- เมื่อ entity ถูกแทนที่ → ใส่ `notes: superseded by [entity ใหม่]`
- ห้ามลบ row — ประวัติต้องอยู่ครบ

---

## Template ไฟล์จริง

```md
<!-- AI-CONTEXT
entities_active: [<ENTITY_1>, <ENTITY_2>]
entities_deprecated: [<ENTITY_3>]
last_updated: <CURRENT_DATE>
-->

---

# Entity Register — <PROJECT_NAME>

อัปเดตล่าสุด: <CURRENT_DATE>

## Active Entities

| Entity | Type | Status | Since | ADR | Notes |
|--------|------|--------|-------|-----|-------|
| <ENTITY_NAME> | <TYPE> | active | <YYYY-MM> | <ADR-XXX> | <คำอธิบายสั้น> |

## Deprecated / Removed Entities

| Entity | Type | Status | Since | Until | ADR | Replaced By |
|--------|------|--------|-------|-------|-----|-------------|
| <ENTITY_NAME> | <TYPE> | deprecated | <YYYY-MM> | <YYYY-MM> | <ADR-XXX> | <entity ใหม่ หรือ —> |
```

---

## ประเภท Entity (Type)

| Type | ความหมาย | ตัวอย่าง |
|------|----------|---------|
| `tech` | เทคโนโลยีหรือ framework | React, PostgreSQL, Redis |
| `integration` | บริการภายนอก | Stripe, SendGrid, AWS S3 |
| `pattern` | รูปแบบการออกแบบที่ตัดสินใจใช้ | event-sourcing, CQRS, JWT auth |
| `dependency` | library หรือ package สำคัญ | lodash, zod, prisma |
| `person` | คนในทีมหรือ stakeholder | product owner, lead dev |
| `service` | internal service หรือ microservice | auth-service, payment-service |

---

## ตัวอย่างที่กรอกแล้ว

```md
<!-- AI-CONTEXT
entities_active: [PostgreSQL, Redis, Stripe, JWT]
entities_deprecated: [MongoDB, Redux]
last_updated: 2026-04-29
-->

# Entity Register — my-app

## Active Entities

| Entity | Type | Status | Since | ADR | Notes |
|--------|------|--------|-------|-----|-------|
| PostgreSQL | tech | active | 2026-01 | ADR-001 | primary database |
| Redis | tech | active | 2026-02 | ADR-004 | session cache only |
| Stripe | integration | active | 2026-02 | ADR-003 | payments, sandbox mode |
| JWT | pattern | active | 2026-01 | ADR-002 | access + refresh token rotation |

## Deprecated / Removed Entities

| Entity | Type | Status | Since | Until | ADR | Replaced By |
|--------|------|--------|-------|-------|-----|-------------|
| MongoDB | tech | deprecated | 2025-11 | 2026-01 | ADR-001 | PostgreSQL |
| Redux | dependency | deprecated | 2025-06 | 2026-03 | ADR-005 | Zustand |
```

---

## กฎ AI ที่ต้องปฏิบัติ

1. **ก่อน implement feature ใหม่** → ตรวจ entity-register ว่า tech ที่จะใช้ยัง active อยู่ไหม
2. **เมื่อเจอ `[ENTITY:deprecated:X]` tag ใน code หรือ doc** → ตรวจ entity-register ก่อนอ้างถึง X
3. **เมื่อ ADR ใหม่ถูก accept** → อัปเดต entity-register พร้อมกัน
4. **เมื่อ task deprecate tech ใด** → อัปเดต entity-register ใน session นั้นเลย อย่ารอ
