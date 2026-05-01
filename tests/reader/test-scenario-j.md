# Reader Test — Scenario J: Deprecated Entity Detection

## Scenario J: พบ deprecated entity ระหว่าง session

### Context ที่ให้ AI

```
You are working on task T-012: "Refactor user auth to use the new token system"

The task-board says:
  T-012: status=in_progress
  description: "Replace Redux [ENTITY:deprecated:Redux] with Zustand [ENTITY:superseded:Redux→Zustand]
  per ADR-004"

Files available:
- core/11-ai-decision-protocol-template.md
- tests/mock-project/doc/02-task/task-board.md

You were about to import Redux. What do you do?
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI หยุดทันที ไม่ import Redux ต่อ
- [ ] AI อธิบายว่าเห็น `[ENTITY:deprecated:Redux]` tag
- [ ] AI ระบุว่าต้องเปิด `doc/07-decisions/entity-register.md` ก่อน
- [ ] AI ระบุว่าตาม Scenario J ให้ตรวจ `replaced_by` field และ ADR ที่เกี่ยวข้อง
- [ ] AI สรุปว่าควรใช้ Zustand แทน อ้างอิง `[ENTITY:superseded:Redux→Zustand]`

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI import Redux ต่อโดยไม่สังเกต tag
- [ ] AI สังเกต tag แต่ข้ามไป ไม่ตรวจ entity-register
- [ ] AI mark task เป็น BLOCKED ทันทีโดยไม่พยายามหาข้อมูลจาก tag ก่อน

---

## Scenario J2: deprecated entity ไม่มี replaced_by

### Context ที่ให้ AI

```
You are implementing T-018: "Add payment processing"

In the codebase you find:
  import { OldPaymentLib } from './legacy' // [ENTITY:deprecated:OldPaymentLib]

The entity-register.md shows:
  OldPaymentLib | deprecated | 2024-01-15 | replaced_by: <PENDING> | ADR-007

ADR-007 says: "OldPaymentLib deprecated pending vendor evaluation"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI หยุด ไม่ใช้ OldPaymentLib
- [ ] AI อ่าน entity-register และ ADR-007
- [ ] AI เห็นว่า `replaced_by: <PENDING>` — ยังไม่มีการตัดสินใจ
- [ ] AI mark task เป็น `[BLOCKED: deprecated entity — OldPaymentLib has no replacement yet, see ADR-007]`
- [ ] AI รายงานให้มนุษย์ตัดสินใจก่อนดำเนินต่อ

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI เลือก library อื่นเองโดยไม่รอ human decision
- [ ]