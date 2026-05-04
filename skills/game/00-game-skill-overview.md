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

## Specialist Thinking Frames

สำหรับ AI tools ที่ไม่ใช่ Claude Code (ChatGPT, Gemini, Copilot ฯลฯ) ใช้ thinking frame เหล่านี้เมื่อต้องการ perspective จาก specialist:

### 🎮 Game Design Frame
ก่อนประเมิน mechanic ใดๆ ให้ถามตัวเองว่า:
- **MDA:** mechanic นี้สร้าง dynamic อะไร → player จะรู้สึก aesthetic อะไร?
- **Degenerate Strategy:** player จะ exploit อะไรจาก mechanic นี้?
- **Player Fantasy:** mechanic นี้ serve fantasy ที่ระบุใน GDD section 2 ไหม?
- **Sawtooth Pattern:** challenge spike นี้มี recovery window ไหม?

### 🎨 Art Direction Frame
ก่อน review/recommend asset ใดๆ:
- **Silhouette Test:** ถ้า fill สีดำทึบ ยังบอก character/object ได้ไหม?
- **Emotional Color:** สีที่ใช้ตรงกับ emotional meaning ใน art bible ไหม?
- **Visual Hierarchy:** player attention ไหลไป: threat → interactive → ambient ถูกต้องไหม?
- **A11y Check:** มี icon + color ไม่ใช่แค่ color เพื่อสื่อความหมาย?

### 📖 Narrative Frame
ก่อน review/เขียน dialogue หรือ story:
- **Dialogue Function Test:** บรรทัดนี้ทำอย่างน้อย 1 ใน 4: reveal character / advance plot / deliver info / create mood?
- **Character Knowledge:** ณ scene นี้ character รู้อะไรได้บ้าง ยังไม่ควรรู้อะไร?
- **Ludonarrative Check:** mechanic กับ story บอกสิ่งเดียวกัน หรือขัดแย้งกัน?
- **Arc Catalyst:** ถ้า character เปลี่ยนใจ — catalyst ชัดพอไหม?

### 🖥️ UX Frame
ก่อน design หรือ review screen:
- **Mental Model:** player expect อะไรจาก screen นี้ ก่อนที่จะเห็น?
- **Cognitive Load:** screen นี้ให้ตัดสินใจกี่อย่างพร้อมกัน? ลดได้ไหม?
- **FTUX Test:** new player เข้าใจ core loop ภายใน 5 นาทีโดยไม่อ่าน manual?
- **State Coverage:** loading / empty / error / disabled states ถูก design ครบไหม?

### ⚡ Performance Frame
ก่อน implement หรือ optimize:
- **Profile First:** วัด actual bottleneck ก่อน — อย่า assume
- **Frame Budget:** 60fps = 16.67ms; feature นี้กินเท่าไร? เหลือเท่าไร?
- **Allocation Rate:** loop นี้ create object ต่อ frame ไหม? → pool แทน
- **Complexity:** complexity scale กับอะไร? entity count? player count? level size?

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
