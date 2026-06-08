# Product Completion Plan — Engine → Runnable Product (vs Odysseus)

**Date:** 2026-06-08 · **Branch:** dev
**Why this exists:** "build complete" ก่อนหน้า = **engine library + blueprint** (สมอง) เท่านั้น — ไม่ได้วางแผนเส้นทางไป **ผลิตภัณฑ์ที่รันได้จริง** (ร่าง) แบบ Odysseus. นี่คือแผนปิดช่องว่างนั้น (user-flagged gap).

> หลักความจริง: บางขั้น **build+test headless ได้** (CLI/API) · บางขั้น **ต้องสภาพแวดล้อมจริง** (Node frontend, API key, hosting) · บางขั้น **ต้องคนใช้จริง** (validation vs Odysseus)

---

## สถานะปัจจุบัน (honest)
- ✅ engine/ = Python modules (logic) + 15 test suites/~146 tests — **สมองทำงาน พิสูจน์แล้ว**
- ❌ ไม่มี: command surface ที่ใช้จริง · API · UI · LLM จริง (stub) · deploy · real user
- = "เสร็จระดับ engine" ≠ "ผลิตภัณฑ์ใช้ได้แบบ Odysseus"

## เส้นทาง 4 Phase สู่ runnable product

### Phase A — Runnable engine (CLI + API) 🟢 **headless ทำได้ทันที**
ทำให้ library กลายเป็น *เครื่องมือที่ใช้ได้จริง* (แม้ยังไม่มี web UI)
- **A1 CLI** `engine/cli.py` — command เดียวรวม: `init` / `gate <id>` / `turn <task> <intent>` / `cockpit` / `inbox` / `inbox resolve <id>` / `audit`
- **A2 HTTP API** (FastAPI) — expose engine ops (gate/turn/cockpit/inbox) เป็น endpoint; backend ที่ Shell เรียก · test ด้วย TestClient (ไม่ต้อง browser)
- **acceptance:** รัน `python -m engine.cli cockpit` ได้ผลจริง · API endpoint ตอบถูก (TestClient test)
- **verify:** integration test (ไม่ใช่แค่ unit) — end-to-end turn ผ่าน CLI/API

### Phase B — Real LLM integration 🟡 **ต้อง API key (user env)**
- B1 wire litellm provider จริง (ตอนนี้ stub+lazy) + retry/error handling
- B2 contract test ด้วย mock (headless) · **live-call test ต้อง key ของคุณ**
- **acceptance:** เสียบ key จริง → agent turn เรียก model จริง → governance ยังบังคับ (model จริงทำ done ปลอมไม่ได้)

### Phase C — Shell web UI 🟡 **ต้อง Node/SvelteKit env**
- C1 SvelteKit Cockpit (เรียก Phase-A API): project dashboard + Decision Inbox (approve/reject) + audit view
- C2 hero-demo flow ใน UI (<10min): gate บล็อก fake-done + Inbox item โผล่
- **headless:** scaffold โค้ดได้ · **รัน/ทดสอบจริงต้อง Node + browser** (preview/Playwright)
- **acceptance:** เปิดเว็บ → เห็น project + กด approve inbox → state เปลี่ยน

### Phase D — Deploy + real-use validation 🔴 **ต้อง hosting + คนใช้จริง**
- D1 Docker Compose (engine API + Qdrant + UI) — buildable headless
- D2 deploy จริง + **คนใช้จริงบนโปรเจ็กต์จริง** = บททดสอบ "โอเคเทียบ Odysseus" ตัวจริง
- D3 real semantic memory (Qdrant embeddings แทน lexical stub)
- **acceptance (ตัวจริง):** มีคน clone+run+ใช้ governance บนโปรเจ็กต์เขา แล้วมันช่วยจริง

---

## What's headless-doable now vs needs-env vs needs-people
| ทำได้เลย (headless) | ต้อง env จริง | ต้องคนจริง |
|--------------------|--------------|-----------|
| A1 CLI · A2 API + tests · B2 mock contract · C1 scaffold · D1 Compose file | B real LLM (key) · C run UI (Node/browser) · D3 Qdrant | D2 real-user validation (vs Odysseus) |

## Sequencing + gates
```
A1 CLI → A2 API (headless, NOW) → B wire LLM (key) → C Shell UI (Node) → D deploy+validate
```
- G-ENV1 (ก่อน B): คุณให้ API key / เลือก provider
- G-ENV2 (ก่อน C): frontend env พร้อม (Node)
- G4/ADR-013 demand-gate: user reopened → build เต็ม; D2 validation = "OK vs Odysseus" จริง

## นิยาม "เสร็จจริง" (vs Odysseus) — ที่ขาดจากแผนเดิม
ไม่ใช่ "unit tests ผ่าน" แต่คือ: **คนเปิดมา รันได้ เสียบ model ใช้ governance บนโปรเจ็กต์จริง แล้วมัน enforce + ช่วยได้** (Phase D2)

---

*ต่อยอด master-plan (P5-P10) + flow-plan — เพิ่มชั้น integration (CLI/API) + env-reality ที่แผนเดิมขาด. เริ่ม Phase A headless ทันที.*
