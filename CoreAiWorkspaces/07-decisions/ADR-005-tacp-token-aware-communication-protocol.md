# ADR-005: Token-Aware Communication Protocol (TACP)

**Date:** 2026-05-08
**Status:** Accepted
**Author:** AI session + User
**Related Tasks:** T-035 (feat/savetoken)

## Context

ระบบ ai-project-template ใช้ภาษาไทยเป็นหลักในการสื่อสารกับผู้ใช้ ซึ่งมีปัญหาหลัก 2 ข้อ:

1. **Token waste ใน machine-facing content**: AI-CONTEXT blocks และ internal logic ที่เขียนเป็นภาษาไทยใช้ token มากกว่า English 2-5x โดยไม่มีประโยชน์เพิ่มขึ้น (AI อ่าน English ได้ดีกว่า)

2. **Verbosity mismatch**: AI ตอบยาวเท่ากันทุก message ทั้ง ๆ ที่บางกรณีต้องการแค่ V1 (ยืนยัน) แต่ได้ V5 (อธิบายเต็ม) ทำให้เปลืองทั้ง token และเวลาผู้ใช้

3. **Thai polite particle overuse**: ประโยคภาษาไทยมีคำ particle ซ้ำซ้อน (นะครับ ทุกประโยค) ทำให้ขยายตัวโดยไม่เพิ่มความหมาย

## Options Considered

**Option A: English-only output**
- Pro: token savings สูงสุด
- Con: ผู้ใช้ไทยอ่านไม่สะดวก, ไม่ตอบโจทย์ project ที่ตั้งค่าภาษาไว้

**Option B: Configurable language (toggle)**
- Pro: flexible
- Con: ผู้ใช้ต้องจำคำสั่ง toggle, AI อาจลืม apply

**Option C: 3-Layer Model with destination-driven rules (เลือก)**
- L1: machine-facing → English always (auto)
- L2: user-facing → L2_LANG (config-driven)
- L3: shared files → dual-block (AI-CONTEXT L1 + HUMAN-CONTEXT L2)
- Pro: transparent ต่อผู้ใช้, AI ไม่ต้อง "ตัดสินใจ" ภาษา, configurable via L2_LANG
- Con: ต้องอัปเดต caw-*.md ทั้งหมดเป็น dual-block

**Option D: Post-process compression plugin**
- Inspired by pordee (JS plugin ที่ remove Thai particles)
- Pro: automatic
- Con: dependency เพิ่ม, ไม่ work กับ Claude.ai web mode, ต้องบำรุงรักษา

## Decision

ใช้ **Option C** — 3-Layer Model บวก Thai compression rules (P-01 ถึง P-06) และ Verbosity Scale (V1-V5)

Key design choices:
- **Destination-driven, not topic-driven**: AI รู้ layer จาก context ของ output ไม่ใช่จาก topic
- **L2_LANG config**: เปลี่ยนหนึ่งค่า → เปลี่ยน language ทั้งระบบ
- **No plugin dependency**: compression เป็น protocol rules ใน TACP ไม่ใช่ code
- **Works on all Claude modes**: Claude Code, Claude.ai web, API

## Consequences

- AI-CONTEXT blocks เป็น English ทั้งหมด: ประหยัด 60-70% ต่อ block
- Thai output ที่ compressed: ประหยัด 25-40% ต่อ message
- Verbosity matching: ประหยัด 30-50% สำหรับ ack/status messages
- caw-*.md files ทั้ง 11 ไฟล์ migrate เป็น dual-block format
- ผู้ใช้ project ใหม่ได้รับ TACP อัตโนมัติผ่าน bootstrap

## Review Trigger

ทบทวนถ้า:
- มี L2_LANG ใหม่ที่ต้องการ compression rules ต่างออกไป
- token pricing model ของ Anthropic เปลี่ยนแปลงอย่างมีนัยสำคัญ
- ผู้ใช้ report ว่า compressed output อ่านยากเกินไป
