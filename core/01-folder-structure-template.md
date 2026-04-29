# Folder Structure Template

ใช้ template นี้เพื่อสร้างโครงสร้างเอกสารตั้งต้นของโปรเจ็กต์ใหม่

## Recommended Structure

```text
doc/
  README.md
  00-source/
    README.md
    01-<SOURCE-DOC-NAME>.md
    02-<SOURCE-DOC-NAME>.md
    versions/
      v0.1/
        01-<SOURCE-DOC-NAME>.md
        02-<SOURCE-DOC-NAME>.md
  01-plan/
    project-plan.md
    work-status.md
  02-task/
    task-board.md
  03-log/
    README.md
    work-log-index.md
    templates/
      daily-log-template.md
    agents/               ← multi-AI projects เท่านั้น
      claude-code.md
      [tool-name].md
    YYYY/
      MM/
        YYYY-MM-DD-log.md
  04-way-of-work/
    way-of-work.md
    coding-standards.md
    ai-decision-protocol.md
    compliance.md
  05-summary/
    README.md
    templates.md
    YYYY/
      YYYY-MM-summary.md
      MM/
        YYYY-MM-DD-summary.md
  06-extensions/
    README.md
    extension-template.md
  07-decisions/
    README.md
    ADR-001-<decision-title>.md
    entity-register.md
  08-design/           ← game projects เท่านั้น
    README.md
    asset-registry.md
    character-registry.md
    FDD-001-<feature-name>.md
```

## Tech Debt Folder (สร้างเมื่อมี REFACTOR-PENDING task แรก)

```text
doc/
  05-tech-debt/
    debt-register.md   ← ลงทะเบียน REFACTOR-PENDING ทั้งหมด (ดู core/15)
```

## Notes

- `00-source/` ไฟล์ชื่อหลักเป็น index/pointer
- source revision จริงเก็บใน `00-source/versions/`
- `03-log/YYYY/MM/` สำหรับ daily logs
- `05-summary/YYYY/MM/` สำหรับ daily summaries
- ถ้า repo ไม่ควรเก็บ daily records ให้ ignore รายวันและเก็บเฉพาะ summary ระดับเดือนขึ้นไป
- `05-tech-debt/` สร้างเมื่อมี REFACTOR-PENDING task แรก ไม่ต้องสร้างตั้งแต่ setup
- `07-decisions/` เก็บ ADR (Architecture Decision Records) และ `entity-register.md` — ห้ามลบ ให้ deprecated/supersede แทน
- `08-design/` สำหรับ game projects เท่านั้น เก็บ FDD และ asset registry
- `04-way-of-work/ai-decision-protocol.md` กำหนดว่า AI ต้องทำอะไรเมื่อเจอสถานการณ์คลุมเครือ (จาก `core/11`)
- `04-way-of-work/compliance.md` รวม compliance rules ทั้งหมดของโปรเจ็กต์ (จาก `core/15`)
- `03-log/agents/` สร้างเฉพาะเมื่อโปรเจ็กต์ใช้ AI tool มากกว่า 1 ตัว
- `08-design/character-registry.md` ใช้กับ game projects ที่มี narrative (จาก `skills/game/06`)
