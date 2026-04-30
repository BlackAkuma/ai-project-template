# Phase 1 Test Results

วันที่ทดสอบ: 2026-04-29
Branch: test/phase-1

---

## Feature 3 — Entity Lifecycle Tags

### Hook Test (validate-commit.sh)

| Case | Description | Result | หมายเหตุ |
|------|-------------|--------|---------|
| C-14 deprecated tag | warn เมื่อพบ [ENTITY:deprecated:X] | ✅ PASS | |
| C-14 no false positive | ไม่ warn บน clean file | ✅ PASS | |
| C-11 hardcoded secret | block + exit 1 | ✅ PASS | **พบ bug**: regex `\s*` และ `\x27` ไม่ทำงานบน Windows grep — แก้เป็น `[[:space:]]*` และ `[\"']` |
| C-04 placeholder | warn เมื่อพบ placeholder | ✅ PASS | |
| Clean file | exit 0 + OK | ✅ PASS | |

**8/8 PASS** — Bug C-11 พบและแก้แล้วใน validate-commit.sh

### Reader Test (Scenario J)

**Scenario:** พบ `[ENTITY:deprecated:Redux]` ใน task description

**ผล:** ✅ PASS — AI ทำตาม Scenario J ถูกต้อง:
- หยุดทันที ไม่ implement Redux
- พยายามเปิด `doc/07-decisions/entity-register.md`
- เมื่อไม่พบไฟล์ (mock project ยังไม่มี) → mark task `[BLOCKED: deprecated entity]`
- เลือก Level 2 escalation ถูกต้อง
- อ้าง "Do less, document more" principle

---

## Feature 1 — Project Entity Register

### Reader Test (สร้าง entity-register.md)

**Scenario:** bootstrap โปรเจ็กต์ใหม่ที่มี Next.js, Supabase, Vercel (no ADR), date-fns, และ Moment.js (deprecated)

**ผล:** ✅ PASS — AI สร้างไฟล์ถูกต้อง:
- AI-CONTEXT block ครบ: `entities_active`, `entities_deprecated`, `last_updated`
- Active section: ครบทุก entity พร้อม type/status/since/adr
- Deprecated section: Moment.js อยู่ถูก section พร้อม `until` และ `replaced_by`
- Handle "no ADR" case: ใช้ `—` ไม่ใช่ blank และไม่แต่งขึ้นมาเอง
- เพิ่ม note "ADR pending" สำหรับ Vercel — proactive และถูกต้อง

---

## Feature 2 — Scoped Memory Map

### Reader Test (read_more field)

**Scenario:** เริ่ม session ใหม่ พบ work-status มี `read_more` field, ต้อง implement T-018 (Stripe payment handler)

**ผล:** ✅ PASS — AI ใช้ read_more ถูกต้อง:
- อธิบาย read_more ว่าเป็น "scoped navigation map" ไม่ใช่ reading checklist
- เลือกแบบ selective: เปิดแค่ entities + architecture ไม่เปิดทุก path
- ให้เหตุผลชัดเจนว่าทำไมเลือก path นั้น
- คำถาม "system architecture" → เปิดแค่ architecture path อย่างเดียว
- ไม่ fall into trap "อ่านทั้งหมด"

---

## สรุป

| Feature | Tests | Pass | Fail |
|---------|-------|------|------|
| F3: Entity Lifecycle Tags | Hook (5) + Reader (1) | 6 | 0 |
| F1: Project Entity Register | Reader (1) | 1 | 0 |
| F2: Scoped Memory Map | Reader (1) | 1 | 0 |
| **รวม** | **8** | **8** | **0** |

**Bug ที่พบและแก้:**
- C-11 secret detection regex ไม่ทำงานบน Windows grep (`\s*` → `[[:space:]]*`, `\x27` → `[\"']`)
  แก้แล้วใน `platforms/claude-code/hooks/validate-commit.sh`

**Phase 1 ผ่านการทดสอบทุก feature — พร้อม merge ไป dev**
