# Development Plan — Stage 2 (Engine + Shell)

**Date:** 2026-06-05
**Branch:** `explore/odysseus-analysis`
**Status:** 🔬 Hypothesis plan — ลงมือได้แบบ incremental, dogfood บน repo นี้เอง
**Pairs with:** `north-star-vision.md`, `odysseus-analysis.md`

> สังเคราะห์จาก 2 deep-dive agent (Engine layer + Shell layer) ที่ converge ไปข้อสรุปเดียวกัน

---

## ข้อสรุปสำคัญที่สุด (ทั้งสอง agent เห็นตรงกัน)

1. **Moat ไม่ใช่ UI ไม่ใช่ swarm ไม่ใช่ model-agnostic** (พวกนี้ commodity ทั้งหมด)
   → Moat คือ **governance ที่ enforce เป็น state จริง** + **Decision Inbox** (human-gate queue)
   → นี่คือสิ่งเดียวที่ 2 ปีของ markdown protocol เราเข้ารหัสไว้แล้ว และยังไม่มีใครสร้าง

2. **Engine ต้องมาก่อน Shell เสมอ** — Engine ใช้แบบ headless (CLI/CI) ได้ Shell เป็นแค่ consumer ตัวหนึ่ง
   → ทุก phase dogfood บน `ai-project-template` repo นี้เองได้ทันที

3. **กลไกหัวใจ = tool-call gating + evidence-based predicates**
   → agent ขยับ project state ได้ผ่าน API ที่ถูก gate เท่านั้น
   → predicate ตรวจกับ state จริง (`git diff`, file, test) **ไม่เคยเชื่อคำพูด agent**
   → นี่คือสิ่งที่ฆ่า "model-floor risk": โมเดลอ่อนพูดอะไรก็ได้ แต่โกหก `git diff` ไม่ได้

---

## หลักการแปลง: advisory → constitutive

| ตอนนี้ (advisory) | ปลายทาง (constitutive) |
|-------------------|------------------------|
| markdown ที่ "ขอให้ AI ทำตาม" | spec ที่ "เครื่องบังคับ ทำผิดไม่ได้" |
| gate = prose | gate = `trigger → predicate → effect` data object |
| "ฉันอัปเดต work-log แล้ว" (claim) | `git diff` มี work-log-index.md (evidence) |
| markdown = storage + API + view ปนกัน | canonical store + rendered views แยกกัน |
| AI-CONTEXT block เขียนมือ (drift ได้) | generated จาก store (drift ไม่ได้) |

**เส้นแบ่ง human vs auto:** automate *verification + bookkeeping* / เก็บ *rule-authorship + irreversible/ambiguous decisions* ไว้กับมนุษย์
→ Engine = referee ไม่ใช่ player

---

## แผนรวม — 9 Phase (Engine นำ, Shell ตาม, interleaved)

แต่ละ phase ต้อง **ใช้งานได้จริงเดี่ยวๆ** ก่อนเริ่ม phase ถัดไป — กฎเราเอง: "Do less, document more"

### 🔧 ENGINE phases (ชั้น 2)

**Phase 0 — Harden pre-commit hook** `~ วัน` `เริ่มที่นี่`
- generalize `validate-commit.sh` → config-driven validator
- อ่าน YAML gate เล็กๆ → eval predicate กับ working tree/git → block on fail
- **seed มีแล้ว:** hook ปัจจุบันคือ constitutive enforcer ตัวแรก
- Done: rules-as-data พิสูจน์ได้ zero infra ใหม่

**Phase 1 — Externalize rules + CLI evaluator** `1–2 สัปดาห์`
- ดึง gate ทั้งหมดออกเป็น `gates/*.yaml` + predicate vocabulary (Python resolvers)
- `engine check <gate> [args]` = standalone CLI
- structured-output validator สำหรับ challenge-necessity contract (JSON Schema)
- Done: linter สำหรับ governance ที่ hook/CI/อะไรก็เรียกได้

**Phase 2 — Intercept agent tool calls (Engine จริง)** `2–4 สัปดาห์` `← จุดเปลี่ยน`
- wrap agent loop (SDK hook / MCP server หน้า governed tools)
- `mark_task_done`, `start_task`, `record_challenge`, `attach_evidence` = gated tools
- governed paths เขียนได้ผ่าน Engine tool เท่านั้น (FS allowlist + tamper detection)
- **จุดที่ governance กลายเป็น constitutive + model-floor risk ถูกแก้จริง**
- Done: agent bypass gate ไม่ได้

**Phase 4 — Canonical state store + generated views** `2–4 สัปดาห์`
- SQLite (หรือ versioned JSON) = canonical; render L1/L3 จาก store
- task/ADR state machine + guarded transitions + audit log
- Done: drift-impossible-by-construction

### 🖥️ SHELL phases (ชั้น 3)

**Phase 3 — Read-only Cockpit** `cheap, high signal` `(แทรกหลัง Phase 2)`
- SvelteKit app render `CoreAiWorkspaces/` live: work-status, task-board, activity feed, ADR/entity graph
- ยังไม่มี agent dispatch — เป็น dashboard เฉยๆ
- Done: ใช้เป็น dashboard ได้แม้ AI = 0, พิสูจน์ data model

**Phase 5 — Single governed agent + Decision Inbox** `← SHIP ที่นี่`
- dispatch 1 agent บน task ผ่าน LiteLLM
- ทุก STOP/gate → Decision Inbox card → human approve → Engine เขียน session sync
- **นี่คือผลิตภัณฑ์ใหม่ที่เล็กที่สุดแต่ของจริง: governed single-agent ใน project workspace**

**Phase 6 — Model-agnostic + role binding**
- per-agent model assignment, encrypted key vault, role floors
- โมเดลอ่อน → จำกัดให้ read-only/advisory lane เท่านั้น
- Done: เสียบ model ไหนก็ได้

**Phase 7 — Fan-out/in Council (swarm)** `"agents รุมวิเคราะห์"`
- port specialist agents (game-designer, ux, performance...) จาก `platforms/claude-code/agents/`
- concurrent read-only critique → synthesizer agent merge + surface conflict (Scenario E)
- map ตรงกับ `/caw-game-review` ที่มีอยู่ — แค่ทำให้ concurrent + observable + model-mixed

**Phase 8 — Multi-repo (detect/route/sequence)**
- project = manifest ของ repos + relationships
- generated **project map** (always-in-context) + cross-repo **entity-register** + impact flagging
- ⚠️ **ไม่รวม** atomic cross-repo refactor (ยังเป็นโจทย์ที่ยังไม่แก้ — human owns the seam)
- Done: detect cross-repo impact + route slices + sequence behind gates

**Phase 9 — Vector memory + polish + packaging**
- Phase-3 vector (Wing/Room/Drawer) + cross-session retrieval
- Docker Compose, SQLite→Postgres, Qdrant

---

## Boundary: Shell ↔ Engine (เก็บ API นี้ให้นิ่ง)

**Shell owns (body):** UI, repo manifest, LiteLLM router + key vault, agent dispatcher, indexers, vector store, Theater rendering, diff review, git ops — *Shell ไม่เคยตัดสินว่าอะไรทำได้*

**Engine owns (nervous system):** evaluate-action, context-assembly policy (L1/L2/L3 + token budget), compliance scan, session-protocol state machine, entity lifecycle, source-of-truth writes

**Shell เรียก Engine ที่จุดเหล่านี้:**
- session start/end → `engine.session.begin/end`
- ก่อนทุก tool call → `engine.evaluate(action, agent, context)` → verdict
- ก่อน code-touch → `engine.scopeGate(taskId, proposal)` → Scenario-M verdict
- ก่อน assemble context → `engine.composeContext(agent, task)`
- ADR/requirement event → `engine.escalate()` → Decision Inbox
- on commit → `engine.compliance.scan(diff)`

กฎ: *อะไรที่ protocol บอกว่า must/forbidden/STOP/human-decides = Engine ทุกอย่างที่เหลือ = Shell*

---

## White space (ยืนยันว่ายังว่าง)

| Tool | project-centric | governed (enforced) | multi-agent swarm | multi-repo |
|------|:---:|:---:|:---:|:---:|
| Cursor/Claude Code/Cline/Aider | ❌ (repo) | ❌ | ❌ | ❌ |
| Odysseus/OpenWebUI | ❌ (chat) | ❌ | ❌ | ❌ |
| AutoGen/CrewAI/LangGraph | ❌ | ❌ (library) | ✅ | ❌ |
| Devin/Factory | ~ | ❌ (autonomy) | ~ | ~ |
| **เรา** | ✅ | ✅ | ✅ | ✅ |

→ **intersection ของ 4 อย่างนี้ยังไม่มีใครถือครบ** — และตัวต่างจริงคือ governed (enforced) + Decision Inbox

---

## ความเสี่ยงสูงสุด (ต้องออกแบบรับตั้งแต่ต้น)

1. **Sandbox-escape = ทั้งเกม** — tool-gating ได้ผลก็ต่อเมื่อ agent ไม่มีทางอื่นถึง effect ถ้ามี bash อิสระ → `echo >> task-board.md` ทะลุทุก gate → ต้อง FS allowlist + governed paths ผ่าน Engine tool เท่านั้น + tamper detection
2. **อย่า enforce "quality" — enforce "presence/structure"** — ตรวจว่า challenge มีคำตอบครบ ไม่ใช่ตรวจว่าคำตอบ "ดี" (จะดึง model-floor risk กลับเข้า evaluator)
3. **Concurrency** — multi-agent เขียน shared state พร้อมกัน → corrupt → ต้อง Engine เป็น serialization point (write-lock/append-only event log)
4. **Context assembly คือ product จริงและยากสุด** — bundle L1/L2/L3 ต่อ agent ต่อ turn ให้ถูก ถูก budget → ลงทุนตรงนี้ก่อน ผิด = ได้ Cursor ที่แย่กว่า
5. **Layer-1 compatibility** — ถ้า truth ย้ายไป SQLite, plain Claude/Cursor session ที่ไม่มี Engine ต้องยังเห็น markdown view ที่ใช้ได้ → Engine ต้อง degrade graceful เป็น advisory markdown
6. **Key custody** — provider keys หลาย user = honeypot (protocol เราจัด credentials = Level 3) → encrypt at rest, egress ผ่าน LiteLLM เท่านั้น
7. **Governance friction** — Decision Inbox คือทั้ง moat และทั้งสิ่งที่ทำให้รู้สึกเป็นงานเอกสาร → tiered autonomy (auto Level 1, batch low-risk, gate Level 2–3)
8. **Cost blow-up จาก swarm** — fan-out × context ใหญ่ × premium model → per-task budget cap

---

## จุดเริ่มที่แนะนำ

**Phase 0 (harden pre-commit hook)** — เริ่มได้เลย ใช้เวลาเป็นวัน เสี่ยงต่ำ พิสูจน์ rules-as-data
→ ไม่ว่าจะสร้าง Shell หรือไม่ Phase 0–1 เป็นกำไรล้วน (linter governance ที่ CI ใช้ได้)
→ ทุก phase dogfood บน repo นี้เอง = เรากลายเป็น user คนแรกของ Engine ตัวเอง

---

## หมายเหตุลำดับ

```
Engine:  P0 ──→ P1 ──→ P2 ─────────→ P4
                          │            │
Shell:                    └→ P3        └→ P5(SHIP) → P6 → P7 → P8 → P9
```

- P0→P1→P2 = Engine core (ห้ามข้าม)
- P3 (read-only Cockpit) แทรกได้หลัง P2 — cheap, พิสูจน์ data model
- P5 = ผลิตภัณฑ์ใหม่ที่ ship ได้จริงตัวแรก ต้องมี P2+P4 รองรับ
- P7 (swarm), P8 (multi-repo) = ของหวาน ทำหลังแกนนิ่ง

---

*สังเคราะห์จาก Engine deep-dive + Shell deep-dive (2 agents, converged)*
*Anchor files: `core/11-ai-decision-protocol-template.md`, `platforms/claude-code/agents/game-designer.md`, `core/19-memory-architecture-overview.md`*
