# /caw-tool-clean — Clean Up Unused AI Tool Config Files

ลบ config ไฟล์ของ AI tool ที่ไม่ใช้แล้ว เหลือเฉพาะ tool ที่ต้องการ

`CoreAiWorkspaces/` และ `AI.md` ไม่ถูกแตะเด็ดขาด

---

## ขั้นตอน

### 1. ตรวจหา tool config ที่มีอยู่

ตรวจไฟล์เหล่านี้ใน project root และ subdirs:

```
CLAUDE.md
.cursorrules
.windsurfrules
.gemini/instructions.md
.github/copilot-instructions.md
[tool-name]-setup.md
CoreAiWorkspaces/03-log/agents/*.md
```

แสดงรายการทั้งหมดที่พบ

### 2. ถามผู้ใช้ว่าจะเก็บ tool ไหน

```
พบ tool config ดังนี้:
  [x] CLAUDE.md (Claude Code)
  [ ] .cursorrules (Cursor)
  [ ] agents/cursor.md

จะเก็บ tool ไหนไว้? (tool ที่ไม่ระบุจะถูกลบ)
```

รอคำยืนยันก่อนดำเนินการ

### 3. แสดง preview รายการที่จะลบ

```
จะลบไฟล์ต่อไปนี้:
  - .cursorrules
  - CoreAiWorkspaces/03-log/agents/cursor.md

จะเก็บไว้:
  - AI.md                    (ห้ามลบ — universal protocol)
  - CLAUDE.md                (tool ที่เลือก)
  - CoreAiWorkspaces/        (ห้ามลบ — project data)

ยืนยันลบ? (yes/no)
```

### 4. ลบหลังได้รับ "yes" เท่านั้น

ลบเฉพาะไฟล์ที่แสดงใน preview
ไม่ลบอะไรเพิ่มเติมจากที่แสดง

### 5. รายงานผล

```
เสร็จแล้ว — เหลือเฉพาะ [tool-name]
ลบแล้ว: [รายการ]
ไม่แตะ: AI.md, CoreAiWorkspaces/
```

---

## กฎสำคัญ

- `AI.md` → ห้ามลบเด็ดขาด (tool ใหม่ยังต้องใช้ถ้าเปลี่ยนใจในอนาคต)
- `CoreAiWorkspaces/` → ห้ามลบเด็ดขาด (ข้อมูลโปรเจ็กต์)
- ต้องได้ "yes" ชัดเจนก่อนลบทุกครั้ง
- ถ้าไม่แน่ใจไฟล์ไหน → ไม่ลบ แจ้งผู้ใช้แทน
