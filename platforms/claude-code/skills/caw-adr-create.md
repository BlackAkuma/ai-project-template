<!-- AI-CONTEXT
cmd: caw-adr-create
trigger: when making non-obvious architectural decisions
steps: [get_title, read_adr_index, create_adr_file_from_template, fill_id_title_date_author, fill_context_options, leave_decision_blank, update_adr_index]
default_status: Proposed
approver: human
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-adr-create

สร้าง Architecture Decision Record ใหม่
บันทึกใน `CoreAiWorkspaces/07-decisions/ADR-NNN-[title].md`
-->

## วิธีใช้

```
/caw-adr-create
/caw-adr-create "ชื่อ decision"
```

## สิ่งที่ทำ

1. ถามชื่อ decision (ถ้าไม่ได้ระบุ)
2. ดู ADR index ใน `CoreAiWorkspaces/07-decisions/README.md` เพื่อหา ID ถัดไป (ADR-NNN)
3. สร้างไฟล์ `CoreAiWorkspaces/07-decisions/ADR-NNN-[title].md` จาก template ใน `core/12-adr-template.md`
4. กรอก: ID, ชื่อ, วันที่, status = Proposed, author = AI session
5. กรอก Context ให้ครบ (สถานการณ์, constraints ที่มี)
6. ระบุ options ที่พิจารณา (อย่างน้อย 2 options)
7. เว้น Decision ว่าง — มนุษย์เป็น approver
8. อัปเดต ADR index

## หมายเหตุ

- ADR ที่ AI สร้างจะมี status = Proposed เสมอ
- มนุษย์ต้องเปลี่ยน status เป็น Accepted/Rejected
- ADR ห้ามลบ — ถ้า outdated ให้ Supersede ด้วย ADR ใหม่
