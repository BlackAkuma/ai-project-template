# Engine — Governed Project Memory (headless governance core)

ชั้น 2 ของ vision (ADR-006) — governance ที่ **เครื่องบังคับได้** ไม่ใช่หวังให้ model ทำตาม

> สถานะ: 🔬 P1-P2 build (config-driven validator → CLI evaluator) · ดู `exploration/master-plan.md` + `flow-plan.md`

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
