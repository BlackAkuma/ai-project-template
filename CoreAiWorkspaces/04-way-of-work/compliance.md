# Compliance — ai-project-template


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

## การบันทึก Compliance Status

เพิ่มบรรทัดนี้ใน `CoreAiWorkspaces/04-way-of-work/way-of-work.md` ของโปรเจ็กต์ เพื่อให้ AI ทุก session รู้สถานะปัจจุบัน:

```
## Compliance Status

สถานะ: active | paused
เหตุผล (ถ้า paused): <เหตุผล เช่น "spike session — ทดลอง approach ใหม่">
```

**กฎ:** ถ้า compliance ถูก pause ไว้ → AI session ถัดไปต้องเห็นสถานะนี้ก่อนเริ่มทำงาน และถามผู้ใช้ว่าจะ resume หรือยัง

---

## สิ่งที่ตรวจ

> **Enforce column (RD-4):** `🔒 gate` = engine บังคับจริง (machine-checked, tamper-evident) — ดูชื่อ gate
> ใน `engine/gates/` (gate จับเฉพาะที่ระบุ; ส่วนที่ไม่ครอบ = prose). `📋 prose` = advisory เท่านั้น (AI/human scan).
> **template-only user (ไม่มี `engine/`):** gate ไม่รัน → **ทุก C-code = prose** สำหรับคุณ; prose
> ด้านล่างคือ guardrail เดียว ห้ามลบทิ้งเพราะคิดว่า "มี gate แล้ว"

### ระดับ 1 — Fix Now หรือ Defer (ต้องตัดสินใจ)

| Code | สิ่งที่ตรวจ | เกณฑ์ | Enforce |
|------|-----------|-------|---------|
| C-01 | File size | > 500 บรรทัด | 📋 prose |
| C-02 | Task ไม่มี source reference | ทุก task ที่ไม่มี `CoreAiWorkspaces/00-source/...` | 📋 prose |
| C-03 | Task `done` ไม่มี validation evidence | ไม่มีบันทึกว่าตรวจสอบอย่างไร | 🔒 gate `task-close` (evidence_count_gte) |
| C-04 | Placeholder ยังค้างในไฟล์ | `ai-project-template`, `<NEEDS_CLARIFICATION>` ฯลฯ | 🔒 gate `placeholder-scan` (เฉพาะ `<NEEDS_CLARIFICATION`/`<PROJECT_NAME>`/`<CURRENT_DATE>`; **ไม่จับ** ชื่อ `ai-project-template` → ส่วนนั้น 📋 prose) |

### ระดับ 2 — Defer เสมอ พร้อม tag ในโค้ด

| Code | สิ่งที่ตรวจ | เกณฑ์ | Enforce |
|------|-----------|-------|---------|
| C-05 | Function/method ยาวเกิน | > 50 บรรทัด | 📋 prose |
| C-06 | Dependency ใหม่ ไม่มี ADR | import ที่ไม่เคยมีในโปรเจ็กต์ | 📋 prose |
| C-07 | AI-CONTEXT block ไม่ sync กับ body | ค่าใน block ≠ ค่าใน body | 📋 prose (block↔body value equality — **ไม่มี gate จับ**) · gate `doc-sync` จับคนละเรื่อง: code staged แต่ docs ค้าง dirty (co-staging) ไม่ใช่ block↔body |
| C-08 | TODO / FIXME ไม่มี task reference | comment ที่ไม่มี T-XXX กำกับ | 📋 prose |

### ระดับ 3 — แจ้งเตือนอย่างเดียว

| Code | สิ่งที่ตรวจ | เกณฑ์ | Enforce |
|------|-----------|-------|---------|
| C-09 | work-status ไม่ได้อัปเดตนานเกิน | มี task `in_progress` แต่ไม่อัปเดต > 3 วัน | 📋 prose |
| C-10 | Session ก่อนไม่มี log entry | work-log-index ไม่มีบันทึก session ล่าสุด | 📋 prose (Stop-gate hook เตือนตอนจบ session) |
| C-11 | Security baseline ไม่ผ่าน | ดูรายการตรวจด้านล่าง | 🔒 gate `secret-scan` (เฉพาะ hardcoded secrets) + 📋 prose (SQL/XSS/IDOR/PII ดูด้านล่าง) |
| C-12 | work-log-index ใหญ่เกิน | > 300 บรรทัด — แนะนำ archive | 📋 prose |
| C-13 | task-board done section ใหญ่เกิน | > 15 รายการ — แนะนำ archive | 📋 prose |
| C-14 | entity-register ไม่ได้อัปเดตเมื่อ tech เปลี่ยน | task ที่ deprecated/เพิ่ม tech ใหม่ แต่ entity-register ไม่เปลี่ยน | 📋 prose |

> **Hot path สรุป (engine user เท่านั้น):** engine บังคับเต็มแค่ C-03 + C-11(hardcoded secret) และ
> บางส่วน C-04. **C-07 ไม่มี gate จับ block↔body — ยังต้อง scan เอง.** สำหรับ engine user: อย่าเสียเวลา
> พิสูจน์ซ้ำเฉพาะ C-03 + C-11-secret ที่ gate จับ fail-closed อยู่แล้ว.
> ⚠️ **template-only user (ไม่มี engine/): ข้ามไม่ได้สักตัว — ไม่มี gate เลย ต้อง scan ครบ 14 codes.**

---

---

## Security Baseline (C-11)

ตรวจทุก session เมื่อมีการแก้ไข code — แจ้งเตือนทันทีถ้าพบ:

| ประเด็น | สิ่งที่ตรวจ |
|--------|-----------|
| Hardcoded secrets | API key, password, token ใน code หรือ config ที่ไม่ได้ encrypt |
| SQL injection | query ที่ต่อ string ตรงโดยไม่ใช้ parameterized query |
| XSS | render HTML จาก user input โดยไม่ sanitize |
| Insecure direct object reference | ใช้ user-supplied ID โดยไม่ตรวจ ownership |
| Sensitive data ใน log | log ที่มี password, token, PII |
| Dependency ที่รู้ว่ามี vulnerability | package version ที่มี CVE ที่ทราบ |

ถ้าพบ C-11 → **Fix ทันที** ก่อนดำเนินงานต่อ ไม่ defer

---

## Tech Debt Register

ใช้ติดตาม REFACTOR-PENDING ทั้งหมดในโปรเจ็กต์
เก็บไว้ใน `CoreAiWorkspaces/05-tech-debt/debt-register.md`

```md
# Tech Debt Register

| ID | Code | ไฟล์ | คำอธิบาย | Task | Priority | เพิ่มเมื่อ |
|----|------|------|---------|------|----------|-----------|
```

**Priority:**
- High — กระทบ behavior หรือ maintainability อย่างชัดเจน
- Medium — ควรแก้ใน milestone ถัดไป
- Low — แก้เมื่อผ่านมา ไม่เร่งด่วน

**กฎ:** task ทุก task ที่ `done` ต้องตรวจก่อนว่ามี REFACTOR-PENDING ค้างอยู่ไหม ถ้ามีต้องมี entry ใน debt register

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

### C-12 / C-13 — Archive Notification Format

เมื่อพบ C-12 หรือ C-13 ให้แจ้งผู้ใช้ก่อนทำงานอื่น รูปแบบ:

```
[INFO] C-12: work-log-index มี 340 บรรทัด (threshold: 300)
       ไฟล์กำลังโตขึ้นเรื่อย ๆ — อาจทำให้ session ถัดไปใช้ token มากขึ้น
       ตัวเลือก:
         "archive logs"  → AI compress session เก่าเป็น monthly summary
         "ข้ามได้"       → ทำงานต่อ ไม่ archive ตอนนี้
```

**กฎ:** AI ไม่ archive โดยไม่ได้รับคำสั่ง — ผู้ใช้ตัดสินใจเสมอ

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
