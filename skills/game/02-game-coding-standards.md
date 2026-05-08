# Game Coding Standards

มาตรฐานโค้ดเพิ่มเติมสำหรับ game projects
ใช้ร่วมกับ `ai/04-way-of-work/coding-standards.md` (core standards ยังใช้ทั้งหมด)

---

## 1. Config-Driven Values (บังคับ)

**ทุก gameplay value ต้องมาจาก config file ห้าม hardcode**

```typescript
// ❌ ห้าม
const PLAYER_SPEED = 5.0;
if (health <= 20) triggerDanger();

// ✓ ถูกต้อง
const PLAYER_SPEED = config.gameplay.playerSpeed;
if (health <= config.gameplay.dangerThreshold) triggerDanger();
```

Config file convention:
- `config/gameplay.json` — ค่า gameplay (speed, damage, cooldown)
- `config/balance.json` — ค่า balance (enemy stats, drop rates)
- `config/ui.json` — ค่า UI (animation duration, sizes)
- ทุก key ใช้ camelCase, ทุกไฟล์มี schema document

---

## 2. Delta Time (บังคับสำหรับ real-time)

**ทุก movement, physics, animation ต้องคำนวณด้วย delta time**

```typescript
// ❌ ห้าม — ผูกกับ frame rate
player.x += speed;

// ✓ ถูกต้อง — frame-rate independent
player.x += speed * deltaTime;
```

---

## 3. Logic / Rendering Separation

**Game logic ต้องไม่ขึ้นกับ rendering layer**

```
GameState (pure logic)     — ไม่รู้จัก renderer, ไม่รู้จัก DOM
    ↓ emits events
Renderer (visual only)     — รับ events, แสดงผล ไม่ตัดสินใจ logic
    ↓
InputHandler               — แปลง input → commands → ส่งให้ GameState
```

ประโยชน์: test game logic ได้โดยไม่ต้อง render, เปลี่ยน renderer ได้โดยไม่แตะ logic

---

## 4. State Machine Documentation

ทุก entity ที่มี state (player, enemy, UI screen) ต้องมี state diagram ใน comment หรือ FDD:

```typescript
/**
 * Player States:
 * idle → moving (input detected)
 * moving → idle (no input)
 * idle/moving → jumping (jump input, grounded)
 * jumping → falling (peak reached)
 * falling → idle (landed)
 * any → dead (health = 0)
 */
class PlayerStateMachine { ... }
```

---

## 5. Performance Budget

ระบุ budget ใน FDD และ enforce ใน code:

```typescript
// Performance budget: < 2ms per frame for this system
// Profile with: performance.mark('system-start') / performance.mark('system-end')
class EnemyAISystem {
  update(deltaTime: number, enemies: Enemy[]) {
    // Implementation here
  }
}
```

**Platform budgets (guideline):**
| Platform | Target FPS | Budget per frame |
|----------|-----------|-----------------|
| Desktop  | 60 fps    | ~16ms total     |
| Mobile   | 30-60 fps | 8-16ms total    |
| Web      | 60 fps    | ~16ms total     |

ระบุ % ของ budget ที่ feature นี้ใช้ได้ใน FDD

---

## 6. Debug Visualization (strongly recommended)

System ที่ซับซ้อน (AI, physics, pathfinding) ควรมี debug mode:

```typescript
class EnemyAI {
  update(dt: number) {
    // Normal logic here

    if (DEBUG_MODE) {
      this.drawDetectionRadius();
      this.drawPathfindingRoute();
      this.logStateTransition();
    }
  }
}
```

Toggle ด้วย config ไม่ใช่ compile flag: `config.debug.showAIOverlay = true`

---

## 7. Prototype vs Production Code

**ระบุชัดเจนก่อนเขียนว่าเป็น prototype หรือ production**

### Prototype Code

ใช้เมื่อต้องการทดสอบ concept เร็ว ๆ ก่อนตัดสินใจ implement จริง:

```typescript
// PROTOTYPE: ทดสอบ feel ของ jump mechanic — ลบทิ้งหลัง playtest
// ห้าม merge เข้า main โดยไม่ rewrite เป็น production code
player.y -= 50; // hardcode ก็ได้ในขั้นนี้
```

**กฎสำหรับ prototype:**
- ต้องมี comment `// PROTOTYPE:` บอกจุดประสงค์
- hardcode ได้, magic number ได้ — เพราะจะ rewrite ทั้งหมด
- ห้าม merge เข้า branch หลักโดยไม่แปลงเป็น production code
- เมื่อ playtest ผ่านแล้ว: สร้าง task ใน board เพื่อ rewrite ก่อน production

### Production Code

ทุกอย่างที่ merge เข้า main ต้องเป็น production standard:

- ปฏิบัติตาม Config-Driven (ข้อ 1), Delta Time (ข้อ 2), Logic/Render Separation (ข้อ 3)
- ไม่มี `// PROTOTYPE:` comment ค้างอยู่
- ผ่าน compliance rules G-01 ถึง G-06

**กฎ compliance เพิ่ม:**

| Code | สิ่งที่ตรวจ |
|------|-----------|
| G-06 | Prototype comment ค้างใน production branch |

---

## 8. Game-Specific Compliance Rules (เพิ่มจาก core)

Rules เหล่านี้เพิ่มเติมจาก C-01 ถึง C-10 ใน compliance check:

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| G-01 | Hardcoded gameplay value | ตัวเลข magic number ใน gameplay logic |
| G-02 | Movement ไม่มี delta time | `position +=` โดยไม่คูณ `dt` หรือ `deltaTime` |
| G-03 | Renderer เรียก game logic โดยตรง | renderer แก้ game state แทนที่จะแค่ render |
| G-04 | Feature ไม่มี FDD | task `in_progress` แต่ไม่มี FDD ใน `ai/08-design/` |
| G-05 | Config value ไม่มี schema | key ใหม่ใน config ไม่มี type/range document |
| G-06 | Prototype comment ค้างใน production branch | มี `// PROTOTYPE:` ใน code ที่ merge แล้ว |

Violation tag format: `// REFACTOR-PENDING[G-01]: hardcoded value 5.0, move to config — T-XXX`
