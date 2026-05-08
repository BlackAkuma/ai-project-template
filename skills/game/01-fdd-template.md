# Feature Design Document (FDD) Template

ใช้ก่อนเริ่ม implement game feature ใหม่ทุกครั้ง
เก็บใน `CoreAiWorkspaces/08-design/[feature-name].md`

FDD ต้องได้รับ approve ก่อน task จะออกจาก `design_validate` ไป `in_progress`
task lifecycle: `todo → design_validate → in_progress → playtest → review → done`
ส่วนที่ 8 ของ FDD กำหนดเกณฑ์ที่ต้องผ่านในขั้น playtest ก่อน task จะออกจาก `playtest` ไป `review`

---

## กฎการเขียนทีละส่วน

AI ต้องเขียน FDD ทีละ section บันทึกไฟล์ แล้วรอคนยืนยันก่อนเขียน section ถัดไป
ห้ามเขียนครบทุก section แล้วค่อยรอ approve ทีเดียว — ป้องกันงานสูญหายเมื่อ context เต็ม

เมื่อเขียน section เสร็จ AI ต้องพูดว่า: **"Section [N] เสร็จแล้ว ยืนยันได้เลยหรือแก้ไขก่อน?"**

---

## Template

```md
# FDD-[NNN]: [ชื่อ Feature]

อัปเดตล่าสุด: YYYY-MM-DD
สถานะ: Draft / Approved / Superseded
ผู้เขียน: [ชื่อ หรือ "AI session — YYYY-MM-DD"]
Task: T-XXX
Source: CoreAiWorkspaces/00-source/versions/vX.X/...
Platform: [Unity / Godot / Phaser / HTML5 / ฯลฯ]

---

## ส่วนที่ 1 — ภาพรวมและเหตุผล

feature นี้คืออะไร ทำไมต้องมี ใครใช้ ใช้ตอนไหนในเกม

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 2 — ประสบการณ์ผู้เล่น (MDA)

ใช้กรอบ MDA วิเคราะห์ feature ก่อนออกแบบ:

| ระดับ | คำถาม | ตอบ |
|-------|--------|-----|
| **Mechanics** (กติกา/ระบบ) | กฎและระบบที่ AI/dev สร้าง | — |
| **Dynamics** (พฤติกรรมที่เกิดขึ้น) | ผู้เล่นจะทำอะไรเมื่อมีระบบนี้? | — |
| **Aesthetics** (ความรู้สึก) | อยากให้ผู้เล่นรู้สึกอะไร? | — |

อธิบายจากมุมมองผู้เล่น ไม่ใช่มุมมอง developer:
- ผู้เล่นเห็น / ได้ยิน / รู้สึกอะไร?
- ลำดับการกระทำ: กดอะไร → เกิดอะไร → ได้อะไร
- ความรู้สึกที่ต้องการ (เช่น: ตื่นเต้น, ผ่อนคลาย, กดดัน)

### Game Feel

คุณภาพ kinesthetic ของ feature — ต่างจาก MDA ตรงที่เน้น "ความรู้สึกขณะควบคุม" ไม่ใช่แค่ outcome

| ด้าน | Target | วิธีวัด |
|------|--------|--------|
| Input responsiveness | < [N] ms จาก input ถึง visual response | performance.mark() |
| Animation timing | anticipation: [N] frames / follow-through: [N] frames | frame count |
| Impact moment | freeze [N] frames + screen shake [N px] amplitude | ดูใน playtest |
| น้ำหนัก/ความรู้สึก | [เช่น: "หนักและมีน้ำหนัก" / "เบาและไว"] | human playtest เท่านั้น |

**Feel reference:** [ระบุเกมที่ feel ใกล้เคียง เช่น "jump mechanic แบบ Celeste — precise และ forgiving"]

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 3 — กลไกและเงื่อนไข

กฎที่แน่นอนและครบถ้วน ไม่คลุมเครือ:
- state ทั้งหมดที่เป็นไปได้
- เงื่อนไขการเปลี่ยน state (ถ้า X → เปลี่ยนเป็น Y)
- สิ่งที่ทำได้ / ทำไม่ได้ในแต่ละ state

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 4 — สูตรและค่าตัวแปร

ค่าตัวเลขและสูตรทั้งหมด — ทุกค่าต้องอ้างอิง config key ห้าม hardcode:

```
player_speed: 5.0    // config: gameplay.json → player.speed | range: 1.0–20.0
jump_force: 10.0     // config: gameplay.json → player.jumpForce | range: 5.0–25.0
damage: base * (1 + level * multiplier)  // multiplier: config: balance.json → levelScale
```

ทุกค่าต้องระบุ: config key, ไฟล์ที่อยู่, ค่า default, range ที่ยอมรับได้

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 5 — กรณีพิเศษและการจัดการข้อผิดพลาด

สิ่งที่อาจเกิดนอกเหนือจาก happy path:
- ถ้าผู้เล่นทำ X ระหว่าง state Y → ต้องเกิดอะไร?
- ค่าที่อยู่ที่ขอบเขต (min, max, zero, overflow)
- กรณี async หรือ network (ถ้าเกี่ยวข้อง)
- สิ่งที่ต้อง guard ไว้ไม่ให้พัง

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 6 — ความสัมพันธ์กับระบบอื่น

- feature อื่นที่ feature นี้ต้องพึ่ง
- system ที่จะได้รับผลกระทบเมื่อ feature นี้เปลี่ยน
- ลำดับที่แนะนำในการ implement

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 7 — ข้อกำหนดด้านประสิทธิภาพ

- Target FPS: [60 / 30 / ฯลฯ]
- Budget ของ feature นี้: ไม่เกิน X ms per frame
- Memory: [ถ้าเกี่ยวข้อง]
- ข้อระวังเฉพาะ platform: [mobile / web / desktop]
- จุดที่ต้อง profile หลัง implement

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 8 — เกณฑ์การยืนยันว่าเสร็จ

feature นี้ถือว่าเสร็จเมื่อ:
- [ ] [พฤติกรรมที่ต้องเกิดขึ้น]
- [ ] [ค่าที่วัดได้และผ่านเกณฑ์]
- [ ] [กรณีพิเศษที่ต้องผ่าน]
- [ ] ประสิทธิภาพอยู่ใน budget ที่กำหนด
- [ ] ทดสอบบน platform เป้าหมายแล้ว

<!-- [AI] FDD ครบทุกส่วน รอ approve ขั้นสุดท้ายก่อนเปลี่ยนสถานะเป็น Approved -->
```

---

## FDD Index (สำหรับ `CoreAiWorkspaces/08-design/README.md`)

```md
<!-- AI-CONTEXT
fdd_count: <จำนวน FDD ทั้งหมด>
pending_approve: <FDD-NNN> | none
latest: FDD-<NNN>
updated: <CURRENT_DATE>
-->

# Design Documents — <PROJECT_NAME>

| FDD | Feature | สถานะ | Task | อัปเดตล่าสุด |
|-----|---------|-------|------|------------|
| FDD-001 | [ชื่อ feature] | Draft / Approved | T-XXX | YYYY-MM-DD |
```
