# Balance Check Template

Protocol สำหรับตรวจสอบความสมดุลของตัวเลขในเกม
ใช้ก่อน milestone close หรือเมื่อมีการเปลี่ยน config ที่กระทบ gameplay

---

## หลักการ

ค่าตัวเลขทุกตัวต้องมาจาก config เสมอ (ตาม G-01) — balance check จึงตรวจที่ config file โดยตรง ไม่ใช่ที่ code

**AI ตรวจได้:** ค่าอยู่ใน range, สูตรคำนวณถูกต้อง, ค่าไม่ขัดแย้งกัน
**มนุษย์ต้องตัดสิน:** รู้สึกสมดุลหรือไม่ (fun factor)

---

## Balance Check Report Template

```md
# Balance Check — [Feature / Milestone]

วันที่: YYYY-MM-DD
Config files ที่ตรวจ: config/gameplay.json, config/balance.json
FDD Reference: FDD-NNN (ถ้าเกี่ยวข้อง)

---

## 1. Range Validation

ตรวจว่าทุกค่าอยู่ใน range ที่ FDD กำหนด:

| Config Key | ค่าปัจจุบัน | Range (FDD) | ผ่าน |
|-----------|------------|-------------|------|
| gameplay.playerSpeed | 5.0 | 1.0–20.0 | ✓ |
| gameplay.jumpForce | 12.0 | 5.0–25.0 | ✓ |
| balance.enemyDamage | 99.0 | 1.0–50.0 | ✗ |

## 2. Formula Validation

ตรวจสูตรที่ FDD ส่วนที่ 4 กำหนด:

| สูตร | ค่า Input | ผลที่คาด | ผลจริง | ผ่าน |
|-----|---------|---------|--------|------|
| damage = base * (1 + level * multiplier) | base=10, level=5, multiplier=0.2 | 20.0 | 20.0 | ✓ |

## 3. Conflict Check

ตรวจว่าค่าที่เกี่ยวข้องกันไม่ขัดแย้ง:

| ประเด็น | ค่า A | ค่า B | ขัดแย้ง |
|--------|------|------|--------|
| player HP vs max enemy damage per hit | hp: 100 | damage: 99 | ✗ (one-shot possible) |

## 4. Human Feel Assessment

*ต้องให้มนุษย์กรอกหลัง playtest*

- ค่าที่รู้สึกว่าเร็ว/แรง/ช้า/อ่อนเกินไป:
- ค่าที่อยากลองปรับ:
- สรุป: สมดุลดีพอสำหรับ milestone นี้ ใช่ / ไม่ใช่

## สรุป

- [ ] Range validation: ผ่านทั้งหมด
- [ ] Formula validation: ผ่านทั้งหมด
- [ ] Conflict check: ไม่มีปัญหา
- [ ] Human feel: ยืนยันแล้ว

**ปัญหาที่ต้องแก้:**
| ค่า | ปัญหา | Action |
|-----|-------|--------|
| balance.enemyDamage | เกิน range FDD | ปรับให้อยู่ใน 1.0–50.0 |
```

---

---

## ตัวอย่าง Balance Check ที่ PASS ครบทุกหัวข้อ

ตัวอย่างนี้แสดงว่า report ที่ผ่านทุก check หน้าตาเป็นอย่างไร
ใช้เป็น reference เมื่อต้องการรู้ว่า "ผ่าน" คืออะไร

```md
# Balance Check — Sprint 2 Milestone: Combat System

วันที่: 2026-04-28
Config files ที่ตรวจ: config/gameplay.json, config/balance.json
FDD Reference: FDD-002 Section 4 — Combat Values

---

## 1. Range Validation

| Config Key | ค่าปัจจุบัน | Range (FDD) | ผ่าน |
|-----------|------------|-------------|------|
| gameplay.playerSpeed | 6.0 | 1.0–20.0 | ✓ |
| gameplay.jumpForce | 14.0 | 5.0–25.0 | ✓ |
| balance.playerHP | 100 | 50–200 | ✓ |
| balance.enemyDamage | 18.0 | 1.0–50.0 | ✓ |
| balance.enemyHP | 40 | 10–150 | ✓ |
| balance.expPerKill | 25 | 5–100 | ✓ |

## 2. Formula Validation

| สูตร | ค่า Input | ผลที่คาด | ผลจริง | ผ่าน |
|-----|---------|---------|--------|------|
| damage = base * (1 + level * multiplier) | base=10, level=5, mult=0.2 | 20.0 | 20.0 | ✓ |
| exp = base * enemy_tier | base=25, tier=2 | 50 | 50 | ✓ |
| ttk = playerHP / enemyDamage | hp=100, dmg=18 | ~5.6 hits | 5.6 | ✓ |

## 3. Conflict Check

| ประเด็น | ค่า A | ค่า B | ขัดแย้ง |
|--------|------|------|--------|
| playerHP vs max enemy damage per hit | hp: 100 | damage: 18 | ✓ ไม่ one-shot |
| expPerKill vs level threshold | exp: 25 | next_level: 100 | ✓ ต้องฆ่า 4 ตัว สมเหตุ |
| playerSpeed vs level layout | speed: 6.0 | min_gap: 3.0u | ✓ ไม่กระโดดข้ามได้ |

## 4. Human Feel Assessment

- ค่าที่รู้สึกว่าเร็ว/แรง/ช้า/อ่อนเกินไป: ไม่มี — ทุกค่าอยู่ใน comfort zone
- ค่าที่อยากลองปรับ: enemyHP อาจเพิ่มเป็น 50 ใน level 3+ แต่ไม่จำเป็นตอนนี้
- สรุป: สมดุลดีพอสำหรับ milestone นี้ **ใช่**

## สรุป

- [x] Range validation: ผ่านทั้งหมด (6/6)
- [x] Formula validation: ผ่านทั้งหมด (3/3)
- [x] Conflict check: ไม่มีปัญหา (3/3)
- [x] Human feel: ยืนยันแล้ว

**ปัญหาที่ต้องแก้:** ไม่มี — พร้อม close milestone
```

---

## Compliance Rule เพิ่มเติม

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| G-07 | Config value เกิน range ที่ FDD กำหนด | ค่าใน config.json เกิน range ที่ระบุใน FDD ส่วนที่ 4 |

Violation tag: `// REFACTOR-PENDING[G-07]: enemyDamage 99.0 exceeds FDD range 1.0–50.0 — T-XXX`
