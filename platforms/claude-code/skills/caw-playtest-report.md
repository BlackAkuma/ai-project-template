<!-- AI-CONTEXT
cmd: caw-playtest-report
requires: CoreAiWorkspaces/08-design/ (game projects only)
steps: [find_playtest_tasks, read_fdd_section8, create_report_template, save_to_08_design, update_task_on_result]
output_path: CoreAiWorkspaces/08-design/playtest-<feature>-YYYY-MM-DD.md
pass_action: move_task_to_review
fail_action: move_task_to_in_progress_with_issues
compliance_ref: skills/game/01-fdd-template.md section 8
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-playtest-report

สร้าง playtest report template สำหรับ feature ที่อยู่ในขั้น `playtest`

**ใช้กับ:** game projects เท่านั้น (ต้องมี `CoreAiWorkspaces/08-design/`)
-->

---

## สิ่งที่ทำ

1. ตรวจ task board หา task ที่มีสถานะ `playtest`
2. อ่าน FDD ที่ task นั้นอ้างถึง — โดยเฉพาะส่วนที่ 8 (เกณฑ์การยืนยัน)
3. สร้าง report template พร้อม checklist จาก FDD ส่วนที่ 8
4. บันทึกไว้ใน `CoreAiWorkspaces/08-design/playtest-<feature-name>-YYYY-MM-DD.md`

---

## Output Template

```markdown
# Playtest Report — <Feature Name>

**วันที่:** YYYY-MM-DD
**Tester:** <ชื่อ>
**FDD Reference:** FDD-NNN
**Task:** T-XXX

## Checklist (จาก FDD ส่วนที่ 8)

- [ ] <เกณฑ์ข้อ 1 จาก FDD>
- [ ] <เกณฑ์ข้อ 2 จาก FDD>
- [ ] ประสิทธิภาพอยู่ใน budget ที่กำหนด

## สิ่งที่พบ

| # | คำอธิบาย | ระดับ | FDD Section |
|---|---------|-------|-------------|
| 1 | ...     | ...   | ...         |

## สรุป

- [ ] PASS — feature พร้อมไป `review`
- [ ] FAIL — ต้องแก้ไขก่อน
```

---

## หลังสร้าง Report

- PASS → เปลี่ยน task เป็น `review` อัปเดต work-status
- FAIL → เปลี่ยน task กลับเป็น `in_progress` ระบุ issue ที่ต้องแก้ใน task description

---

## Compliance Rule

ตาม **lifecycle enforcement**: task ต้องผ่าน FDD ส่วนที่ 8 ทั้งหมดก่อนออกจาก `playtest` → `review`
