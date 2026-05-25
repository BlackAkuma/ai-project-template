<!-- AI-CONTEXT
cmd: caw-debug
trigger: manual
steps: [step1_reproduce, step2_isolate, step3_hypothesize, step4_verify, report_findings]
flags: [--silent, --log]
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-debug

รัน 4-step debug-mantra checklist อัตโนมัติเพื่อ diagnose ปัญหาอย่างเป็นระบบ
-->

## วิธีใช้

```
/caw-debug
/caw-debug "error message หรือ อาการที่พบ"
/caw-debug --log     ← บันทึกผลลงใน work-log-index ด้วย
/caw-debug --silent  ← แสดงเฉพาะ findings สรุป ไม่แสดง step-by-step
```

## 4-Step Debug Mantra

### Step 1 — Reproduce (ทำซ้ำได้ไหม?)

> "ถ้าทำซ้ำไม่ได้ ยังไม่รู้ว่า bug จริงไหม"

- ระบุ exact steps ที่ trigger ปัญหา
- ระบุ expected vs actual behavior
- ระบุ environment: branch, version, config ที่ใช้
- ถ้าทำซ้ำไม่ได้ → mark เป็น `[INTERMITTENT]` และบันทึก condition ที่สังเกตได้

### Step 2 — Isolate (ปัญหาอยู่ที่ไหน?)

> "Narrow down ให้เหลือน้อยที่สุดก่อน fix"

- ระบุ component / module / function ที่น่าสงสัย
- ตัดสิ่งที่ไม่เกี่ยวออก — test ทีละส่วน
- ตรวจ dependency chain: ปัญหาเกิดที่ caller หรือ callee?
- ตรวจ recent changes: มี commit ล่าสุดที่แตะส่วนนี้ไหม? (`git log --oneline -10`)

### Step 3 — Hypothesize (สาเหตุที่เป็นไปได้คืออะไร?)

> "ตั้ง hypothesis ก่อน fix — ห้ามเดาแล้วแก้ทันที"

- ระบุ hypothesis อย่างน้อย 2 ข้อ เรียงจาก most likely → least likely
- สำหรับแต่ละ hypothesis ระบุ:
  - สิ่งที่ต้องเป็นจริงถ้า hypothesis นี้ถูก
  - วิธี verify ที่เร็วที่สุด
- เลือก hypothesis ที่จะ test ก่อน — อธิบายเหตุผล

### Step 4 — Verify (hypothesis ถูกไหม?)

> "Test hypothesis — ไม่ใช่ fix สุ่ม"

- รัน test ตาม hypothesis ที่เลือก
- บันทึกผล: confirmed / refuted
- ถ้า refuted → กลับ Step 3 เลือก hypothesis ถัดไป
- ถ้า confirmed → ระบุ root cause และเสนอ fix

## Output Format

```
=== Debug Report ===
Issue: [อาการที่ผู้ใช้ระบุ]
Timestamp: [วันที่/เวลา]

Step 1 — Reproduce
  Reproducible: yes / no / intermittent
  Steps: [...]
  Expected: [...]
  Actual: [...]

Step 2 — Isolate
  Scope: [component/module/function]
  Recent changes: [commit หรือ none]
  Isolated to: [...]

Step 3 — Hypotheses
  H1 (most likely): [...]  →  verify by: [...]
  H2: [...]  →  verify by: [...]

Step 4 — Verify
  Tested: H1
  Result: confirmed / refuted
  Root cause: [...]

Fix recommendation: [...]
Next action: [fix inline | create task T-XXX | escalate]
```

## กฎการใช้

- ห้าม skip step — ถ้าข้อมูลไม่พอให้ระบุ `[UNKNOWN — need more info]` แทนการเดา
- ถ้า root cause เกี่ยวกับ architecture → สร้าง ADR draft ก่อน fix (`/caw-adr-create`)
- ถ้า fix ใหญ่กว่า 1 function → สร้าง task ใหม่แทนการ inline fix
- ใช้ `--log` เมื่อต้องการ traceability เช่น ก่อน release หรือ bug ที่ reoccur
