<!-- AI-CONTEXT
cmd: caw-fdd-create
trigger: before implementing any new feature (game projects)
steps: [get_feature_name, read_fdd_index, create_fdd_from_template, fill_id_name_date_task_ref, write_section1_only, wait_approve, update_fdd_index]
template_src: skills/game/01-fdd-template.md
output_path: CoreAiWorkspaces/08-design/[feature-name].md
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-fdd-create

สร้าง Feature Design Document ใหม่จาก template
บันทึกใน `CoreAiWorkspaces/08-design/[feature-name].md`
-->

## วิธีใช้

```
/caw-fdd-create
/caw-fdd-create "ชื่อ feature"
```

## สิ่งที่ทำ

1. ถามชื่อ feature (ถ้าไม่ได้ระบุ)
2. ดู FDD index ใน `CoreAiWorkspaces/08-design/README.md` เพื่อหา ID ถัดไป (FDD-NNN)
3. สร้างไฟล์ `CoreAiWorkspaces/08-design/[feature-name].md` จาก template ใน `skills/game/01-fdd-template.md`
4. กรอก: FDD ID, ชื่อ, วันที่, task reference (ถ้ามี)
5. เขียนส่วนที่ 1 ก่อน รอ approve ก่อนไปส่วนถัดไป (ตาม FDD protocol)
6. อัปเดต FDD index ใน `CoreAiWorkspaces/08-design/README.md`

## หมายเหตุ

- FDD ต้องได้รับ approve ก่อน task จะออกจาก design_validate
- เขียนทีละ section รอ approve ก่อนเสมอ — ห้ามเขียนครบทีเดียว
