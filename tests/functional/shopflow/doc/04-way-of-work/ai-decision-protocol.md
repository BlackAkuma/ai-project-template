# AI Decision Protocol — ShopFlow

นำมาจาก `core/11-ai-decision-protocol-template.md`
ปรับเพิ่มเติมสำหรับ ShopFlow ได้ที่ section "Project-Specific Rules" ด้านล่าง

---

## 1. การตรวจสอบก่อนลงมือ (3-Question Check)

ก่อนทำงานใด ๆ ให้ตอบ 3 คำถามนี้:

1. ฉันรู้ผลลัพธ์ที่คาดหวังชัดเจนหรือไม่?
2. งานนี้สอดคล้องกับ source docs หรือไม่?
3. ถ้าฉันทำผิด งานนี้ย้อนกลับได้หรือไม่?

→ ถ้าตอบ "ใช่" ทั้ง 3 ข้อ: ดำเนินการได้เลย
→ ถ้าตอบ "ไม่" ข้อใดข้อหนึ่ง: ดู Decision Tree

---

## 2. Decision Tree ตามสถานการณ์

### Scenario A — Task คลุมเครือ
```
→ ดูใน task board ว่ามี task คล้ายกันที่เสร็จแล้วไหม
→ ถ้าไม่มี: ตรวจ source docs
→ ถ้ายังไม่ชัด: STOP → [BLOCKED] + อธิบายสิ่งที่ต้องการ
```

### Scenario B — Source docs ขัดแย้งกับ code
```
→ ตรวจว่าอันไหนใหม่กว่า
→ สร้าง extension doc บันทึกความขัดแย้ง
→ work-status: [NEEDS HUMAN DECISION]
```

### Scenario C — Scope creep
```
→ ทำเฉพาะ scope เดิม
→ สร้าง task ใหม่สำหรับส่วนที่เกิน
```

### Scenario D — พบ bug ไม่เกี่ยว task ปัจจุบัน
```
→ สร้าง task [FOUND-IN-PASSING]
→ กลับทำ task เดิม
```

### Scenario E — Requirements ขัดแย้ง
```
→ สร้าง extension doc
→ task: [BLOCKED: CONFLICT]
```

### Scenario F — ไม่มีข้อมูล
```
→ placeholder: <NEEDS_CLARIFICATION: ...>
→ บันทึก gap ใน work-status
```

### Scenario G — Context ใกล้เต็ม
```
→ บันทึก checkpoint ใน work-log
→ mark task: [IN_PROGRESS: checkpoint saved]
```

### Scenario H — Gap ระหว่าง task board กับ source
```
→ ห้าม implement จนกว่าจะระบุ gap
→ gap เล็ก: อัปเดต task แล้วบันทึก log
→ gap ใหญ่: [NEEDS HUMAN DECISION]
```

### Scenario I — Code ไม่มี doc
```
→ ทำ reverse-document
→ task: [REVERSE-DOC]
```

### Scenario J — พบ [ENTITY:deprecated] tag
```
→ ห้ามใช้ entity ต่อ
→ เปิด entity-register.md
→ ตรวจ replaced_by และ ADR
```

### Scenario K — ไม่รู้เก็บข้อมูลที่ไหน
```
1. Architecture decision? → ADR
2. Entity เปลี่ยน? → Entity Register
3. Cross-project pattern? → cross-project-memory (ถามก่อน)
4. Session progress? → work-log + agent diary
5. Task? → task-board
```

---

## 3. Escalation Levels

| Level | สถานการณ์ | การกระทำ |
|-------|-----------|----------|
| L1 — Log & Continue | ผลกระทบต่ำ ย้อนได้ | บันทึกแล้วทำต่อ |
| L2 — Block & Flag | ปานกลาง ไม่แน่ใจ | mark blocked + รอมนุษย์ |
| L3 — Stop Session | สูง ย้อนไม่ได้ | หยุดทันที + บันทึก |

**Default:** ถ้าไม่แน่ใจ — Do less, document more

---

## Project-Specific Rules

*(เพิ่มได้ตามต้องการ)*
