# FDD-001: Hex Grid Movement System

อัปเดตล่าสุด: 2026-04-30
สถานะ: Approved
ผู้เขียน: AI session — 2026-04-30
Task: T-003
Source: doc/00-source/versions/v0.1/game-design-document.md §3
Platform: Phaser 3 / HTML5

---

## ส่วนที่ 1 — ภาพรวมและเหตุผล

ระบบ movement สำหรับ HexGame — ให้ผู้เล่นเดิน unit บน hex grid
จำเป็นเพราะเป็น core mechanic หลักของเกม — ทุก feature อื่นขึ้นอยู่กับนี้

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 2 — ประสบการณ์ผู้เล่น (MDA)

| ระดับ | คำถาม | ตอบ |
|-------|--------|-----|
| **Mechanics** (กติกา/ระบบ) | กฎและระบบที่ AI/dev สร้าง | Unit มี movement_range — คลิก hex ที่อยู่ในระยะ → unit เดินไปตาม path หาไปเอง |
| **Dynamics** (พฤติกรรมที่เกิดขึ้น) | ผู้เล่นจะทำอะไรเมื่อมีระบบนี้? | ผู้เล่นจะวางแผน route ก่อนเดิน, หลีกเลี่ยง obstacle, ใช้ movement_range อย่างมีประสิทธิภาพ |
| **Aesthetics** (ความรู้สึก) | อยากให้ผู้เล่นรู้สึกอะไร? | รู้สึกถึงการวางแผน, รู้สึกว่า unit เป็น "ตัวของตัวเอง" เมื่อเดิน |

ลำดับการกระทำ: คลิก unit → เห็น hex ที่เดินได้ highlight → คลิก hex ปลายทาง → unit เดิน

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 3 — กลไกและเงื่อนไข

States ที่เป็นไปได้:
- `idle` — unit ยืนอยู่ รอคำสั่ง
- `selected` — ผู้เล่นคลิก unit แล้ว เห็น reachable hexes
- `moving` — unit กำลังเดิน ห้าม interrupt
- `exhausted` — ใช้ movement แล้ว ไม่สามารถเดินซ้ำ

เงื่อนไขการเปลี่ยน state:
- idle → selected: ผู้เล่นคลิก unit
- selected → moving: ผู้เล่นคลิก hex ที่ reachable
- selected → idle: ผู้เล่นคลิก hex ที่ไม่ reachable หรือ cancel
- moving → exhausted: unit ถึงปลายทาง
- exhausted → idle: เริ่ม turn ใหม่

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 4 — สูตรและค่าตัวแปร

```
movement_range: 3        // config: balance.json → units.default.movement_range | range: 1–6
move_speed_px: 120       // config: gameplay.json → animation.moveSpeedPx | range: 60–300
highlight_color: 0x44ff44 // config: ui.json → colors.reachable | hex color
path_algorithm: "a-star" // config: gameplay.json → pathfinding.algorithm | "a-star" | "bfs"
```

ทุกค่าอ้างอิง config key — ห้าม hardcode ใน game logic

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 5 — Asset ที่ต้องการ

| Asset | ประเภท | Path | หมายเหตุ |
|-------|--------|------|---------|
| unit_walk | Spritesheet | assets/sprites/unit_walk.png | 4 frames, 64x64 |
| hex_highlight | Image | assets/ui/hex_highlight.png | semi-transparent green |

<!-- [AI] เขียน section นี้เสร็จแล้ว รอ approve ก่อนไปส่วนถัดไป -->

---

## ส่วนที่ 6 — Dependencies

- ต้องมี hex grid renderer (T-002) เสร็จก่อน
- A-star pathfinding library ต้องถูก include ใน project

---

## ส่วนที่ 7 — Out of Scope (FDD นี้)

- Attack range (FDD อื่น)
- Terrain cost / obstacle types (phase 2)
- Multiplayer sync (phase 2)

---

## ส่วนที่ 8 — เกณฑ์การยืนยัน (Playtest Criteria)

- [ ] Unit เดินไปถึง hex ที่คลิกได้ใน 100% ของกรณีที่ reachable
- [ ] Highlight แสดงถูกต้อง — ไม่เกิน movement_range
- [ ] Animation เล่นตั้งแต่ต้นถึงปลายไม่กระตุก
- [ ] เดินผ่าน occupied hex ไม่ได้
- [ ] ประสิทธิภาพ: ≤ 2ms per move calculation บน grid ขนาด 20x20
- [ ] หลัง exhausted แล้ว unit ตอบสนอง click ไม่ได้ (ไม่มี accidental move)
