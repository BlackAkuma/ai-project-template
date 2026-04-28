# Compliance Check Template

Protocol สำหรับตรวจสอบ code quality และ documentation standards อัตโนมัติ
ทำงานทุกครั้งที่ AI รับงานจากคนอื่น จนกว่าจะสั่ง `pause compliance`

---

## คำสั่ง Control

| คำสั่ง | ผล |
|--------|-----|
| *(ไม่มีคำสั่ง)* | scan อัตโนมัติทุก session |
| `pause compliance` | หยุด scan ชั่วคราว session นี้ |
| `resume compliance` | เปิด scan กลับ |
| `scan` | scan ทันที ออก report ทั้งหมด |
| `scan refactor` | เฉพาะ REFACTOR-PENDING ทั้งโปรเจ็กต์ |

---

## สิ่งที่ตรวจ

### ระดับ 1 — Fix Now หรือ Defer (ต้องตัดสินใจ)

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| C-01 | File size | > 500 บรรทัด |
| C-02 | Task ไม่มี source reference | ทุก task ที่ไม่มี `doc/00-source/...` |
| C-03 | Task `done` ไม่มี validation evidence | ไม่มีบันทึกว่าตรวจสอบอย่างไร |
| C-04 | Placeholder ยังค้างในไฟล์ | `<PROJECT_NAME>`, `<NEEDS_CLARIFICATION>` ฯลฯ |

### ระดับ 2 — Defer เสมอ พร้อม tag ในโค้ด

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| C-05 | Function/method ยาวเกิน | > 50 บรรทัด |
| C-06 | Dependency ใหม่ ไม่มี ADR | import ที่ไม่เคยมีในโปรเจ็กต์ |
| C-07 | AI-CONTEXT block ไม่ sync กับ body | ค่าใน block ≠ ค่าใน body |
| C-08 | TODO / FIXME ไม่มี task reference | comment ที่ไม่มี T-XXX กำกับ |

### ระดับ 3 — แจ้งเตือนอย่างเดียว

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| C-09 | work-status ไม่ได้อัปเดตนานเกิน | มี task `in_progress` แต่ไม่อัปเดต > 3 วัน |
| C-10 | Session ก่อนไม่มี log entry | work-log-index ไม่มีบันทึก session ล่าสุด |

---

## Violation Tag Format

ใส่ใน code comment เมื่อ defer:

```
// REFACTOR-PENDING[C-01]: file too long (850 lines), needs splitting — T-042
// REFACTOR-PENDING[C-05]: function too long (80 lines) — T-043
// REFACTOR-PENDING[C-06]: new lib introduced, ADR needed — T-044
// REFACTOR-PENDING[C-08]: TODO without task reference — T-045
```

รูปแบบ: `// REFACTOR-PENDING[C-XX]: <คำอธิบาย> — <T-XXX>`

---

## Report Format

เมื่อ scan เสร็จ AI ต้อง output ในรูปแบบนี้:

```
=== Compliance Report — YYYY-MM-DD ===

LEVEL 1 (Fix or Defer):
  [C-01] src/game/player.ts — 820 lines (limit: 500)
  [C-03] T-012 marked done — no validation evidence

LEVEL 2 (Defer):
  [C-05] src/ui/hud.ts:GameHUD.render() — 72 lines
  [C-06] import 'three.js' in src/scene.ts — no ADR found

LEVEL 3 (Notice):
  [C-09] T-008 in_progress — work-status not updated for 4 days

Action required:
  - Fix or create REFACTOR-PENDING tasks for Level 1 items
  - Create REFACTOR-PENDING tasks for Level 2 items
  - Note Level 3 items in work-log
```

---

## กฎการตัดสินใจ Fix vs Defer

**Fix ทันที เมื่อ:**
- เป็น task ที่กำลังทำอยู่อยู่แล้ว (ไม่มี extra cost)
- แก้ใช้เวลา < 30 นาที
- มีผลต่อ correctness ไม่ใช่แค่ cleanliness

**Defer เมื่อ:**
- ไม่ใช่ scope ของ task ปัจจุบัน
- ต้องใช้เวลามากกว่า 30 นาที
- เป็นเรื่อง refactor ล้วน ๆ ไม่มีผลต่อ behavior

เมื่อ defer → สร้าง task T-XXX ใน task-board ทันที แท็ก `[COMPLIANCE-DEFER]`
