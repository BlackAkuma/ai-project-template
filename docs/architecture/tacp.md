---
title: TACP — Token-Aware Communication Protocol
---

# Token-Aware Communication Protocol (TACP)

ระบบประหยัด token ในทุก session — ออกแบบมาสำหรับทั้งภาษาไทยและภาษาอังกฤษ

→ [ภาพรวมระบบ](overview.md) | [How It Works](how-it-works.html)

---

## ปัญหาที่ TACP แก้

### ภาษาไทยแพงกว่าภาษาอังกฤษ 2–4 เท่า

AI tokenizers (รวมถึง Claude) ตัดภาษาไทยที่ 1–3 ตัวอักษรต่อ token ขณะที่ภาษาอังกฤษตัดที่ 4–5 ตัวอักษรต่อ token หมายความว่าข้อความภาษาไทยที่มีความหมายเท่ากันจะใช้ token **2–4 เท่า** ของภาษาอังกฤษ

นอกจากนี้ AI มักตอบแบบ "สุภาพเกินจำเป็น" ทั้งภาษาไทยและภาษาอังกฤษ — เพิ่ม token โดยไม่เพิ่มความหมาย

### ตัวอย่าง: AI-CONTEXT block ภาษาไทย vs ภาษาอังกฤษ

**ก่อน TACP (ไทย):**
```
<!-- AI-CONTEXT
กำลังทำงานอยู่ในเฟส 3 ซึ่งเป็นการพัฒนา feature ใหม่
งานที่กำลังทำอยู่คือ T-042 ซึ่งเกี่ยวกับการ implement payment flow
งานถัดไปที่ต้องทำคือการ implement payment gateway integration
-->
```
**~52 tokens**

**หลัง TACP (English key-value):**
```
<!-- AI-CONTEXT
phase: 3
active: T-042 (payment flow)
next: implement payment gateway integration
-->
```
**~19 tokens — ประหยัด 63%**

---

## TACP คืออะไร

TACP แบ่งการสื่อสารเป็น **3 ชั้น** ตามปลายทาง:

```
L1 — AI อ่าน          English key-value  ประหยัด token สูงสุด
L2 — User อ่าน         ภาษาที่ตกลงไว้    verbosity ตามบริบท
L3 — ไฟล์ที่แชร์        dual-block        L1 + L2 ในไฟล์เดียว
```

### Layer 1 — AI-CONTEXT Blocks (Machine-Facing)

ทุก AI-CONTEXT block ในระบบนี้เขียนด้วย **English key-value** เสมอ:

```yaml
<!-- AI-CONTEXT
phase: 3
active: T-035 (TACP implementation)
blocked: none
next: merge to dev → master
risk: low
-->
```

AI อ่าน block นี้เพื่อ orient ตัวเอง ไม่ต้องอ่านทั้งไฟล์

### Layer 2 — User Communication (Human-Facing)

AI คุยกับคนใช้ด้วยภาษาที่เหมาะสมกับบริบท — มี **Verbosity Scale V1–V5**:

| Level | ใช้เมื่อ | ตัวอย่าง |
|-------|---------|---------|
| V1 | ยืนยัน / ack | `push ขึ้น dev เรียบร้อยครับ` |
| V2 | รายการสั้น | `อัปเดต 3 ไฟล์: work-status ✓ task-board ✓ log ✓` |
| V3 | อธิบาย / ถาม | paragraph ปกติ |
| V4 | เสนอ design | อธิบายทางเลือก พร้อม pros/cons |
| V5 | คำเตือน / destructive | **ไม่ compress เด็ดขาด** |

### Layer 3 — Shared Files (Dual-Block)

ไฟล์ `.claude/commands/caw-*.md` มีสองส่วน:

```
<!-- AI-CONTEXT          ← AI อ่านส่วนนี้ (L1)
cmd: caw-session-end
steps: [update_work_status, sync_context, append_log, ...]
-->

<!-- HUMAN-CONTEXT       ← คนอ่านส่วนนี้ (L2)
# /caw-session-end
Sync work-status, work-log-index, task-board ครบในคำสั่งเดียว
-->

[body — เนื้อหาที่อ่านได้ทั้งคนและ AI]
```

---

## ตัวเลขประหยัดจาก Benchmark

ทดสอบด้วย 15 test cases บน session จริง:

| Operation | ก่อน TACP | หลัง TACP | ประหยัด |
|-----------|-----------|-----------|---------|
| Session start (อ่าน AI-CONTEXT 4 ไฟล์) | ~2,030 tokens | ~135 tokens | **93%** |
| caw-*.md AI read path | ~380 tokens | ~52 tokens | **86%** |
| Simple confirm (V1) | ~90 tokens | ~10 tokens | **89%** |
| AI-CONTEXT block (ไทย→English) | ~89 tokens | ~28 tokens | **69%** |
| Short status update (V2) | ~132 tokens | ~47 tokens | **64%** |
| Design proposal (V4) | ~186 tokens | ~89 tokens | **52%** |
| Warning (V5) | ~120 tokens | ~120 tokens | 0% (ตั้งใจ) |

### ผลรวม Session จริง (100 messages)

| Metric | ก่อน TACP | หลัง TACP |
|--------|-----------|-----------|
| Session start tokens | ~2,030 | ~135 |
| Average response tokens | ~180 | ~95 |
| 100-message session total | ~20,000 | ~9,600 |
| **ประมาณการลดค่าใช้จ่าย** | — | **~52%** |

> **หมายเหตุ:** วัดด้วย tiktoken cl100k_base เป็น proxy สำหรับ Claude tokenizer ค่าจริงอาจต่างกัน ±10%

---

## ทำไมถึงใช้ได้ทั้งภาษาไทยและภาษาอังกฤษ

**ภาษาไทย** — ได้ประโยชน์หลัก 3 ทาง:
1. AI-CONTEXT blocks เป็น English → ประหยัด 65–70% ทันที
2. Chat compression rules (P-01–P-06) ลด particle ซ้ำซ้อน
3. Verbosity matching ลด "สุภาพเกินจำเป็น"

**ภาษาอังกฤษ** — ได้ประโยชน์เช่นกัน:
1. AI-CONTEXT blocks ยังได้ประโยชน์จาก key-value format (dense) vs prose
2. Verbosity matching ใช้ได้เหมือนกัน
3. Session orientation savings เหมือนกัน (~93%)

การตั้ง `L2_LANG: en` ใน `way-of-work.md` ทำให้ chat output เป็น English แต่ยังได้ savings จาก L1/L3 layers เต็มที่

---

## ตั้งค่า L2_LANG

ไฟล์ `CoreAiWorkspaces/04-way-of-work/way-of-work.md` มี TACP config:

```yaml
tacp:
  L2_LANG: th          # ← เปลี่ยนเป็น en สำหรับโปรเจ็กต์ภาษาอังกฤษ
  verbosity_default: 3
  politeness_level: minimal
```

AI จะ switch ภาษา chat output ทันที — แต่ L1 (AI-CONTEXT blocks) และ L3 (dual-block format) ไม่เปลี่ยน เพราะต้องเป็น English เสมอ

---

## สิ่งที่ TACP ไม่ทำ

- **ไม่ compress คำเตือน (V5)** — safety > token savings เสมอ
- **ไม่ตัดข้อมูลจำเป็น** — ย่อ form ไม่ตัด content
- **ไม่กระทบ human readability** — ทุกไฟล์ยังอ่านออกด้วยตาเปล่า

---

→ ต่อไป: [Memory System](memory-system.md) | [ADR System](adr-system.md)
