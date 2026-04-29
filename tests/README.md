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

### Phase 1

| Feature | Test Type | ไฟล์ | ผล |
|---------|-----------|------|----|
| F3: Entity Lifecycle Tags | Hook test | hooks/test-validate-commit.sh | ✅ 5/5 |
| F3: Entity Lifecycle Tags | Reader test | reader/test-scenario-j.md | ✅ |
| F1: Project Entity Register | Reader test | reader/test-entity-register.md | ✅ |
| F1: Project Entity Register | Bootstrap sim | mock-project/ | ✅ |
| F2: Scoped Memory Map | Reader test | reader/test-scoped-memory.md | ✅ |

### Phase 2

| Feature | Test Type | ไฟล์ | ผล |
|---------|-----------|------|----|
| F4: Agent Diary Protocol | Reader test (session start) | reader/test-agent-diary.md — Scenario L | ✅ |
| F4: Agent Diary Protocol | Integration test (session end) | reader/test-agent-diary.md — Scenario M | ✅ |
| F5: Cross-Project Memory Bridge | Reader test (bootstrap) | reader/test-cross-project-memory.md — Scenario N | ✅ |
| F5: Cross-Project Memory Bridge | Reader test (session end) | reader/test-cross-project-memory.md — Scenario O | ✅ |
| F6: Memory Scope Protocol | Reader test (5 items) | reader/test-memory-scope.md — Scenario P | ✅ |
| F6: Memory Scope Protocol | Reader test (edge case) | reader/test-memory-scope.md — Scenario P2 | ✅ |

## วิธีรัน

```bash
# Hook tests
bash tests/hooks/test-validate-commit.sh

# Reader tests — ใช้ AI agent อ่าน prompt แล้วประเมินผล
# ดู tests/reader/ สำหรับ prompt files แต่ละ scenario
```
