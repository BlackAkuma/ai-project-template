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
7. **agent diary** — ถ้า `doc/03-log/agents/` มีอยู่ ให้เพิ่ม entry ใน `doc/03-log/agents/claude-code.md`:
   - งานที่ทำใน session นี้, decisions ที่ทำเอง, blocked items, next
   - ถ้าไฟล์ยังไม่มีให้สร้างใหม่ตาม format ใน `core/08-log-and-summary-template.md`
   - sync AI-CONTEXT block: `agent`, `last_session`, `focus`, `checkpoint`
8. **daily log** — ถ้ามีงานที่ต้องบันทึกรายละเอียด ให้เพิ่มหรือสร้าง `doc/03-log/YYYY/MM/YYYY-MM-DD-log.md`
9. รายงานสรุปสิ่งที่ sync ไปทั้งหมด

## ถ้า task ยังค้าง

task ที่ยัง in_progress จะถูก mark เป็น:
`[IN_PROGRESS: checkpoint saved — <สิ่งที่ทำไปแล้ว>]`

พร้อม next action ที่ชัดเจนใน work-log

## Cross-Project Memory (optional)

หลังจาก sync ครบ 9 ขั้นแล้ว — ถามผู้ใช้ว่า:

> "มี pattern หรือ lesson จาก session นี้ที่ควรบันทึกข้ามโปรเจ็กต์ไหม?  
> (เช่น วิธีแก้ปัญหาที่น่าจะใช้ได้กับโปรเจ็กต์อื่น)"

ถ้าผู้ใช้ตอบว่ามี:
1. ตรวจว่า `~/ai-workspace/cross-project-memory.md` มีอยู่ไหม — ถ้าไม่มีให้สร้างจาก `core/18-cross-project-memory-template.md`
2. เพิ่ม pattern หรือ lesson ลงในส่วนที่ถูกต้อง (Patterns That Worked / Lessons Learned / ADR Cross-Reference)
3. อัปเดต AI-CONTEXT block: `last_updated`, `active_patterns`
4. แจ้งผู้ใช้ว่าบันทึกเรียบร้อยแล้วที่ path ไหน

ถ้าผู้ใช้ตอบว่าไม่มี หรือข้าม — ไม่ต้องทำ
