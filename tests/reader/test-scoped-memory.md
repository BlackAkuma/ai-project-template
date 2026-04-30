# Reader Test — Scoped Memory Map: read_more Protocol

## Scenario SM-1: AI เลือก path ที่เกี่ยวข้อง ไม่เปิดทั้งหมด

### Context ที่ให้ AI

```
You are starting a session. work-status.md AI-CONTEXT block says:

  phase: payment_integration
  active_task: T-018 (Stripe webhook handler)
  blocker: none
  read_more:
    - doc/00-source/versions/v1.2/payment-spec.md      ← payment details
    - doc/07-decisions/ADR-003-stripe-integration.md   ← why Stripe
    - doc/07-decisions/ADR-004-webhook-security.md     ← security decisions
    - doc/04-way-of-work/coding-standards.md            ← code style
    - doc/05-summary/2024/05/2024-05-summary.md        ← monthly summary

Your task is to implement the Stripe webhook handler for T-018.
Which read_more paths do you open, and why?
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI เปิด `payment-spec.md` — เพราะเกี่ยวกับ T-018 โดยตรง
- [ ] AI เปิด `ADR-003-stripe-integration.md` — เพราะเป็น architectural decision เกี่ยวกับ Stripe
- [ ] AI เปิด `ADR-004-webhook-security.md` — เพราะเกี่ยวกับ security ของ webhook
- [ ] AI ให้เหตุผลชัดเจนว่าเปิดแต่ละ path เพราะอะไร
- [ ] AI ไม่เปิด `coding-standards.md` ทันที (อ่านเมื่อต้องการ style check เท่านั้น)
- [ ] AI ไม่เปิด monthly summary (ไม่เกี่ยวกับ task ปัจจุบัน)

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI เปิดทุก path ใน read_more โดยไม่คัดเลือก
- [ ] AI ไม่เปิด path ใดเลย และ implement โดยเดา
- [ ] AI เปิด coding-standards ก่อน payment-spec (ผิดลำดับความสำคัญ)

---

## Scenario SM-2: read_more ว่าง — AI orient จาก AI-CONTEXT เท่านั้น

### Context ที่ให้ AI

```
work-status.md AI-CONTEXT block:

  phase: ui_polish
  active_task: T-022 (Fix button alignment on mobile)
  blocker: none
  read_more: []

task-board shows T-022:
  description: "Button in checkout page misaligned on iPhone SE (375px width)"
  source_ref: doc/00-source/versions/v1.1/ui-spec.md#section-3

Start the session and proceed with T-022.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI เริ่มงานได้ทันที ไม่ถามว่า "ต้องอ่านไฟล์อะไรเพิ่ม?"
- [ ] AI ระบุว่า `read_more` ว่าง แปลว่า AI-CONTEXT ให้ context พอแล้ว
- [ ] AI ใช้ `source_ref` จาก task-board เพื่อดู spec ของ button alignment
- [ ] AI อธิบาย plan สำหรับ T-022 ก่อน implement

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI หยุดรอและถามว่า "ต้องอ่านไฟล์เพิ่มไหม?" ทั้งที่ read_more ว่าง
- [ ] AI implement โดยไม่ดู source_ref ใน task
