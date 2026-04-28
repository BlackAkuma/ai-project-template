# Asset Protocol

การจัดการ assets สำหรับ game projects
ใช้กับทุก platform — ปรับ format/tool ตาม engine แต่หลักการเดียวกัน

---

## 1. Naming Convention

รูปแบบ: `[type]_[name]_[variant].[ext]`

| Type prefix | ประเภท | ตัวอย่าง |
|------------|--------|---------|
| `spr_` | Sprite / 2D image | `spr_player_idle.png` |
| `anim_` | Animation | `anim_player_run.json` |
| `sfx_` | Sound effect | `sfx_jump_01.wav` |
| `bgm_` | Background music | `bgm_level1.mp3` |
| `ui_` | UI element | `ui_button_play.png` |
| `bg_` | Background | `bg_forest_layer1.png` |
| `fx_` | Visual effect | `fx_explosion_01.png` |
| `model_` | 3D model | `model_tree_01.glb` |
| `tex_` | Texture | `tex_ground_grass.png` |
| `font_` | Font | `font_pixel_main.ttf` |
| `data_` | Data file | `data_enemies.json` |

**กฎ:**
- lowercase ทั้งหมด
- underscore แทน space หรือ dash
- variant ใช้ `_01`, `_02` หรือ `_idle`, `_run`, `_jump`
- ห้ามใช้ชื่อ generic เช่น `image1.png`, `sound.wav`

---

## 2. Folder Structure

```
assets/
  sprites/
    characters/
      player/
      enemies/
    ui/
    backgrounds/
    effects/
  audio/
    sfx/
    bgm/
  fonts/
  models/          ← 3D projects
  textures/        ← 3D projects
  data/
    config/
    levels/
  raw/             ← source files (PSD, AI, FLA) — ไม่ export เข้า git ถ้าใหญ่มาก
```

---

## 3. Asset Registry

ทุก asset ที่ใช้ในโปรเจ็กต์ต้องลงทะเบียนใน `doc/08-design/asset-registry.md`

```md
# Asset Registry

| Asset ID | File | Type | Size | Status | Used By |
|----------|------|------|------|--------|---------|
| AST-001 | spr_player_idle.png | sprite | 64x64 | Active | PlayerRenderer |
| AST-002 | sfx_jump_01.wav | sfx | 22kHz | Active | PlayerAudio |
```

**Status:** Active / Deprecated / Placeholder

---

## 4. Format & Compression Guidelines

### Images
| Use case | Format | Notes |
|----------|--------|-------|
| Sprites (ต้องการ transparency) | PNG | lossless |
| Backgrounds (ไม่ต้องการ transparency) | JPG | quality 85% |
| UI icons | PNG หรือ SVG | |
| Texture atlases | PNG | pack ด้วย TexturePacker หรือ similar |
| Web game | WebP + PNG fallback | |

### Audio
| Use case | Format | Notes |
|----------|--------|-------|
| SFX | WAV หรือ OGG | WAV สำหรับ quality, OGG สำหรับ web |
| BGM | MP3 หรือ OGG | bitrate 128-192kbps |
| Web game | OGG + MP3 fallback | |

### ขนาด guidelines
- Sprite sheet: ไม่เกิน 2048x2048 px (mobile: 1024x1024)
- Audio SFX: ไม่เกิน 500KB
- BGM: ไม่เกิน 5MB

---

## 5. Compliance Rules สำหรับ Assets

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| A-01 | Asset ไม่ได้ลงทะเบียน | ใช้ใน code แต่ไม่มีใน registry |
| A-02 | Naming ไม่ตรง convention | ไม่มี type prefix หรือใช้ space/capital |
| A-03 | Asset ใหญ่เกิน guideline | เกินขนาดที่กำหนด |
| A-04 | Raw files ใน git | ไฟล์ .psd, .ai, .fla ใน main repo |

Violation tag: `// REFACTOR-PENDING[A-01]: asset not in registry — T-XXX`
