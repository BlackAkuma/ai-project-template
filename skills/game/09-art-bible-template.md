# Art Bible Template

เอกสารกำหนด visual identity ของเกม — เขียนก่อนสร้าง asset จริงตัวแรก
เก็บใน `doc/08-design/art-bible.md`

Art Bible คือ source of truth ของทุกการตัดสินใจด้าน visual — ถ้าไม่มีใน bible → ต้องสร้างกฎก่อน

---

## Template

```md
# Art Bible — <PROJECT_NAME>

อัปเดตล่าสุด: YYYY-MM-DD
สถานะ: Draft / Approved
ผู้อนุมัติ: [ชื่อ]

---

## 1. Visual Identity Statement

**1 ประโยคที่อธิบาย look ทั้งเกม:**
"[PROJECT_NAME] ดูเหมือน [reference A] ที่มี [คุณสมบัติ B] แต่รู้สึกแบบ [ความรู้สึก C]"

ตัวอย่าง: "เกมนี้ดูเหมือน pixel art ยุค 16-bit ที่มีแสงเงาแบบ painterly แต่รู้สึก crisp และ modern"

---

## 2. Reference Board

| ภาพ / เกม / งานศิลปะ | สิ่งที่ดูด | สิ่งที่หลีกเลี่ยง |
|--------------------|----------|----------------|
| [reference 1] | [เช่น: color palette, silhouette] | [เช่น: level of detail] |
| [reference 2] | | |

**กฎ:** reference ใช้เพื่อสื่อสาร ไม่ใช่เพื่อ copy — ระบุ "ดูดอะไร" ให้ชัด

---

## 3. Color Palette

### Primary Colors (ใช้ทั่วทั้งเกม)

| ชื่อ | Hex | ใช้สำหรับ |
|------|-----|---------|
| [ชื่อสี] | #XXXXXX | [เช่น: background หลัก, UI frame] |
| [ชื่อสี] | #XXXXXX | [เช่น: character หลัก, interactive object] |

### Accent Colors (ใช้เน้นจุดสนใจ)

| ชื่อ | Hex | ใช้สำหรับ |
|------|-----|---------|
| [ชื่อสี] | #XXXXXX | [เช่น: collectible, danger zone] |

### Emotional Color Mapping

| สถานการณ์ / mood | สี | เหตุผล |
|----------------|-----|-------|
| Safe zone / ปลอดภัย | [#XXXXXX] | [เช่น: โทน warm ให้รู้สึกอุ่น] |
| Danger / อันตราย | [#XXXXXX] | [เช่น: โทน red/orange สัญชาตญาณ] |
| Mystery / ลึกลับ | [#XXXXXX] | |
| Victory / ชนะ | [#XXXXXX] | |
| UI / neutral | [#XXXXXX] | |

**กฎ:** ห้ามใช้สีนอก palette โดยไม่มีเหตุผล — ถ้าต้องการสีใหม่ต้องอัปเดต bible ก่อน

---

## 4. Art Style

| ด้าน | กำหนด |
|------|-------|
| Rendering | [เช่น: pixel art 16x16 base / vector flat / hand-drawn / 3D low-poly] |
| สัดส่วนตัวละคร | [เช่น: chibi 2-head / realistic 7-head / stylized 4-head] |
| Outline | [มี / ไม่มี / เฉพาะ character] ความหนา: [Npx] |
| Shading | [flat / cell-shaded / painterly / no shading] |
| Detail level | [minimal / moderate / detailed] — [อธิบาย guideline] |
| Perspective | [side-view / top-down / isometric / 3D perspective] |

---

## 5. Character Art Standards

**Silhouette test:** character ต้องจำได้จาก silhouette คนเดียว — ทดสอบด้วย black fill

| ประเภท | Silhouette guideline | Color coding |
|--------|---------------------|-------------|
| Player | [เช่น: โค้งมน, สูง] | [สีหลักที่ใช้] |
| Enemy (ปกติ) | [เช่น: เหลี่ยม, เตี้ย] | [สีที่บ่งบอก threat] |
| NPC / Ally | [เช่น: นุ่มนวล] | [สีที่แยกออกจาก enemy] |
| Boss | [เช่น: ใหญ่, ซับซ้อน] | [unique สีเฉพาะ] |

**Animation guidelines:**
- Idle: ต้องมี animation (ห้าม static) — ความถี่: [N fps]
- ความสำคัญของ frame ก่อน/หลัง action: [anticipation N frames / follow-through N frames]

---

## 6. Environment Art Standards

| ด้าน | กำหนด |
|------|-------|
| Tileset design | [modular / organic / mixed] — tile base size: [NxN px] |
| Modularity | ทุก environment element ต้องใช้ร่วมกันได้ข้าม scene |
| Foreground / Background | layer separation: [N layers] — depth blur: [ใช่ / ไม่ใช่] |
| แสง | [เช่น: hard shadow / soft / dynamic / baked] |
| Visual landmark | แต่ละ area ต้องมี element เด่น 1 อย่างที่ทำให้จำได้ |

**Readability:**
- Walkable area ต้องชัดเจนกว่า background เสมอ — contrast อย่างน้อย [N]%
- Interactive object ต้องมี visual cue ชัดเจน [เช่น: glow / outline / animation]

---

## 7. UI / HUD Standards

| ด้าน | กำหนด |
|------|-------|
| Font หลัก | [ชื่อ font] — size ขั้นต่ำ: [N px] |
| Font รอง | [ชื่อ font] — ใช้สำหรับ: [เช่น: tooltip, lore] |
| Button style | [ขอบ, corner radius, state: normal / hover / pressed / disabled] |
| HUD layout | [มุมไหน = อะไร] — หลัก: top-left / top-right / bottom |
| Icon style | [filled / outline / mixed] — size มาตรฐาน: [NxN px] |

**กฎ HUD:**
- ข้อมูลที่ผู้เล่นต้องอ่านบ่อย → วางใกล้ center of action
- ข้อมูลที่ดูเป็นครั้งคราว → มุมจอ
- ห้าม block พื้นที่เกิน 20% ของหน้าจอ

---

## 8. VFX Standards

| ประเภท | Guideline | ตัวอย่าง |
|--------|----------|---------|
| Hit feedback | ต้องมี frame freeze [N frames] + screen shake ถ้า impact หนัก | player hit: 2 frames freeze |
| Particle budget | ไม่เกิน [N] particles ต่อ effect | explosion: ≤ 50 particles |
| VFX สี | ใช้ accent color ตาม emotional mapping section 3 | damage = red, heal = green |
| Duration | [เช่น: VFX ต้องจบใน 0.3–0.5 วินาที ไม่งั้นรกหน้าจอ] | |
| Screen shake | ใช้สำหรับ: [impact สำคัญ, explosion] — ห้ามใช้: [damage เล็กน้อย] | amplitude: max [N px] |

**กฎ:** VFX ต้องเสริม game feel ไม่ใช่บัง gameplay — ถ้า player ไม่เห็น hitbox เพราะ VFX = ปัญหา

---

## 9. Accessibility

| ด้าน | Requirement |
|------|-------------|
| Colorblind safety | Deuteranopia check: สี danger/safe ต้องแยกได้โดยไม่ใช้สีเดียว (ใช้ shape/icon ด้วย) |
| Contrast ratio | text บน background: ≥ 4.5:1 (WCAG AA), HUD element สำคัญ: ≥ 3:1 |
| Icon + color | อย่าสื่อความหมายด้วยสีอย่างเดียว — ต้องมี icon หรือ label ด้วย |
| Animation | ถ้ามี flashing → ห้ามเกิน 3 ครั้ง/วินาที (photosensitivity) |

```

---

## Compliance Rules

| Code | สิ่งที่ตรวจ |
|------|-----------|
| A-05 | Asset ใช้สีนอก color palette โดยไม่มีเหตุผล |
| A-06 | VFX เกิน particle budget ที่กำหนด |
| A-07 | UI element มี contrast ratio ต่ำกว่า minimum |
