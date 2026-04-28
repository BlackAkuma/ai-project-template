# Game Development Skill Pack

เปิดใช้งานเมื่อโปรเจ็กต์เป็น game หรือ web game
อ่านไฟล์ทั้งหมดในโฟลเดอร์นี้ต่อจาก core templates

---

## เมื่อไหร่ที่ควรใช้ skill pack นี้

ใช้เมื่อโปรเจ็กต์มีลักษณะอย่างน้อย 1 ข้อ:
- มี gameplay loop (win/lose condition, scoring, progression)
- มี real-time updates หรือ game loop (update per frame)
- มี physics หรือ collision detection
- มี player input → game state → render cycle
- เป็น web game, browser game, mobile game, desktop game

**ครอบคลุมทุก platform:** Unity, Godot, Phaser, Three.js, HTML5 Canvas, WebGL, PixiJS, native mobile game

---

## ไฟล์ในชุดนี้

| ไฟล์ | หน้าที่ |
|------|--------|
| `00-game-skill-overview.md` | ภาพรวม (ไฟล์นี้) |
| `01-fdd-template.md` | Feature Design Document — ออกแบบ feature ก่อนโค้ด |
| `02-game-coding-standards.md` | มาตรฐานโค้ดสำหรับ game โดยเฉพาะ |
| `03-asset-protocol.md` | การจัดการ assets — naming, structure, validation |

---

## การเปลี่ยนแปลงจาก Core Workflow

Game projects เพิ่มข้อกำหนดต่อไปนี้บน core workflow:

### 1. บังคับ FDD ก่อน implement feature ใหม่
ทุก feature ใหม่ที่มี gameplay logic ต้องมี FDD อยู่ใน `doc/08-design/` ก่อน task จะออกจาก `design_validate`

### 2. เพิ่มโฟลเดอร์ `doc/08-design/`
เก็บ Feature Design Documents ทั้งหมด
```
doc/08-design/
  README.md          ← index of all FDDs
  [feature-name].md  ← individual FDD
```

### 3. Task lifecycle สำหรับ game feature
```
todo → design_validate → in_progress → playtest → review → done
```
เพิ่มขั้น `playtest` ระหว่าง implement และ review — ต้องทดสอบ feel จริงก่อน

### 4. Performance budget ต้องระบุก่อน implement
ทุก feature ที่มี real-time logic ต้องระบุ budget ใน FDD:
- Target FPS
- Max ms per frame สำหรับ feature นี้
- Memory budget (ถ้าเกี่ยวข้อง)

---

## สิ่งที่ไม่เปลี่ยนจาก Core

- Source docs versioning — ใช้เหมือนเดิม
- ADR — ใช้เหมือนเดิม (architecture decisions ยังต้องบันทึก)
- Compliance check — ใช้เหมือนเดิม พร้อม game-specific rules เพิ่ม
- Way of work / session protocol — ใช้เหมือนเดิม
- work-status, task-board, log-index — ใช้เหมือนเดิม
