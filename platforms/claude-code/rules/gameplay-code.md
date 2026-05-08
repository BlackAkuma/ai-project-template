---
globs: ["src/game/**/*", "src/gameplay/**/*", "src/systems/**/*"]
---

# Gameplay Code Standards

Rules สำหรับ game logic code — โหลดอัตโนมัติเมื่อแก้ไขไฟล์ใน src/game/, src/gameplay/, src/systems/

## Config-Driven (G-01)

- ทุก gameplay value ต้องมาจาก config file
- ห้าม magic number ใน gameplay logic
- ทุก config key ใหม่ต้องมี schema: type, range, default

```typescript
// ❌ ห้าม
player.speed = 5.0;

// ✓ ถูกต้อง
player.speed = config.gameplay.playerSpeed; // range: 1.0–20.0
```

## Delta Time (G-02)

- ทุก movement, physics, animation ต้องคูณ deltaTime
- ห้าม `position +=` โดยไม่มี `* deltaTime` หรือ `* dt`

## Logic/Render Separation (G-03)

- Renderer ห้ามแก้ game state โดยตรง
- Game logic ห้ามเรียก render method โดยตรง
- ใช้ event/callback pattern สำหรับ communication

## Prototype Code (G-06)

- ถ้าเป็น prototype: ต้องมี comment `// PROTOTYPE: จุดประสงค์`
- ห้าม merge prototype code เข้า main โดยไม่ rewrite
- ถ้าพบ `// PROTOTYPE:` ใน main branch: สร้าง REFACTOR-PENDING[G-06] task

## Performance

- ทุก system ที่มี real-time update ต้องระบุ budget ใน FDD
- ถ้าไม่มี FDD สำหรับ feature นี้: สร้าง task [G-04] ก่อน implement
