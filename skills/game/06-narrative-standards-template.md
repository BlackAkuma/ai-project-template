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

ทุก character ที่พูด dialogue ต้องลงทะเบียนใน `ai/08-design/character-registry.md`

```md
# Character Registry

| ID | ชื่อ | ประเภท | Voice | หมายเหตุ |
|----|-----|-------|-------|---------|
| hero | นักรบ | player | — | ตัวละครหลัก |
| npc-merchant | พ่อค้า | npc | — | ปรากฏใน act-1 |
```

---

## 6. Character Sheet

สำหรับ character หลักแต่ละตัว (player, main NPC, antagonist) ให้สร้าง character sheet แยก
เก็บใน `ai/08-design/character-[id].md`

```md
# Character Sheet — <CHARACTER_ID>

## ข้อมูลพื้นฐาน

| ด้าน | รายละเอียด |
|------|-----------|
| ชื่อ | [ชื่อที่ผู้เล่นเห็น] |
| ID | [id ที่ใช้ใน dialogue system] |
| ประเภท | [player / ally / antagonist / npc] |
| ปรากฏตั้งแต่ | [act / scene ไหน] |

## บุคลิก

**สรุปใน 3 คำ:** [เช่น: กล้า, ขี้สงสัย, ไม่ไว้ใจคนง่าย]

**วิธีพูด:**
- ใช้ประโยค [สั้น / ยาว] — [เป็นทางการ / ไม่เป็นทางการ]
- คำที่ใช้บ่อย: [เช่น: ถามคำถาม, ใช้ sarcasm, พูดตรงไปตรงมา]
- สิ่งที่ไม่พูดเด็ดขาด: [เช่น: ไม่ขอความช่วยเหลือ, ไม่พูดว่า "ไม่รู้"]

## Arc

| จุด | สถานะ | สิ่งที่เปลี่ยน |
|----|-------|-------------|
| ต้นเรื่อง | [เชื่ออะไร / ต้องการอะไร] | — |
| Midpoint | [เกิดอะไรขึ้น] | [เปลี่ยนอะไร] |
| ปลายเรื่อง | [จบที่ไหน] | [เติบโตอะไร] |

## Consistency Rules

- [ ] ความเชื่อหลักไม่เปลี่ยนโดยไม่มี catalyst ที่ชัดเจน
- [ ] น้ำเสียงในทุก dialogue ตรงกับ "วิธีพูด" ด้านบน
- [ ] ไม่รู้ข้อมูลที่ character ยังไม่ควรรู้ ณ scene นั้น
```
