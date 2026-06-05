<!-- AI-CONTEXT
doc: BRD
version: 0.1
status: draft (await panel review)
product: Governed Project Memory
schema_version: "0.1"
review_method: 3-lens panel (technical/strategic/contrarian) 2/3 + marketing advisory
rationale_refs: [exploration/north-star-vision.md, exploration/what-it-should-be.md, exploration/master-plan.md, exploration/flow-plan.md, exploration/a1-core-schema.md]
decisions_locked: [ADR-006, ADR-007, ADR-008, ADR-009]
-->

# BRD — Governed Project Memory

**Version:** 0.1 (draft) · **Date:** 2026-06-05 · **Status:** await panel review
**เอกสารนี้ = source of truth ของ requirements** · rationale/analysis อยู่ใน `exploration/` (อ้างอิง ไม่ duplicate)

---

## 1. Vision & Problem

**Vision:** ระบบ governance + project memory ที่ AI ตัวไหนก็ทำงานเชิงโครงการได้น่าเชื่อถือ เพราะกฎถูก **บังคับเป็น state จริง** ไม่ใช่หวังให้โมเดลทำตาม — รันบนเครื่องตัวเอง เสียบ model ไหนก็ได้

**Problem (pain ที่ยืนยันจากผู้ใช้ + ตลาด):**
- AI พัฒนาโครงการผ่าน web/tool → "ให้ AI อ่าน docs เสมอ แต่หลุดบ่อย" (context ไม่เสถียร, advisory)
- การตัดสินใจถูกถกซ้ำทุก session, docs drift กับ code, governance เป็นแค่คำขอ
- ตลาด: 88% องค์กรเจอ AI-agent incident, project memory (structured/durable) ยังไม่มีใครแก้

**Thesis:** AI capability = context engineering ไม่ใช่ตัว model (model = commodity)

## 2. Goals & Success Metrics

| Goal | Metric |
|------|--------|
| Governance ที่ enforce ได้จริง | agent bypass gate ไม่ได้ (adversarial test ผ่าน) |
| Context ไม่หลุดข้าม session | state ไม่ drift (generated จาก canonical store) |
| Model-agnostic | swap frontier↔local แล้ว governance ยังอยู่ |
| ลด human review load | risk-tiered: เฉพาะ Level 2-3 เข้า Decision Inbox |
| Multi-project/repo | govern ข้ามหลาย repo เป็นโครงการเดียว |

## 3. Target Users / Segments

- **Primary:** ทีม dev/ops 2-10 คน ที่ต้องการ self-hosted AI governance (data อยู่บ้าน, cost คุมได้)
- **Secondary:** solo developer ที่ทำหลายโครงการ/หลาย repo
- **Beachhead:** SEA/Thai teams (sovereignty + local-model routing) — credibility ไม่ใช่ TAM หลัก
- **Underserved gap:** project-centric + enforced-governance + multi-agent + multi-repo (ไม่มีใครถือครบ 4)

## 4. Scope

**In scope:**
- Substrate (methodology/template) · Engine (machine-enforced governance) · Shell (project-centric app)
- Domain-agnostic CORE + PROFILE packs (generic-software + game โฟกัส; ต่อ Godot/Unreal)
- Self-hosted, model-agnostic (LiteLLM), multi-repo orchestration

**Out of scope (อย่าทำ):**
- ❌ out-index Sourcegraph/Augment (orchestrate ไม่ใช่ index)
- ❌ out-orchestrate LangGraph / out-gateway Portkey (compose underneath)
- ❌ reinvent AGENTS.md (interoperate)
- ❌ atomic cross-repo refactor (detect/route/sequence เท่านั้น — human owns seam)
- ❌ headline "swarm" (orchestrated specialist สำหรับงาน parallel เท่านั้น)

## 5. Functional Requirements (5 เสา)

### FR-1 Governed (enforced, risk-tiered)
- FR-1.1 gate = trigger→predicate→effect, predicate ตรวจ state จริง (git/file/test) ไม่เชื่อ agent claim
- FR-1.2 risk-tier Level 0-3 (ADR-008): L0 triage(always) · L1 auto-log · L2 Decision Inbox · L3 hard-stop
- FR-1.3 hard-stop conditions ห้ามลด: data loss, security, prod, ขัด requirement ชัดเจน
- FR-1.4 risk classification = Engine-determined ไม่ใช่ AI self-assess; default unknown→L2
- FR-1.5 enforce presence/structure ไม่ใช่ quality

### FR-2 Project Memory (structured, durable, evolving)
- FR-2.1 canonical state store; prose = generated view (dual-authority, ADR-007)
- FR-2.2 AI-CONTEXT schema เดียว typed (เลิก field collision)
- FR-2.3 CORE entities: Project/Requirement/Task/Evidence/Decision/TeamMember/Gate/Repo/Entity/Event (ADR-009, a1-core-schema)
- FR-2.4 evidence = machine-verifiable | human-attested (ADR-009 D2)
- FR-2.5 task lifecycle `todo→design_validate→in_progress→review→done` + profile sub-gate

### FR-3 Decision Inbox (human-gate first-class)
- FR-3.1 ทุก Level 2-3 → durable Decision Inbox item (project-level ไม่ใช่ per-run)
- FR-3.2 ADR Proposed → 3-lens panel (Scenario O) → 2/3 + dissent logged → human approve
- FR-3.3 ทุก review บันทึก Panel Review Record (เหตุผล+โหวต+การตัดสิน) กลับไปอ่านได้

### FR-4 Model-agnostic + Self-hosted
- FR-4.1 เสียบ model ไหนก็ได้ผ่าน LiteLLM (local + cloud)
- FR-4.2 role floor: โมเดลต่ำกว่า floor → จำกัด read-only/advisory lane
- FR-4.3 self-hosted, data อยู่ในเครื่อง, key encrypted at rest

### FR-5 Multi-repo orchestration
- FR-5.1 project = manifest ของ repos + project map (always-in-context)
- FR-5.2 cross-repo entity-register (drift detection)
- FR-5.3 detect impact + route slice + sequence behind gates (ไม่ atomic refactor)

## 6. Non-Functional Requirements

- NFR-1 Security: credentials = Level 3, SSRF/prompt-injection defense, no secret in log
- NFR-2 Sovereignty: git-native, no proprietary cloud lock-in
- NFR-3 Layer-1 compat: degrade graceful เป็น advisory markdown เมื่อไม่มี Engine
- NFR-4 Concurrency: Engine = serialization point (append-only event log)
- NFR-5 Cost: per-task budget cap (กัน swarm blow-up)
- NFR-6 Bilingual (Thai/English) — TACP L1/L2/L3

## 7. Constraints & Dependencies (compose underneath)

- LiteLLM (routing) · OPA / MS Agent Governance Toolkit (runtime policy) · Qdrant (vector) · SvelteKit (Shell) · SQLite→Postgres
- interoperate AGENTS.md standard

## 8. Risks (ดู master-plan §5 เต็ม)

R1 sandbox-escape (กำแพงทั้งเกม) · R3 SQLite vs git-native (G3) · R5 "ร้อนรน"/build Shell ก่อน · R7 approval fatigue · R9 คู่แข่งปิด gap (Cursor/Factory) · model-floor

## 9. Roadmap (ดู flow-plan.md granular)

Substrate(✅partial) → Engine P1-P2 (MVW: governance linter) → P3 interception → P4 store → P5 Cockpit → **P6 SHIP** (governed agent + Decision Inbox) → P7-P10

## 10. Open Decisions (ต้อง panel + user vote → lock)

| ID | decision | สถานะ |
|----|----------|-------|
| OD-1 | G3: SQLite vs JSON-in-git canonical store | open (panel เมื่อถึง P4) |
| OD-2 | G1: หยุดที่ Engine-CLI (ship linter) หรือไป P3 | open (หลัง P2) |
| OD-3 | G4: build Shell หรือหยุดที่ Engine | open |
| OD-4 | G5: universal vs optimize own-tool | deferred (post-SHIP) |

> decision เหล่านี้: สร้าง panel หาเหตุผล+ทางเลือก+โหวต+dissent → iterate จน consensus → lock เป็น ADR

---

*BRD v0.1 draft — สังเคราะห์จาก exploration + ADR-006..009. รอ panel review (3-lens 2/3 + marketing) → iterate → lock*
