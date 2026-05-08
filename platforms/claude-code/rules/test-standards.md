---
globs: ["tests/**/*", "test/**/*", "**/*.test.*", "**/*.spec.*"]
---

# Test Standards

Rules สำหรับ test files ทั้งหมด

## โครงสร้าง Test

- test แต่ละตัวต้องมี: Arrange → Act → Assert
- test name ต้องบอก: สถานการณ์ + ผลที่คาดหวัง
  - ดี: `"player.takeDamage() reduces health by damage amount"`
  - ไม่ดี: `"test health"`

## Scope

- unit test: ทดสอบ function เดียว ไม่มี side effect
- integration test: ทดสอบการทำงานร่วมกัน ระบุชัดในชื่อ test file
- ห้าม mock ที่ซับซ้อนจนเกินไป — ถ้า mock มากกว่า logic ให้ reconsider design

## Test Coverage

- ทุก function ที่มีใน FDD ส่วนที่ 3 (กลไกและเงื่อนไข) ต้องมี test
- edge cases จาก FDD ส่วนที่ 5 ต้องมี test ครบ
- ห้าม mark task `done` โดยไม่มี test สำหรับ happy path

## Game-Specific

- game logic test ต้องไม่ขึ้นกับ renderer (ตาม logic/render separation)
- ใช้ fixed deltaTime ใน test เสมอ: `const dt = 1/60`
- test ที่เกี่ยวกับ config: ใช้ test config แยกต่างหาก ไม่ใช้ production config
