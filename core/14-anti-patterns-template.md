# Anti-Pattern Catalog Template

รายการสิ่งที่ไม่ควรทำเมื่อทำงานร่วมกับ AI บนโปรเจ็กต์
นำไปเพิ่มหรืออ้างอิงใน `doc/04-way-of-work/way-of-work.md` ของโปรเจ็กต์

---

## หมวด 1 — Source Docs & Requirements

### ❌ ให้ AI แก้ไข source docs โดยตรง

**ปัญหา:** AI ปรับ requirement ตาม code ที่มีอยู่ แทนที่จะปรับ code ตาม requirement
**ผลลัพธ์:** source docs ไม่ใช่ source of truth อีกต่อไป ทีมทำงานโดยไม่รู้ว่า requirement เปลี่ยนไปเมื่อไหร่
**แนวทางที่ถูก:** มนุษย์เป็นผู้ควบคุม source docs เสมอ AI สร้างได้เฉพาะ extension doc หรือ ADR draft

---

### ❌ เขียนทับ source doc version เดิมโดยไม่สร้าง version ใหม่

**ปัญหา:** แก้ไขไฟล์ใน `versions/v0.1/` โดยตรงแทนที่จะสร้าง `versions/v0.2/`
**ผลลัพธ์:** สูญเสีย context ว่า requirement เดิมเป็นอะไร ไม่รู้ว่าเปลี่ยนไปเพราะอะไร
**แนวทางที่ถูก:** ดู `02-source-document-versioning-template.md` สำหรับเงื่อนไขการสร้าง version ใหม่

---

### ❌ Task ไม่มี source reference

**ปัญหา:** สร้าง task โดยไม่ระบุว่า requirement มาจากไหน
**ผลลัพธ์:** ไม่รู้ว่างานนี้เกิดจาก business need จริง หรือ AI คิดเอง scope creep เงียบ ๆ
**แนวทางที่ถูก:** ทุก task ต้องมี source reference ถ้าไม่มีให้แท็ก `[NEEDS SOURCE VALIDATION]`

---

## หมวด 2 — Session Discipline & AI-CONTEXT

### ❌ ไม่อัปเดต work-status ตอนจบ session

**ปัญหา:** session ถัดไปไม่รู้ว่าทำอะไรไปแล้ว ต้องเดาสถานะจาก code
**ผลลัพธ์:** ทำงานซ้ำ, เดินผิดทาง, เสียเวลา re-orient นาน
**แนวทางที่ถูก:** อัปเดต `work-status.md` และ `work-log-index.md` ก่อนจบทุกครั้ง ไม่มีข้อยกเว้น

---

### ❌ เริ่ม implement โดยไม่อ่าน session startup files

**ปัญหา:** AI เริ่มเขียน code ทันทีโดยไม่รู้สถานะปัจจุบัน
**ผลลัพธ์:** ทำงานบน assumption เก่า ทำซ้ำในสิ่งที่เสร็จแล้ว หรือข้ามสิ่งที่ค้างอยู่
**แนวทางที่ถูก:** อ่าน `work-status` → `work-log-index` → `task-board` ก่อนเสมอ

---

### ❌ อัปเดต body แต่ไม่อัปเดต AI-CONTEXT block

**ปัญหา:** แก้ work-status หรือ task-board แล้วลืมอัปเดต `<!-- AI-CONTEXT -->` block ด้านบน
**ผลลัพธ์:** session ถัดไปอ่าน block เก่า → orient ผิด → ทำงานบน assumption ที่ outdated
**แนวทางที่ถูก:** block และ body ต้องอัปเดตพร้อมกันทุกครั้ง ถ้า block กับ body ไม่ตรงกัน ให้เชื่อ body

---

### ❌ ประกาศว่างานเสร็จโดยไม่มี validation

**ปัญหา:** mark task เป็น `done` โดยไม่ผ่านการตรวจสอบใด ๆ
**ผลลัพธ์:** งานที่ "เสร็จ" อาจมี bug หรือไม่ตรง acceptance criteria จริง
**แนวทางที่ถูก:** ทุก task ต้องผ่าน validation อย่างน้อย 1 อย่างก่อนปิด ดู `04-coding-standards-template.md`

---

## หมวด 3 — การตัดสินใจ

### ❌ AI แก้ conflict ระหว่าง source docs เงียบ ๆ

**ปัญหา:** เมื่อ requirement สองข้อขัดแย้งกัน AI เลือกข้างหนึ่งโดยไม่แจ้ง
**ผลลัพธ์:** ทีมไม่รู้ว่ามีความขัดแย้ง ไม่มีโอกาสตัดสินใจ
**แนวทางที่ถูก:** สร้าง extension doc บันทึกความขัดแย้ง mark task `[BLOCKED: CONFLICT]` รอมนุษย์

---

### ❌ ตัดสินใจ architecture โดยไม่สร้าง ADR

**ปัญหา:** เลือก pattern หรือ library โดยไม่บันทึกเหตุผล
**ผลลัพธ์:** session ถัดไปเปลี่ยน approach โดยไม่รู้ว่าเหตุใดถึงเลือกแบบเดิม
**แนวทางที่ถูก:** ดู `12-adr-template.md` และสร้าง ADR draft เมื่อตัดสินใจ non-obvious

---

### ❌ เดาเมื่อไม่มีข้อมูล แทนการใช้ placeholder

**ปัญหา:** AI เติมข้อมูลที่ดูสมเหตุสมผลแต่ไม่มีใน source docs
**ผลลัพธ์:** requirement ที่ AI แต่งเองถูกปฏิบัติเสมือนเป็นความต้องการจริง
**แนวทางที่ถูก:** ใช้ `<NEEDS_CLARIFICATION: ...>` แทนการเดาเสมอ ดู `11-ai-decision-protocol-template.md`

---

## หมวด 4 — Git & Version Control

### ❌ Commit credentials, .env, หรือ local config เข้า repo

**ปัญหา:** ข้อมูลสำคัญรั่วไหลใน git history — แม้จะลบใน commit ถัดไป ก็ยังอยู่ใน history
**ผลลัพธ์:** ถ้า repo เป็น public หรือ clone ออกไปแล้ว credential รั่วถาวร
**แนวทางที่ถูก:** ตรวจ `.gitignore` ก่อน commit เสมอ ไม่มีข้อยกเว้น ถ้าเผลอ commit ให้ revoke credential ทันที

---

### ❌ Commit ไฟล์ log รายวันโดยไม่ได้ตั้งใจ

**ปัญหา:** repo อ้วนด้วย working records ที่ไม่ควรอยู่ใน git
**ผลลัพธ์:** clone ช้า, PR diff ยาว, ประวัติ git ถูกรบกวนด้วย noise
**แนวทางที่ถูก:** ตัดสินใจก่อน setup ว่า daily logs เก็บ local หรือ git ดู `08-log-and-summary-template.md`

---

### ❌ Force push ไปที่ branch ที่คนอื่นใช้งานอยู่

**ปัญหา:** AI rewrite history โดยไม่รู้ว่ามีคนอื่น (หรือ tool อื่น) ที่ base อยู่บน commit เดิม
**ผลลัพธ์:** ทีมต้อง reset และ re-apply งาน, commit history ของคนอื่นหาย
**แนวทางที่ถูก:** force push ได้เฉพาะ branch ที่ตัวเองสร้างและยังไม่มีใคร pull ไป — ถ้าไม่แน่ใจ ห้ามทำ ถามมนุษย์ก่อน

---

### ❌ Commit โดยไม่มี message ที่อธิบายได้

**ปัญหา:** AI สร้าง commit message แบบ "fix", "update", "changes" โดยไม่บอกว่าทำอะไร
**ผลลัพธ์:** `git log` ไม่บอกอะไรเลย ไม่รู้ว่า commit ไหนแก้อะไร ทำให้ debug และ rollback ยาก
**แนวทางที่ถูก:** commit message ต้องบอก "ทำอะไร เพราะอะไร" เช่น `fix: prevent negative health on simultaneous damage (T-034)`

---

### ❌ ตัดสินใจ merge หรือ rebase โดยไม่ถามมนุษย์

**ปัญหา:** AI merge branch หรือ rebase history โดยไม่รู้ว่า branch นั้นมีสถานะอะไรในทีม
**ผลลัพธ์:** อาจ merge code ที่ยังไม่ผ่าน review, ทำลาย feature branch ที่คนอื่นกำลังทำงาน
**แนวทางที่ถูก:** merge/rebase เป็น destructive operation — เสนอให้มนุษย์สั่ง ไม่ทำเอง

---

## หมวด 5 — Scope

### ❌ แก้ bug ที่ไม่เกี่ยวกับ task ปัจจุบัน โดยไม่บันทึก

**ปัญหา:** ทำ diff ขยายเกิน scope โดยไม่มี task รองรับ ไม่มีใครรู้ว่าทำไปแทรกไว้ตรงไหน
**แนวทางที่ถูก:** สร้าง task ใหม่ `[FOUND-IN-PASSING]` แล้วกลับมาทำ task เดิม

---

### ❌ เพิ่ม feature "ไปพลาง" โดยไม่มี source reference

**ปัญหา:** scope creep ที่ไม่ถูก track ทำให้ project plan ไม่สะท้อนความเป็นจริง
**แนวทางที่ถูก:** ถ้าเห็นโอกาสเพิ่ม feature — log ไว้ใน task-board ก่อน อย่าทำทันที
