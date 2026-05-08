# Work Status Template

คัดลอกและปรับไฟล์นี้เป็น `ai/01-plan/work-status.md`

**กฎสำคัญ:** เมื่ออัปเดตส่วน body ด้านล่าง ต้องอัปเดต `AI-CONTEXT` block ด้านบนพร้อมกันเสมอ

---

## รูปแบบ AI-CONTEXT Block

Block นี้อยู่ด้านบนสุดของไฟล์ เพื่อให้ AI อ่านได้ทันทีโดยไม่ต้องผ่าน body ทั้งหมด
ใช้ HTML comment เพื่อไม่แสดงผลใน rendered markdown

**Field ที่ใช้:**

| Field | ความหมาย | ตัวอย่าง |
|-------|----------|---------|
| `src` | source doc version ปัจจุบัน | `v0.2` |
| `phase` | milestone/phase ปัจจุบัน | `M1` |
| `direction` | เป้าหมายหลักของ phase | `Core API build` |
| `focus` | task ที่กำลังทำอยู่ (ID) | `[T-003, T-004]` |
| `done` | task ที่เสร็จแล้ว (ID ย่อ) | `[T-001, T-002]` |
| `blocked` | task ที่ติดขัด + เหตุผลสั้น | `T-005: waiting API spec` หรือ `none` |
| `next` | งานลำดับถัดไปตามลำดับ | `T-003 > T-004 > T-005` |
| `risk` | risk ที่ active อยู่ | `auth latency > 500ms` หรือ `none` |
| `adr` | ADR index ที่เกี่ยวข้องกับ phase นี้ | `ADR-001 ADR-002` หรือ `none` |
| `read_more` | map "topic: path" สำหรับ AI ที่ต้องการ context เพิ่ม | ดูตัวอย่างด้านล่าง |
| `updated` | วันที่อัปเดตล่าสุด | `2026-04-28` |
| `git_prod_branch` | production branch — ห้าม commit ai/ ที่นี่ | `main` |
| `git_dev_branch` | dev branch ที่ AI ทำงานและ ai/ อาศัยอยู่ | `dev` |
| `git_mode` | branch strategy ของโปรเจ็กต์นี้ | `branch-separated` หรือ `single-branch` |

---

## Template ไฟล์จริง

```md
<!-- AI-CONTEXT
src: <CURRENT_SOURCE_VERSION>
phase: <PROJECT_PHASE>
direction: <PHASE_GOAL_SHORT>
focus: [<TASK_IDS_IN_PROGRESS>]
done: [<TASK_IDS_DONE>]
blocked: <TASK_ID: reason> | none
next: <T-XXX> > <T-XXX> > <T-XXX>
risk: <SHORT_RISK_DESC> | none
adr: <ADR_IDS_RELEVANT> | none
read_more:
  architecture: ai/07-decisions/README.md
  entities: ai/07-decisions/entity-register.md
  source_current: ai/00-source/versions/<CURRENT_SOURCE_VERSION>/
updated: <CURRENT_DATE>
git_prod_branch: <PROD_BRANCH>
git_dev_branch: <DEV_BRANCH>
git_mode: <branch-separated|single-branch>
-->

---

# สถานะโปรเจ็กต์ — <PROJECT_NAME>

อัปเดตล่าสุด: <CURRENT_DATE>

## Source ที่ใช้อ้างอิง

- `ai/00-source/versions/<CURRENT_SOURCE_VERSION>/<SOURCE_DOC>.md`

## เฟสและทิศทาง

**เฟสปัจจุบัน:** <PROJECT_PHASE>

<PRODUCT_DIRECTION_SUMMARY>

## งานที่กำลังทำ

- `T-XXX` — <คำอธิบาย>

## งานที่เสร็จแล้ว

- `T-XXX` — <คำอธิบาย>

## งานที่ติดขัด

- ไม่มี / `T-XXX` — <เหตุผล> — รอ: <สิ่งที่ต้องการ>

## งานถัดไปที่ต้องทำ

1. <ITEM>
2. <ITEM>

## ความเสี่ยงและหมายเหตุ

- <ITEM>
```

---

## ตัวอย่าง AI-CONTEXT ที่กรอกแล้ว

```
<!-- AI-CONTEXT
src: v0.2
phase: M1
direction: Core API build
focus: [T-003, T-004]
done: [T-001, T-002]
blocked: none
next: T-003 > T-004 > T-005
risk: none
adr: ADR-001
read_more:
  architecture: ai/07-decisions/README.md
  entities: ai/07-decisions/entity-register.md
  source_current: ai/00-source/versions/v0.2/
updated: 2026-04-28
-->
```
