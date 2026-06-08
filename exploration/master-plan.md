# Master Development Plan — "Governed Project Memory"

**Date:** 2026-06-05
**Branch:** `explore/odysseus-analysis`
**Status:** ✅ Executable master plan — **supersedes** `development-plan.md`
**Reconciles:** `north-star-vision.md` + `development-plan.md` กับ corrections ใน `what-it-should-be.md` (capstone) + internal gap audit

> Substrate → Engine → Shell · ลำดับนี้ fixed · dogfood บน repo นี้เอง

---

## 0. หลักการที่ตัดสินแล้ว (invariants — ไม่ re-litigate รายphase)

1. **ลำดับ fixed: Substrate → Engine → Shell** — value ของ Shell *คือ* Substrate; สร้าง Shell ก่อน = "Odysseus อีกตัว"
2. **Moat = enforced, risk-tiered, persistent project governance + Decision Inbox** — ไม่ใช่ UI/swarm/model-agnostic (commodity หมด)
3. **Governance RISK-TIERED ไม่ใช่ uniform** — bind ทุก gate เข้า escalation Level 0–3; uniform gate = Gartner failure mode *(แก้จาก dev-plan เดิมที่ Scenario-M ทุก action)*
4. **Compose underneath, own the top** — LiteLLM (routing) + OPA/MS Agent Governance Toolkit (policy) ใต้ฝา; เป็นเจ้าของแค่ project-stateful governance + Decision Inbox + multi-repo orchestration; interoperate AGENTS.md อย่า reinvent
5. **Enforce presence/structure ไม่ใช่ quality** — predicate ตรวจ evidence กับ state จริง (git/file/test exit) ไม่ตัดสินว่าคำตอบ "ดี"
6. **Dogfood บน repo นี้** — user คนแรกของทุก phase คือ governance ของ repo เอง
7. **Single governed agent = default** สำหรับงาน sequential; multi-agent = orchestrated specialist สำหรับงาน *parallel เท่านั้น* — ไม่ headline "swarm"

---

## 1. Phase model (reconciled, linearized)

```
P0  Substrate Fixes (machine-ready contract)   ← เริ่มสัปดาห์นี้
P1  Hardened config-driven validator (rules-as-data)
P2  CLI evaluator + predicate vocabulary + risk-tier binding
P3  Engine: tool-call interception (constitutive)   ← INFLECTION / bottleneck
P4  Canonical state store + generated views
P5  Read-only Cockpit (first Shell artifact)
P6  Single governed agent + Decision Inbox   ← SHIP
P7  Model-agnostic + role floors
P8  Orchestrated specialists (parallel-only)
P9  Multi-repo orchestration
P10 Vector memory + packaging
```
Map เก่า→ใหม่: P0=ใหม่ · P1=oldP0+P1 · P2=oldP1+risk-tier · P3=oldP2 · P4=oldP4 · P5=oldP3 · P6=oldP5 · P7=oldP6 · P8=oldP7 · P9=oldP8 · P10=oldP9

---

## รายละเอียดแต่ละ phase

### P0 — Substrate Fixes `5–9 วัน` `← เริ่มที่นี่`
**Goal:** ทำ methodology ให้ machine-readable + consistent เพื่อสร้าง Engine ได้โดยไม่โกหก
**Deliverables:** AI-CONTEXT JSON Schema เดียว (versioned) · canonical inversion documented · evidence fields ใน DoD+Task Close Gate · tag ทุก rule presence/quality · risk-tier binding table · housekeeping fixed
**Dependencies:** none (root)
**Exit:** docs core-count ตรงกัน (00–22) · zero orphan reference · C-15..19 แก้ · git_pipeline ใน schema · 3 state files validate ผ่าน schema · ทุก Scenario A–N tag Level เดียว
**Risk:** canonical inversion ทำลาย Layer-1 compat → prose ยังเป็น generated view ห้ามลบ; block authoritative *สำหรับ Engine*, prose human-authoritative จนถึง P4 (C-07 เป็นสะพาน)
**Gate:** **G0 — commit canonical inversion?** (เปลี่ยน core contract "body = source of truth")

### P1 — Hardened validator `3–5 วัน`
**Goal:** พิสูจน์ rules-as-data zero infra ใหม่ โดย generalize enforcer ที่มีแล้ว
**Deliverables:** `validate-commit.sh` อ่าน `gates/*.yaml` (trigger→predicate→effect) · 4–6 check เดิมเป็น data · risk_level→effect
**Dependencies:** P0 · **Exit:** hook เก่าลบได้, validator ใหม่ reproduce ทุก block/warn เดิม, เพิ่ม gate = แก้ YAML อย่างเดียว
**Gate:** none (pure win)

### P2 — CLI evaluator + predicate vocabulary `1.5–2.5 สัปดาห์`
**Goal:** governance linter standalone: `engine check <gate>` ที่ hook/CI/Shell เรียกได้
**Deliverables:** predicate resolver library (Python) · CLI verdict (pass/fail+predicate+Level) · JSON-Schema validator สำหรับ challenge-necessity (presence-only) · risk-tier routing
**Dependencies:** P0, P1 · **Exit:** CI รัน `engine check` ทุก PR; broken state (done task ไม่มี evidence) ถูกจับโดย CLI ไม่ใช่คน
**Risk:** vocabulary แคบ → derive bottom-up จาก Scenario A–N จริง; drift ไป quality → enforce presence/quality tag เป็น code-review rule
**Gate:** **G1 — หยุดที่ Engine-as-CLI หรือไปต่อ?** (P0–P2 = governance linter ที่ ship ได้เลย)

### P3 — Engine: tool-call interception `2.5–4 สัปดาห์` `← bottleneck ใหญ่สุด`
**Goal:** governance กลายเป็น constitutive — agent bypass ไม่ได้ = ฆ่า model-floor risk
**Deliverables:** governed-tool layer (MCP/SDK hook) front `start_task/mark_task_done/record_challenge/attach_evidence` · FS allowlist + tamper detection · ทุก mutation ผ่าน `engine.evaluate()` tier-aware
**Dependencies:** P2 · **Exit:** adversarial test — agent `echo >> task-board.md` mark done **fail**; mark done พร้อม evidence จริง **success**; Level-1 auto-pass ไม่ prompt
**Risk:** sandbox escape = ทั้งเกม → no unrestricted shell ถึง governed paths, tamper detection บังคับ · concurrency → Engine เป็น serialization point *ตอนนี้* (append-only log/lock) ก่อนมี multi-agent
**Gate:** **G2 — commit สร้าง runtime?** (เปลี่ยนจาก tooling → platform = commitment หนักสุด)

### P4 — Canonical store + generated views `2.5–4 สัปดาห์`
**Goal:** drift impossible by construction
**Deliverables:** canonical store (SQLite vs JSON-in-git) · renderer สร้าง L1+L3 จาก store · task+ADR state machine + guarded transitions + audit log · graceful degrade เป็น markdown
**Dependencies:** P3 · **Exit:** แก้ store → regenerate ทั้ง 2 view เหมือนเดิมทุกครั้ง; hand-edit view ถูก detect/overwrite; no-Engine session อ่าน markdown snapshot ได้
**Risk:** SQLite ทำลาย git-native/sovereignty pillar + Layer-1 compat
**Gate:** **G3 — SQLite vs JSON/markdown-canonical?** (fork สถาปัตยกรรมลึกสุด: concurrency/query vs git-native sovereignty)

### P5 — Read-only Cockpit `1.5–2.5 สัปดาห์`
**Goal:** dashboard live เหนือ CoreAiWorkspaces — cheap, พิสูจน์ data model ก่อน dispatch
**Deliverables:** SvelteKit render work-status/task-board/activity/ADR graph จาก store; ยังไม่ dispatch
**Dependencies:** P4 (เริ่ม parallel ปลาย P4 ได้) · **Exit:** ใช้เป็น dashboard ได้แม้ AI=0
**Risk:** frontend underestimate → bits-ui, timebox · **Gate:** none (safe stop)

### P6 — Single governed agent + Decision Inbox `3–5 สัปดาห์` `← SHIP`
**Goal:** ผลิตภัณฑ์ใหม่ที่เล็กที่สุดแต่จริง — governed agent + human gate เป็น Decision Inbox first-class
**Deliverables:** dispatch 1 agent/task ผ่าน LiteLLM · Level-2/3 gate→Inbox card→approve→Engine sync; Level-1 auto-pass (risk-tiered จริง) · Decision Inbox = persistent project object (ไม่ per-run แบบ Conductor)
**Dependencies:** P3, P4, P5 · **Exit:** task จริงบน repo นี้เสร็จ end-to-end, ≥1 Level-2 decision ผ่าน Inbox+approved, state change ผ่าน governed tool พร้อม evidence
**Risk:** governance friction → tiered autonomy ต้องเห็นผลจริง · cost → per-task budget cap
**Gate:** **G4 — สร้าง Shell หรือหยุดที่ Engine?** (fork "methodology+tool" vs "AI product"; universal-vs-own tension เริ่มที่นี่)

### P7 — Model-agnostic + role floors `1.5–3 สัปดาห์`
เสียบ model ไหนก็ได้; โมเดลอ่อนจำกัด read-only lane · fix 50 agents hardcoded · key vault encrypted
**Dependencies:** P6 · **Exit:** swap frontier→local 7B, governance ยังอยู่ (gate constitutive) · **Risk:** key honeypot (Level 3) → encrypt, egress ผ่าน LiteLLM

### P8 — Orchestrated specialists (parallel-only) `2–4 สัปดาห์`
fan-out/in *งาน parallel เท่านั้น* (multi-lens review/research) ไม่ headline swarm; sequential = single-agent · port subset agents → synthesizer surface conflict (Scenario E)
**Dependencies:** P6, P7, P3 concurrency · **Risk:** token 15× → budget cap บังคับ

### P9 — Multi-repo orchestration `3–6 สัปดาห์`
govern ข้าม repo ไม่ใช่ out-index · project = manifest + project map + cross-repo entity-register + impact flag · **ไม่รวม** atomic cross-repo refactor
**Dependencies:** P6, P4

### P10 — Vector memory + packaging `2–4 สัปดาห์`
Qdrant (Wing/Room/Drawer) · Docker Compose · SQLite→Postgres path · **Dependencies:** P6+ stable

---

## 2. P0 รายละเอียด (เริ่มสัปดาห์นี้)

### P0-A — Housekeeping (reversible, ไม่แตะ contract) `~1.5 วัน`
1. core-count contradiction: docs บอก 00–18/00–21 จริง 00–22 → แก้ bootstrap เป็น 00–22
2. missing `skills/game/04-compliance-codes.md` (อ้าง ~20× แต่ไม่มี; file 04 = playtest-report) → สร้างไฟล์ (extract G/A/N/U/L codes จาก CLAUDE.md) หรือ repoint; grep พิสูจน์ zero orphan
3. C-15..C-19 undefined + ชนกับ run-audit test IDs → define ใน core/15 หรือ rename
4. `git_pipeline` ไม่อยู่ใน work-status schema → เพิ่ม (เป็น groundwork ของ schema P0-B ด้วย)
5. orphans: `tools/vector-memory/README.md`, daily-log/summary templates → note

### P0-B — Structural (เปลี่ยน core contract — ทำหลัง G0) `~4–7 วัน`
1. **AI-CONTEXT schema เดียว** (Critical#2): field→type→required→version ข้ามทุก state file; แก้ field collision (`done`/`blocked` ต่างความหมาย) + `schema_version` — *safe-ish*
2. **evidence fields** (Critical#3) ใน DoD+Task Close Gate: `{commit_sha, test_cmd, test_exit, artifact}` — *safe, backward-compat*
3. **tag presence vs quality** (gap#9) ทุก Scenario+C-code — *safe annotation, load-bearing*
4. **bind risk tiers** (correction#1): table gate/Scenario→Level 0–3→effect — *safe, strategic สูง; ข้อมูลมีใน core/11 §3 แต่ยังไม่ bind*
5. **canonical inversion** (Critical#1): block authoritative, prose=view — **ไม่ safe เปลี่ยน contract** → ทำท้ายสุด หลัง G0, P0 แค่ declare intent, enforce จริงที่ P4; จนถึง P4 ใช้ C-07 เป็นสะพาน

**Reversibility:** P0-A ทั้งหมด + P0-B 1–4 = reversible/safe · P0-B step5 = เปลี่ยน core contract (gate ด้วย G0)

---

## 3. Critical path

```
P0-B(schema+inversion) → P1 → P2 → P3 → P4 → P6(SHIP)
≈ 0.8 + 0.8 + 2 + 3.5 + 3.5 + 4 = ~14–15 สัปดาห์ (3.5 เดือน) focused solo ถึง ship
realistic 4–5 เดือน
```
**Bottleneck เดียวใหญ่สุด: P3** (interception) — ยาวสุด, sandbox-escape+concurrency ต้องถูกทั้งคู่, downstream ทั้งหมดพึ่งมัน, เป็น gate เปลี่ยน character (G2)

**Parallelize ได้:** P0-A คู่ P0-B/P1 · P5 overlap ปลาย P4 (slack) · P7/P8 prep ระหว่าง P6 · P0-B 1–4 อิสระต่อกัน (5 ต้องท้าย)
**Serial บังคับ:** P1→P2→P3→P4→P6 (กระดูกสันหลัง ไม่มีลัด)

---

## 4. Dependency graph

```
P0-A ──┐ (parallel)
       ├─► P1 ─► P2 ─► P3 ─► P4 ─┬─► P5 (slack)
P0-B ──┘                          │
  step5 ····(declare P0, enforce P4)
                                  └─► P6(SHIP) ─► P7 ─► P8
                                                  └─► P9 ─► P10
Gates: G0<P0-B5 · G1>P2 · G2<P3 · G3∈P4 · G4<P6 · G5(latent)>P6
```

---

## 5. Risk register

| # | Risk | L | I | Phase | Mitigation |
|---|------|---|---|-------|------------|
| R1 | Sandbox escape — bypass gate ผ่าน free bash | M | **H** | P3 | FS allowlist, effect ผ่าน governed tool, tamper detection, adversarial test |
| R2 | Canonical inversion ทำลาย Layer-1 compat | M | H | P0/P4 | prose = generated view ห้ามลบ, degrade เป็น markdown, C-07 bridge |
| R3 | SQLite ทำลาย sovereignty/git-native | M | H | P4(G3) | ตัดสิน G3; default JSON-in-git ถ้า sovereignty คือ pillar |
| R4 | Concurrency corruption | M | H | P3,P8 | Engine = serialization point ที่ P3 ก่อนมี multi-agent |
| R5 | "ร้อนรน" trap — กระโดด Shell ก่อนสมองพร้อม | M | H | any | order = invariant; G4 บังคับเลือก; P0–P2 มี standalone value |
| R6 | predicate drift ไป quality-judgment | M | M | P2 | presence/quality tag เป็น code-review rule; predicate แตะแค่ git/file/exit |
| R7 | Governance friction / approval fatigue | M | H | P6 | risk-tiering ต้องเห็นผล: L1 auto, batch low-risk, gate L2–3 |
| R8 | Cost blow-up จาก fan-out (15× token) | M | M | P8 | budget cap; specialist parallel เท่านั้น |
| R9 | คู่แข่งปิด gap (Cursor+multi-repo/ledger, Factory) | M | M | post-P6 | นำด้วย enforced persistent project-state + Decision Inbox; ship P6 ก่อน window ปิด |
| R10 | Schema churn → rework P1–P4 | M | M | P0→P4 | schema_version, additive-only, vocabulary bottom-up |
| R11 | Key custody honeypot | L | H | P7 | encrypt at rest, egress ผ่าน LiteLLM (Level 3) |
| R12 | Frontend underestimate | M | L | P5 | bits-ui, timebox, read-only ก่อน |

---

## 6. Decision gates

| Gate | เมื่อ | เลือกอะไร | ทำไมสำคัญ |
|------|------|-----------|-----------|
| **G0** | ก่อน P0-B5 | invert canonical truth? | เปลี่ยน core contract, reverse ยาก |
| **G1** | หลัง P2 | หยุดที่ Engine-CLI หรือไปต่อ? | P0–P2 = governance linter ship ได้ |
| **G2** | ก่อน P3 | commit สร้าง runtime? | tooling→platform, commitment หนักสุด |
| **G3** | ใน P4 | SQLite vs JSON/markdown-canonical? | concurrency/query vs git-native sovereignty |
| **G4** | ก่อน P6 | สร้าง Shell หรือหยุดที่ Engine? | methodology-only vs AI product |
| **G5** (latent) | หลัง P6 | universal หรือ optimize own Shell? | north-star เลื่อนไว้ — "ไม่ใช่ตอนนี้" |

---

## 7. Stop points ที่มี standalone value

1. **หลัง P0** — methodology ที่ machine-readable + risk-tiered (ดีกว่าวันนี้แม้ engine=0) ship ได้
2. **หลัง P2** — **governance linter standalone** (`engine check`) ใช้ CI ใดก็ได้, OSS-able — "หยุดแล้วยังชนะ" ที่สะอาดสุด (G1)
3. **หลัง P4** — drift-impossible state + generated views, self-enforce แม้ใน plain Claude/Cursor
4. **หลัง P5** — dashboard อ่านได้ ใช้ได้แม้ AI=0
5. **หลัง P6** — **SHIP**: governed single-agent + Decision Inbox = ผลิตภัณฑ์ใหม่จริงที่เล็กสุด

→ MVW = P2 (linter) · MVP = P6

---

## 8. เริ่มสัปดาห์นี้ (concrete, ordered)

ทั้งหมด P0-A (safe, reversible) + tee up G0 · แต่ละอันแยก commit บน feature branch จาก `dev`

1. **แก้ core-count** (1–2 ชม.) root + platforms CLAUDE.md bootstrap "00–18/00–21" → "00–22"
2. **แก้ missing compliance-codes** (ครึ่งวัน) สร้าง `skills/game/04-compliance-codes.md` extract G/A/N/U/L จาก CLAUDE.md (หรือ repoint); grep พิสูจน์ zero orphan
3. **reconcile git_pipeline** (1–2 ชม.) เพิ่มเข้า core/06 schema (= schema groundwork)
4. **C-15..C-19** (2–4 ชม.) define หรือ rename ออกจาก collision
5. **tee up G0** (note ไม่ใช่ code) เขียน 1 หน้า trade-off canonical inversion → ตัดสินก่อนเริ่ม P0-B

ทำ 1–4 parallel → land small commits → ตัดสิน G0 → เริ่ม P0-B step1 (AI-CONTEXT schema) = จุดเริ่มจริงสู่ Engine

---

## Critical files
- `core/15` — Task Close Gate + C-codes (evidence fields, presence/quality tag, C-15..19)
- `core/11` — Scenarios A–N + Level 0–3 (source ของ risk-tier binding)
- `core/06` — AI-CONTEXT schema home + git_pipeline + canonical-inversion contract
- `core/07` — task state machine + DoD (evidence fields)
- `platforms/claude-code/hooks/validate-commit.sh` — enforcer ตัวเดียว → generalize ที่ P1

---

*Reconciled by Plan agent (stress-tested sequencing/dependency/risk). Supersedes development-plan.md.*
