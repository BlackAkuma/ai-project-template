# Governed Project Memory — Engine

> **enforcement เหนือ AGENTS.md + durable project Decision Inbox** — governance ที่ **เครื่องบังคับเป็น state จริง** ไม่ใช่หวังให้ model ทำตาม

ชั้น 2 ของ vision (ADR-006). agent ทำ "done" ปลอมไม่ได้เชิงโครงสร้าง · ทุกการตัดสิน tamper-evident audit ได้ · risk-tiered (กัน approval fatigue)

> สถานะ: Engine core complete — linter + constitutive enforcement + JSON-in-git canonical store + Decision Inbox data layer (45 tests/6 suites). Shell UI gated on demand (ADR-013). ดู `../exploration/master-plan.md`

## ▶ Run the product (end-to-end, no Node/build needed)
```bash
pip install -r engine/requirements.txt        # pyyaml
python engine/api.py                           # starts API + web Cockpit on http://127.0.0.1:8777
# → open http://127.0.0.1:8777 in a browser: project + Decision Inbox (approve/reject) + run governed turn
```
Or as a CLI tool:
```bash
python engine/cli.py cockpit                   # render project state
python engine/cli.py turn T-1 mark_done --model claude-sonnet   # governed agent turn
python engine/cli.py gate task_close_gate --task T-1            # check a gate
python engine/cli.py inbox                      # open Decision Inbox items
python engine/cli.py audit                      # verify tamper-evident chain
```

## Quickstart (tests + demo)
```bash
python engine/demo.py                          # ▶ <10min hero demo (end-to-end narrated)
for t in resolvers events govern store inbox adversarial llm agent repo memory cockpit migrate entities evidence check cli api; do python engine/test_$t.py; done   # 17 suites
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
