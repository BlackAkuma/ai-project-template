# Game Compliance Codes — Consolidated Index

ดัชนีรวม compliance code ทั้งหมดของ game skill pack (G / A / N / U / L)
นิยามฉบับเต็ม + violation tag format อยู่ในไฟล์ต้นทางแต่ละหมวด (คอลัมน์ "Source")

> ใช้คู่กับ core compliance (C-01..C-14, C-20..C-22) ใน `core/15` + `core/19`
> Violation tag format: `// REFACTOR-PENDING[<CODE>]: <คำอธิบาย> — T-XXX`

---

## G — Game Logic & Config

| Code | สิ่งที่ตรวจ | Source |
|------|-----------|--------|
| G-01 | Hardcoded gameplay value (magic number ใน gameplay logic) | `02-game-coding-standards.md` |
| G-02 | Movement ไม่มี delta time (`position +=` ไม่คูณ `dt`) | `02-game-coding-standards.md` |
| G-03 | Renderer เรียก/แก้ game logic โดยตรง | `02-game-coding-standards.md` |
| G-04 | Feature ไม่มี FDD (`in_progress` แต่ไม่มี FDD ใน `08-design/`) | `02-game-coding-standards.md` |
| G-05 | Config value ไม่มี schema (ไม่มี type/range) | `02-game-coding-standards.md` |
| G-06 | Prototype comment ค้างใน production (`// PROTOTYPE:` ที่ merge แล้ว) | `02-game-coding-standards.md` |
| G-07 | Config value เกิน range ที่ FDD กำหนด | `05-balance-check-template.md` |
| G-08 | FDD ไม่ระบุว่ารองรับ Game Pillar ข้อไหน | `07-gdd-template.md` |
| G-09 | Feature ใหม่กระทบความยาก แต่ไม่อัปเดต difficulty curve | `08-difficulty-curve-template.md` |
| G-10 | Tuning lever ไม่มีใน config (hardcoded) | `08-difficulty-curve-template.md` |

## A — Asset & Art

| Code | สิ่งที่ตรวจ | Source |
|------|-----------|--------|
| A-01 | Asset ไม่ได้ลงทะเบียน (ใช้ใน code แต่ไม่มีใน registry) | `03-asset-protocol.md` |
| A-02 | Naming ไม่ตรง convention (ไม่มี type prefix / space / capital) | `03-asset-protocol.md` |
| A-03 | Asset ใหญ่เกิน guideline | `03-asset-protocol.md` |
| A-04 | Raw files ใน git (.psd, .ai, .fla) | `03-asset-protocol.md` |
| A-05 | Asset ใช้สีนอก palette โดยไม่มีเหตุผล | `03-asset-protocol.md` / `09-art-bible-template.md` |
| A-06 | VFX เกิน particle budget | `03-asset-protocol.md` / `09-art-bible-template.md` |
| A-07 | UI element contrast ratio ต่ำกว่า minimum (<4.5:1 / <3:1 large) | `09-art-bible-template.md` |

## N — Narrative & Strings

| Code | สิ่งที่ตรวจ | Source |
|------|-----------|--------|
| N-01 | Hardcoded player-facing string | `06-narrative-standards-template.md` |
| N-02 | String concatenation (แทนการใช้ template) | `06-narrative-standards-template.md` |
| N-03 | Dialogue node ไม่มี unique ID | `06-narrative-standards-template.md` |
| N-04 | Speaker ID ไม่มีใน character registry | `06-narrative-standards-template.md` |

## U — UX & HUD

| Code | สิ่งที่ตรวจ | Source |
|------|-----------|--------|
| U-01 | Screen implement โดยไม่มี UX spec | `10-ux-hud-template.md` |
| U-02 | UI component แก้ game state โดยตรง (ไม่ผ่าน event) | `10-ux-hud-template.md` |
| U-03 | Input method ที่ระบุว่ารองรับแต่ทำงานไม่ครบ | `10-ux-hud-template.md` |

## L — Level Design

| Code | สิ่งที่ตรวจ | Source |
|------|-----------|--------|
| L-01 | Level implement โดยไม่มี LDD ที่ Approved | `11-level-design-template.md` |
| L-02 | Encounter ที่ไม่มีใน LDD ถูกเพิ่มโดยไม่อัปเดต LDD | `11-level-design-template.md` |

---

**กฎ:** code เหล่านี้บังคับใช้เมื่อโปรเจ็กต์มี `CoreAiWorkspaces/08-design/` (game skill pack active)
ถ้าพบ violation → tag ในโค้ด + สร้าง task ใน debt register ตาม `core/15`
