# Launch Checklist Template

ใช้ก่อน deploy หรือ release ทุกครั้ง
คัดลอกและปรับเป็น `CoreAiWorkspaces/01-plan/launch-checklist.md`

ทำร่วมกับมนุษย์ — AI ตรวจและรายงาน มนุษย์เป็นผู้ approve ก่อน deploy

---

## หมวด 1 — Code & Quality

- [ ] Compliance scan ผ่านทั้งหมด (ไม่มี Level 1 violation)
- [ ] ไม่มี C-11 security issue ค้าง
- [ ] REFACTOR-PENDING ทั้งหมดมี task ใน board (ไม่ได้หายไป)
- [ ] ไม่มี `<NEEDS_CLARIFICATION>` placeholder ค้างในโค้ด
- [ ] ไม่มี hardcoded config value ที่ต้องแตกต่างระหว่าง environment

## หมวด 2 — Documentation

- [ ] work-status สะท้อน phase ปัจจุบันถูกต้อง
- [ ] task-board: ทุก task ที่ scope นี้อยู่ใน `done` หรือ `blocked` พร้อมเหตุผล
- [ ] ADR index ครบ — ทุก architectural decision ที่ทำใน milestone นี้มีบันทึก
- [ ] CHANGELOG หรือ release note เขียนแล้ว (ถ้าโปรเจ็กต์ต้องการ)

## หมวด 3 — Testing

- [ ] Test suite ผ่านทั้งหมดบน environment เป้าหมาย
- [ ] Manual smoke test บน environment เป้าหมายแล้ว
- [ ] Regression: feature เดิมที่ไม่ได้แก้ยังทำงานได้
- [ ] ทดสอบ edge cases ที่ระบุใน source docs แล้ว

## หมวด 4 — Environment & Config

- [ ] Environment variables / config ครบสำหรับ production
- [ ] ไม่มี debug flag หรือ test data รั่วไปใน production build
- [ ] Database migration (ถ้ามี) ทดสอบบน staging แล้ว
- [ ] Rollback plan มีและทดสอบแล้ว (ถ้า high-risk)

## หมวด 5 — สำหรับ Game Projects (ถ้าเกี่ยวข้อง)

- [ ] Playtest report สำหรับ milestone นี้มีแล้ว
- [ ] Balance check ผ่าน (ค่าตัวเลขอยู่ใน range ที่ FDD กำหนด)
- [ ] Asset registry ครบ — ไม่มี asset ที่ใช้แต่ไม่ได้ลงทะเบียน
- [ ] Performance budget ผ่าน (FPS target ตาม FDD)
- [ ] ทดสอบบน platform เป้าหมายจริงแล้ว (mobile / web / desktop)

---

## วิธีใช้

```
1. AI รัน checklist นี้ก่อน milestone ปิด
2. report ผลในรูปแบบ:
   PASS ✓ / FAIL ✗ / SKIP (ไม่เกี่ยวกับโปรเจ็กต์นี้)
3. ทุก FAIL ต้องมี task ใน board ก่อน deploy
4. Human approve checklist ก่อน deploy จริง
```

## Report Format

```
=== Launch Checklist — <PROJECT_NAME> v<VERSION> — YYYY-MM-DD ===

หมวด 1 — Code & Quality
  ✓ Compliance scan: PASS
  ✓ Security C-11: PASS
  ✗ REFACTOR-PENDING: T-042 ยังไม่มีใน board → สร้างแล้ว

หมวด 2 — Documentation
  ✓ work-status: current
  ✓ task-board: scope complete
  ✗ ADR: architecture-decision ของ session นี้ยังไม่มี ADR

หมวด 3 — Testing
  ✓ Test suite: PASS
  ✓ Smoke test: PASS

สรุป: 2 รายการต้องแก้ก่อน deploy — T-042, ADR-XXX
```
