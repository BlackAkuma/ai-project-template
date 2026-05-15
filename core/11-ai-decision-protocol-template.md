# AI Decision Protocol Template

เอกสารนี้กำหนดว่า AI ควรตัดสินใจอย่างไรเมื่อเจอสถานการณ์คลุมเครือ ขัดแย้ง หรือไม่มีข้อมูล
นำไปวางใน `CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md` ของโปรเจ็กต์

---

## 1. การตรวจสอบก่อนลงมือ (4-Question Check)

ก่อนทำงานใด ๆ ให้ตอบ 4 คำถามนี้:

1. ฉันรู้ผลลัพธ์ที่คาดหวังชัดเจนหรือไม่?
2. งานนี้สอดคล้องกับ source docs หรือไม่?
3. ถ้าฉันทำผิด งานนี้ย้อนกลับได้หรือไม่?
4. **สิ่งที่ฉันจะเสนอหรือสร้าง — มีอยู่แล้วในระบบหรือไม่?**

→ ถ้าตอบ "ใช่" ทั้ง 4 ข้อ: ดำเนินการได้เลย
→ ถ้าตอบ "ไม่" ข้อใดข้อหนึ่ง: ดู Decision Tree ด้านล่าง

**ข้อ 4 บังคับ** ก่อนเสนอ "สร้างใหม่" หรือ "ระบบขาด X" ทุกครั้ง → ดู Scenario L

---

## 2. Decision Tree ตามสถานการณ์

### Scenario A — Task คลุมเครือ ไม่รู้จะทำอะไร

```
มี task คล้ายกันที่เสร็จแล้วใน task-board ไหม?
  → ใช่: ทำตามรูปแบบนั้น และบันทึกว่าอ้างอิงจาก T-XXX
  → ไม่: มี section ที่เกี่ยวข้องใน source docs ไหม?
           → ใช่: ตีความจาก source docs และระบุว่าอิง section ใด
           → ไม่: STOP → เปลี่ยนสถานะ task เป็น [BLOCKED]
                         → ระบุชัดเจนว่าต้องการข้อมูลอะไร
                         → อัปเดต work-status
```

### Scenario B — Source docs ขัดแย้งกับ code ที่มีอยู่

```
ตรวจสอบว่าอันไหนใหม่กว่า (doc version vs git log)
→ ห้ามแก้ปัญหาเงียบ ๆ โดยไม่แจ้ง
→ สร้าง extension doc บันทึกความขัดแย้ง
→ อัปเดต work-status เป็น [NEEDS HUMAN DECISION: อธิบายความขัดแย้ง]
→ รอการตัดสินใจจากมนุษย์
```

### Scenario C — พบว่างานที่ทำอยู่ขยายเกิน scope เดิม

```
→ ทำเฉพาะส่วนที่ scope เดิมกำหนดไว้
→ สร้าง task ใหม่ T-XXX ใน task-board สำหรับส่วนที่เกิน
→ ถ้ามี source reference: ใส่ไว้
→ ถ้าไม่มี: แท็ก [NEEDS SOURCE VALIDATION]
→ บันทึกใน work-log ว่าพบ scope เพิ่มเติม
```

### Scenario D — พบ bug ที่ไม่เกี่ยวกับ task ปัจจุบัน

```
→ ห้ามแก้ bug นั้นเงียบ ๆ โดยไม่แจ้ง
→ สร้าง task T-XXX ใน task-board แท็ก [FOUND-IN-PASSING]
→ บันทึกไว้ใน work-log
→ กลับมาทำ task เดิมต่อ
```

### Scenario E — Requirement สองข้อขัดแย้งกัน

```
→ ห้ามเลือกข้างใดข้างหนึ่งเงียบ ๆ
→ สร้าง extension doc อธิบายความขัดแย้งและอ้างอิงทั้งสอง requirement
→ เปลี่ยนสถานะ task เป็น [BLOCKED: CONFLICT] พร้อมอ้างอิงทั้งสองจุด
→ อัปเดต work-status รอการตัดสินใจ
```

### Scenario F — ไม่มีข้อมูลในเอกสารใดเลย

```
→ ห้ามเดาหรือแต่งข้อมูลเอง
→ ใช้ placeholder: <NEEDS_CLARIFICATION: [ระบุว่าต้องการข้อมูลอะไร]>
→ บันทึก gap นี้ใน work-status
→ ดำเนินการต่อในส่วนอื่นที่มีข้อมูลพอ
```

### Scenario G — Context window ใกล้เต็มกลางคัน

```
→ หยุดและบันทึก progress ปัจจุบันใน work-log ก่อนที่ context จะหาย
→ อัปเดต work-status ให้สะท้อน checkpoint ปัจจุบัน
→ เปลี่ยนสถานะ task เป็น [IN_PROGRESS: checkpoint saved — <สรุปสิ่งที่ทำไปแล้ว>]
→ Session ถัดไปอ่าน work-status เพื่อ resume
```

### Scenario H — พบ gap ระหว่าง task board กับ source docs

เกิดเมื่อ: task ใน board อ้างอิง source version เก่า / task ที่ in_progress ไม่มี source reference / source doc ถูกอัปเดตแต่ task board ยังไม่สะท้อน

```
→ ห้ามเริ่ม implement จนกว่าจะระบุ gap ชัดเจน
→ รายการ gap ทั้งหมดที่พบ: task ID + สิ่งที่ขาด/ไม่ตรง
→ ถ้า gap เล็ก (task ขาด reference): อัปเดต task ได้เลย บันทึกใน work-log
→ ถ้า gap ใหญ่ (source เปลี่ยนแต่หลาย task ได้รับผล): เปลี่ยน work-status เป็น
   [NEEDS HUMAN DECISION: source/task gap detected — <รายการ task ที่ได้รับผล>]
→ รอ human ยืนยันก่อนดำเนินต่อ
```

**ตัวอย่าง gap จริง — gap เล็ก (แก้ได้เลย):**

```
Session เริ่มต้น → อ่าน task-board พบ:

T-022 [in_progress]: implement product search
  ref: CoreAiWorkspaces/00-source/versions/v1.0/03-search.md  ← source version เก่า

แต่ current source version คือ v1.2 ซึ่งเพิ่ม fuzzy search requirement

Gap: T-022 อ้างอิง v1.0 ขณะที่มี v1.2 แล้ว

→ gap เล็ก (แค่ task เดียว ขาด reference ใหม่)
→ อัปเดต T-022 ให้ ref v1.2 แทน + บันทึกใน work-log
→ ตรวจว่า fuzzy search requirement ใน v1.2 กระทบ scope T-022 หรือไม่
   ถ้ากระทบ: mark T-022 [BLOCKED] รอ human ยืนยัน scope
   ถ้าไม่กระทบ: ดำเนินต่อได้เลย
```

**ตัวอย่าง gap จริง — gap ใหญ่ (รอมนุษย์):**

```
Session เริ่มต้น → อ่าน task-board พบ T-020, T-021, T-022, T-023 ทั้งหมด ref v1.0
แต่ source ถูกอัปเดตเป็น v1.3 เมื่อ 3 วันก่อน และมีการเปลี่ยน auth model ใหม่ทั้งหมด

Gap: 4 tasks ที่กำลังทำอยู่อาจต้องแก้ scope ทั้งหมด

→ gap ใหญ่ — ไม่ implement อะไรเพิ่ม
→ เปลี่ยน work-status เป็น:
   [NEEDS HUMAN DECISION: source v1.3 เปลี่ยน auth model — T-020, T-021, T-022, T-023
    อาจกระทบ scope ทั้งหมด รอยืนยันก่อนดำเนิน]
→ รอ human ยืนยันก่อน
```

### Scenario I — พบ code ที่ไม่มี documentation รองรับ

```
→ ห้ามแก้ไข code นั้นทันที
→ ทำ reverse-document ตาม protocol ใน extension-doc-template.md
→ สร้าง task [REVERSE-DOC] ใน task-board
→ รอ human review ก่อนแก้ไข
```

### Scenario J — พบ `[ENTITY:deprecated]` หรือ `[ENTITY:superseded]` tag

เกิดเมื่อ: อ่าน code, ADR, หรือ task แล้วพบ tag ระบุว่า entity นั้นเปลี่ยนสถานะแล้ว

```
→ ห้ามใช้ entity นั้นต่อโดยไม่ตรวจสอบก่อน
→ เปิด CoreAiWorkspaces/07-decisions/entity-register.md
→ ตรวจสอบ status ปัจจุบัน, replaced_by (ถ้ามี), และ ADR ที่เกี่ยวข้อง
→ ถ้า entity ถูกแทนที่: ใช้ entity ใหม่แทน และบันทึกใน work-log
→ ถ้าไม่แน่ใจ: mark task เป็น [BLOCKED: deprecated entity] รอ human decision
```

**Entity Tag Format:**

| Tag | ความหมาย |
|-----|----------|
| `[ENTITY:deprecated:X]` | entity X เลิกใช้แล้ว ตรวจ entity-register |
| `[ENTITY:superseded:X→Y]` | entity X ถูกแทนด้วย Y |
| `[ENTITY:proposed:X]` | entity X ยังไม่ได้ตัดสินใจ รอ ADR |
| `[ENTITY:active:X]` | ยืนยันว่า X ยังใช้งานอยู่ (optional ใช้เมื่ออยากชัดเจน) |

### Scenario L — ก่อนเสนอ "สร้างใหม่" หรือ "ระบบขาด X"

⚠️ **นี่คือ Scenario ที่อันตรายที่สุดสำหรับผู้ใช้** — AI เสนอสิ่งที่มีอยู่แล้วทำให้เสียเวลาและความไว้วางใจ

```
ก่อนพูดว่า "ระบบขาด X" หรือ "ควรสร้าง Y เพิ่ม":

1. อ่าน core/00 ก่อน — เข้าใจ architecture ภาพรวม
2. ตรวจ platforms/ ทั้งหมด — มี folder สำหรับ X อยู่แล้วไหม?
3. ตรวจ CoreAiWorkspaces/07-decisions/ — มี ADR ที่ตัดสินใจเรื่องนี้แล้วไหม?
4. ตรวจ source docs — requirement บอกว่ายังไม่มีจริง ๆ หรือ?

→ ถ้าพบว่ามีอยู่แล้ว: ห้ามเสนอสร้างใหม่ — แจ้งผู้ใช้ว่ามีอยู่แล้วที่ไหน
→ ถ้าตรวจครบแล้วยังไม่พบ: เสนอได้ พร้อมระบุว่าตรวจแล้ว
```

**หลักการ:** AI มีหน้าที่ลดภาระผู้ใช้ ไม่ใช่สร้างภาระ
การเสนอสิ่งที่มีอยู่แล้ว = สร้างงานเพิ่มให้ผู้ใช้โดยไม่จำเป็น = ผิดบทบาท

### Scenario K — ไม่รู้ว่าควรเก็บข้อมูลที่ไหน

เกิดเมื่อ: พบข้อมูลใหม่ระหว่าง session แต่ไม่แน่ใจว่าควร log ลง work-log, สร้าง ADR, อัปเดต entity-register, หรือเขียนลง cross-project memory

```
ข้อมูลใหม่ที่ต้องเก็บ — ถามตามลำดับ:

1. เป็น architectural decision?
   → ADR (CoreAiWorkspaces/07-decisions/ADR-NNN-*.md + README.md)

2. เป็น entity ใหม่ หรือ status ของ entity เปลี่ยน?
   → Entity Register (CoreAiWorkspaces/07-decisions/entity-register.md)

3. เป็น pattern หรือ lesson ที่น่าจะใช้ได้กับโปรเจ็กต์อื่น?
   → Cross-Project Memory (~/ai-workspace/cross-project-memory.md)
   [ถามผู้ใช้ก่อนเสมอ — ไม่เขียนลง cross-project memory โดยไม่ได้รับอนุญาต]

4. เป็น progress, detail, หรือ decision ที่ทำเองในระหว่าง session?
   → Agent Diary + work-log-index (CoreAiWorkspaces/03-log/)

5. เป็น task ใหม่ หรือ status เปลี่ยน?
   → Task Board (CoreAiWorkspaces/02-task/task-board.md)

ถ้าตอบ "ใช่" หลายข้อ: เก็บในทุกที่ที่เกี่ยวข้อง — ไม่ mutual exclusive
ถ้าไม่ตรงกับข้อใดเลย: บันทึกไว้ใน work-log ก่อน แล้วระบุว่า "ยังไม่แน่ใจว่าควรอยู่ที่ไหน"
```

---

### Scenario M — ก่อนเริ่ม code หรือ commit ใหม่

เกิดเมื่อ: กำลังจะเริ่มแตะโค้ด หรือสร้าง commit ใหม่ในทุก task

**6-Step Pre-Code Checklist (บังคับทุก task):**

```
1. git status
   → มี uncommitted changes จาก task ก่อนไหม?
   → ถ้ามี: commit หรือ stash ก่อน — ห้ามปนกับงานใหม่

2. git branch --show-current
   → อยู่บน dev หรือ feature branch ที่ถูกต้องไหม?
   → ถ้าอยู่บน main/master: หยุด — แจ้งผู้ใช้ก่อนดำเนินการใดๆ

3. git branch --list "feature/*" "fix/*"
   → มี feature branch ค้างอยู่ไหม?
   → ถ้ามี: แจ้งผู้ใช้ รอ decision ก่อนสร้าง branch ใหม่ (กฎ One feature at a time)

4. ตรวจขนาดงาน
   → ≤2 ไฟล์? ทำบน dev ได้
   → ≥3 ไฟล์ หรือ feature/architecture/ADR-level? สร้าง feature branch จาก dev ก่อน
   → ไม่แน่ใจ? แยก branch ไว้ก่อน (safe-default)

5. task board reference
   → task นี้มี ID ใน task-board ไหม?
   → ถ้าไม่มี: เพิ่มก่อน หรือยืนยันว่า scope ชัดแล้ว

6. source reference
   → รู้ว่า implement จาก source doc ไหน?
   → ถ้าไม่รู้: ถามก่อน — ห้าม implement เดา
```

**ผลลัพธ์ที่ต้องการ:** ก่อนแตะโค้ดแต่ละ task — branch ถูก, ไม่มี uncommitted ค้าง, ไม่มี feature branch ซ้อน, task มี ID, scope ชัด

---

## 3. Escalation Levels

| Level | สถานการณ์ | การกระทำ | Scenarios |
|-------|-----------|----------|-----------|
| **Level 0 — Verify First** | ก่อนเริ่มแตะโค้ด / ก่อนเสนอสร้างใหม่ | ตรวจ branch + existing structure ก่อนเสมอ | M, L |
| **Level 1 — Log & Continue** | ผลกระทบต่ำ ย้อนกลับได้ | บันทึกการตัดสินใจใน work-log แล้วดำเนินต่อ | C, D, G, I, K |
| **Level 2 — Block & Flag** | ผลกระทบปานกลาง ไม่แน่ใจ | mark task blocked, อัปเดต work-status, รอมนุษย์ | A, B, E, F, H, J |
| **Level 3 — Stop Session** | ผลกระทบสูง ย้อนไม่ได้ หรือมีความเสี่ยง | หยุดทันที, บันทึกชัดเจนว่าทำไม, ไม่ดำเนินการต่อ | — (ดูเงื่อนไขด้านล่าง) |

สถานการณ์ที่ต้อง Level 3 เสมอ — ไม่ว่า scenario ใด:
- อาจทำให้ข้อมูลสูญหาย
- เกี่ยวข้องกับ security หรือ credentials
- ส่งผลต่อ production environment
- ขัดแย้งกับ requirement ที่ชัดเจน

---

## 4. ขอบเขตความรับผิดชอบ (Responsibility Boundary)

| ประเภทการตัดสินใจ | Solo — AI ทำได้ | Team — AI ทำได้ |
|------------------|-----------------|-----------------|
| Code style / formatting | ตัดสินใจได้เลย | ตัดสินใจได้เลย |
| Refactoring (logic เดิม) | ตัดสินใจได้เลย | ตัดสินใจได้เลย |
| เพิ่ม dependency ใหม่ | เสนอใน work-log รอ approve | เสนอใน work-log รอ approve |
| ตีความ scope ที่คลุมเครือ | เสนอ + ระบุ risk | Flag ไว้ รอมนุษย์ |
| เปลี่ยน architecture | สร้าง ADR draft | สร้าง ADR draft |
| เปลี่ยน requirement | **ห้ามเด็ดขาด — มนุษย์เท่านั้น** | **ห้ามเด็ดขาด — มนุษย์เท่านั้น** |
| Production operations | **ห้ามเด็ดขาด** | **ห้ามเด็ดขาด** |

---

## 5. หลักการสำคัญ

> **"Do less, document more."**
> การหยุดพร้อมบันทึกชัดเจน ดีกว่าการตัดสินใจเงียบ ๆ แล้วผิดพลาด

> **"ช่วยลดภาระ ไม่สร้างภาระ"**
> ถ้า AI เสนอสิ่งที่ทำให้ผู้ใช้ต้องทำงานมากขึ้น หรือเสนอสิ่งที่มีอยู่แล้ว = ผิดบทบาท

- ถ้าไม่แน่ใจระหว่าง Level 1 กับ Level 2: เลือก Level 2
- ถ้าไม่แน่ใจระหว่าง Level 2 กับ Level 3: เลือก Level 3
- placeholder ที่ชัดเจน ดีกว่าการเดาที่ดูสมเหตุสมผล
- **ก่อนเสนออะไรใหม่: ตรวจก่อนว่ามีอยู่แล้วหรือยัง** (Scenario L)

---

## 6. Status Tags ที่ใช้

| Tag | ความหมาย |
|-----|----------|
| `[BLOCKED]` | หยุดรอข้อมูลหรือการตัดสินใจ |
| `[BLOCKED: CONFLICT]` | มี requirement ขัดแย้ง รอ resolution |
| `[NEEDS HUMAN DECISION]` | ต้องการการตัดสินใจจากมนุษย์ก่อนดำเนินต่อ |
| `[NEEDS SOURCE VALIDATION]` | งานนี้ไม่มี source doc รองรับ ต้องตรวจสอบก่อน |
| `[FOUND-IN-PASSING]` | พบระหว่างทำงานอื่น ยังไม่ได้รับ assign |
| `[IN_PROGRESS: checkpoint saved]` | ทำไปบ้างแล้ว บันทึก checkpoint ไว้แล้ว |
| `[REVERSE-DOC]` | พบ undocumented code รอ human review |
| `[ENTITY:deprecated:X]` | entity X เลิกใช้แล้ว — ตรวจ entity-register ก่อนใช้ |
| `[ENTITY:superseded:X→Y]` | entity X ถูกแทนด้วย Y |
| `[ENTITY:proposed:X]` | entity X ยังรอ ADR |
| `<NEEDS_CLARIFICATION: ...>` | placeholder แทนข้อมูลที่ยังไม่มี |
