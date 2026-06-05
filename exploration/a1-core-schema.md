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

### Task
```yaml
Task:
  id: string                    # required (T-XXX)
  title: string                 # required
  status: enum(todo|design_validate|in_progress|review|done|blocked)  # lifecycle §2
  source_ref: requirement_id    # required — ห้าม implement ไม่มี source (C-02)
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
> P0-B step1: นิยาม field set ต่อ file_kind เป็น typed schema · normalize list delimiter · เพิ่ม schema_version

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
1. 🟠 **source_ref บังคับไม่ได้กับ exploration/spike task** → เพิ่ม Requirement.kind=`spike` หรือ allow `source_ref: spike:<note>`
2. 🟠 **work-status field จริง ≠ core/06 template** (active_task vs focus, blocker vs blocked, last_updated vs updated) → P0-B step1 ต้อง reconcile ให้เป็น schema เดียว (นี่คือ Critical gap #2 ตัวจริงที่ retrofit เผย)
3. 🟢 Decision/Evidence/Task แกนหลัก fit ดี

---

## 6. Open / next

- **เคาะ:** source_ref สำหรับ spike/exploration (finding #1)
- **P0-B step1:** reconcile work-status field 2 ชุด → typed schema เดียว (finding #2)
- retrofit เพิ่มกับ domain ห่าง (research/industrial) ตาม panel guidance ก่อน lock core/profile line
- schema นี้ = input ของ P1 (validator predicates อ้าง field พวกนี้)

---

*A1 draft — ต่อยอด ADR-009. Findings #1-2 จาก retrofit = ของจริงที่ paper-first จับได้ก่อน build*
