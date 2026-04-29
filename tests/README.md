# Tests

โฟลเดอร์นี้มีไว้สำหรับทดสอบ template features เท่านั้น
**ไม่ใช่ส่วนหนึ่งของ template** — ห้าม copy ไปใช้ใน project จริง

---

## โครงสร้าง

```
tests/
  hooks/                ← test scripts สำหรับ Claude Code hooks
  reader/               ← prompts สำหรับ fresh AI reader tests
  mock-project/         ← โปรเจ็กต์จำลองที่ใช้ template จริง
  results/              ← ผลการทดสอบ (gitignored)
```

## Feature ที่ทดสอบ

| Feature | Test Type | ไฟล์ |
|---------|-----------|------|
| F3: Entity Lifecycle Tags | Hook test | hooks/test-validate-commit.sh |
| F3: Entity Lifecycle Tags | Reader test | reader/test-scenario-j.md |
| F1: Project Entity Register | Reader test | reader/test-entity-register.md |
| F1: Project Entity Register | Bootstrap sim | mock-project/ |
| F2: Scoped Memory Map | Reader test | reader/test-scoped-memory.md |

## วิธีรัน

```bash
# Hook tests
bash tests/hooks/test-validate-commit.sh

# Reader tests — ใช้ AI agent อ่าน prompt แล้วประเมินผล
```
