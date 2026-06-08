<!-- AI-CONTEXT
cmd: caw-adr-review
trigger: any ADR in Proposed status (Scenario O) — run before asking human to approve
steps: [find_proposed_adrs, spawn_3lens_panel, vote_2of3, surface_dissent, analyze_majority, fix_small_defects_inline, lock_big_to_review, log_panel_record, present_to_human]
panel_lenses: [technical, strategic, contrarian]
optional_lens: marketing (feature/trend/market opinion)
pass_rule: 2_of_3
contrarian_rule: must produce real objection (no "no objection")
output_layer: L2
ref: ai-decision-protocol §7 (Scenario O)
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-adr-review

รัน 3-lens panel review บน ADR ที่ Proposed (Scenario O)
2/3 ผ่าน · บันทึก dissent + เหตุผลทุกครั้ง · ลดงาน human
-->

## วิธีใช้

```
/caw-adr-review            # review ADR Proposed ทั้งหมด
/caw-adr-review ADR-NNN    # review ตัวเดียว
```

## สิ่งที่ทำ

1. หา ADR สถานะ Proposed ใน `CoreAiWorkspaces/07-decisions/`
2. spawn **3 reviewer อิสระ/ADR** (lens ต่างกัน):
   - 🔬 **technical** — sound/feasible/implementable/consistent กับ ADR อื่น?
   - 🎯 **strategic** — serve vision/scope/defensible/priority?
   - 🔴 **contrarian** — บังคับหาเหตุผลที่แข็งสุดที่ควร REJECT + surface conflict ทุกตัว (ห้ามตอบ "ไม่มี")
   - (optional) 📈 **marketing** — feature/trend/market opinion
3. แต่ละ reviewer โหวต PASS/FAIL + reasons + conflicts + suggested fixes
4. **กติกา: 2/3 PASS = ผ่าน**
5. วิเคราะห์ต่อยอดจากเสียงส่วนใหญ่ + **เคารพ contrarian** (ถ้า defect จริง → iterate แก้ ไม่ override)
6. **เรื่องเล็ก/safe** → AI แก้ revise เองได้ + log
7. **เรื่องใหญ่ (reverse shipped behavior / irreversible)** → lock เป็น task รอ human/project-review
8. บันทึก **Panel Review Record** (โหวต + dissent + การตัดสิน) ท้าย ADR — อ่านย้อนได้
9. เสนอผล + ทางเลือก + ความเห็นต่าง ให้ human ตัดสิน lock

## หมายเหตุ

- reusable workflow: `workflows/scripts/adr-review-panel-*.js`
- precedent: ADR-006..013 (G1/G3/G4) — ทุกตัวผ่าน panel + dissent logged
- decision ที่ต้อง human ตัดสิน → present เสมอ ไม่ auto-decide เรื่อง strategic fork
