# ADR-003: docs/ web pages อยู่บน gh-pages branch เท่านั้น

**Date:** 2026-05-07
**Status:** Accepted
**Author:** AI session - 2026-05-07
**Source Reference:** user feedback (docs/ vs doc/ conflict)
**Related Tasks:** T-011

## Context

Template repo มี `docs/` folder สำหรับ GitHub Pages (how-it-works.html, workflow-diagram.html)
เมื่อ user clone repo นี้มาใช้เป็น starting point ของโปรเจ็กต์ตัวเอง:
- `docs/` จาก template จะติดมาด้วย
- user ไม่ต้องการ web pages เหล่านี้ในโปรเจ็กต์ตัวเอง
- ถ้าโปรเจ็กต์ user ใช้ docs/ อยู่แล้ว (เช่น Next.js) จะชนกัน

นอกจากนี้ `docs/` และ `doc/` (เดิม) อยู่ด้วยกันบน dev branch ทำให้สับสน

## Options Considered

1. **gh-pages branch (orphaned)** — docs/ อยู่แค่บน gh-pages ไม่อยู่บน dev/master
   Pro: user ที่ clone ไม่ได้รับ web pages, GitHub Pages ยังทำงานได้
   Con: ต้อง setup orphaned branch + configure GitHub Pages ให้ใช้ gh-pages

2. **ลบ web pages ออกจาก repo** — ไม่มี documentation เลย
   Pro: ไม่มี conflict Con: user ไม่มี visual guide

3. **เก็บบน dev แต่เพิ่มใน .gitignore ของ user** — Pro: ง่าย Con: ยังชนถ้า user ใช้ docs/

4. **เปลี่ยนชื่อเป็น website/ หรือ pages/** — Pro: ไม่ชน docs/ Con: GitHub Pages ต้องการ docs/ หรือ root

## Decision

เลือก **gh-pages branch** เพราะ:
- user ที่ clone repo จะไม่เจอ docs/ เลย (ไม่อยู่บน dev/master)
- GitHub Pages ยังทำงานได้ตามปกติ (อ่านจาก gh-pages branch)
- เป็น pattern มาตรฐานของ GitHub สำหรับแยก source code กับ web pages

## Consequences

- **ง่ายขึ้น:** user clone โปรเจ็กต์ใหม่ได้โดยไม่มี docs/ ติดมา
- **ยากขึ้น:** ต้องจัดการ 2 branch แยกกัน เมื่ออัปเดต web pages ต้อง push ไปที่ gh-pages
- **ต้องระวัง:** อย่า merge gh-pages กลับเข้า dev — content ต่างกันโดยสิ้นเชิง

## Review Trigger

ถ้า GitHub เปลี่ยน Pages policy หรือมี hosting option ที่ดีกว่า → revisit
