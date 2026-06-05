# A1 — CORE Schema Draft (Stage A / T-045)

**Date:** 2026-06-05
**Branch:** `explore/odysseus-analysis`
**Status:** 🔬 Draft — paper-first, รอ retrofit (A5) + whole-project review
**Implements:** ADR-009 (CORE+PROFILE), ADR-007 (dual-authority), ADR-008 (risk-tier)
**schema_version:** 0.1 · **กฎ:** additive-only (เพิ่ม field ได้, ห้ามลบ/เปลี่ยนความหมาย → bump version)

> นี่คือ contract ที่ Engine (P1-P4) จะ enforce — structured = source of truth ของ enforceable state (ADR-007)

---

## 1. CORE entities (invariant — ทุกซอฟต์แวร์)

### Project
```yaml
Project:
  id: string                    # required
  name: string                  # required
  goals: [string]
  status: enum(active|paused|done|archived)
  phase: string                 # milestone ปัจจุบัน
  type_profiles: [profile_id]   # compose ได้ เช่น [generic-software, game]
  pipeline: string              # git_pipeline เช่น dev→main
  prod_branch / dev_branch: string
  git_mode: enum(branch-separated|single-branch)
  l2_lang: string               # TACP output lang (th)
  schema_version: string        # 0.1
```

### Requirement (source of truth, versioned)
```yaml
Requirement:
  id: string                    # required
  version: string               # required เช่น v0.2
  title: string
  content_ref: path             # ชี้ไฟล์ source จริง
  status: enum(draft|active|superseded)
  supersedes: id?
```

### Plan (panel fix — หายไปจาก draft แรก, ADR-009 มี)
```yaml
Plan:
  id: string
  milestones: [{ id, title, target_date, status }]
  dependencies: [{ from: task_id|milestone_id, to: task_id|milestone_id }]
  phase_map: { phase_id: [task_id] }   # FR→phase (MoSCoW)
```

### Task
```yaml
Task:
  id: string                    # required (T-XXX)
  title: string                 # required
  status: enum(todo|design_validate|in_progress|review|done|blocked)  # lifecycle §2
  source_ref: requirement_id | "spike:<note>"   # required; spike/exploration ใช้ spike: prefix (T-056 resolved)
  owner: { kind: enum(human|ai), ref: string }
  risk_level: enum(0|1|2|3)     # Engine-determined (ADR-008), default unknown→2
  evidence: [evidence_id]       # required ก่อน done (Task Close Gate)
  profile_stage: string?        # sub-gate จาก profile เช่น playtest
  parent: task_id?
  created / updated: date
```

### Evidence (D2 — machine-verifiable vs human-attested)
```yaml
Evidence:
  id: string
  task_ref: task_id
  class: enum(machine-verifiable | human-attested)   # ← D2 core split
  type: enum(commit|test|artifact|review|playtest|...) # extensible per profile
  ref: string                   # SHA | "cmd→exit" | path | signoff_id
  verified: bool
  verified_by: enum(engine|human)   # machine→engine, attested→human
  ts: date
```
> **กฎ enforce (ADR-007):** Engine ตรวจ machine-verifiable แบบ deterministic; human-attested ตรวจแค่ *presence ของ sign-off* (truth = trust-based)

### Decision (ADR)
```yaml
Decision:
  id: string                    # ADR-XXX
  title: string
  status: enum(Proposed|Accepted|Deprecated|Superseded)
  context / decision: string
  options / consequences: [string]
  panel_record: { votes: [...], approved: bool }?   # Scenario O
  supersedes: id?
```

### TeamMember
```yaml
TeamMember:
  id: string
  role: string                  # frontend, game-designer, ...
  kind: enum(human|ai)
  model: string?                # ai เท่านั้น (via LiteLLM)
  capability_lane: enum(read-only|advisory|code-author|architect)
  model_floor: enum(0|1|2|3)    # โมเดลต่ำกว่า floor → จำกัด lane
```

### Gate
```yaml
Gate:
  id: string
  trigger: { action: string }   # เช่น task.transition→done, write_file
  predicates: [predicate_ref]   # vetted vocabulary (P2)
  risk_level: enum(0|1|2|3)
  effect: enum(auto-log|decision-inbox|hard-stop)   # ตาม risk (ADR-008)
```

### Repo · Entity · Event (multi-repo + audit)
```yaml
Repo:   { id, path_or_url, role, purpose, branches: [string] }
Entity: { id, name, kind, status: enum(active|deprecated|superseded), repo_refs: [repo_id] }  # cross-repo drift
Event:  { id, ts, actor, action, target, result, prev_hash }  # append-only = serialization point (concurrency, R4)
```

---

## 2. Task Lifecycle (D1 — แกนคงที่ + profile sub-gate)

```
todo → design_validate → in_progress → review → done
                                          ↘ blocked ↙ (จากทุก state)
```

**Transition guards (Engine enforce):**
| from → to | guard |
|-----------|-------|
| todo → design_validate | source_ref present |
| design_validate → in_progress | design approved (human-attested) |
| in_progress → review | changes committed (machine: commit exists) |
| review → done | **Task Close Gate**: work-log entry + task-board synced + evidence ≥1 verified |

**Profile sub-gate (ไม่เพิ่ม state ในแกน):** profile แทรกเงื่อนไข *ภายใน* stage
- เช่น game: `review → done` ต้องมี evidence class=playtest เพิ่ม

> ⚠️ **reconcile note (verification finding):** `skills/game/00-overview` + CLAUDE.md ปัจจุบัน model game lifecycle ว่ามี state `playtest` แยก (`in_progress → playtest → review`) แต่ A1/ADR-009 model เป็น *sub-gate* ใน review → ต้อง reconcile ตอน T-046/T-048 (profile design) ให้ตรงกัน — เลือกแบบ sub-gate (แกนคงที่)

---

## 3. AI-CONTEXT block schema (แก้ Critical gap #2 — schema เดียว)

ทุก state file ใช้ schema เดียวกัน (เลิก field collision `done`/`blocked`):
```yaml
ai_context:
  schema_version: "0.1"         # required ทุก block
  file_kind: enum(work-status|task-board|work-log)
  # fields ตาม file_kind — typed, ไม่ ad-hoc
  # generated จาก canonical store (ADR-007) — ไม่เขียนมือหลัง P4
```

### Unified work-status fields (T-057 — แก้ field จริง vs core/06 template ที่ต่างกัน)
canonical (typed) + mapping จาก 2 ชุดที่มีอยู่:

| canonical field | type | จาก template (core/06) | จากไฟล์จริง | หมายเหตุ |
|-----------------|------|------------------------|-------------|---------|
| `schema_version` | string | — | — | **ใหม่ required** |
| `phase` | string | phase | phase | ตรงกัน ✅ |
| `active_tasks` | [task_id] | focus | active_task | **collision → canonical: `active_tasks`** |
| `blocker` | string\|none | blocked | blocker | unify เป็น `blocker` |
| `next` | string | next | next_action | unify เป็น `next` |
| `updated` | date | updated | last_updated | unify เป็น `updated` |
| `src` | string | src | (ขาด) | เพิ่มเข้าไฟล์จริง |
| `adr` | [adr_id] | adr | (ขาด) | เพิ่ม |
| `risk` | string\|none | risk | (ขาด) | เพิ่ม |
| `active_branch` | string | (ขาด) | active_branch | เพิ่มเข้า template |
| `git_*` / `git_pipeline` | string | ✅ (มี git_pipeline แล้ว T-043) | ✅ | ตรงกัน |
| `read_more` | map | read_more | read_more | ตรงกัน ✅ |

> **กฎ delimiter:** list ใช้ `[a, b]` เสมอ (เลิกปนกับ space-list)
> P0-B step1: apply schema นี้กับ core/06 template + ไฟล์จริง พร้อมกัน (= งาน implement ของ T-057)

---

## 4. PROFILE extension (D3 — hook + game; defer compose engine)

ตาม panel guidance (ADR-009): substrate phase = นิยาม **CORE เต็ม + extension hook + 1 profile (game)** เท่านั้น; compose engine (web-game) defer post-SHIP

```yaml
Profile:
  id: string                    # game
  lifecycle_substages: [...]    # playtest sub-gate
  evidence_kinds: [...]         # scene_runs, playtest_report, balance_check
  roles: [...]                  # game-designer, level-designer
  quality_codes: [...]          # G/A/N/U/L (skills/game/12)
  toolchain: [...]              # godot | unreal
  doc_types: [...]              # GDD, FDD
# compose: additive merge + priority — interface กำหนดไว้, engine ทำทีหลัง
```

---

## 5. A5 Retrofit check (validate กับ state จริงของ repo นี้)

ลอง map ข้อมูลจริง → schema:

| ข้อมูลจริง | map เป็น | fit? |
|-----------|---------|------|
| T-040 (Odysseus analysis) | Task{status:done, source_ref:?, evidence:[exploration docs], risk_level:1} | ⚠️ **gap: T-040 ไม่มี source_ref** (เป็น exploration ไม่ใช่ requirement) → ต้องมี source kind ใหม่ "exploration/spike" หรือ exempt |
| ADR-006 | Decision{status:Accepted, panel_record:{3/3}} | ✅ fit |
| work-status AI-CONTEXT | ai_context{file_kind:work-status} | ⚠️ **gap: ฟิลด์จริง (active_task, blocker) ≠ core/06 template (focus, blocked)** → schema เดียวต้อง reconcile 2 ชุดนี้ |
| evidence ของ T-035 ("67/67 tests pass") | Evidence{class:machine-verifiable, type:test} | ✅ fit (แต่ legacy ไม่มี ref จริง) |
| ADR panel votes | Decision.panel_record | ✅ fit |

**Findings จาก retrofit:**
1. ✅ **source_ref บังคับไม่ได้กับ exploration/spike task** → resolved (T-056): allow `source_ref: spike:<note>` ใน §1 Task
2. ✅ **work-status field จริง ≠ core/06 template** → resolved (T-057): unified field table ใน §3; apply = P0-B step1
3. 🟢 Decision/Evidence/Task แกนหลัก fit ดี
4. ✅ (verification) playtest modeling → **เลือก sub-gate** (T-058, note §2); align game docs ตอน T-046

### T-049 — retrofit domain ห่าง (research + industrial) เพื่อ stress-test core/profile line

| domain | map เข้า CORE | profile (variant) | fit? |
|--------|--------------|-------------------|------|
| **Research** | Requirement=hypothesis/question · Task=experiment/analysis · Evidence=reproduced_result/dataset_validated · lifecycle: design_validate=hypothesis review, review=peer review | research: evidence_kinds[reproduced_result, dataset_validated], roles[researcher, reviewer], toolchain[notebook/compute], doc_types[research-plan, results] | 🟢 CORE fit · hypothesis fuzzy → `spike:` (T-056) ครอบ |
| **Industrial/embedded** | Requirement=safety-spec · Task=control-module · Evidence=hil_test(machine)+safety_cert(human-attested+external) · lifecycle: design_validate=safety review | industrial: evidence_kinds[hil_test, safety_cert, compliance_audit], roles[safety-engineer], toolchain[PLC/simulator], doc_types[FMEA, safety-spec] | 🟢 CORE fit · ยืนยัน D2 machine/attested split ถูก |

**Findings T-049:**
- ✅ **process layer (CORE) ครอบ 2 domain ห่างได้** — Project/Task/Evidence/Decision/Gate ไม่ต้องแตะ
- 🟠 industrial เพิ่ม **evidence subtype `external-cert`** (cert จาก regulator ภายนอก) → เป็น human-attested ชนิดพิเศษ (Engine ตรวจ presence + cert-id) → เพิ่มใน Evidence.type enum (additive)
- 🟢 core/profile line ผ่าน stress-test → ยืนยัน Option C (ADR-009) ถูก; ไม่เจอ domain ที่ใส่กรอบ process ไม่ได้

---

## 6. Open / next

- **เคาะ:** source_ref สำหรับ spike/exploration (finding #1)
- **P0-B step1:** reconcile work-status field 2 ชุด → typed schema เดียว (finding #2)
- retrofit เพิ่มกับ domain ห่าง (research/industrial) ตาม panel guidance ก่อน lock core/profile line
- schema นี้ = input ของ P1 (validator predicates อ้าง field พวกนี้)

---

*A1 draft — ต่อยอด ADR-009. Findings #1-2 จาก retrofit = ของจริงที่ paper-first จับได้ก่อน build*
