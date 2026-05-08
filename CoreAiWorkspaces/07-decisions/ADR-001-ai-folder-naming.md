# ADR-001: เลือก CoreAiWorkspaces/ เป็นชื่อ AI working folder

**Date:** 2026-05-07
**Status:** Accepted
**Author:** AI session - 2026-05-07
**Source Reference:** ROADMAP.md, user feedback
**Related Tasks:** T-010, T-011, T-012

## Context

template เดิมใช้ชื่อ `doc/` สำหรับ AI working folder
เมื่อ user clone repo นี้มาใช้งาน จะมี:
- `doc/` — AI working space (จาก template)
- `docs/` — web pages สำหรับ GitHub Pages (อยู่ใน repo)

ทั้งสองชื่อคล้ายกันมากจนสับสน — user ไม่รู้ว่าโฟลเดอร์ไหนคืออะไร
นอกจากนี้ scripts/ ยังสร้าง `doc/` ซ้อนกับ `docs/` ทำให้เกิด conflict ในโครงสร้าง

## Options Considered

1. **CoreAiWorkspaces/** — สื่อความหมายชัดเจน ไม่ชนกับ docs/ — Pro: ชัดเจน, distinct Con: ต้อง rename ทุกไฟล์
2. **doc/** (เดิม) — Pro: สั้น Con: สับสนกับ docs/, ไม่สื่อว่าเป็น AI workspace
3. **workspace/** — Pro: ทั่วไป Con: ไม่ชัดว่าเป็น AI-related
4. **context/** — Pro: บอกว่าเป็น context สำหรับ AI Con: ยาวกว่า CoreAiWorkspaces/

## Decision

เลือก **CoreAiWorkspaces/** เพราะ:
- สื่อความหมายทันทีว่า folder นี้คือ workspace สำหรับ AI
- ไม่ชนกับ `docs/` ทำให้ user ไม่สับสน
- เป็น naming convention ที่เริ่มใช้กันใน developer community (เช่น .cursorrules → CoreAiWorkspaces/)

## Consequences

- **ง่ายขึ้น:** user เข้าใจโครงสร้างทันที — CoreAiWorkspaces/ คือที่ AI ทำงาน, docs/ คือเว็บ
- **ยากขึ้น:** ต้อง rename 589 occurrences ใน 101 files (ทำด้วย script)
- **ต้องระวัง:** script บางตัวใช้ `doc/` hardcoded — ต้องตรวจหลัง rename

## Review Trigger

ถ้า community standard เปลี่ยนไปใช้ชื่ออื่น (เช่น .CoreAiWorkspaces/ มี special meaning) ให้ revisit
