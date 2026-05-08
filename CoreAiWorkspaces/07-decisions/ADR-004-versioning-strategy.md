# ADR-004: Versioning Strategy — Single Release + Layer Separation

**Date:** 2026-05-08
**Status:** Accepted
**Author:** AI session + User
**Related Tasks:** T-034

## Context

ระบบมี capabilities หลายส่วนที่พัฒนาในอัตราต่างกัน:
- `core/` — session protocol, templates (เปลี่ยนน้อย)
- `platforms/claude-code/skills/` — slash commands (เปลี่ยนบ่อย)
- `skills/game/` — game-specific (optional, แยกกลุ่มผู้ใช้)
- `scripts/` — bootstrap + update tooling

คำถาม: ควร version แต่ละ component แยกกัน หรือใช้ single release version?

## Options Considered

**Option A: Component versioning**
- แต่ละไฟล์/component มี version ของตัวเอง
- Pro: update เฉพาะจุด, รู้ว่าส่วนไหนเปลี่ยน
- Con: ทุก component อ้างอิงกัน — version drift ทำให้เกิด incompatibility, ซับซ้อนเกินจำเป็น

**Option B: Single release version (current)**
- ทุกอย่างออก version เดียวกัน
- Pro: ง่าย, ผู้ใช้รู้ว่า compatible
- Con: small fix ต้อง bump ทั้งก้อน

**Option C: Single release + Layer separation (เลือก)**
- System version เดียว (v MAJOR.MINOR.PATCH) — ผู้ใช้เห็นตัวนี้
- แต่แบ่ง layers ชัดเจน: `core/`, `platforms/`, `skills/game/`
- Bump rule ผูกกับ impact:
  - PATCH: bug fix, เนื้อหา → `/caw-update` จัดการได้
  - MINOR: feature ใหม่ → `/caw-update` จัดการได้
  - MAJOR: โครงสร้าง CoreAiWorkspaces/ หรือ protocol เปลี่ยนใหญ่ → re-bootstrap

## Decision

ใช้ **Option C** — Single release version พร้อม layer separation ใน CHANGELOG

Version เก็บใน `VERSION` file ที่ root — `new-project.sh` อ่านและ embed ลง bootstrapped `CoreAiWorkspaces/README.md` ทำให้แต่ละโปรเจ็กต์รู้ว่าใช้ template version อะไร

## Consequences

- ง่ายสำหรับผู้ใช้ — เห็น version เดียว
- `/caw-update` ใช้ได้กับ PATCH และ MINOR — ไม่ต้อง re-bootstrap บ่อย
- MAJOR version = signal ชัดว่าต้อง re-bootstrap
- CHANGELOG แบ่ง section ตาม layer เพื่อบอกว่าส่วนไหนเปลี่ยน

## Review Trigger

ทบทวนถ้าระบบมี layer ที่ release cycle แตกต่างกันมากจนผู้ใช้สับสนว่า version ไหน compatible กับ setup ของตัวเอง
