<!-- AI-CONTEXT
cmd: caw-launch-check
steps: [run_compliance_scan, check_tasks_in_scope_done, verify_adrs_recorded, check_placeholders, game_checks_if_flag, output_report_with_pass_fail, list_action_required_if_fail]
flags: [--game, version_string]
rule: all_FAIL_need_task_before_ready | human_approves_before_deploy
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-launch-check

รัน launch checklist ก่อน deploy หรือ release milestone
ใช้ร่วมกับ `core/16-launch-checklist-template.md`
-->

## วิธีใช้

```
/caw-launch-check
/caw-launch-check --game     ← รวม game-specific checks
/caw-launch-check v1.2.0     ← ระบุ version ใน report
```

## สิ่งที่ทำ

1. รัน compliance scan ครบทุก rule (เทียบกับ /caw-compliance-check)
2. ตรวจ task-board: ทุก task ใน scope นี้อยู่ใน done หรือมี task สำหรับ blocked
3. ตรวจ ADR index: ทุก architectural decision ใน milestone นี้มีบันทึก
4. ตรวจ placeholder ค้างในทุกไฟล์
5. ถ้า `--game`: ตรวจ playtest report, balance check, asset registry, performance budget
6. Output report พร้อมรายการ PASS/FAIL/SKIP
7. ถ้ามี FAIL: แสดง action required พร้อม task ID ก่อน deploy

## กฎ

- ทุก FAIL ต้องมี task ใน board ก่อนที่ report จะถือว่า "ready to deploy"
- มนุษย์ต้อง approve checklist ก่อน deploy จริง — AI ไม่ deploy เอง
