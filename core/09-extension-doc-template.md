# Extension Document Template

คัดลอกและปรับไฟล์นี้เป็นเอกสารภายใต้ `CoreAiWorkspaces/06-extensions/`

```md
# <EXTENSION_TITLE>

วันที่: <CURRENT_DATE>
สถานะ: Draft

## Reason

อธิบายว่าทำไมต้องมีเอกสารนี้ และสิ่งนี้ต่างจาก source docs เดิมอย่างไร

## Related Source References

- `CoreAiWorkspaces/00-source/versions/<CURRENT_SOURCE_VERSION>/<SOURCE_DOC>.md`

## Description

อธิบายสิ่งที่เพิ่ม

## Impact

- กระทบแผนอย่างไร
- กระทบ task อะไร
- กระทบ data model / API / UX หรือไม่

## Required Updates

- `CoreAiWorkspaces/01-plan/project-plan.md`
- `CoreAiWorkspaces/01-plan/work-status.md`
- `CoreAiWorkspaces/02-task/task-board.md`
```

---

## ตัวอย่าง Extension Doc กรณี Conflict (source vs code)

ใช้เมื่อ AI พบว่า code ที่ทำงานอยู่ขัดแย้งกับสิ่งที่ source doc กำหนดไว้
ห้ามแก้ไขเงียบ ๆ — ต้องบันทึก conflict และรอมนุษย์ตัดสินใจ

```md
# Extension: Conflict — Auth Middleware vs Source v1.1

วันที่: 2026-04-28
สถานะ: Needs Human Decision
สร้างโดย: AI session — Claude Code

## Reason

พบ conflict ระหว่าง source doc v1.1 กับ code ที่ implement อยู่จริง
Source doc ระบุ approach หนึ่ง แต่ code ใช้อีก approach — ไม่ทราบว่าอันไหนคือ "ความตั้งใจจริง"

## Related Source References

- `CoreAiWorkspaces/00-source/versions/v1.1/02-auth-requirements.md` — Section 3.2: "ทุก endpoint ต้องผ่าน JWT middleware"

## Description

**Source doc v1.1 ระบุ:**
> ทุก endpoint รวมถึง `/api/public/*` ต้องผ่านการ verify JWT ก่อน

**Code ที่พบ (`src/middleware/auth.ts:47`):**
```typescript
// Public routes bypass auth
const PUBLIC_PATHS = ['/api/public/products', '/api/public/health'];
if (PUBLIC_PATHS.includes(req.path)) return next();
```

code ปัจจุบัน bypass auth สำหรับ public endpoints ซึ่งขัดกับ source doc โดยตรง

**ข้อมูลเพิ่มเติม:**
- code ส่วนนี้ commit ครั้งแรก: 2026-03-15 (ก่อน source v1.1 ออก: 2026-04-01)
- ไม่มี task ใน task-board อ้างถึงการเปลี่ยนแปลงนี้
- ไม่มี ADR บันทึกเหตุผลที่เลือก bypass

## Impact

- ถ้า source doc ถูก: ต้องแก้ middleware ให้ครอบคลุม public paths ด้วย → กระทบ T-020 (public catalog)
- ถ้า code ถูก: ต้องอัปเดต source doc v1.2 ให้ระบุ exception กรณี public endpoints → ต้องสร้าง ADR

## Required Updates

เมื่อมนุษย์ตัดสินใจแล้ว:
- ถ้าเลือก "ตาม source doc": แก้ `src/middleware/auth.ts` + อัปเดต task-board
- ถ้าเลือก "ตาม code": สร้าง source v1.2 + สร้าง ADR บันทึกเหตุผล
- ทั้งสองกรณี: อัปเดต work-status ออกจาก [NEEDS HUMAN DECISION]
```

**งาน task-board ที่ต้องสร้างพร้อมกัน:**
```
T-XXX: [NEEDS HUMAN DECISION] Resolve auth middleware vs source v1.1 conflict
  ref: CoreAiWorkspaces/06-extensions/conflict-auth-middleware-2026-04-28.md
  blocked by: human decision on which is source of truth
```

---

## Reverse-Document Protocol

ใช้เมื่อ AI พบ code ที่ทำงานอยู่แล้วแต่ไม่มีเอกสารรองรับ เช่น พบ function ที่ implement logic ซับซ้อนแต่ไม่มี requirement หรือ design doc ใดอ้างถึง

### เมื่อไหร่ต้องทำ

- พบ code ที่ไม่มี task reference ใน task-board
- พบ logic ที่ไม่สอดคล้องกับ source docs ใด ๆ
- ถูกขอให้แก้ไข code ที่ไม่มีใครรู้ว่าทำอะไรอยู่

### ขั้นตอน

```
1. ห้ามแก้ไข code ที่ไม่เข้าใจก่อนทำ reverse-document
2. อ่าน code แล้วสรุปว่ามันทำอะไร (เขียนเป็น plain language)
3. สร้าง extension doc ใน CoreAiWorkspaces/06-extensions/reverse-<ชื่อ>.md โดยใช้ template ด้านบน
   - Reason: "code นี้มีอยู่แล้วแต่ไม่มี documentation"
   - Description: สรุปสิ่งที่ code ทำ พร้อมอ้างอิง file:line
   - Impact: ไม่รู้ — ระบุ <NEEDS_CLARIFICATION: ต้องการ owner ยืนยัน>
4. สร้าง task ใน task-board แท็ก [REVERSE-DOC] รอ human review
5. อัปเดต work-status ว่าพบ undocumented code
6. รอ human confirm ก่อนแก้ไข code นั้น
```

### Template Reverse-Doc

```md
# Reverse-Doc: <ชื่อ module/function>

วันที่: <CURRENT_DATE>
สถานะ: Needs Review
ไฟล์: <path/to/file.ts:line>

## สิ่งที่ code ทำ (สรุปจากการอ่าน)

<อธิบาย logic ที่พบ>

## สิ่งที่ไม่ทราบ

- ทำไมถึงเขียนแบบนี้?
- มี requirement ใดอ้างถึงหรือไม่?
- ใครเป็น owner?

## Action Required

- [ ] Human ยืนยันว่า code นี้ยังต้องการอยู่
- [ ] ถ้าใช่: สร้าง source doc หรือ task reference
- [ ] ถ้าไม่: สร้าง task เพื่อ remove
```
