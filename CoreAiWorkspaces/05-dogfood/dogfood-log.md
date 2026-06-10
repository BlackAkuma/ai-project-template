<!-- AI-CONTEXT
doc: dogfood-log (BL-5/A7 -> M-A3)
started: 2026-06-10
target: governance live on this repo >=7 days hands-off + friction captured
day_count: 2
rule: ทุก block/hold/override/annoyance = 1 entry (สั้น) · จบสัปดาห์ = review -> BL-11 tuning
live_now: [secret-scan+placeholder block on commit, risky-git-op -> Decision Inbox, session digest auto-load, session write-back, Cockpit live + one-click]
-->

# Dogfood Log — ใช้จริงบน repo นี้ (เริ่ม 2026-06-10)

> เป้า (M-A3): governance ทำงานจริง ≥1 สัปดาห์ + เก็บทุก friction → จบสัปดาห์ตัดสินว่า "ใช้ได้จริง" ผ่านไหม

## Day 1 — 2026-06-10
- ✅ เปิดใช้ครบ: commit gates (secret/placeholder) · risky-git → Inbox · digest auto-load · write-back · Cockpit live
- 📝 baseline: 19 test suites green · hook latency ยังไม่วัด (BL-10)
- friction: (ยังไม่มี — เริ่มนับ)

## Day 2 — 2026-06-11
- ✅ P0+P1 backlog approved (panels 3/3) · 24 suites · stale-green cache loophole อุดแล้ว
- 📝 inbox: 0 ค้าง · writeback: ทำงานปกติ (0 new commits ตอนเช็ค) · latency 175ms PASS
- friction: ยังไม่มีรายงานจาก usage จริง (รอ user ทำงานบน repo)

<!-- เพิ่ม entry ใหม่ด้านล่าง: วันที่ · เกิดอะไร (block/hold/น่ารำคาญ/ช่วยได้จริง) · สั้นๆ -->
- Day 1 latency baseline: worst 175ms (budget 1000ms) — PASS (BL-10)
