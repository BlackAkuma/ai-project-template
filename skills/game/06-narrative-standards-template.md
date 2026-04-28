# Narrative Standards Template

มาตรฐานสำหรับ game ที่มี dialogue, story, หรือ text content
ใช้เมื่อโปรเจ็กต์มีเนื้อหาที่ผู้เล่นอ่าน — ไม่บังคับสำหรับ game ที่ไม่มี narrative

---

## 1. โครงสร้างไฟล์ Narrative

```
assets/data/
  narrative/
    dialogue/
      [scene-id].json      ← dialogue ต่อ scene
    story/
      act-[N].json         ← story structure
    strings/
      ui-strings.json      ← text ทั้งหมดใน UI
      tutorial.json        ← tutorial text
```

**กฎ:** ห้าม hardcode string ที่ผู้เล่นเห็น ทุก text ต้องอยู่ใน data file

```typescript
// ❌ ห้าม
button.label = "เริ่มเกม";

// ✓ ถูกต้อง
button.label = strings.get("ui.mainMenu.startGame");
```

---

## 2. Dialogue File Format

```json
{
  "scene": "scene-id",
  "dialogues": [
    {
      "id": "dlg-001",
      "speaker": "hero",
      "text": "ข้อความที่ผู้เล่นเห็น",
      "next": "dlg-002",
      "conditions": [],
      "flags": []
    }
  ]
}
```

**กฎ:**
- ทุก dialogue ต้องมี `id` unique ในรูปแบบ `dlg-NNN`
- `speaker` ต้องอ้างอิง character ID ที่มีในระบบ
- ถ้า dialogue เปลี่ยนตาม condition ต้องระบุใน `conditions` ห้าม hardcode logic ใน code

---

## 3. Localization-Ready

แม้จะยังไม่ localize ให้ออกแบบให้พร้อม:

- ทุก string key ใช้ dot notation: `category.subcategory.key`
- ไม่ต่อ string ใน code: ห้ามใช้ `"คุณมี " + count + " ชีวิต"`
- ใช้ template แทน: `strings.get("ui.lives", { count: lives })`
- ห้าม assume text จะสั้นหรือยาวแค่ไหน (ภาษาอื่นอาจยาวกว่า 2x)

---

## 4. Narrative Compliance Rules

| Code | สิ่งที่ตรวจ | เกณฑ์ |
|------|-----------|-------|
| N-01 | Hardcoded player-facing string | string ที่ผู้เล่นเห็นอยู่ใน code โดยตรง |
| N-02 | String concatenation | ต่อ string แทนที่จะใช้ template |
| N-03 | Dialogue ไม่มี ID | dialogue node ไม่มี unique id |
| N-04 | Speaker ไม่มีใน character registry | speaker ID ที่ไม่มีในระบบ |

Violation tag: `// REFACTOR-PENDING[N-01]: hardcoded string, move to strings.json — T-XXX`

---

## 5. Character Registry

ทุก character ที่พูด dialogue ต้องลงทะเบียนใน `doc/08-design/character-registry.md`

```md
# Character Registry

| ID | ชื่อ | ประเภท | Voice | หมายเหตุ |
|----|-----|-------|-------|---------|
| hero | นักรบ | player | — | ตัวละครหลัก |
| npc-merchant | พ่อค้า | npc | — | ปรากฏใน act-1 |
```
