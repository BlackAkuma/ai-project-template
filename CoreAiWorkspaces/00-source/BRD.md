<!-- AI-CONTEXT
doc: BRD
version: 1.0
status: ACCEPTED (locked 2026-06-05 via 3-iteration panel; 2/3 rule met x3, converged) — see ADR-010
product: Governed Project Memory
schema_version: "0.1"
review_method: 3-lens panel (technical/strategic/contrarian) 2/3 + marketing advisory
panel_history: [iter1: 3/3 (tech.70/strat.78/contra.60), iter2: 2/3 (tech.74/strat.80/contra-FAIL.66), iter3: 2/3 (tech.78/strat.82/contra-FAIL.63 on named-deferrals), marketing=viable x3]
lock_note: contrarian residual FAIL = adversarial strictness on named-deferrals (OD-1/T-058/model-agnostic@SHIP), not new defects; contrarian self-acknowledged "named-deferral != incompleteness". Reopenable if user disagrees.
rationale_refs: [exploration/north-star-vision.md, exploration/what-it-should-be.md, exploration/master-plan.md, exploration/flow-plan.md, exploration/a1-core-schema.md]
decisions_locked: [ADR-006, ADR-007, ADR-008, ADR-009]
-->

# BRD — Governed Project Memory

**Version:** 1.0 · **Date:** 2026-06-05 · **Status:** ✅ ACCEPTED (locked via 3-iteration panel — ADR-010)
**source of truth ของ requirements** — self-contained (ไม่ต้องอ่าน 5 doc เพื่อรู้ว่า "done" คืออะไร); rationale อยู่ `exploration/`

---

## 0. Glossary (panel: source-of-truth ต้องนิยามศัพท์)

| term | นิยาม |
|------|------|
| **Substrate** | ชั้น 1 — methodology/template (core/, สมอง) |
| **Engine** | ชั้น 2 — governance ที่เครื่องบังคับได้ (constitutive) |
| **Shell** | ชั้น 3 — แอป project-centric (UI + Decision Inbox) |
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
| Governance enforce จริง | bypass blocked = **100% ของ maintained adversarial suite** (N≥10, expandable +cases/release, fuzz/red-team) — "known attack classes" ชัดเจน |
| Context ไม่ drift | block↔body mismatch = **0** (generated จาก store; CI check) |
| Model-agnostic (≥floor) | swap frontier↔local 7B (**at-or-above floor**) → governance test pass เท่าเดิม (regression) |
| ลด review load | **Level-1 auto-pass ≥70%** · **Decision Inbox ≤2/task** (median, จาก event log) |
| Multi-repo *(post-SHIP, P9)* | cross-repo impact detect 100% ของ declared dependency change — **ไม่ใช่ SHIP metric** |

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

**In (at SHIP/P6):** Substrate · Engine · Shell · CORE + **game profile เดียว (deep) + extension hook** · self-hosted, model-agnostic
**In (post-SHIP):** multi-repo orchestration (P9) · compose-engine web-game (post-SHIP) · specialists (P8)
> ⚠️ reconcile (panel iter2 — scope/MoSCoW contradiction แก้): multi-repo = **post-SHIP เท่านั้น**, ที่ SHIP ไม่มี (ไม่ In + Could + metric-bound พร้อมกันอีก); substrate = game profile เดียว, compose-engine defer (ADR-009)

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
| FR-2.1 | canonical store; prose=generated view | **store-agnostic accept: drift=0 ไม่ว่า backend ใด** (testable ก่อน OD-1); store type (SQLite/JSON) = OD-1/G3 ไม่ block SHIP | ADR-007 |
| FR-2.2 | AI-CONTEXT schema เดียว typed | 3 state file validate ผ่าน schema | a1 §3 |
| FR-2.3 | CORE 11 entities: Project/Requirement/**Plan**/Task/Evidence/Decision/TeamMember/Gate/Repo/Entity/Event | ครบ 11 (แก้ Plan ที่หาย) | ADR-009 |
| FR-2.4 | evidence = machine-verifiable \| human-attested | 2 class ใน schema + Engine ตรวจต่างกัน | ADR-009 D2 |
| FR-2.5 | lifecycle todo→design_validate→in_progress→review→done + profile sub-gate | state machine + guard (done ต้องมี evidence) · ⚠️ game playtest=sub-gate **provisional pending T-058** | a1 §2 |
| FR-2.6 | audit/observability: Event log queryable + tamper-evidence (prev_hash verify) | inspect audit trail + detect tampered chain (test) | NFR-4 |

### FR-3 Decision Inbox — phase P6, **Must**
| ID | requirement | accept | trace |
|----|-------------|--------|-------|
| FR-3.1 | Level 2-3 → durable project-level Inbox item | card persist ข้าม session | ADR-006 |
| FR-3.2 | ADR Proposed → Scenario O panel 2/3 + dissent → human | panel รัน + log ทุก ADR | Scenario O |
| FR-3.3 | ทุก review = Panel Review Record (เหตุผล+โหวต+ตัดสิน) | อ่านย้อนได้ใน ADR/BRD | Scenario O |
| FR-3.4 | Inbox item lifecycle: expiry/escalation/SLA (กัน Level 2-3 ค้างนาน) | item เกิน SLA → escalate/flag (test) | R7 |

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
| NFR-8 | Engine performance | gate-eval budget **≤200ms/action** (hot path ทุก code-touch); Event-log growth bounded + hash-chain verify amortized |
| NFR-9 | Decision Inbox durability | crash mid-approval → queue persist (no lost item); recovery resumes pending items |

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

## 9. Roadmap + Phase/Gate Definitions (self-contained)

| Phase | entry → exit | Gate (pass criteria, status) |
|-------|-------------|------------------------------|
| P0 Substrate | docs inconsistent → machine-ready schema | G0 canonical-inversion = **decided** (ADR-007, high-cost-to-reverse) |
| P1-P2 Engine MVW | gate-as-data → `engine check` CLI + CI (governance linter) | **G1** ship-CLI vs go-P3 = **open** (after P2) |
| P3 interception | advisory → constitutive (agent can't bypass) | **G2** build-runtime = decided-by-commitment |
| P4 store | drift-possible → canonical+generated views | **G3** SQLite vs JSON-in-git = **open** (OD-1) |
| P5 Cockpit | no-UI → read-only dashboard | — |
| **P6 SHIP** | → governed single-agent + Decision Inbox | **G4** build-Shell vs stop-Engine = **open** (OD-3) |
| P7-P10 | model-agnostic → specialists → multi-repo → vector | **G5** universal vs own-tool = **deferred** (OD-4) |

**What SHIP (P6) proves vs defers** (panel: honest scoping):
- ✅ **proves at SHIP:** enforced-governance-as-state · Decision Inbox · project-memory (3 of 4 differentiators' core)
- ⏳ **defers (roadmap):** model-agnostic (P7) · multi-repo (P9) · specialists (P8) → **ห้าม headline เป็น shipped differentiator**

## 10. GTM & Value-Capture (panel/marketing)
- **Single lead message = category name (1 ประโยค):** *"Governed Project Memory — enforcement เหนือ AGENTS.md พร้อม durable project Decision Inbox"* (เลิกมี 2 tagline แข่งกัน; lead ด้วยแค่ของที่ ship จริง: enforced-state + Decision Inbox + project-memory)
- **Distribution:** OSS-core bottom-up (motion เดียวที่สู้ install-base Cursor/Factory ได้) — proof: Odysseus 52k stars · ต้องมี launch surface (HN/GitHub Show) + content engine
- **Hero demo (highest-ROI):** <10-min first-run → gate บล็อก "agent แกล้ง mark done" จริง + Decision Inbox item โผล่ (commit SHA/failing test) = asset ที่ Cursor/Factory เลียนแบบ cheap ไม่ได้
- **Value-capture:** OSS-core (linter) ฟรี → paid: hosted Decision Inbox / team ACLs / compliance reporting · **OD-3 ต้อง gate บน willingness-to-pay signal (≥1 design-partner) ก่อน build Shell** ไม่ใช่แค่ build/no-build
- **Onboarding (Day-2):** path จาก clone → governing real project; import AGENTS.md/CLAUDE.md; **จัดการ local-7B sub-floor first-run friction** (FR-4.2 อาจ confuse) ต้องมี story
- **Category:** ปัก "Governed Project Memory" + publish adversarial-bypass result — **ก่อน P6 SHIP** (window ปิด, Cursor decision-ledger fast-follow = นาฬิกาเดิน)

## 11. Open Decisions (panel + user vote → lock เป็น ADR; reconcile กับ gate G0-G5)

| OD | decision | gate | สถานะ |
|----|----------|------|-------|
| OD-1 | SQLite vs JSON-in-git canonical store | G3 | open (panel เมื่อ P4) |
| OD-2 | หยุดที่ Engine-CLI หรือไป P3 | G1 | ✅ **resolved → C-conservative** (ADR-011): soft-ship OSS + protect P3 |
| OD-3 | build Shell หรือหยุด Engine (+ revenue hypothesis) | G4 | open |
| OD-4 | universal vs optimize own-tool | G5 | deferred post-SHIP |
| (G0 canonical-inversion = decided via ADR-007 "high-cost-to-reverse"; G2 build-runtime = decided via P3 commitment) | | | noted |

## 12. Known Contradictions w/ Shipped Behavior (panel landmine — builder ต้องรู้)
ระบบ live **ยังบังคับตรงข้าม** FR-1.2/FR-2.1 — ต้อง remediate (owner: project-review round, phase P0-B; marketing: ต้องทำ **ก่อน** market risk-tiered/structured-as-truth = credibility prerequisite):
- **T-052** (P0-B): CLAUDE.md "Scenario M ทุกครั้ง" (commit 08ba8a7 uniform gate) → risk-tiered
- **T-053** (P0-B): C-07 "block≠body→เชื่อ body" → invert (structured wins enforceable-state)
- **T-051** (P0-B): re-publish Scenario A-N → new risk-Level mapping
- **T-058** (Stage A/T-046): game playtest state↔sub-gate reconcile
> predicate grammar artifact = `engine/gates/_grammar.md` (**มีอยู่จริงแล้ว**, P1-1) — ไม่ใช่ forward-ref ค้าง

## 13. Panel Review Record

### Iteration 1 (2026-06-05) — BRD v0.1 → 3/3 PASS (contrarian borderline 0.60)
- **votes:** technical PASS .70 · strategic PASS .78 · contrarian PASS .60 ("vision ดี, spec ยังไม่ผ่าน QA") · marketing=viable
- **consensus gaps (ทั้ง 3):** ไม่มี acceptance criteria/measurable metric/req-ID · Plan entity หาย · shipped-reversal ไม่ surface · NFR ไม่มี target · risks ไม่ self-contained · ไม่มี glossary/FR-phase/GTM
- **marketing:** thesis/trend แรง แต่ขาด GTM/onboarding/hero-demo/pricing
- **การตัดสิน (AI):** ผ่าน 2/3 แต่ contrarian borderline + consensus ชัด → **revise เป็น v0.2 แก้ทุก consensus gap** (วิเคราะห์ต่อยอดจากเสียงส่วนใหญ่) ก่อน lock → re-review iteration 2
- **v0.2 แก้:** +glossary(§0) +measurable metrics(§2) +competitive/why-now(§3) +acceptance/phase/MoSCoW ต่อ FR(§5) +Plan entity +NFR targets(§6) +self-contained risks(§8) +GTM/value-capture(§10) +OD↔gate reconcile(§11) +shipped-contradiction(§12) +scope reconcile(§4) +model_floor def(FR-4.2) +path fix

### Iteration 2 (2026-06-05) — BRD v0.2 → 2/3 PASS (contrarian FAIL 0.66 ↑)
- **votes:** technical PASS .74 · strategic PASS .80 · contrarian **FAIL .66** · marketing=viable
- **contrarian defects จริง (AI ยอมรับ — ไม่ override):** (1) scope/MoSCoW ขัด: multi-repo อยู่ In+Could+metric พร้อมกัน (2) placeholder "X" ยังอยู่ (3) OD-1 open แต่ FR-2.1 Must, dependency ไม่ visible (4) ขาด FR: Inbox lifecycle/audit (5) phase/gate ไม่นิยามใน-doc (6) T-058 ขัด FR-2.5
- **contrarian meta-warning:** "อย่า override contrarian แล้วประกาศ fixed ซ้ำ" — รับฟัง → iterate แทนการ override
- **marketing:** SHIP โชว์แค่ 2/4 differentiator → ต้อง honest scope + single lead message + monetization design-partner ก่อน Shell
- **การตัดสิน (AI):** contrarian มี defect จริง (ไม่ใช่แค่ deferral) → **v0.3 แก้ทุก defect** (ตามที่สั่ง "เห็นด้วยทุกฝ่าย") ก่อน lock → re-review iteration 3
- **v0.3 แก้:** scope multi-repo=post-SHIP เท่านั้น(§4) · เติม X→≤2/task + reword adversarial/parity metric(§2) · FR-2.1 pending OD-1 · FR-2.5 T-058 provisional · +FR-2.6 audit +FR-3.4 Inbox lifecycle · phase/gate definition table(§9) · "SHIP proves vs defers"(§9) · single lead message + OD-3 willingness-to-pay(§10)

### Iteration 3 (2026-06-05) — BRD v0.3 → 2/3 PASS (contrarian FAIL 0.63) → **CONVERGED → LOCK v1.0**
- **votes:** technical PASS .78↑ · strategic PASS .82↑ · contrarian **FAIL .63** · marketing=viable
- **contrarian self-acknowledged (สำคัญ):** "OD-1/T-058/model-agnostic = legitimate deferred decisions ผูก gate G3/G4/P7... **named-deferral != incompleteness**... a less adversarial lens จะถือเป็น acceptable iteration debt"
- **contrarian residual items:** (a) small fixes ที่แก้แล้วใน v0.4 (version header, rationale path, +NFR-8 perf, +NFR-9 Inbox durability, glossary split, FR-2.1 store-agnostic accept, §12 owner/phase, _grammar.md exists) (b) named-deferrals (OD-1/T-058/model-agnostic@SHIP) ที่ **ถ้าตัดสินตอนนี้ = premature gate / ร้อนรน trap**
- **การตัดสิน (AI) — LOCK:** 2/3 rule (เกณฑ์ผู้ใช้) ผ่าน **3 รอบติด** + confidence ไต่ขึ้น + defect จริงแก้หมด + contrarian agree-on-direction (ค้านแค่ adversarial-strictness บน deferrals) → **lock เป็น v1.0 accepted** (ADR-010); deferrals = OD-1..4 ผูก gate, จะ panel+lock เมื่อถึง phase
- **transparency:** lock ทับ contrarian-FAIL โดย **ไม่ override แบบเงียบ** — residual dissent บันทึกครบ; **reopenable ถ้าผู้ใช้ไม่เห็นด้วย**
- **v0.4 แก้:** version 1.0 + body header sync · rationale_refs path · +NFR-8/9 · glossary split S/E/Shell · FR-2.1 store-agnostic · §12 owner/phase + marketing-prereq · _grammar.md exists note

---

*BRD v1.0 — ✅ ACCEPTED 2026-06-05 (3-iteration panel, 2/3 x3, converged). Open decisions OD-1..4 ผูก gate G3/G4/G5 — panel+lock เมื่อถึง phase. ดู ADR-010*
