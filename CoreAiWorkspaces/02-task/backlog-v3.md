<!-- AI-CONTEXT
doc: backlog-v3 (SINGLE ACTIVE ROADMAP — supersedes backlog-v2)
updated: 2026-06-12
rule: นี่คือที่เดียวที่ track ทุกอย่าง — ผลวิจัย/panel ทุกรอบถูกแปลงเป็น item ที่มี id+status+source แล้ว
status_legend: ✅done · 🔄now · 🟢next · ⏸️deferred(มี gate) · ❌killed
now: [A7-dogfood, BL-11]
done_recent: [DEV-FP]
done_recent: [DEV-FP, FU-2(3-round), FU-1(3/3), FU-3(3/3), FU-4(2-round: tokenizer+quote-aware+fail-closed)]
next: [FU-5, FU-6-auditlog-concurrency, OBS-1, RD-1..4(user)]
deferred_until_M-A3: [B1,B2,B3,B4,B5,B6,B7,B8]
killed: [B9-team]
freeze: MASTER (no master update until user order) · DEV-DIRECT (feature work -> branch)
-->

# Backlog v3 — Roadmap เดียว (single source) · 2026-06-12

> รวมผลวิจัย+panel ทุกรอบเป็น item ที่ track ได้ · ไม่ต้องกลับไปอ่าน backlog-v2/work-log เก่า
> legend: ✅เสร็จ · 🔄กำลังทำ · 🟢ทำต่อ · ⏸️พัก(มีเงื่อนไขปลด) · ❌ทิ้ง

---

## ✅ เสร็จแล้ว (shipped + verified)

| กลุ่ม | รายการ | ที่อยู่ |
|------|--------|--------|
| **Engine core** | F1-F12: model-floor, agent-dispatch, multi-repo, memory, cockpit, schema-cutover, carry-over, CORE-11-entities, evidence 2-class, AI-CONTEXT validator | engine/ (24 suites) |
| **Phase A usable** | BL-1 cockpit-live · BL-2 memory-autoload · BL-3 writeback · BL-4 one-click · BL-6 test-evidence · BL-7 engine-init · BL-8 notify · BL-9 receipts · BL-10 latency · BL-12 agent-run-spike | dev (panel 3/3) |
| **Template enforcement** | **T-060** Enforcement Pack → **master** (prose→machine gate: branch/secret/T-ref/Task-Close/Stop/debt) | master befab38 |
| **Hook reconcile** | **BL-13** dev-hook 3 dogfood bugs (doc-exempt, consume-once bypass, quoted-msg-safe) | dev |
| **Decisions** | ADR-006..013 (ทุกตัว panel 2/3 + dissent) | 07-decisions/ |
| **Rules locked** | MASTER FREEZE · DEV-DIRECT FREEZE · template-only mode · branch-per-feature | hooks + memory |

## 🔄 กำลังทำ (NOW)

| id | งาน | สถานะ | รออะไร |
|----|-----|-------|--------|
| **A7** | dogfood week บน repo จริง | day 2/7 | เวลา + usage (จบ 2026-06-17) |
| **BL-11** | fatigue-tuning (ลด rule noisy หลังเก็บ data) | รอ | A7 ครบสัปดาห์ |
| **M-A3** | panel verdict = ประกาศ G1 "ใช้ได้จริง" | รอ | A7 + BL-11 |

## 🟢 ทำต่อ (NEXT — actionable, ผลวิจัยที่ยังไม่ทำ)

| id | งาน | source (วิจัย) | กระทบ shipped? |
|----|-----|---------------|----------------|
| ~~DEV-FP~~ ✅ | forward-port enforcement → dev (merged ad5a8a9, panel 3/3) | dogfood divergence | done |
| ~~FU-2~~ ✅ | inbox file-lock/atomic (merged, panel 2/3, cross-process fix) | P0 re-review | done |
| ~~FU-1~~ ✅ | reject re-open flow (reopen_item + cli, audited, re-escalate fix) — panel 3/3 | P0 re-review | done |
| ~~FU-3~~ ✅ | approval scoping canonical key (ws+quote, case-safe) — panel 3/3, false-merge fixed | P0 re-review | done |
| **FU-6** | audit-log concurrency: append_event hash-chain fork ใต้ concurrent writes — **บังคับก่อน Phase B** | FU-2 panel | engine |
| ~~FU-4~~ ✅ | dangerous-git classifier (engine/gitguard): tokenized+quote-aware(shlex)+segmented+subcommand-parsed, fail-CLOSED hook. ปิด flag-order/refspec-force/ws/=value/branch-combo/quote-wrap/cross-cmd. panel round1 FAIL→fix→round2 3/3 | P0 re-review + FU-3 panel | done |
| **FU-5** | "was-configured" state กัน deletable testcmd | P1 re-review | engine |
| **RD-1** | **rule diet**: CLAUDE.md เหลือ ~12 กฎ HARD + รวม 2 CLAUDE.md ที่ซ้ำ 80% | compliance-decay (4-lens) | ⚠️ shipped template — ต้อง panel+user |
| **RD-2** | ยุบ Scenario A-O (15→4-5 ตัวจริง) | compliance-decay | ⚠️ shipped |
| **RD-3** | ย้าย TACP/vector-memory ออกจาก bootstrap read path | compliance-decay | ⚠️ shipped |
| **RD-4** | แยก C-codes: machine-checked (เป็น hook) vs advisory (เป็น reference) | compliance-decay | ⚠️ shipped |
| **OBS-1** | UserPromptSubmit re-inject obligations (สู้ recency decay) | compliance-decay (behavior lens) | hook |

> RD-1..4 = "reverse shipped behavior" (เหมือน carry-over เดิม) → ต้องผ่าน panel + คุณ approve ก่อนแตะ · DEV-FP/FU/OBS = engine/hook ทำบน feature branch ได้เลย

## ⏸️ พักไว้ (DEFERRED — ปลดเมื่อ M-A3 ผ่าน, กฎ BRD R3)

| id | งาน | เงื่อนไขปลด |
|----|-----|-----------|
| B1 | agent loop เต็ม (จาก spike → งาน arbitrary) | M-A3 + FU-2 |
| B2 | UI เต็ม (ต่อ vanilla, ไม่ rewrite SvelteKit) | M-A3 |
| B3 | model-picker UI | M-A3 |
| B4 | semantic memory (Qdrant) | dogfood พิสูจน์ lexical ไม่พอ |
| B5 | multi-repo live | ใช้จริง 2+ repos |
| B6 | specialists/multi-agent | B1 + FU-2 (inbox lock) |
| B7 | deploy/Docker | มีผู้ใช้คนที่ 2 |
| B8 | game profile pack | M-A3 |

## ❌ ทิ้ง (KILLED)
- **B9 team/collaboration** — ไม่มี user คนที่ 2 ในขอบฟ้า (panel consensus)

## 🔒 กฎที่ active (enforce ด้วย hook)
1. **MASTER FREEZE** — ห้ามแตะ master จนกว่าคุณสั่งปลดทางการ
2. **DEV-DIRECT FREEZE** — งานฟีเจอร์ → แตก feature branch (doc-only commit บน dev ได้)
3. **branch-per-feature** → merge → ลบ branch ทันที

---

## หมายเหตุ traceability
- ผลวิจัยเต็ม (votes+dissent ทุก panel) = `03-log/work-log-index.md` + panel transcripts
- backlog-v2 = **superseded** by this doc (เก็บไว้อ้างอิงประวัติ)
- ผลวิจัยที่เคย "ลอย" (compliance-decay ~24 ข้อ) ตอนนี้ = RD-1..4 + OBS-1 + DEV-FP (track ครบแล้ว)
