# Bootstrap Checklist Template

AI ใช้ checklist นี้ตรวจสอบก่อนประกาศว่า setup เสร็จ
ห้ามถือว่าเสร็จจนกว่าจะผ่านทุกข้อ

---

## 0. Git Branch Setup — ต้องผ่านก่อนเริ่มทุกอย่าง

- [ ] ตรวจ branch ปัจจุบันด้วย `git branch --show-current` แล้ว
- [ ] ถ้าอยู่บน production branch: ผู้ใช้ตัดสินใจแล้วว่าจะ (A) สร้าง dev branch หรือ (B) single-branch mode
- [ ] `git_prod_branch` และ `git_dev_branch` บันทึกใน `work-status.md` AI-CONTEXT block แล้ว
- [ ] `git_mode` บันทึกแล้ว (`branch-separated` หรือ `single-branch`)
- [ ] ถ้า `single-branch`: `.deployignore` สร้างแล้วและมี `ai/`, `CLAUDE.md`, `*.lance`
- [ ] `.gitignore` มี `ai/08-vector-index/` และ `*.lance`

---

## 1. โครงสร้างโฟลเดอร์

- [ ] `ai/` และโฟลเดอร์หลักทั้งหมดสร้างแล้ว
- [ ] `ai/00-source/versions/<CURRENT_SOURCE_VERSION>/` มีอยู่
- [ ] `ai/07-decisions/` มีอยู่

## 2. ไฟล์ที่ต้องมี

- [ ] `ai/README.md`
- [ ] `ai/00-source/README.md` (source index)
- [ ] `ai/01-plan/project-plan.md`
- [ ] `ai/01-plan/work-status.md`
- [ ] `ai/02-task/task-board.md`
- [ ] `ai/03-log/work-log-index.md`
- [ ] `ai/04-way-of-work/way-of-work.md`
- [ ] `ai/04-way-of-work/coding-standards.md`
- [ ] `ai/04-way-of-work/ai-decision-protocol.md`
- [ ] `ai/04-way-of-work/compliance.md`
- [ ] `ai/07-decisions/README.md` (ADR index)
- [ ] `ai/07-decisions/entity-register.md` (ถ้าโปรเจ็กต์มี tech decisions แล้ว)

## 3. AI-CONTEXT Blocks

- [ ] `work-status.md` มี `<!-- AI-CONTEXT ... -->` block ด้านบนสุด และ field ครบ
- [ ] `work-status.md` มี `read_more` field ชี้ไปที่ path ที่ถูกต้อง
- [ ] `task-board.md` มี `<!-- AI-CONTEXT ... -->` block ด้านบนสุด และ field ครบ
- [ ] `work-log-index.md` มี `<!-- AI-CONTEXT ... -->` block ด้านบนสุด และ field ครบ
- [ ] ค่าใน block สะท้อนสถานะจริง ณ ตอน setup (ไม่ใช่ template placeholder ว่าง)

## 4. เนื้อหาต้องมี placeholder หรือข้อมูลจริง

- [ ] `<PROJECT_NAME>` ถูกแทนด้วยชื่อจริงหรือ placeholder ที่ชัดเจน
- [ ] `<CURRENT_SOURCE_VERSION>` ระบุแล้ว (เช่น `v0.1`)
- [ ] `<PROJECT_PHASE>` ระบุแล้ว
- [ ] `<NEXT_REQUIRED_WORK>` ระบุแล้ว
- [ ] ไม่มีการ invent requirement เชิงธุรกิจที่ไม่มีใน source docs

## 5. Source Docs

- [ ] ถ้ามี source docs: วางไว้ใน `ai/00-source/versions/<VERSION>/` แล้ว
- [ ] ถ้ายังไม่มี source docs: ระบุชัดใน work-status ว่า "source docs ยังไม่ได้นำเข้า"
- [ ] source version policy ระบุแล้วว่าจะ versioning อย่างไร

## 6. Work Status & Log

- [ ] `work-status.md` บันทึกสถานะเริ่มต้นจริง ไม่ใช่ template เปล่า
- [ ] `work-log-index.md` มี entry แรกบันทึกการ setup session นี้
- [ ] `task-board.md` มี task เริ่มต้นอย่างน้อย 1 รายการ (หรือระบุว่ายังไม่มี task)

## 7. Git & Template Cleanup

- [ ] `.gitignore` มี `_template/` อยู่แล้ว (ถ้าไม่มี AI ต้องเพิ่มให้)
- [ ] ไม่มีไฟล์ของ template ค้างอยู่นอก `_template/` โดยไม่ได้ตั้งใจ
- [ ] `ai/` พร้อม commit เข้า git บน **dev branch เท่านั้น** — ไม่ขึ้น production branch
- [ ] ถ้า `git_mode: branch-separated`: `git push origin [dev_branch]` รัน bootstrap ครั้งแรกแล้ว
- [ ] ยืนยัน: `ai/` และ `CLAUDE.md` **ไม่มีอยู่บน production branch** (ตรวจด้วย `git checkout [prod] && ls`)

## 8. Policy ที่ต้องตัดสินใจ

- [ ] ระบุแล้วว่า daily logs จะเก็บใน git หรือ local เท่านั้น
- [ ] ภาษาเอกสารระบุแล้วใน `way-of-work.md` (`<PROJECT_LANGUAGE>`)
- [ ] Language policy บันทึกแล้วใน `way-of-work.md`: reasoning=English, output=`<PROJECT_LANGUAGE>`, AI-CONTEXT block=English

---

## Completion Rule

ถ้า checklist ผ่านครบ → setup เสร็จ โฟลเดอร์ template ลบทิ้งได้เลย

ถ้ายังมีข้อที่ไม่ผ่าน → แก้ให้ครบก่อน ห้ามประกาศว่าเสร็จ
