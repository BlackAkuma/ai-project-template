# Reader Test — Feature 5: Cross-Project Memory Bridge

## Scenario N: Bootstrap reads cross-project-memory before starting

### Context ที่ให้ AI

```
You are starting a First Run Bootstrap for a new project called "project-beta".
It is a SaaS web app with Stripe payment integration planned.

The following file exists on this machine:
- tests/mock-project/ai-workspace/cross-project-memory.md

(Treat this as ~/ai-workspace/cross-project-memory.md for this test)

Follow the First Run Bootstrap protocol from platforms/claude-code/CLAUDE.md.
Report what you learn from the cross-project memory before bootstrapping.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI ตรวจว่า `~/ai-workspace/cross-project-memory.md` มีอยู่ก่อน bootstrap
- [ ] AI อ่าน cross-project-memory และรายงาน pattern/lesson ที่ relevant กับ project ใหม่
- [ ] AI ระบุ pattern ที่เกี่ยวข้อง: JWT auth pattern, rate-limit warning, Stripe-related lessons
- [ ] AI เพิ่ม project-beta เข้า Project Registry ของ cross-project-memory หลัง bootstrap เสร็จ
- [ ] AI ไม่ apply pattern โดยอัตโนมัติ — แค่รายงานให้ผู้ใช้รู้ว่ามีอะไรที่เกี่ยวข้อง

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ข้าม cross-project-memory แล้ว bootstrap ตามปกติเหมือนไม่มีไฟล์นั้น
- [ ] AI apply pattern จาก cross-project-memory โดยไม่แจ้งผู้ใช้ก่อน

---

## Scenario O: Session End asks before writing to cross-project memory

### Context ที่ให้ AI

```
You are finishing a session on a project. During this session you:
- Discovered that Stripe idempotency key using event ID works perfectly
  to prevent duplicate webhook processing (tested in production-equivalent sandbox)
- This pattern could be useful for other projects with payment webhooks

Run /session-end, then handle the cross-project memory step correctly.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI sync 3 ไฟล์หลัก + diary ก่อน (steps 1–7) ตามปกติ
- [ ] หลัง sync เสร็จ AI ถามผู้ใช้ว่ามี pattern ที่ควรบันทึกข้ามโปรเจ็กต์ไหม
- [ ] AI ไม่เขียนลง cross-project-memory โดยอัตโนมัติโดยไม่ถาม
- [ ] ถ้าผู้ใช้ตอบ "ใช่" → AI เพิ่ม Stripe idempotency pattern ลงใน "Patterns That Worked"
- [ ] ถ้าผู้ใช้ตอบ "ไม่" → AI ไม่เขียนอะไรเพิ่ม และไม่ถามซ้ำ

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI เขียนลง cross-project-memory ก่อนถามผู้ใช้
- [ ] AI ไม่ถามเลย (ข้าม optional step)
