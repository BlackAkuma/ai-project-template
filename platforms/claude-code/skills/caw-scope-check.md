<!-- AI-CONTEXT
cmd: caw-scope-check
steps: [read_task, read_source_ref, compare_impl_vs_scope, report_in_scope_out_scope_missing, create_task_if_out_of_scope]
output_format: scope_check_report
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-scope-check

ตรวจ scope ของ task ปัจจุบันว่า implement ตรงกับที่กำหนดไว้หรือไม่
-->

## วิธีใช้

```
/caw-scope-check
/caw-scope-check T-042
```

## สิ่งที่ทำ

1. อ่าน task ที่ระบุ (หรือ task ที่ in_progress อยู่ตอนนี้)
2. อ่าน source reference ของ task นั้น
3. เปรียบเทียบสิ่งที่กำลัง implement กับ scope ที่กำหนด
4. รายงาน:
   - **In scope:** สิ่งที่ทำอยู่ตรงกับ requirement
   - **Out of scope:** สิ่งที่พบว่าเพิ่มเกิน scope
   - **Missing:** สิ่งที่ requirement ต้องการแต่ยังไม่ได้ทำ
5. ถ้าพบ out of scope: สร้าง task ใหม่ตาม Scenario C ใน ai-decision-protocol.md

## Output Format

```
=== Scope Check — T-042 ===

Source: CoreAiWorkspaces/00-source/versions/v0.2/feature-spec.md#section-3

In scope ✓
  - player movement with delta time
  - collision detection

Out of scope ✗ → task T-048 สร้างแล้ว
  - particle effects on collision (ไม่มีใน requirement)

Missing ⚠
  - sound effect trigger (ระบุใน requirement แต่ยังไม่ implement)
```
