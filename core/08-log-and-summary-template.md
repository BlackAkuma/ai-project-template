# Log and Summary Template

ใช้ไฟล์นี้เป็นแม่แบบสำหรับ:

- `doc/03-log/work-log-index.md`
- `doc/03-log/templates/daily-log-template.md`
- `doc/05-summary/templates.md`

---

## Work Log Index Template

`work-log-index.md` เป็นไฟล์ที่ AI อ่านทุก session เพื่อรู้ว่า session ก่อนหน้าทำอะไรไปแล้ว
AI-CONTEXT block บันทึก snapshot ของ session ล่าสุดเท่านั้น — body เก็บประวัติทั้งหมด

**Field ที่ใช้ใน AI-CONTEXT:**

| Field | ความหมาย | ตัวอย่าง |
|-------|----------|---------|
| `last_session` | วันที่ของ session ล่าสุด | `2026-04-28` |
| `tool` | AI tool ที่ใช้ใน session ล่าสุด | `Claude Code` |
| `completed` | task ที่เสร็จใน session นั้น | `[T-001, T-002]` หรือ `none` |
| `checkpoint` | task ที่ค้างกลางคัน (ถ้ามี) | `T-003: finished auth logic, pending tests` หรือ `none` |
| `next_from_last` | งานที่ session นั้นแนะนำให้ทำต่อ | `T-003 T-004` |
| `notes` | สิ่งสำคัญที่ session ถัดไปควรรู้ (สั้น) | `ADR-002 created` หรือ `none` |

**กฎสำคัญ:** อัปเดต AI-CONTEXT ทุกครั้งที่เพิ่ม entry ใหม่ ให้สะท้อน session ล่าสุดเสมอ

```md
<!-- AI-CONTEXT
last_session: <CURRENT_DATE>
tool: <AI_TOOL_NAME>
completed: [<TASK_IDS>] | none
checkpoint: <T-XXX: detail> | none
next_from_last: <T-XXX> <T-XXX>
notes: <SHORT_NOTE> | none
-->

---

# Work Log Index — <PROJECT_NAME>

อัปเดตล่าสุด: <CURRENT_DATE>

## Entries

### <CURRENT_DATE> — [<AI_TOOL_NAME>]

- **สรุป session:** <SUMMARY>
- **Tasks:** `T-XXX` `T-XXX`
- **Validation:** <วิธีที่ใช้ตรวจสอบ>
- **ผลลัพธ์:** <RESULT>
- **Daily Log:** `doc/03-log/YYYY/MM/YYYY-MM-DD-log.md`
```

---

## Daily Log Template

ไฟล์นี้ไม่มี AI-CONTEXT block เพราะ AI ไม่อ่านทุก session — อ่านเฉพาะเมื่อต้องการรายละเอียด

```md
# YYYY-MM-DD Log

วันที่: YYYY-MM-DD
ผู้บันทึก: <ชื่อ หรือ "AI session — Claude Code">

## Source References

- <REF>

## Work Sessions

### Session 1

เวลา:
สิ่งที่ทำ:
- <ITEM>

สิ่งที่เพิ่มหรือแก้:
- <ITEM>

การทดสอบ:
- <ITEM>

ผลการทดสอบ:
- <ITEM>

ปัญหาที่พบ:
- <ITEM>

งานคงค้าง:
- <ITEM>
```

---

## Daily Summary Template

```md
# YYYY-MM-DD Summary

วันที่: YYYY-MM-DD

## สรุป

- <ITEM>

## การทดสอบ

- <ITEM>

## ขั้นถัดไป

- <ITEM>

## Log อ้างอิง

- `doc/03-log/YYYY/MM/YYYY-MM-DD-log.md`
```

---

## Monthly Summary Template

```md
# YYYY-MM Summary

เดือน: YYYY-MM

## ความคืบหน้าโดยรวม

- <ITEM>

## งานสำคัญที่เสร็จ

- <ITEM>

## งานที่ยกไปเดือนหน้า

- <ITEM>

## การตัดสินใจสำคัญ

- <ITEM>

## ความเสี่ยง

- <ITEM>
```

---

## ตัวอย่าง AI-CONTEXT ของ work-log-index ที่กรอกแล้ว

```
<!-- AI-CONTEXT
last_session: 2026-04-28
tool: Claude Code
completed: [T-001, T-002]
checkpoint: none
next_from_last: T-003 T-004
notes: ADR-001 created for auth approach
-->
```
