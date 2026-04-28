# /session-end

Sync work-status, work-log-index, และ task-board ครบในคำสั่งเดียว
ใช้ก่อนปิด session เสมอ

## วิธีใช้

```
/session-end
/session-end "สรุปสั้น ๆ ว่าทำอะไรใน session นี้"
```

## สิ่งที่ทำตามลำดับ

1. **work-status** — อัปเดต body: phase, focus, done, blocked, next, risk
2. **work-status** — sync AI-CONTEXT block ให้ตรงกับ body
3. **work-log-index** — เพิ่ม entry ใหม่: วันที่, tool, สิ่งที่ทำ, checkpoint, next
4. **work-log-index** — sync AI-CONTEXT block: last_session, completed, next_from_last
5. **task-board** — อัปเดต status ของ task ที่เปลี่ยนใน session นี้
6. **task-board** — sync AI-CONTEXT block: active, blocked, done, priority_next
7. **daily log** — ถ้ามีงานที่ต้องบันทึกรายละเอียด ให้เพิ่มหรือสร้าง `doc/03-log/YYYY/MM/YYYY-MM-DD-log.md`
8. รายงานสรุปสิ่งที่ sync ไปทั้งหมด

## ถ้า task ยังค้าง

task ที่ยัง in_progress จะถูก mark เป็น:
`[IN_PROGRESS: checkpoint saved — <สิ่งที่ทำไปแล้ว>]`

พร้อม next action ที่ชัดเจนใน work-log
