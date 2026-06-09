<!-- AI-CONTEXT
doc: BRD-v2 (master)
version: 2.0
status: Draft (awaiting user accept)
supersedes_context: BRD.md v1.0 (engine-scoped) — v2 reframes around usable-first (A) -> full app (B)
direction_lock: usable-first via governance-layer (Path A) then grow to full app (Path B). user-decided 2026-06-09.
ga_key: LOCAL (Ollama, free, no key) — user-decided 2026-06-09 (machine: 32GB RAM, GTX1070 8GB — viable)
ga_host: Claude Code hooks first — user-decided 2026-06-09 (3-analyst consensus)
m_a1_status: A1 local-LLM wiring DONE (llm.py ollama provider). next: install Ollama + pull model + verify real call, then A2 hooks
phases: [A usable-layer, B full-app]
-->

# BRD v2 — Governed Project Memory (usable-first → full app)

> **กฎอ่านง่าย:** ทุก item เขียนเป็นรูปธรรม (ทำอะไรจริง) ไม่ใช่ศัพท์ลอย · มี Status: ✅done / 🟡partial / 🔴todo · มี "ต้องการ env" ถ้าทำ headless ไม่ได้

---

## 0. การตัดสินใจที่ล็อกแล้ว (2026-06-09)

- **เป้าหมาย: ใช้งานได้จริงก่อน** แล้วค่อยโตเป็นแอปเต็ม
- **เส้นทาง: A → B** · A = governance เกาะ agent ที่ใช้อยู่ (ใช้ได้เร็ว) · B = แอปเต็มแบบ Odysseus เชิงโปรเจ็กต์
- **ไม่ทิ้งวิชั่นแอปเต็ม** — แต่ A คือบันไดขั้นแรกที่ "ใช้ได้จริง" ของ B ไม่ใช่ทางแยก

---

## 1. มันคืออะไร (1 ย่อหน้า)

เครื่องมือที่ทำให้ **AI agent พัฒนาโปรเจ็กต์ซอฟต์แวร์ได้อย่างน่าเชื่อถือ** — agent ทำงานเร็ว แต่ **โกหก/มั่ว/ทำพังไม่ได้** เพราะมีชั้น governance ที่ตรวจ state จริง (git/ไฟล์/เทส), บล็อกของปลอม, ดันงานเสี่ยงให้คนอนุมัติ, จำบริบทโปรเจ็กต์ข้าม session, และทำงานข้าม repo ได้ — เสียบ model ไหนก็ได้

## 2. วิชั่น + Goals (วัดผลได้)

| Goal | คำอธิบาย | วัดด้วย |
|------|----------|---------|
| **G1** | ผมใช้มันเองได้จริงบน repo จริง สัปดาห์นี้ | governance ทำงานจริงบน repo นี้ ≥1 สัปดาห์ ไม่ต้องป้อนมือ |
| **G2** | agent โกง/ทำพังไม่ได้ | fake-done/secret/prod ถูกบล็อก/ถาม 100% บน action จริง |
| **G3** | จำโปรเจ็กต์ได้ข้าม session | เปิด session ใหม่ → AI รู้สถานะ/decision เดิมโดยไม่ต้องเล่าซ้ำ |
| **G4** | เสียบ model ไหนก็ได้ | สลับ provider/model ได้โดยไม่แก้โค้ด governance |
| **G5** | โตเป็นแอปเต็มได้ | มี agent loop + UI ที่รันงานจริงภายใต้ governance |
| **G6** | ข้าม repo ได้ | คุม entity ที่ใช้ร่วมหลาย repo + เตือน impact |

## 3. สถานะปัจจุบัน (ตรงไปตรงมา)

- ✅ **กลไก governance (engine logic)** — gate/risk-tier/tamper-evidence/role-floor/inbox/store/entities + 17 test suites
- ✅ **รันได้แบบ demo** — CLI + HTTP API + web Cockpit (บน stub model, demo project)
- 🔴 **ยังไม่เสียบงานจริง** — ไม่ต่อ AI จริง, ไม่ดัก action จริงของ agent, ไม่อ่าน repo จริง
- = "พิสูจน์ในแล็บแล้ว ยังไม่ลงสนาม" → Phase A คือการลงสนาม

---

## 4. ผู้ใช้ + งานที่ต้องการ (jobs-to-be-done)

| ผู้ใช้ | งานที่อยากให้ทำได้ |
|--------|---------------------|
| **เจ้าของโปรเจ็กต์ (คุณ ก่อน)** | ให้ AI ทำงาน dev แต่คุมได้ ไม่ต้องไล่เช็คเอง / ไม่กลัวมันมั่ว |
| **ทีม dev (ภายหลัง)** | governance ร่วม + decision log + ข้าม repo |
| **เกม dev (profile)** | governance + playtest/balance gate เฉพาะเกม |

---

# PHASE A — ทำให้ "ใช้ได้จริง" (governance เกาะ agent ที่ใช้อยู่)

> เป้า: **G1+G2+G3** · ใช้ได้บน repo จริงภายในไม่กี่วัน-สัปดาห์ · dogfood repo นี้

| ID | ทำอะไร (รูปธรรม) | ทำไม | Acceptance | Status / ต้องการ |
|----|------------------|------|------------|------------------|
| **A1** | เสียบ LLM จริง — `dispatch`/agent เรียก model จริงผ่าน LiteLLM ด้วย API key | governance ต้องหุ้ม AI จริง ไม่ใช่ stub | ใส่ key → turn เรียก model จริง → governance ยังบังคับ | 🟡 adapter มีแล้ว · **ต้อง: API key** |
| **A2** | **ดัก action จริงผ่าน Claude Code hooks** — PreToolUse/PostToolUse/Stop → engine ตรวจก่อน commit/เขียนไฟล์/ปิด task จริง | นี่คือหัวใจ "ใช้ได้จริง" — คุม action จริง ไม่ใช่ action ของเล่น | commit ที่มี secret/ปิด task ไม่มี evidence บน repo นี้ → ถูกบล็อกจริง | 🔴 todo · repo มี hook อยู่แล้วต่อยอดได้ |
| **A3** | อ่าน state จริง — ผูก resolver กับ git/ไฟล์/ผลเทสจริงของ repo (มีบางส่วนแล้ว) | gate ต้องตัดสินจากความจริง | gate อ่าน git log/test exit จริง ไม่ใช่ fixture | 🟡 resolver git/file มีแล้ว · ขยาย test-runner |
| **A4** | Decision Inbox โผล่ในงานจริง — เมื่อ L2/L3 ให้หยุด+ถามคนในเวิร์กโฟลว์จริง (terminal/hook prompt) | คนต้องได้ตัดสินตอนที่ควร | action เสี่ยง → workflow หยุด รออนุมัติจริง | 🔴 todo |
| **A5** | Project memory จริง — บันทึก/อ่าน state+decision ข้าม session จาก JSON-in-git (มี store แล้ว) ให้ AI โหลดอัตโนมัติ | G3 จำข้ามรอบ | session ใหม่ → AI สรุปสถานะถูกโดยไม่เล่าซ้ำ | 🟡 store + render มีแล้ว · ต่อ auto-load |
| **A6** | ติดตั้งง่าย — คำสั่งเดียวเพิ่ม governance เข้า repo ใดก็ได้ (`init`) + เอกสาร setup | คนอื่น (และคุณ) ติดตั้งได้ | `engine init` ใน repo เปล่า → hook+gate+memory พร้อม | 🔴 todo |
| **A7** | dogfood — เปิด governance บน repo นี้ + 1 โปรเจ็กต์จริงของคุณ ใช้ ≥1 สัปดาห์ | พิสูจน์ G1 ของจริง | ใช้จริง, เก็บ pain points, iterate | 🔴 todo · **ต้อง: repo จริง** |

**นิยาม "เสร็จ Phase A":** เปิด Claude Code (หรือ agent) บน repo จริงของคุณ → มันทำงาน dev ได้ + governance บล็อก/ถามจริงเมื่อควร + จำโปรเจ็กต์ได้ข้าม session → **คุณใช้มันเองทุกวัน**

---

# PHASE B — แอปเต็ม (Odysseus-like, project-centric)

> เป้า: **G4+G5+G6** · เริ่มเมื่อ A ใช้ได้จริงแล้ว · หลายส่วนต้อง env จริง

| ID | ทำอะไร (รูปธรรม) | ทำไม | Acceptance | Status / ต้องการ |
|----|------------------|------|------------|------------------|
| **B1** | Agent loop — แอปรัน agent ที่ "ลงมือทำงาน dev เอง" ภายใต้ governance (วน: คิด→ทำ→gate→evidence) | จาก "การ์ดเงียบ" → "ผู้ช่วยที่ทำงานให้" | สั่งงาน → agent ทำหลายสเต็ป, ทุกสเต็ปผ่าน gate | 🔴 todo · governed_turn เป็นฐาน |
| **B2** | UI เต็ม — chat/console + project dashboard + inbox + audit (ต่อยอด web Cockpit) | คนใช้งานจริงผ่านหน้าจอ | สั่งงาน agent + ดู/อนุมัติ ผ่าน UI ครบ | 🟡 Cockpit เป็นฐาน · **ต้อง: frontend env (เต็ม)** |
| **B3** | Model-agnostic UI — เลือก/สลับ provider+model ในหน้าจอ (local/cloud) | G4 | สลับ model ใน UI ได้, role-floor ทำงาน | 🟡 backend มี · ต่อ UI |
| **B4** | Semantic memory จริง — embeddings (Qdrant) แทน lexical stub | จำแบบเข้าใจความหมาย | ถามด้วยคำต่างแต่เจอ memory ที่เกี่ยว | 🟡 interface มี · **ต้อง: Qdrant** |
| **B5** | Multi-repo orchestration จริง — manifest + ดัก impact ข้าม repo ในงานจริง | G6 | แก้ entity ใน repo A → เตือน repo B จริง | 🟡 detect logic มี · ต่อใช้งานจริง |
| **B6** | Specialists / multi-agent — หลาย agent (เขียน/รีวิว/เทส) ทำงานขนานใต้ governance | คุณภาพ + ขนาน | งานใหญ่ → หลาย agent + governance รวม | 🔴 todo |
| **B7** | Deploy + packaging — Docker compose (engine+UI+Qdrant), self-host | คนอื่นรันได้ | `docker compose up` → ใช้งานได้ | 🟡 Dockerfile มี · **ต้อง: hosting** |
| **B8** | Profile packs — เกม (playtest/balance gate) + domain อื่น compose ได้ | ครอบหลายสาขา | เปิด profile เกม → gate เกมทำงาน | 🔴 todo · schema profile มีฐาน |
| **B9** | Team/collaboration — decision log ร่วม, หลายคนอนุมัติ inbox, สิทธิ์ | ใช้เป็นทีม | 2 คนเห็น inbox เดียว, audit ร่วม | 🔴 todo |

**นิยาม "เสร็จ Phase B":** คนเปิดแอป → สั่ง agent ทำงาน dev บนโปรเจ็กต์จริง (เสียบ model เอง) → agent ทำงานหลายสเต็ปภายใต้ governance, ข้าม repo ได้, จำได้ → **เป็นเครื่องมือเทียบ Odysseus แต่จุดต่าง = governance + project memory**

---

## 5. Non-Functional (NFR)

| ID | ข้อกำหนด |
|----|----------|
| N1 | Sovereignty — ข้อมูลอยู่ใน git ของผู้ใช้, self-host ได้, ไม่ผูก cloud เจ้าใด |
| N2 | Model-agnostic — เปลี่ยน provider ไม่แตะโค้ด governance |
| N3 | Tamper-evident — audit chain ตรวจการแก้ย้อนหลังได้ |
| N4 | ความปลอดภัย — key เข้ารหัส at rest, ไม่ leak ลง log |
| N5 | Performance — gate ต้องไม่ทำ workflow ช้าจนน่ารำคาญ (<~1s/ตรวจ) |
| N6 | ติดตั้งง่าย — คำสั่งเดียว, dependency น้อย |

## 6. Milestones (เรียงตามคุณค่า)

```
M-A1  LLM จริง + ดัก action จริง (A1+A2+A3)        → governance ลงสนาม
M-A2  Inbox+memory ในงานจริง (A4+A5) + ติดตั้ง (A6) → ครบลูป usable
M-A3  dogfood 1 สัปดาห์ (A7)                        → ★ G1 "ใช้ได้จริง" ✓
─────────────────────────────────────────────────
M-B1  agent loop + UI เต็ม (B1+B2+B3)               → จากการ์ด → ผู้ช่วย
M-B2  memory จริง + multi-repo (B4+B5)              → เชิงโปรเจ็กต์เต็ม
M-B3  specialists + deploy + profile (B6+B7+B8)     → แอปเต็ม
M-B4  team (B9)                                     → ใช้เป็นทีม
```

## 7. Gates — จุดที่ต้องให้ผู้ใช้ตัดสิน

| Gate | คำถาม | เมื่อไหร่ |
|------|-------|----------|
| GA-key | provider/model ไหน + ให้ key ยังไง (ปลอดภัย) | ก่อน A1 |
| GA-host | hook เข้า Claude Code เป็นทางหลักไหม หรือรองรับ agent อื่นด้วย | ก่อน A2 |
| GB-ui | UI เต็มใช้ stack ไหน (vanilla ต่อ / SvelteKit / อื่น) | ก่อน B2 |
| GB-deploy | self-host อย่างเดียว หรือมี hosted ด้วย | ก่อน B7 |

## 8. Risks

| Risk | ผลกระทบ | กัน |
|------|---------|-----|
| R1 governance ช้า/น่ารำคาญ → คนปิดทิ้ง | สูง | NFR-N5, risk-tier (ไม่ถามพร่ำเพรื่อ) |
| R2 ผูกกับ Claude Code มากไป | กลาง | A2 ทำ interface กลาง, รองรับ agent อื่นได้ |
| R3 build B เต็มแต่ไม่มีคนใช้ | สูง | ต้องผ่าน M-A3 (พิสูจน์ใช้จริง) ก่อนลุย B |
| R4 แข่งกับ Cursor/Odysseus บนของที่ไม่ใช่จุดเด่น | สูง | จุดต่าง = governance+memory เท่านั้น, ที่เหลือ minimal |

## 9. นิยาม "ใช้ได้จริง" (กันเข้าใจคลาดอีก)

- ❌ ไม่ใช่ "unit test ผ่าน"
- ✅ คือ **เปิดงานจริงของคุณ → AI ทำงานให้ + governance บล็อก/ถามจริง + จำได้ → คุณใช้ทุกวันโดยไม่ต้องป้อนมือ** (= จบ M-A3)

---

*ถัดไป: ผู้ใช้ accept BRD-v2 → ตอบ GA-key + GA-host → เริ่ม M-A1 (A1→A2→A3)*
