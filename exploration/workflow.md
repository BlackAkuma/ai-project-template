# Build Workflow — feature-by-feature (clear, explicit)

**Goal (user, 2026-06-07):** build ระบบครบทุก feature ตาม BRD · ทีละ feature · test ทุกตัว · panel review 2/3 · log ทุกอย่าง · จนเสร็จ
**Supersedes:** ADR-013 G4=B demand-gate — user reopened, build full now (logged in work-log + ADR-013 review-trigger)

---

## The per-feature loop (ทำซ้ำต่อ feature เดียว ทีละตัว)

```
1. PICK      หยิบ feature ถัดไปจาก backlog (ตัวเดียว)
2. ANALYZE   challenge-necessity: (a) ทำเพื่ออะไร (b) source = BRD FR ไหน (c) ทางเล็กกว่า?
             + 3-lens (expert/technical/contrarian) ก่อนแตะโค้ด
3. BUILD     implement feature นั้น (เล็ก, focused)
4. TEST      เขียน + รัน test → ต้องผ่านจริง (verify behavior, ไม่ใช่แค่ compile)
             + regression: test suite เดิมทั้งหมดต้องยังเขียว
5. REVIEW    3-lens panel (technical/strategic/contrarian) + marketing advisory → โหวต 2/3
             contrarian บังคับหาเหตุ reject (ห้าม "ไม่มี")
6. GATE      2/3 PASS → ไป 7 · ไม่ผ่าน → กลับ 2 (วิเคราะห์+ทำใหม่) วนจนผ่าน
7. LOG       Panel Review Record (โหวต+dissent+การตัดสิน) + work-log entry
8. DECIDE?   ถ้าต้อง human ตัดสิน (strategic fork/irreversible) → present panel+options+vote+dissent
             → user → lock ADR · ไม่งั้น AI ตัดสินเรื่องเล็ก + log
9. COMMIT    git commit + push → กลับ 1 (feature ถัดไป)
```
จบเมื่อ: ทุก BRD FR build + test ครบ (backlog ว่าง)

## Definition of Done (ต่อ feature)
- [ ] code + test เขียนแล้ว · test ผ่าน (รันจริง แสดงผล)
- [ ] regression ทั้ง suite เขียว
- [ ] panel 2/3 PASS · dissent logged
- [ ] Panel Review Record + work-log บันทึก
- [ ] committed + pushed

## Gate policy (เมื่อไหร่หยุดถาม user)
- 🟢 FLOW: build/test/refactor ที่ safe+reversible → ทำเอง+log
- 🔴 STOP→user: reverse shipped behavior · irreversible · strategic fork · security/prod

## Headless limits (honest)
- frontend (SvelteKit Cockpit UI) → build CLI/renderer ที่ test ได้ headless; full browser UI flag ว่าต้อง frontend env
- external dep (LiteLLM/Qdrant) → build adapter + stub/in-memory fallback ที่ test ได้ offline; real provider flag

---

## Feature backlog (remaining BRD FRs → build order)

| # | feature | BRD FR | phase | สถานะ |
|---|---------|--------|-------|-------|
| F1 | model-agnostic adapter (LiteLLM routing + role-floor) | FR-4.1/4.2 | P7 | todo |
| F2 | governed agent dispatch loop (gate→act→evidence→event) | FR-1/3 | P6 | todo |
| F3 | multi-repo: manifest + cross-repo entity-register + impact | FR-5 | P9 | todo |
| F4 | vector memory interface + in-memory fallback | FR-2 (memory) | P10 | todo |
| F5 | Cockpit renderer (CLI read-only view of state+inbox) | FR-3 | P5 | todo |
| F6 | apply unified work-status schema (live cutover) | FR-2.2 | T-057 | todo |
| F7 | carry-over: CLAUDE.md uniform→tiered, C-07 invert, A-N mapping | — | T-051/052/053 | todo (🔴 reverse-shipped → review per-feature) |
| F8 | loose ends: T-044b run-audit rename, T-055 promote Scenario O→core, T-058 game playtest | — | — | todo |

> built so far (Engine core): P0-P4 + P6-data + adversarial suite = 54 tests/7 suites
