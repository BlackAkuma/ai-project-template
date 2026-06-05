<!-- AI-CONTEXT
doc: BRD
version: 0.2
status: v0.2 — panel-1 consensus gaps addressed; re-review pending (iteration 2)
product: Governed Project Memory
schema_version: "0.1"
review_method: 3-lens panel (technical/strategic/contrarian) 2/3 + marketing advisory
panel_history: [iter1: 3/3 PASS (tech .70/strat .78/contra .60 borderline), marketing=viable]
rationale_refs: [../../exploration/north-star-vision.md, ../../exploration/what-it-should-be.md, ../../exploration/master-plan.md, ../../exploration/flow-plan.md, ../../exploration/a1-core-schema.md]
decisions_locked: [ADR-006, ADR-007, ADR-008, ADR-009]
-->

# BRD — Governed Project Memory

**Version:** 0.2 · **Date:** 2026-06-05 · **Status:** panel-1 gaps addressed, re-review pending
**source of truth ของ requirements** — self-contained (ไม่ต้องอ่าน 5 doc เพื่อรู้ว่า "done" คืออะไร); rationale อยู่ `exploration/`

---

## 0. Glossary (panel: source-of-truth ต้องนิยามศัพท์)

| term | นิยาม |
|------|------|
| **Substrate / Engine / Shell** | ชั้น 1 methodology(template) / ชั้น 2 governance ที่เครื่องบังคับ / ชั้น 3 แอป project-centric |
| **constitutive enforcement** | agent ทำผิดกฎไม่ได้เชิงโครงสร้าง (ต่างจาก advisory = ขอให้ทำตาม) |
| **gate** | trigger→predicate→effect ที่ Engine eval กับ state จริง |
| **predicate** | ฟังก์ชันตรวจ state (git/file/test) — vetted vocab (`engine/gates/_grammar.md`) |
| **risk tier (L0-3)** | ระดับความเสี่ยง action → กำหนด effect (L0 triage/L1 auto/L2 inbox/L3 hard-stop) |
| **dual-authority** | structured=truth ของ enforceable state · prose=truth ของ narrative (ADR-007) |
| **Decision Inbox** | คิว human-approval ระดับ project แบบ durable (ไม่ใช่ per-run) |
| **role floor** | tier ความสามารถขั้นต่ำของ model ต่อ lane (FR-4.2) |
| **dogfood** | ใช้ระบบกับ repo ตัวเองเป็น user คนแรก |

## 1. Vision & Problem
**Vision:** governance + project memory ที่ AI ตัวไหนก็ทำงานเชิงโครงการได้น่าเชื่อถือ เพราะกฎ **บังคับเป็น state จริง** — self-hosted, model-agnostic
**Problem:** "ให้ AI อ่าน docs เสมอ แต่หลุดบ่อย" (advisory ไม่เสถียร) · decision ถกซ้ำ · docs drift · governance = แค่คำขอ · ตลาด: 88% เจอ AI-agent incident, project-memory ยังไม่มีใครแก้
**Thesis:** AI capability = context engineering ไม่ใช่ model (model=commodity)

## 2. Goals & Success Metrics (วัดผลได้)

| Goal | Metric (target + method) |
|------|--------------------------|
| Governance enforce จริง | adversarial bypass blocked = **100%** (suite: agent พยายาม `echo>>task-board` mark done ฯลฯ, N≥10 เคส, 0 bypass) |
| Context ไม่ drift | block↔body mismatch = **0** (generated จาก store; CI check) |
| Model-agnostic | swap frontier↔local 7B → governance test pass **เท่าเดิม** (regression suite) |
| ลด review load | **Level-1 auto-pass ≥70%** ของ action · Decision Inbox ≤ X/task (วัดจาก event log) |
| Multi-repo | cross-repo impact detect **100%** ของ declared dependency change |

## 3. Target Users & Competitive Position

**Users:** primary = ทีม dev/ops 2-10 (self-hosted, data อยู่บ้าน) · secondary = solo multi-repo · beachhead = SEA/Thai (sovereignty, credibility ไม่ใช่ TAM)

**Competitive (first-class — panel: load-bearing):**
| คู่แข่ง | มี | ขาด (ช่องเรา) |
|--------|-----|--------------|
| Cursor 2.0 | multi-agent, model-agnostic, enforced admin-rules, distribution | multi-repo, **durable decision-ledger** |
| Factory.ai | cross-codebase, governance(roadmap), $1.5B | shipped governance, self-host, Decision Inbox |
| Odysseus/OpenWebUI | UI, self-host | governance, project-model, multi-repo |
| MS Conductor+Toolkit | runtime policy | project-persistent state, Decision Inbox |

**4 differentiator ที่ไม่มีใครถือครบ:** project-centric + enforced-governance-as-state + multi-agent + multi-repo
**Why now:** model commoditize + ราคาลด 80% · governance pain เฉียบ · project-memory category เพิ่งเปิด (mem0/Letta กำลังมา → ต้องปัก flag ตอนนี้)

## 4. Scope

**In:** Substrate · Engine · Shell · CORE + **game profile เดียว (deep) + extension hook** · self-hosted, model-agnostic, multi-repo orchestration
> ⚠️ reconcile (ADR-009 guidance): substrate phase = game profile เดียว; **compose-engine (web-game) defer post-SHIP** (แก้ scope ที่ panel ชี้ว่ากว้างเกิน)

**Out:** ❌ out-index Sourcegraph · ❌ out-orchestrate LangGraph · ❌ out-gateway Portkey · ❌ reinvent AGENTS.md · ❌ atomic cross-repo refactor · ❌ headline "swarm"

**Invariant:** **dogfood บน repo นี้** (user คนแรก = governance ของเราเอง)

## 5. Functional Requirements (+ phase + MoSCoW + acceptance)

> ID = FR-x.y · trace → ADR/task · phase ตาม flow-plan · M=Must(MVP) S=Should C=Could(post-SHIP)

### FR-1 Governed — phase P1-P3, **Must**
| ID | requirement | accept criteria | trace |
|----|-------------|-----------------|-------|
| FR-1.1 | gate trigger→predicate→effect ตรวจ state จริง | `engine check <gate>` ให้ verdict ถูกกับ staged state (มี test) | engine/gates, ADR-006 |
| FR-1.2 | risk-tier L0-3 (L0 triage always · L1 auto · L2 inbox · L3 hard-stop) | gate รัน effect ตาม level ถูก (verified) | ADR-008 |
| FR-1.3 | hard-stop ห้ามลด: data-loss/security/prod/ขัด-requirement | 4 condition force L3 ไม่ว่า classifier | ADR-008 |
| FR-1.4 | risk = Engine-determined, default unknown→L2 | AI self-downgrade ไม่ได้ (test) | ADR-008 |
| FR-1.5 | enforce presence/structure ไม่ใช่ quality | predicate แตะแค่ git/file/exit | ADR-007 |

### FR-2 Project Memory — phase P0-P4, **Must**
| ID | requirement | accept | trace |
|----|-------------|--------|-------|
| FR-2.1 | canonical store; prose=generated view | edit store → 2 view ตรงกันทุกครั้ง | ADR-007 |
| FR-2.2 | AI-CONTEXT schema เดียว typed | 3 state file validate ผ่าน schema | a1 §3 |
| FR-2.3 | CORE 11 entities: Project/Requirement/**Plan**/Task/Evidence/Decision/TeamMember/Gate/Repo/Entity/Event | ครบ 11 (แก้ Plan ที่หาย) | ADR-009 |
| FR-2.4 | evidence = machine-verifiable \| human-attested | 2 class ใน schema + Engine ตรวจต่างกัน | ADR-009 D2 |
| FR-2.5 | lifecycle todo→design_validate→in_progress→review→done + profile sub-gate | state machine + guard (done ต้องมี evidence) | a1 §2 |

### FR-3 Decision Inbox — phase P6, **Must**
| ID | requirement | accept | trace |
|----|-------------|--------|-------|
| FR-3.1 | Level 2-3 → durable project-level Inbox item | card persist ข้าม session | ADR-006 |
| FR-3.2 | ADR Proposed → Scenario O panel 2/3 + dissent → human | panel รัน + log ทุก ADR | Scenario O |
| FR-3.3 | ทุก review = Panel Review Record (เหตุผล+โหวต+ตัดสิน) | อ่านย้อนได้ใน ADR/BRD | Scenario O |

### FR-4 Model-agnostic + Self-hosted — phase P4/P7, **Should**
| ID | requirement | accept | trace |
|----|-------------|--------|-------|
| FR-4.1 | เสียบ model ผ่าน LiteLLM (local+cloud) | assign 2 provider ต่าง role ได้ | ADR-006 |
| FR-4.2 | role floor: model tier = **curated registry** (กำหนด floor ต่อ lane); ต่ำกว่า floor → read-only/advisory | bind sub-floor model → Engine ปฏิเสธ code-author lane | ADR-008 |
| FR-4.3 | self-hosted, key encrypted at rest, egress ผ่าน LiteLLM | no key in log (scan) | NFR-1 |

### FR-5 Multi-repo orchestration — phase P9, **Could (post-SHIP)**
| ID | requirement | accept | trace |
|----|-------------|--------|-------|
| FR-5.1 | project = repo manifest + project map (always-in-context) | map generate ได้ | a1 |
| FR-5.2 | cross-repo entity-register (drift detect) | API change repo A → flag repo B | ADR-009 |
| FR-5.3 | detect impact + route slice + sequence (ไม่ atomic) | governed slice routed | master-plan |

## 6. Non-Functional Requirements (+ target)

| ID | NFR | target/standard |
|----|-----|-----------------|
| NFR-1 | Security | OWASP Agentic Top 10 + MS Agent Governance Toolkit; credentials=L3; no secret in log |
| NFR-2 | Sovereignty | git-native, no proprietary cloud (⚠️ provisional pending OD-1/G3) |
| NFR-3 | Layer-1 compat | no-Engine session อ่าน markdown view ได้ (degrade graceful) |
| NFR-4 | Concurrency | **single-writer via Engine**, append-only Event log + `prev_hash` chain, per-file lock จน P4 |
| NFR-5 | Cost | per-task token budget cap, default **configurable (เริ่ม 50k/task)**, hard ceiling |
| NFR-6 | Bilingual | TACP L1(en)/L2(th)/L3(dual) |
| NFR-7 | Data-model evolution | additive-only; breaking change → `schema_version` bump + migration note (R10) |

## 7. Dependencies (compose underneath)
LiteLLM (routing) · OPA / MS Agent Governance Toolkit (policy) · Qdrant (vector) · SvelteKit (Shell) · SQLite→Postgres (⚠️ pending OD-1) · interoperate **AGENTS.md** (enforcement layer เหนือ advisory — headline interop)

## 8. Risks (self-contained R1-R12, ดู master-plan §5 รายละเอียด)
| R | risk | sev | mitigation |
|---|------|-----|-----------|
| R1 | sandbox-escape (ทั้งเกม) | H | FS allowlist + tamper detect + adversarial test (FR-1 accept) |
| R2 | canonical inversion ทำลาย Layer-1 compat | H | prose=generated view, degrade graceful (NFR-3) |
| R3 | SQLite ทำลาย git-native | H | OD-1/G3 decide |
| R4 | concurrency corruption | H | Engine serialization (NFR-4) |
| R5 | "ร้อนรน" build Shell ก่อน | H | order invariant; stop-points |
| R6 | predicate drift→quality | M | presence-tag code-review |
| R7 | approval fatigue | H | risk-tier (FR-1.2) |
| R8 | cost blow-up swarm | M | budget cap (NFR-5) |
| R9 | คู่แข่งปิด gap (Cursor/Factory) | M | ปัก flag enforced-state+Inbox now |
| R10 | schema churn→rework | M | additive-only (NFR-7) |
| R11 | key custody honeypot | H | encrypt+LiteLLM egress (FR-4.3) |
| R12 | frontend underestimate | L | bits-ui, timebox |

## 9. Roadmap (flow-plan granular)
Substrate(✅partial) → **P1-P2 Engine (MVW: governance linter)** → P3 interception → P4 store → P5 Cockpit → **P6 SHIP** → P7 model-agnostic → P8 specialists → P9 multi-repo → P10 vector

## 10. GTM & Value-Capture (panel/marketing: ขาดทั้งหมด → เพิ่ม)
- **Distribution:** OSS-core bottom-up (motion เดียวที่สู้ install-base ของ Cursor/Factory ได้สำหรับ self-hosted) — proof: Odysseus 52k stars
- **Hero demo (highest-ROI):** <10-min first-run → gate บล็อก bad-agent-action จริง + Decision Inbox item โผล่ (commit SHA/failing test เป็นหลักฐาน)
- **Lead message:** *"enforcement layer เหนือ AGENTS.md — gate ตรวจ state จริง + project-level Decision Inbox"* (ไม่ใช่ 5 pillar นามธรรม) · headline = risk-tiered reliability, disavow swarm
- **Value-capture hypothesis:** OSS-core (linter) ฟรี → paid: hosted Decision Inbox / team ACLs / compliance reporting (ผูกกับ OD-3/OD-4)
- **Category:** ปัก "Governed Project Memory" + publish adversarial-bypass test result เป็น credibility — **ก่อน P6 SHIP**

## 11. Open Decisions (panel + user vote → lock เป็น ADR; reconcile กับ gate G0-G5)

| OD | decision | gate | สถานะ |
|----|----------|------|-------|
| OD-1 | SQLite vs JSON-in-git canonical store | G3 | open (panel เมื่อ P4) |
| OD-2 | หยุดที่ Engine-CLI หรือไป P3 | G1 | open (หลัง P2) |
| OD-3 | build Shell หรือหยุด Engine (+ revenue hypothesis) | G4 | open |
| OD-4 | universal vs optimize own-tool | G5 | deferred post-SHIP |
| (G0 canonical-inversion = decided via ADR-007 "high-cost-to-reverse"; G2 build-runtime = decided via P3 commitment) | | | noted |

## 12. Known Contradictions w/ Shipped Behavior (panel landmine — builder ต้องรู้)
ระบบ live **ยังบังคับตรงข้าม** FR-1.2/FR-2.1 — ต้อง remediate (carry-over, project review):
- **T-052:** CLAUDE.md "Scenario M ทุกครั้ง" (commit 08ba8a7 uniform gate) → ต้องเปลี่ยนเป็น risk-tiered
- **T-053:** C-07 "block≠body→เชื่อ body" → ต้อง invert (structured wins for enforceable-state)
- **T-051:** re-publish Scenario A-N → new risk-Level mapping
- **T-058:** game playtest state↔sub-gate reconcile

## 13. Panel Review Record

### Iteration 1 (2026-06-05) — BRD v0.1 → 3/3 PASS (contrarian borderline 0.60)
- **votes:** technical PASS .70 · strategic PASS .78 · contrarian PASS .60 ("vision ดี, spec ยังไม่ผ่าน QA") · marketing=viable
- **consensus gaps (ทั้ง 3):** ไม่มี acceptance criteria/measurable metric/req-ID · Plan entity หาย · shipped-reversal ไม่ surface · NFR ไม่มี target · risks ไม่ self-contained · ไม่มี glossary/FR-phase/GTM
- **marketing:** thesis/trend แรง แต่ขาด GTM/onboarding/hero-demo/pricing
- **การตัดสิน (AI):** ผ่าน 2/3 แต่ contrarian borderline + consensus ชัด → **revise เป็น v0.2 แก้ทุก consensus gap** (วิเคราะห์ต่อยอดจากเสียงส่วนใหญ่) ก่อน lock → re-review iteration 2
- **v0.2 แก้:** +glossary(§0) +measurable metrics(§2) +competitive/why-now(§3) +acceptance/phase/MoSCoW ต่อ FR(§5) +Plan entity +NFR targets(§6) +self-contained risks(§8) +GTM/value-capture(§10) +OD↔gate reconcile(§11) +shipped-contradiction(§12) +scope reconcile(§4) +model_floor def(FR-4.2) +path fix

---

*BRD v0.2 — panel-1 consensus addressed. รอ re-review iteration 2 → ถ้าทุกฝ่าย agree → lock เป็น accepted*
