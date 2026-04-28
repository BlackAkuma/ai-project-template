# AI Decision Protocol Template

เอกสารนี้กำหนดว่า AI ควรตัดสินใจอย่างไรเมื่อเจอสถานการณ์คลุมเครือ ขัดแย้ง หรือไม่มีข้อมูล
นำไปวางใน `doc/04-way-of-work/ai-decision-protocol.md` ของโปรเจ็กต์

---

## 1. การตรวจสอบก่อนลงมือ (3-Question Check)

ก่อนทำงานใด ๆ ให้ตอบ 3 คำถามนี้:

1. ฉันรู้ผลลัพธ์ที่คาดหวังชัดเจนหรือไม่?
2. งานนี้สอดคล้องกับ source docs หรือไม่?
3. ถ้าฉันทำผิด งานนี้ย้อนกลับได้หรือไม่?

→ ถ้าตอบ "ใช่" ทั้ง 3 ข้อ: ดำเนินการได้เลย
→ ถ้าตอบ "ไม่" ข้อใดข้อหนึ่ง: ดู Decision Tree ด้านล่าง

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

---

## 3. Escalation Levels

| Level | สถานการณ์ | การกระทำ |
|-------|-----------|----------|
| **Level 1 — Log & Continue** | ผลกระทบต่ำ ย้อนกลับได้ | บันทึกการตัดสินใจใน work-log แล้วดำเนินต่อ |
| **Level 2 — Block & Flag** | ผลกระทบปานกลาง ไม่แน่ใจ | mark task blocked, อัปเดต work-status, รอมนุษย์ |
| **Level 3 — Stop Session** | ผลกระทบสูง ย้อนไม่ได้ หรือมีความเสี่ยง | หยุดทันที, บันทึกชัดเจนว่าทำไม, ไม่ดำเนินการต่อ |

สถานการณ์ที่ต้อง Level 3 เสมอ:
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

- ถ้าไม่แน่ใจระหว่าง Level 1 กับ Level 2: เลือก Level 2
- ถ้าไม่แน่ใจระหว่าง Level 2 กับ Level 3: เลือก Level 3
- placeholder ที่ชัดเจน ดีกว่าการเดาที่ดูสมเหตุสมผล

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
| `<NEEDS_CLARIFICATION: ...>` | placeholder แทนข้อมูลที่ยังไม่มี |
