# Governed Project Memory — Engine

> **enforcement เหนือ AGENTS.md + durable project Decision Inbox** — governance ที่ **เครื่องบังคับเป็น state จริง** ไม่ใช่หวังให้ model ทำตาม

ชั้น 2 ของ vision (ADR-006). agent ทำ "done" ปลอมไม่ได้เชิงโครงสร้าง · ทุกการตัดสิน tamper-evident audit ได้ · risk-tiered (กัน approval fatigue)

> สถานะ: Engine core complete — linter + constitutive enforcement + JSON-in-git canonical store + Decision Inbox data layer (45 tests/6 suites). Shell UI gated on demand (ADR-013). ดู `../exploration/master-plan.md`

## Quickstart (OSS soft-ship)
```bash
pip install -r engine/requirements.txt        # pyyaml
python engine/demo.py                          # ▶ <10min hero demo (end-to-end)
python engine/check.py task-close --task T-1   # governance gate vs real state
for t in resolvers events govern store inbox; do python engine/test_$t.py; done   # 45 tests
```
> ⚠️ **LICENSE ยังไม่มี** — ก่อน publish OSS ต้องเลือก license (MIT แนะนำสำหรับ OSS-core wedge, ADR-013) = การตัดสินของผู้ใช้

## หลักการ (ADR-007/008)
- **structured = source of truth** ของ enforceable state · predicate ตรวจ state จริง (git/file/test) ไม่เชื่อคำพูด agent
- **risk-tiered** (Level 0-3) ไม่ uniform · **enforce presence/structure ไม่ใช่ quality**

## โครงสร้าง
```
engine/
├── gates/              # gate definitions (rules-as-data)
│   ├── _grammar.md     # YAML gate grammar spec
│   └── *.yaml          # gate แต่ละตัว (trigger → predicate → effect)
├── resolvers/          # predicate vocabulary (Python) — vetted, ไม่ใช่ open expression
└── cli/                # `engine check <gate>` (P2)
```

## Roadmap (flow-plan §3)
- **P1** config-driven validator: gate YAML + resolver + wire validate-commit.sh (dogfood repo นี้)
- **P2** `engine check` CLI + risk-tier + CI = **MVW (governance linter ship ได้)**
- **G1** หลัง P2: หยุดที่ CLI หรือไป P3 (interception)
