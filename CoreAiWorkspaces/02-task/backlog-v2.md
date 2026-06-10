<!-- AI-CONTEXT
doc: backlog-v2
source: BRD-v2 + 4-lens panel 2026-06-10 (product/tech/contrarian/marketing — full results in work-log)
status: active
insight: A1/A2/A4 work but are INVISIBLE on screen — user runs no commands, so "works but invisible = doesn't work". Close see-decide-remember loop on the LIVE repo before any new capability.
p0: [BL-1 cockpit-live, BL-2 memory-autoload, BL-3 memory-writeback, BL-4 one-click-start, BL-5 dogfood-start]
p1: [BL-6 test-evidence, BL-7 engine-init, BL-8 hold-notification, BL-9 receipts-panel, BL-10 latency-budget, BL-11 fatigue-tuning, BL-12 agent-run-spike]
deferred: [B3 model-picker, B4 qdrant, B5 multi-repo-live, B6 specialists, B7 deploy, B8 game-profile, B9 team(KILL), B2-rewrite(extend vanilla instead)]
rule: B-anything stays locked until M-A3 dogfood passes (BRD R3)
-->

# Backlog v2 — "เห็นบนจอ จำได้ ใช้ทุกวัน" (จาก 4-lens panel, 2026-06-10)

## 🔍 Insight หลักจากการวิเคราะห์ (ทุก lens เห็นตรงกัน)

> **ของที่สร้างมาทำงานจริงแล้ว แต่ "มองไม่เห็นบนจอ"** — governance บล็อก/hold ใน hook จริง แต่ Cockpit ยังโชว์ demo project · memory มี store แล้วแต่ไม่ auto-load · สำหรับคนที่ไม่รันคำสั่ง **"ทำงานแต่มองไม่เห็น = ไม่ทำงาน"**
> ดังนั้น: ปิดลูป **เห็น → ตัดสิน → จำ** บน repo จริง ก่อนเพิ่มความสามารถใหม่ใดๆ

---

## 🔴 P0 — ทำตอนนี้ (ปิดลูปบนจอ)

| ID | งาน | คุณค่า | BRD | ขนาด |
|----|-----|--------|-----|------|
| **BL-1** | **Cockpit Live Mode** — Cockpit อ่าน repo จริงนี้เป็น default (inbox จริงจาก hook, audit จริง, สถานะจริง) · demo แยกเป็นโหมด `/demo` · ปิดลูป approve/reject บนจอ→มีผลจริง | สิ่งที่ hook บล็อก/hold **โผล่บนจอให้กดตัดสินจริง** | A4→G1 | M |
| **BL-2** | **Memory auto-load (A5)** — SessionStart hook ฉีด digest สถานะโปรเจ็กต์ (state + decisions + held items + สรุป session ก่อน) เข้า Claude Code ทุก session ใหม่ — render จาก store ไม่ใช่ให้ AI เดา | เปิด session ใหม่ **AI รู้เรื่องเดิมเอง** (G3 ที่รอมานาน) | A5→G3 | M |
| **BL-3** | **Memory write-back** — session-end hook บันทึกสิ่งที่เกิดขึ้น (commits/decisions/blocks) ลง store อัตโนมัติ | memory เลี้ยงตัวเอง ไม่ต้องจดมือ | A5→G3 | M |
| **BL-4** | **One-click always-on** — shortcut/auto-start เปิด Cockpit + browser เอง · มี indicator "governance ON, watching repo X" | จอ**อยู่ตรงนั้นเอง**ทุกเช้า ไม่ต้องเปิด server มือ | A6→G1 | S |
| **BL-5** | **เริ่ม dogfood ทันที (A7-start)** — governance live บน repo นี้อยู่แล้ว → เริ่มนับวันจริง + ทุก block/hold/override ถูก log เป็น friction อัตโนมัติ | ตัวเดียวที่**พิสูจน์ G1 ได้จริง** เริ่มได้วันนี้ | A7→G1 | S |

## 🟡 P1 — ถัดไป (ทำให้คำโฆษณาเป็นจริง + ขยายสู่ repo อื่น)

| ID | งาน | คุณค่า | BRD | ขนาด |
|----|-----|--------|-----|------|
| BL-6 | **Test-evidence (จบ A3)** — gate รัน/อ่านผลเทสจริง · "done" โดยไม่มีเทสเขียว → block/hold | ปิดคำโกหกที่พบบ่อยสุด: "เทสผ่านแล้ว" | A3→G2 | M |
| BL-7 | **`engine init` (A6)** — คำสั่งเดียวติดตั้ง hooks+gates+memory+Cockpit ลง repo ไหนก็ได้ + doc ไทย 2 นาที | ออกจาก repo ตัวเองได้ → dogfood repo ที่ 2 | A6→G1 | M |
| BL-8 | **แจ้งเตือนเมื่อ hold** — Windows toast / badge เมื่อมี item รออนุมัติ | item ค้างเงียบๆ = agent stall + คนเลิกใช้ (R1) | A4→R1 | S |
| BL-9 | **"Receipts" panel** — สรุปรายสัปดาห์: ตรวจ N, บล็อก N, hold N, จำ N sessions + chain verified | เห็นคุณค่าสะสมเป็นตัวเลขจริง | G2/N3 | S |
| BL-10 | **Latency budget** — วัด overhead ทุก gate, เส้นตาย <1s (deterministic path) | governance ช้า = โดนปิดทิ้ง (R1/N5) | N5→R1 | S |
| BL-11 | **Fatigue tuning หลัง dogfood** — รีวิวทุก block/hold ที่ยิงจริง, ลด rule ที่ noisy, threshold ปรับได้ต่อ repo | กัน rubber-stamp / governance theater | R1→G1 | S |
| BL-12 | **Governed agent run จริง 1 งาน (B1 spike)** — งานเล็กจริง 1 งาน ผ่าน loop คิด→ทำ→gate→evidence ด้วย local model จริง บันทึกไว้ดูได้ | ก้าวแรกจาก "การ์ด" → "ผู้ช่วยที่ทำงาน" + เทส loop จริงครั้งแรก | B1→G5 | M |

## ⏸️ Defer/Kill (consensus ทั้ง 4 lens — ล็อกจนกว่า M-A3 ผ่าน ตาม BRD R3)

- **B9 team — KILL** จาก active planning (ยังไม่มี user คนที่ 2 ในขอบฟ้า)
- **B4 Qdrant** — lexical ยังไม่เคยพิสูจน์ว่าไม่พอ · **B3 model-picker** — มี model เดียว dropdown ไร้ค่า · **B7 Docker** — user เดียวเครื่องเดียว · **B6 specialists** — loop เดียวยังไม่เคยรันจริง · **B8 game profile** — หลังมี daily user ก่อน · **B5 multi-repo live** — รอใช้จริง 2+ repos ก่อน
- **B2 SvelteKit rewrite** — ต่อยอด vanilla Cockpit เดิมตลอด Phase A
- **หยุด polish เดโม** (try_it/seed_demo) — จบหน้าที่แล้ว เก็บไว้ ไม่โต

## ⚠️ Dissent ที่บันทึกไว้ (เหตุผลย้อนอ่านได้)

1. **(tech/contrarian)** "watchdog เป็น passive — ต่อให้เห็นบนจอ อาจยังไม่เกิด daily habit" → mitigations: BL-2 memory คือ value เชิงรุกประจำวัน + BL-12 spike ไปทาง "ผู้ช่วย"
2. **(tech)** SessionStart injection อาจซ้ำซ้อนกับ CLAUDE.md/CoreAiWorkspaces protocol ที่ทำมือยู่ → ต้อง dedupe ตอน build BL-2 (digest แทนที่การอ่านมือ ไม่ใช่เพิ่มเข้าไป)
3. **(ทุก lens)** solo founder อนุมัติ hold ของตัวเอง → rubber-stamp ใน 2-3 วัน = governance theater → BL-11 บังคับรีวิว + ลด noise ให้เหลือแต่ของจริง
4. **(contrarian)** Cockpit Live อาจเป็น screen-candy — G1 จริงๆ วัดที่ "governance รันบน repo จริง ≥1 สัปดาห์" ซึ่ง hook ทำอยู่แล้ว → ตอบ: user ไม่รันคำสั่ง จอคือ interface เดียวที่เขาตัดสินได้
5. **(contrarian)** local 7B fail structured output 15-30% — gate ที่ต้องใช้ LLM ตัดสินจะเพี้ยน → กฎ: **gate หลักทั้งหมด = deterministic เท่านั้น** LLM เป็น advisory
6. **(marketing เตือนตัวเอง)** receipts อาจกลายเป็น vanity metric ถ้า block น้อย → ไม่ engineer dramatic blocks เพื่อเดโม

## ลำดับการทำ (สัปดาห์นี้)
```
✅ P0 ครบ + panel re-review 3/3 PASS (2026-06-10): BL-1 → BL-4 → BL-2 → BL-3 → BL-5
   (รอบแรก FAIL 1/3 → แก้ causal-approval/re.sub/CLAUDE.md/live-writeback → ผ่าน)
→ ตอนนี้: P1 เริ่ม BL-6 test-evidence
```

## Follow-ups จาก P0 re-review dissent (logged 2026-06-10)
- FU-1 reject re-open flow (in-band เปลี่ยนใจได้) — รอ M-A3
- FU-2 inbox.jsonl file-lock/atomic — **บังคับก่อน Phase B multi-agent**
- FU-3 approval scoping เปราะ (exact string) — รีวิวใน BL-11
- FU-4 hold-list → parsing จริง (กัน refspec-force bypass) — รอ M-A3
