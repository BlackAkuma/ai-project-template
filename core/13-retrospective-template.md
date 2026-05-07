# Retrospective Template

ใช้ทบทวนการทำงานร่วมกันระหว่างทีมและ AI ในช่วงเวลาหนึ่ง
เก็บไว้ใน `ai/05-summary/YYYY/YYYY-MM-retrospective.md` หรือ `ai/05-summary/YYYY/MM/`

ควรทำทุก milestone หรือทุก sprint หรืออย่างน้อยทุกเดือน

---

## Template

```markdown
# Retrospective — <PROJECT_NAME> — <PERIOD>

**วันที่ทำ Retrospective:** YYYY-MM-DD
**ช่วงที่ทบทวน:** YYYY-MM-DD ถึง YYYY-MM-DD
**Milestone หรือ Sprint:** <M1 / Sprint 3 / ฯลฯ>
**Source Version ที่ใช้อยู่:** <CURRENT_SOURCE_VERSION>
**ผู้ร่วม Retrospective:** <ชื่อทีมหรือ solo>

---

## 1. สิ่งที่ทำได้ดี (Keep Doing)

สิ่งที่ทำแล้วได้ผล ควรทำต่อ:

- [ ] <ตัวอย่าง: session startup อ่านไฟล์ครบก่อนเริ่มเสมอ>
- [ ] <ตัวอย่าง: สร้าง ADR ก่อนตัดสินใจ library ใหม่ ทำให้ session ถัดไปไม่ต้องเถียงซ้ำ>

---

## 2. สิ่งที่ต้องปรับ (Stop / Change)

สิ่งที่เสียเวลาหรือสร้างปัญหา:

- [ ] <ตัวอย่าง: task description คลุมเครือเกินไป AI ต้องถามบ่อย>
- [ ] <ตัวอย่าง: ลืมอัปเดต work-status ตอนจบ session หลายครั้ง>

---

## 3. สิ่งที่อยากลองทำ (Try Next)

ไอเดียหรือแนวทางใหม่ที่ยังไม่ได้ทดลอง:

- [ ] <ตัวอย่าง: ลอง template เฉพาะสำหรับ bug task เพื่อให้ reproduction steps ชัดขึ้น>
- [ ] <ตัวอย่าง: เพิ่ม review trigger ใน ADR ที่มีอยู่>

---

## 4. การทำงานร่วมกับ AI — สิ่งที่เรียนรู้

สิ่งที่ค้นพบว่าทำให้ AI ทำงานได้ดีขึ้นหรือแย่ลง:

**ได้ผลดี:**
- <ตัวอย่าง: บอก AI ก่อนว่า session นี้มีเวลาจำกัด ทำให้ AI โฟกัสเฉพาะสิ่งสำคัญ>

**ไม่ได้ผล:**
- <ตัวอย่าง: ให้ AI ตีความ requirement ที่คลุมเครือเองโดยไม่บอก context>

---

## 5. Way-of-Work ที่ต้องอัปเดต

ถ้ามีสิ่งที่ควรเปลี่ยนใน working guidelines ให้ระบุที่นี่:

| ไฟล์ที่ต้องแก้ | การเปลี่ยนแปลง | ความเร่งด่วน |
|--------------|--------------|-------------|
| `way-of-work.md` | <อธิบาย> | High / Medium / Low |
| `ai-decision-protocol.md` | <อธิบาย> | High / Medium / Low |

---

## 6. Metrics (ถ้ามี)

| Metric | ค่า | หมายเหตุ |
|--------|-----|---------|
| Tasks completed | X / Y | |
| Tasks blocked ≥ 1 วัน | X | |
| ADRs สร้างในรอบนี้ | X | |
| Session ที่ลืมอัปเดต status | X | |

---

## 7. สรุป — สิ่งที่จะเปลี่ยนใน Sprint/Milestone ถัดไป

1. <การเปลี่ยนแปลงที่ตกลงจะทำ>
2. <การเปลี่ยนแปลงที่ตกลงจะทำ>
```

---

## กฎการใช้งาน

- ทำ retrospective ทุก milestone, sprint, หรืออย่างน้อยทุกเดือน
- ถ้ามีการเปลี่ยน way-of-work ให้อัปเดตไฟล์จริงทันที อย่าปล่อยไว้ใน retrospective อย่างเดียว
- AI session สามารถเตรียม draft retrospective ให้ได้โดยดูจาก work-log-index ของช่วงนั้น
- มนุษย์ต้อง review และเพิ่มมุมมองที่ AI ไม่เห็น (เช่น ความรู้สึกของทีม, external factor)
