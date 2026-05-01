# Reader Test — Entity Register: Bootstrap & Maintenance

## Scenario ER-1: Bootstrap สร้าง entity-register.md

### Context ที่ให้ AI

```
You are bootstrapping a new project called "ShopFlow" (e-commerce web app).

Tech stack confirmed:
- Next.js 14 (frontend framework) — ADR-001
- Supabase (database + auth) — ADR-002
- Vercel (deployment) — no ADR yet
- date-fns (date utilities) — no ADR yet
- Moment.js — was used in prototype, now deprecated in favor of date-fns — no ADR yet

Create doc/07-decisions/entity-register.md following core/17-entity-register-template.md
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] ไฟล์มี AI-CONTEXT block ที่ถูกต้อง (active_count, deprecated_count, last_updated)
- [ ] Next.js และ Supabase อยู่ใน Active Entities พร้อม ADR reference (ADR-001, ADR-002)
- [ ] Vercel และ date-fns อยู่ใน Active Entities แต่ ADR column แสดง `—` ไม่ใช่ blank
- [ ] Moment.js อยู่ใน Deprecated Entities พร้อม `replaced_by: date-fns`
- [ ] Moment.js มี `until` date (bootstrap date หรือ estimated)
- [ ] ไม่มี row ใดที่ทุก column ว่างเปล่าหมด

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ใส่ ADR reference ว่าง (blank) — ต้องใส่ `—` แทน
- [ ] AI ไม่ใส่ Moment.js ใน deprecated (เพราะ "ไม่มี ADR")
- [ ] AI สร้างไฟล์โดยไม่มี AI-CONTEXT block

---

## Scenario ER-2: อัปเดต entity-register หลัง ADR ถูก Accept

### Context ที่ให้ AI

```
ADR-003 ได้รับการ Accept แล้ว: "Use Stripe for payment processing"
ADR-004 ได้รับการ Accept แล้ว: "Deprecate custom payment module in favor of Stripe"

Current entity-register.md has:
- Stripe: not listed yet
- custom-payment-module: listed as Active

Update entity-register.md according to Scenario K in ai-decision-protocol.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] Stripe ถูกเพิ่มใน Active Entities พร้อม ADR-003 reference
- [ ] custom-payment-module ถูกย้ายจาก Active ไป Deprecated พร้อม `replaced_by: Stripe` และ ADR-004
- [ ] AI-CONTEXT block ถูกอัปเดต: active_count เพิ่ม 1, deprecated_count เพิ่ม 1
- [ ] บันทึกใน work-log ว่า "Updated entity-register per ADR-003 and ADR-004"

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ลบ row ของ custom-payment-module แทนที่จะย้ายไป Deprecated
- [ ] AI อัปเดต body แต่ลืมอัปเดต AI-CONTEXT b