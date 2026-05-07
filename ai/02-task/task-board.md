<!-- AI-CONTEXT
total_tasks: 3
in_progress: []
blocked: []
done: [T-001,T-002,T-003,T-004,T-005,T-006,T-007,T-010,T-011,T-012,T-013,T-014]
last_updated: 2026-05-07
-->

# Task Board — ai-project-template

## In Progress

*(ไม่มี task กำลังทำอยู่)*

## Todo

### T-020: Update ROADMAP.md — Phase 3 status

**Priority:** medium
**Ref:** ai/01-plan/project-plan.md
**Description:** ROADMAP.md ยังแสดง Phase 3 (Semantic Search Layer) เป็น "planned"
แต่ core/20-vector-memory-optional.md เสร็จแล้ว — ต้องอัปเดตให้ตรง

**Acceptance:**
- ROADMAP.md แสดง Phase 3 เป็น ✅ done (template phase)
- ระบุชัดว่า MemPalace เป็น implementation ที่เลือก

---

### T-021: Update CHANGELOG.md

**Priority:** medium
**Ref:** git log
**Description:** บันทึก 2 milestone ใหญ่:
1. doc/ → ai/ structural rename
2. MemPalace Phase 3 template (core/20 + tools/vector-memory/)

---

### T-022: Field test MemPalace workflow

**Priority:** low (ต้องทำก่อน release)
**Ref:** core/20-vector-memory-optional.md
**Description:** ทดสอบ workflow จริงกับโปรเจ็กต์ที่มี ai/ หลายสิบไฟล์:
- pip install mempalace → mempalace init → mempalace mine → mempalace search
- ตรวจว่า token budget rules (1,500 token, 5 chunks, score ≥ 0.60) ทำงานได้จริง

---

## Done

| Task | Description | Completed |
|------|-------------|-----------|
| T-001–007 | core/ templates ครบ (00–21) + skills/game/ + platforms/ | 2026-05 |
| T-010 | doc/ → ai/ rename ครบ 101 files | 2026-05-07 |
| T-011 | docs/ web pages ย้ายไป gh-pages branch | 2026-05-07 |
| T-012 | Root CLAUDE.md สร้างแล้ว — fix clone flow | 2026-05-07 |
| T-013 | Functional test suite 35/35 passing | 2026-05-07 |
| T-014 | scripts/new-project.sh สร้าง ai/ ไม่ใช่ doc/ | 2026-05-07 |
