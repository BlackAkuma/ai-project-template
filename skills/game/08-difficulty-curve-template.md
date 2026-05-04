# Difficulty Curve Template

ออกแบบ curve ความยากของเกมก่อน implement ระบบใด ๆ ที่กระทบความท้าทาย
เก็บใน `doc/08-design/difficulty-curve.md`

สร้างไฟล์นี้ก่อน milestone แรก — ปรับได้ทุก milestone แต่ต้องมีอยู่เสมอ

---

## แนวคิดหลักที่ต้องเข้าใจก่อนเขียน

### 4 Difficulty Philosophies — เลือก 1

| Philosophy | ความหมาย | เหมาะกับ |
|-----------|---------|---------|
| **Mastery Challenge** | ความยากคือ product — ผู้เล่นซื้อ challenge | Dark Souls-style, hardcore platformer |
| **Accessible Depth** | ง่ายเข้าถึงได้ แต่มีความลึกให้ขุด | Puzzle game, casual-to-core |
| **Narrative Service** | ความยากรับใช้เรื่อง — ตึงเมื่อ drama ตึง | Story game, visual novel hybrid |
| **Relaxed Engagement** | ไม่มีความล้มเหลวจริง — เน้น exploration | Walking sim, cozy game |

### Difficulty Axes — แยก dimension ให้ชัด

ความยากไม่ใช่ตัวเลขเดียว แต่ประกอบจาก axis ต่าง ๆ:

| Axis | คือ | ตัวอย่าง lever |
|------|-----|--------------|
| **Execution** | ความแม่นยำที่ต้องการ | enemy speed, hitbox size, timing window |
| **Knowledge** | ข้อมูลที่ต้องรู้ก่อน | mechanic ที่ต้อง learn, pattern ของ boss |
| **Resource** | ทรัพยากรที่มีจำกัด | HP, ammo, time, lives |
| **Decision** | ความซับซ้อนในการตัดสินใจ | จำนวน option, ผลลัพธ์ที่ต้องประเมิน |
| **Time** | แรงกดดันจากเวลา | timer, spawn rate, อัตราการโจมตี |

### Sawtooth Pattern — โครงสร้าง macro

```
ความยาก
   │        ╱╲      ╱╲        ╱╲
   │      ╱    ╲  ╱    ╲    ╱    ╲
   │    ╱        ╲        ╲╱
   │  ╱  รวบทักษะ  boss   พัก   boss
   │╱
   └────────────────────────────── เวลา
   Tutorial  Early     Mid      Late
```

ผู้เล่นต้องรู้สึก: เรียน → เก่งขึ้น → ถูกท้าทายใหม่ → ผ่านได้ → รู้สึกดี → วนซ้ำ

---

## Template

```md
# Difficulty Curve — <PROJECT_NAME>

อัปเดตล่าสุด: YYYY-MM-DD
Milestone: [M1 / M2 / ...]

---

## 1. Difficulty Philosophy

**เราเลือก:** [Mastery Challenge / Accessible Depth / Narrative Service / Relaxed Engagement]

**เหตุผล:** [1–2 ประโยค ว่าทำไม philosophy นี้ถึงเหมาะกับ player fantasy ใน GDD]

**ผลที่ตามมา:**
- สิ่งที่เราจะทำ: [เช่น: ไม่มี auto-save กลาง level]
- สิ่งที่เราจะไม่ทำ: [เช่น: ไม่มี assist mode]

---

## 2. Difficulty Axes ของเกมนี้

Axis ที่เราใช้ (เลือกที่เกี่ยวข้องกับ game เท่านั้น):

| Axis | ใช้ใช่/ไม่ | Primary Lever | Range (1–10) Early → Late |
|------|----------|--------------|--------------------------|
| Execution | | | → |
| Knowledge | | | → |
| Resource | | | → |
| Decision | | | → |
| Time | | | → |

**หมายเหตุ:** อย่าเพิ่มทุก axis พร้อมกัน — cognitive overload เกิดเมื่อ 3+ axis เพิ่มพร้อมกัน

---

## 3. Curve Overview

| Phase | เวลา (ประมาณ) | ความยากรวม (1–10) | จุดประสงค์ |
|-------|-------------|-------------------|---------|
| Tutorial | นาทีที่ 0–[N] | 1–2 | สอน core mechanic โดยไม่มีโทษ |
| Early | [X]–[Y] นาที | 2–4 | ให้ผู้เล่นรู้สึกเก่ง สร้าง confidence |
| Mid | [Y]–[Z] นาที | 4–7 | ท้าทายจริง รวม mechanic หลายอย่าง |
| Late | [Z]+ นาที | 6–9 | ทดสอบทักษะทั้งหมด |
| Climax | [boss/final] | 8–10 | จุดสูงสุด ก่อน resolution |

---

## 4. First-Hour Breakdown

80% ของผู้เล่นที่หยุดเล่น หยุดในชั่วโมงแรก — ออกแบบให้ละเอียดที่สุด

| ช่วงเวลา | สิ่งที่เกิดขึ้น | Mechanic ที่แนะนำ | ความยาก |
|---------|-------------|-----------------|--------|
| นาที 0–2 | [hook แรก] | ไม่มี — ดูก่อน | 0 |
| นาที 2–5 | [core action แรก] | [mechanic ที่ 1] | 1 |
| นาที 5–10 | [challenge แรก] | [mechanic ที่ 1 ใน context] | 2–3 |
| นาที 10–20 | [mechanic ที่ 2] | [สอนแยก ยังไม่รวม] | 3 |
| นาที 20–30 | [รวม mechanic 1+2] | [challenge รวม] | 4 |
| นาที 30–60 | [first real challenge] | [ทดสอบทักษะทั้งที่สอน] | 5 |

**กฎ:** ผู้เล่นไม่สามารถเรียน 2 ทักษะพร้อมกันภายใต้แรงกดดัน — แนะนำทีละอย่าง

---

## 5. Skill Teaching Chain

ทุก mechanic ที่ใช้ต้องถูกสอนก่อนถูกทดสอบจริง:

| Mechanic | สอนตอนไหน | ทดสอบครั้งแรกตอนไหน | Notes |
|---------|----------|-------------------|-------|
| [mechanic] | [ช่วงเวลา / scene] | [ช่วงเวลา / scene] | [ห่างกันพอให้ฝึก] |

**Gap ที่อันตราย:** ถ้า "สอน" และ "ทดสอบ" ห่างกันน้อยกว่า 2 นาที → ผู้เล่นยังไม่พร้อม

---

## 6. Difficulty Spikes & Valleys

| จุด | ประเภท | ความยาก | เหตุผลที่ตั้งใจ |
|----|--------|--------|--------------|
| [boss / ด่าน / moment] | Spike | 8/10 | [ทดสอบทักษะ X ก่อน progression] |
| [rest area / safe zone] | Valley | 2/10 | [ให้ผู้เล่นหายใจ สะสมทรัพยากร] |

**กฎ:** ทุก spike ต้องตามด้วย valley — ผู้เล่นที่เหนื่อยจะออกจากเกม

---

## 7. Tuning Levers

ค่าที่ปรับได้เพื่อควบคุมความยาก — ทุกค่าต้องอยู่ใน config (ตาม G-01):

| Lever | Config Key | ค่าตอนนี้ | ผลเมื่อเพิ่ม | ผลเมื่อลด |
|-------|-----------|---------|------------|---------|
| [เช่น: enemy speed] | balance.enemySpeed | 3.0 | ยากขึ้น (execution) | ง่ายขึ้น |

---

## 8. Validation Checklist

ตรวจหลัง playtest แต่ละรอบ:

**First-Hour:**
- [ ] ผู้เล่นใหม่เข้าใจ core loop ภายใน 3 นาทีโดยไม่อ่าน tutorial
- [ ] ไม่มีจุดที่ผู้เล่นหยุดนิ่งมากกว่า 30 วินาทีโดยไม่รู้ว่าต้องทำอะไร
- [ ] ความล้มเหลวครั้งแรกรู้สึกยุติธรรม ไม่ใช่สับสน

**Mid Game:**
- [ ] ผู้เล่นไม่รู้สึกซ้ำซากใน 30 นาที
- [ ] Spike แต่ละจุดผู้เล่นผ่านได้ใน ≤ 5 ครั้ง (ถ้าไม่ผ่าน → ปรับ lever)

**Full Game:**
- [ ] ผู้เล่นที่ผ่าน late game รู้สึกว่าตัวเองเก่งขึ้น ไม่ใช่เกมง่ายลง
```

---

## Compliance Rules

| Code | สิ่งที่ตรวจ |
|------|-----------|
| G-09 | feature ใหม่ที่กระทบความยากไม่ได้อัปเดต difficulty curve |
| G-10 | Tuning lever ไม่มีใน config (hardcoded) |
