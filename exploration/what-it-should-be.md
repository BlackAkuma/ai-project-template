# What It Should Be — Synthesis (capstone)

**Date:** 2026-06-05
**Branch:** `explore/odysseus-analysis`
**Status:** 🧭 Deep synthesis — gap audit (internal) + market (competitors) + market (trends)
**Pairs with:** `north-star-vision.md`, `development-plan.md`, `odysseus-analysis.md`

> สังเคราะห์จาก 3 deep-dive agent: internal gap audit (อ่าน repo จริง), competitive landscape (web), market trends (web)
> ⚠️ เอกสารนี้ **แก้แผนเดิมหลายจุด** — อ่านส่วน "สิ่งที่ตลาดบอกให้เราแก้" ก่อน

---

## TL;DR — ตำแหน่งที่ refined แล้ว

> **"Governed Project Memory"** — context/governance ที่ enforce เป็น *persistent project state* บน substrate ที่ self-host + model-agnostic ได้
>
> ไม่ใช่ "AI workspace อีกตัว" · ไม่ใช่ "agent IDE อีกตัว" · ไม่ใช่ "swarm"

ตลาดยืนยัน thesis หลักเรา **แต่บอกให้แก้ 4 อย่างสำคัญ** (ด้านล่าง) ไม่งั้นเดินเข้ากับดักที่ Gartner เตือนตรงๆ

---

## ส่วนที่ 1 — Thesis Scorecard (ตลาดตัดสิน)

### ✅ Validated — เดินได้มั่นใจ
| Thesis | หลักฐานตลาด |
|--------|------------|
| **Context engineering = value layer** | กลายเป็น discipline mainstream 2025-26 (Phil Schmid/DeepMind, Anthropic, ACE paper: "context, not model size, is the real performance driver" ลด drift 86%) |
| **Governance demand จริง** | 88% องค์กรเจอ AI-agent security incident, มีแค่ 14.4% ที่ approve เต็ม — pain-driven ไม่ใช่เก็ง |
| **Structured *project* memory = ช่องว่างที่ยังไม่มีใครแก้** | vendor (mem0/Letta/Zep) แก้ *user/conversation* memory หมด — *project* memory ยังว่าง; 2 ปัญหาใหญ่สุดที่ mem0 ยอมรับเอง (cross-session evolution, staleness) = สิ่งที่ CoreAiWorkspaces แก้ตรงๆ |
| **Model-agnostic + self-host** | model commoditization เป็น structural (5 open families ถึง frontier: DeepSeek/Qwen/Kimi/GLM/Mistral; API ราคาลด 80%); sovereignty ดัน self-host |
| **Orchestrated specialist + phase gate** | คือ pattern multi-agent ที่ "รอด" สู่ production |

### ⚠️ Risky — ต้อง reframe (สำคัญมาก)
| Bet เดิม | ปัญหา | แก้เป็น |
|---------|-------|--------|
| **"multi-agent swarm รุมวิเคราะห์"** เป็นหัวข้อขาย | multi-agent generic ถูก discredit บางส่วน — multi-agent ใช้ token ~15× / single-agent ชนะงาน *sequential*; งาน dev ส่วนใหญ่ sequential | reframe: "orchestrated specialists + phase gates สำหรับงาน *parallelizable เท่านั้น*" — ไม่ headline swarm |
| **Scenario-M บังคับทุก action** | 🔴 **Gartner เตือนตรงๆ: uniform governance = สาเหตุ enterprise AI failure** — approval fatigue = false safety | **risk-tiered governance**: gate หนักเฉพาะ action เสี่ยงสูง, auto-pass งานเสี่ยงต่ำ (ตรงกับ escalation Level 0-3 ที่เรามีแล้ว — ต้องใช้จริง) |
| **multi-repo indexing เป็น core IP** | crowded + capital-intensive (Sourcegraph Cody, Augment 400K+ files knowledge graph) | **orchestrate ข้าม repo ไม่ใช่ out-index** — govern "repo ไหน agent ไหน approve อะไร" ไม่ใช่แข่ง indexing |
| **SEA/Thai เป็น TAM หลัก** | จริงแต่ตลาดเล็ก/early, ไม่มีข้อมูล adoption ชัด | ใช้เป็น **beachhead + credibility** ไม่ใช่ทั้ง bet |

---

## ส่วนที่ 2 — สิ่งที่ตลาดบอกให้เราแก้ (แก้ development-plan.md)

**1. 🔴 Governance ต้อง risk-tiered ตั้งแต่ออกแบบ — ไม่ใช่ uniform**
ของเดิม: challenge-necessity + gate บังคับทุก code-touch
ปัญหา: นี่คือ anti-pattern ที่ Gartner ชี้ว่าทำ project ล่ม (approval fatigue)
แก้: ผูก gate กับ **risk tier** — Level 1 (reversible, low-stakes) → auto log+continue; Level 2 → Decision Inbox; Level 3 (irreversible/security/prod) → hard stop. เรามี escalation Level 0-3 ใน `core/11` อยู่แล้ว **แต่ยังไม่ได้ bind เข้ากับ gate** — นี่คืองานสำคัญ

**2. Multi-agent = orchestrated specialists สำหรับงาน parallel เท่านั้น**
reframe Phase 7: ไม่ใช่ "swarm รุมวิเคราะห์" เป็น default แต่เป็น tool เฉพาะงาน parallelizable (research, multi-lens review) — งาน dev sequential ใช้ single governed agent (Phase 5) เป็นหลัก

**3. Compose underneath — อย่า rebuild plumbing**
- model routing → **LiteLLM** (ตามแผน ✅)
- runtime policy enforcement → **OPA-style / Microsoft Agent Governance Toolkit** (MIT, sub-ms deterministic, ครอบ OWASP Agentic Top 10)
- เราเป็นเจ้าของ **project-stateful governance + Decision Inbox + multi-repo orchestration** layer บนสุดเท่านั้น

**4. Interoperate กับ AGENTS.md (de-facto standard แล้ว)**
AGENTS.md อยู่ใต้ Linux Foundation, อ่านโดย Codex/Cursor/Copilot/Gemini/Aider/Windsurf/Zed — **แต่มันเป็น advisory text ป้อนโมเดล ไม่ enforce**
→ จุดยืนเรา: **enforced layer ที่นั่งเหนือ advisory AGENTS.md** — เรา consume AGENTS.md ได้ แล้วเพิ่ม enforcement ที่มันไม่มี (อย่า reinvent context-file format)

---

## ส่วนที่ 3 — Substrate ต้องแก้อะไรก่อน (จาก internal audit)

**3 รอยร้าวลึกสุด — รูปร่างเดียวกันหมด:**
1. **truth อยู่ในครึ่งที่ parse ไม่ได้** — body เป็น free-form Thai prose = source of truth, AI-CONTEXT block (ครึ่งที่ parse ได้) ถูกประกาศว่า "ไม่ authoritative" → **กลับด้านสำหรับ Engine ไม่ได้**
2. **"done" เป็นคำพูด ไม่ใช่หลักฐาน** — validation evidence = narrative claim ใน work-log ไม่มี commit SHA/test exit code; มีแค่ `validate-commit.sh` ที่เดียวที่ตรวจ state จริง
3. **shared state ไม่มี concurrency primitive** — work-status/task-board/work-log เป็น multi-writer ไม่มี lock/ordering/conflict rule

**Top gaps (severity Critical/High) ที่ต้องแก้ใน core ก่อน Stage 2:**

| # | Gap | Severity | Block |
|---|-----|----------|-------|
| 1 | truth ใน prose body; AI-CONTEXT non-authoritative | Critical | Engine, Shell |
| 2 | ไม่มี shared schema สำหรับ AI-CONTEXT (field collision: `done`/`blocked` ต่างความหมายต่อไฟล์) | Critical | Engine, Shell |
| 3 | evidence = claim ไม่ใช่ artifact (ไม่มี SHA/test-id/exit code) | Critical | Engine |
| 4 | ไม่มี concurrency/locking model | High | Engine, multi-agent |
| 8 | ไม่มี model-agnostic agent contract (50 agents hardcode claude-sonnet-4-5) | High | Shell |
| 9 | quality-judgment ไม่แยกจาก presence/structure check | High | Engine |

**ข่าวดี:** task lifecycle (`todo→design_validate→in_progress→review→done`) และ ADR lifecycle เป็น state machine จริงแล้ว พร้อม encode · `validate-commit.sh` คือ constitutive enforcer ตัวแรกจริง

**Housekeeping gaps (แก้ง่าย ทำเลย):**
- core/ จริงมี **00–22** แต่ root CLAUDE.md บอก 00–21, platforms/CLAUDE.md บอก 00–18 — ขัดกันเอง
- `skills/game/04-compliance-codes.md` ถูกอ้าง ~20 ที่ แต่ **ไฟล์ไม่มีอยู่จริง** (file 04 คือ playtest-report)
- C-15..C-19 ไม่ได้นิยามเป็น compliance code + ชนกับ test-ID ใน run-audit.sh
- `git_pipeline` บังคับโดย bootstrap แต่ไม่อยู่ใน work-status schema
- orphaned: `tools/vector-memory/README.md`, daily-log/summary templates

---

## ส่วนที่ 4 — คู่แข่ง & timing

### Four-way intersection ยังว่างจริง (ยืนยัน)
ไม่มีใครถือครบ: **project-centric + enforced-governance + multi-agent + multi-repo** และ **ไม่มีใคร model governance เป็น durable project state** หรือมี **Decision Inbox** เป็น first-class

### Threat watchlist (เรียงตามความใกล้)
1. **Cursor 2.0** — ใกล้สุด: multi-agent + model-agnostic + enforced admin rules (push จาก dashboard) + enterprise distribution; ขาด multi-repo + decision-ledger → ถ้าเพิ่ม 2 อันนี้ปิด gap เร็ว
2. **Factory.ai** — $1.5B val, cross-codebase, governance อยู่ใน roadmap, integrates Linear/Jira
3. **Cognition/Devin Desktop** — multi-agent command center + ทุน; roadmap สั่นจาก acquisition = ช่อง
4. **Microsoft (Conductor + Agent Governance Toolkit)** — platform risk ใหญ่สุด; Conductor = human-gate analog ที่ดีสุดตอนนี้ (แต่ per-run ไม่ใช่ project-persistent)

### ตัวต่างที่ป้องกันได้ (ไม่มีใครมี)
1. **Governance as enforced persistent project state** (ไม่ใช่ advisory AGENTS.md, ไม่ใช่ per-call gateway guardrail)
2. **Decision Inbox** ระดับ project (ไม่ใช่ per-run แบบ Conductor, ไม่ใช่ per-ticket แบบ Jira)
3. **Native multi-repo** (ทุกคนอ่อนสุดตรงนี้)
4. **Self-hosted + model-agnostic** (Cursor/Factory เป็น SaaS + partly model-locked)

### Timing: now ดี แต่ window กำลังปิด
- ✅ เอื้อตอนนี้: model commoditize + ราคาลด 80%, open frontier weights (self-host ได้จริง), memory category เพิ่งฟอร์มแต่ *project*-memory ยังว่าง, governance pain เฉียบ
- ⏰ นาฬิกาเดิน: memory/governance category กำลังฟอร์ม — หน้าต่างยึด "governed project memory" เปิด *ตอนนี้* แต่ mem0/Letta/Zep มีทุนและขยับ
- ⚠️ ไม่เร่งเท่าที่กลัว: EU AI Act high-risk เลื่อนเป็น Dec 2027 (Digital Omnibus, พ.ค. 2026) — อย่า anchor pitch กับ legal cliff 2026; anchor กับ procurement + incident pain ที่เกิดทันที
- 🌊 headwind: Gartner ทำนาย 40% agentic project ถูกยกเลิกภายใน 2027 → buyer ระแวง hype → **นำด้วย governance/reliability/cost-control ไม่ใช่ "more agents"**

---

## ส่วนที่ 5 — สิ่งที่มันควรจะเป็น (product definition refined)

**ประโยคขาย:**
> ระบบ governance + project memory ที่ AI ตัวไหนก็ทำงานเชิงโครงการได้อย่างน่าเชื่อถือ — เพราะกฎถูก *บังคับเป็น state จริง* ไม่ใช่หวังให้โมเดลทำตาม รันบนเครื่องตัวเอง เสียบ model ไหนก็ได้

**5 เสาที่นิยามตัวตน:**
1. **Governed** — กฎ enforce เป็น persistent state, evidence-based (ไม่เชื่อคำพูด agent), **risk-tiered** (ไม่ uniform)
2. **Project Memory** — structured, curated, durable, evolving (แก้ปัญหา staleness + cross-session evolution ที่ vendor ยังแก้ไม่ได้)
3. **Decision Inbox** — human-gate ระดับ project เป็น first-class durable object
4. **Model-agnostic + Self-hosted** — LiteLLM ใต้ฝา, sovereignty-friendly (markdown ใน git ไม่มี proprietary cloud)
5. **Multi-repo orchestration** (ไม่ใช่ indexing) — govern ข้าม repo, compose Sourcegraph/Augment ถ้าต้อง index จริง

**สิ่งที่ "ไม่" ทำ (สำคัญพอกัน):**
- ❌ ไม่ out-index Sourcegraph/Augment
- ❌ ไม่ out-orchestrate LangGraph (compose ใต้ฝา)
- ❌ ไม่ out-gateway Portkey (compose ใต้ฝา)
- ❌ ไม่ headline "swarm" — orchestrated specialist สำหรับงาน parallel เท่านั้น
- ❌ ไม่ uniform mandatory gate — risk-tiered
- ❌ ไม่ reinvent context-file format — interoperate AGENTS.md

---

## ลำดับที่แนะนำ (revised)

**ก่อนแตะ Stage 2 — fix substrate ให้ machine-ready (พวกนี้คือ Phase 0-1 ตัวจริง):**
1. แก้ housekeeping contradictions (core count, missing compliance-codes file, C-15..19, git_pipeline) — *ง่าย ทำเลย*
2. นิยาม **AI-CONTEXT schema เดียว** (field→type→required→version) ข้ามทุก state file — *Critical gap #2*
3. กลับด้าน canonical: structured = source of truth, prose = view — *Critical gap #1*
4. เพิ่ม **evidence field** (commit SHA, test cmd+exit, artifact) ใน Definition-of-Done + Task Close Gate — *Critical gap #3*
5. tag ทุก rule: **enforceable-presence vs advisory-quality** — *gap #9*
6. bind escalation Level 0-3 เข้ากับ gate = **risk-tiered governance** — *market correction #1*

**แล้วค่อย:** Engine (P0-P2) → read-only Cockpit (P3) → governed single agent + Decision Inbox (P5 SHIP)

→ ทุกอย่าง dogfood บน repo นี้เอง

---

*สังเคราะห์จาก 3 agents (internal audit + 2 market). Verification caveats: market-size figures + บาง adoption % มาจาก vendor blog (directional ไม่ authoritative); EU AI Act high-risk เลื่อนเป็น Dec 2027; Gartner 40% ลงวันที่ 2025-06-25*
