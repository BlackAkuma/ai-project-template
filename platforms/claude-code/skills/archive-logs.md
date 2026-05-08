# /archive-logs

Compress session entries เก่าใน work-log-index และ task-board
ใช้เมื่อ AI แจ้ง C-12 หรือ C-13 หรือสั่งเองเมื่อต้องการ

## วิธีใช้

```
/archive-logs              ← archive ทั้ง log และ task-board
/archive-logs --logs-only  ← archive เฉพาะ work-log-index
/archive-logs --tasks-only ← archive เฉพาะ task-board done section
```

## สิ่งที่ทำ — Log Archive

1. อ่าน Recent Sessions ทั้งหมดใน work-log-index
2. สร้าง `CoreAiWorkspaces/03-log/archive/YYYY-MM-sessions.md` สำหรับแต่ละเดือนที่ archive
   - บันทึก: งานที่เสร็จ, decisions สำคัญ, สิ่งที่ยกไปต่อ, task references
3. อัปเดต **Milestone Summary** ใน work-log-index ให้ครอบคลุม session ที่ archive
4. ลบ session entry เก่าออก เหลือแค่ 10 session ล่าสุด
5. อัปเดต AI-CONTEXT block

## สิ่งที่ทำ — Task Archive

1. หา task ใน done section ที่เก่ากว่า 30 วัน
2. ย้ายไป `CoreAiWorkspaces/02-task/archive/done-YYYY-MM.md`
3. เก็บ 5 task ล่าสุดไว้ใน task-board เพื่อ context
4. อัปเดต AI-CONTEXT block ของ task-board

## สิ่งที่ไม่เปลี่ยน

- **Milestone Summary** ใน work-log-index — ไม่ archive ไม่ย่อ เพิ่มข้อมูลอย่างเดียว
- **AI-CONTEXT block** ของทุกไฟล์ — อัปเดตให้ตรงหลัง archive เสมอ
- **archive files** — ไม่ลบ สะสมไปเรื่อย ๆ ใน archive/ folder

## Output หลัง archive

```
=== Archive Complete ===

Log archive:
  สร้าง CoreAiWorkspaces/03-log/archive/2026-01-sessions.md (23 sessions)
  สร้าง CoreAiWorkspaces/03-log/archive/2026-02-sessions.md (18 sessions)
  work-log-index: 340 บรรทัด → 87 บรรทัด

Task archive:
  ย้าย 12 done tasks → CoreAiWorkspaces/02-task/archive/done-2026-01.md
  task-board done section: 15 รายการ → 5 รายการ

Milestone Summary อัปเดตแล้ว — AI session ใหม่จะยังรู้ว่าทำอะไรไปแล้ว
```
