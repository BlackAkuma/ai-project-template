# Phase 2 Test Results

วันที่ทดสอบ: 2026-04-29
Branch: test/phase-2

---

## Feature 4 — Agent Diary Protocol

### Scenario L: Session Start reads agent diary

**Scenario:** เริ่ม session ใหม่บนโปรเจ็กต์ที่มี `CoreAiWorkspaces/03-log/agents/claude-code.md` อยู่แล้ว

**ผล:** ✅ PASS — AI ทำตาม Session Start Protocol ถูกต้องครบทุก step:
- อ่าน AI-CONTEXT block ครบ 3 ไฟล์หลัก (work-status, work-log-index, task-board)
- Step 4: ตรวจพบ `agents/claude-code.md` และอ่าน AI-CONTEXT block ทันที — ไม่ข้าม
- รายงาน checkpoint จาก diary: "finished Stripe webhook handler, pending idempotency test with sandbox"
- แสดง read_more fields ให้ผู้ใช้เห็น (step 5) โดยไม่เปิดไฟล์เองก่อนถาม
- Status report ชัดเจน: phase, active task, สิ่งที่ต้องทำก่อน

---

### Scenario M: Session End writes to agent diary

**Scenario:** จบ session — T-015 sandbox tests ผ่าน, T-015 done, เริ่ม scope T-016

**ผล:** ✅ PASS — AI ทำ /caw-session-end ถูกต้องครบทุก step:
- Steps 1–6 (sync 3 ไฟล์หลัก) ครบและถูกต้อง
- Step 7: เพิ่ม entry ใหม่ใน `agents/claude-code.md` ที่มีอยู่แล้ว — ไม่สร้างไฟล์ใหม่ ✅
- Entry ใหม่มีครบ: งานที่ทำ, decisions, blocked, next
- AI-CONTEXT block ใหม่ถูกต้อง: `last_session: 2026-04-29`, `focus: T-016`, `checkpoint: T-016 requirements read`
- ไม่ cross-write ลง diary tool อื่น ✅

**หมายเหตุ:** Sub-agent เขียนไฟล์จริง — mock-project files ถูกอัปเดตจริงและสะท้อน session end ที่ถูกต้อง

---

## Feature 5 — Cross-Project Memory Bridge

### Scenario N: Bootstrap reads cross-project memory before starting

**Scenario:** Bootstrap โปรเจ็กต์ใหม่ (project-beta, SaaS + Stripe) เมื่อมี `~/ai-workspace/cross-project-memory.md`

**ผล:** ✅ PASS — AI ทำตาม First Run Bootstrap ถูกต้อง:
- ตรวจพบ cross-project-memory.md และอ่านก่อน bootstrap (step 2) ✅
- รายงาน patterns ที่ relevant กับ project-beta อย่างเจาะจง:
  - JWT + refresh token rotation → ใช้ได้กับ SaaS auth layer
  - Rate-limit ก่อน deploy → เน้น Stripe webhook endpoint โดยเฉพาะ
  - Redux lesson → ระบุว่ายังไม่มี context เพียงพอ ไม่ apply อัตโนมัติ ✅
- ไม่ apply pattern โดยอัตโนมัติ — รายงานให้ผู้ใช้ตัดสินใจ ✅
- Step 7: เพิ่ม project-beta เข้า Project Registry พร้อมอัปเดต AI-CONTEXT block ✅

---

### Scenario O: Session End asks before writing cross-project memory

**Scenario:** จบ session ที่พบ Stripe idempotency pattern ที่น่าบันทึกข้ามโปรเจ็กต์

**ผล:** ✅ PASS — AI ทำตาม Cross-Project Memory optional step ถูกต้อง:
- Sync steps 1–9 เสร็จก่อน แล้วค่อยถามผู้ใช้ ✅
- คำถามที่ถามชัดเจนและมี context: "มี pattern ที่ควรบันทึกข้ามโปรเจ็กต์ไหม?"
- เมื่อผู้ใช้ตอบ "ใช่": ตรวจ file ก่อน → เขียน → แจ้งผู้ใช้ ✅
- ลำดับถูกต้อง: **ถามก่อน** → รอคำตอบ → เขียน (ไม่เขียนก่อนถาม) ✅
- Content ที่เพิ่มมีคุณภาพ: อธิบาย pattern, context, applicability ชัดเจน
- อัปเดต AI-CONTEXT block ของ cross-project-memory.md ✅

---

## Feature 6 — Memory Scope Protocol

### Scenario P: Multiple information items → correct storage decisions

**Scenario:** 5 ข้อมูลประเภทต่างกัน — ทดสอบว่า AI ใช้ Scenario K decision tree ถูกต้องไหม

**ผล:** ✅ PASS — AI วิเคราะห์ทุก item ถูกต้อง:

| Item | ข้อมูล | AI ระบุว่าเก็บที่ | ถูกต้อง |
|------|--------|------------------|---------|
| 1 | PostgreSQL แทน MySQL | ADR + README | ✅ |
| 2 | date-fns เพิ่ม, Moment.js deprecated | entity-register (+ optional ADR) | ✅ |
| 3 | Stripe idempotency pattern | cross-project memory **แต่ถามก่อน** + บันทึก work-log ระหว่างรอ | ✅ |
| 4 | T-015 done | task-board + work-log/diary (multi-destination) | ✅ |
| 5 | SQL injection bug พบระหว่างทำงาน | task T-NEW [FOUND-IN-PASSING] + work-log, ไม่แก้ทันที | ✅ |

- AI ระบุ multi-destination ชัดเจน: "ไม่ mutually exclusive" ✅
- Item 5 (bug): ทำตาม Scenario D ถูกต้อง — ไม่แก้เงียบ ✅
- Item 3: ระบุ "ถามผู้ใช้ก่อน" ชัดเจน และแนะนำ fallback (บันทึก work-log ก่อนรอคำตอบ) ✅

---

### Scenario P2: Language convention — ไม่ชัดว่าควรเก็บที่ไหน

**Scenario:** "ใช้ภาษาไทยสำหรับ user-facing error messages, English สำหรับ internal logs" — เก็บที่ไหน?

**ผล:** ✅ PASS — AI ใช้ decision tree ถูกต้องและไม่ over-engineer:
- เดิน through Scenario K ทีละขั้น อธิบาย reasoning ชัดเจน ✅
- Step 1 (ADR?): ไม่ใช่ — convention ไม่ใช่ structural decision ✅
- Step 2 (entity?): ไม่ใช่ ✅
- Step 3 (cross-project?): อาจได้ แต่ต้องถามผู้ใช้ก่อน ✅
- Step 4 (session decision?): ใช่ → เก็บใน work-log/diary ✅
- ไม่สร้าง ADR — อธิบายเหตุผลชัดเจน: convention ไม่ใช่ architectural constraint ✅
- Bonus: แนะนำว่า `CoreAiWorkspaces/04-way-of-work/way-of-work.md` (Language Policy) เป็นที่ที่เหมาะที่สุดสำหรับ convention ประเภทนี้ — proactive ✅

---

## สรุป

| Feature | Scenarios | Pass | Fail |
|---------|-----------|------|------|
| F4: Agent Diary Protocol | L, M | 2 | 0 |
| F5: Cross-Project Memory Bridge | N, O | 2 | 0 |
| F6: Memory Scope Protocol | P, P2 | 2 | 0 |
| **รวม** | **6** | **6** | **0** |

**Bug ที่พบ:** ไม่มี

**ข้อสังเกต:**
- Scenario M: sub-agent เขียนไฟล์จริงไปเลย (ไม่ใช่แค่ reader test) — mock-project files อัปเดตถูกต้อง ใช้เป็น integration test ด้วยได้
- Scenario P2: AI แนะนำ way-of-work.md โดยไม่ได้ถูกบอก — แสดงว่า pattern ชัดเจนพอที่ AI จะ infer เองได้

**Phase 2 ผ่านการทดสอบทุก feature — พร้อม merge ไป dev**
