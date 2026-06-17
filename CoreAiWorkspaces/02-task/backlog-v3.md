<!-- AI-CONTEXT
doc: backlog-v3 (SINGLE ACTIVE ROADMAP — supersedes backlog-v2)
updated: 2026-06-12
rule: นี่คือที่เดียวที่ track ทุกอย่าง — ผลวิจัย/panel ทุกรอบถูกแปลงเป็น item ที่มี id+status+source แล้ว
status_legend: ✅done · 🔄now · 🟢next · ⏸️deferred(มี gate) · ❌killed
now: [BL-11-counters]  # G1-SELF LOCKED 2026-06-17 (M-A3 3/3 PASS_CONDITIONAL, user Option A). A7 self-dogfood DONE; A7-literal 2nd-project = B-entry cond
done_recent: [DEV-FP]
done_recent: [DEV-FP, FU-1..8, OBS-1, RD-1..4] — tracked backlog ว่างหมด
next: [] — เหลือแต่ที่รอเวลา/รอ user: A7 dogfood(ถึง 2026-06-17), M-A3 verdict, deferred Option-D gates(user), FU-7b log-rotation, B*(M-A3)
rd_status: DONE 2026-06-16 — RD-1..4 dedup merged (no new gates). deferred-by-user: Option-D gates (adr-proposed, scope-change, risk-tier-dispatch) รอวัดผล token/compliance ก่อนตัดสิน
phase_b_prereqs: CLEARED (FU-2 inbox-lock + FU-6 audit-lock + FU-7 lasthash-cache + FU-8 state-atomic) — เหลือ FU-7b log-rotation (bound worst-case) ก่อน sustained Phase-B write
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
| ~~A7~~ ✅(self) | dogfood week บน **repo นี้** ครบ 7/7 (2026-06-10..17): 90 commits, 34/34 suites, 6 sessions auto-logged, 3 risky-git holds, hooks end-to-end | self-dogfood DONE | A7-literal "+1 โปรเจ็กต์จริง" → ⏸️ B-entry cond |
| ~~M-A3~~ ✅ | panel verdict **3/3 PASS_CONDITIONAL** → **G1-SELF LOCKED 2026-06-17** (user Option A). ขอบเขต = BRD-v2 §2 (repo นี้, ไม่ป้อนมือ). ห้าม inflate เป็น A7-DONE/public claim | LOCKED | — |
| **BL-11** | ✅verdict=CONFIRM CALIBRATED (no threshold change). action = **bypass-path counters (observability)** | 🔄 building (feature branch, user-approved) | panel review |

> **G1-SELF lock note:** panel จับ caveat ตรง — DI-0001..3 = synthetic gitguard self-test probes (ไม่ใช่ organic risky op) + ยัง OPEN → approve→execute loop ยังไม่ปิด. ⇒ A7-literal 2nd-project + cloud-path + ≥1 organic hold + 1 end-to-end inbox-approve = **B-entry conditions** (encoded ใน B5/B7), **ไม่ใช่ G1 blocker**. Phase-B ยังไม่ปลดทั้งก้อน — G1 authorize เฉพาะ item ที่ prereq เคลียร์เอง (FU-2/6/7/8 done).

## 🟢 ทำต่อ (NEXT — actionable, ผลวิจัยที่ยังไม่ทำ)

| id | งาน | source (วิจัย) | กระทบ shipped? |
|----|-----|---------------|----------------|
| ~~DEV-FP~~ ✅ | forward-port enforcement → dev (merged ad5a8a9, panel 3/3) | dogfood divergence | done |
| ~~FU-2~~ ✅ | inbox file-lock/atomic (merged, panel 2/3, cross-process fix) | P0 re-review | done |
| ~~FU-1~~ ✅ | reject re-open flow (reopen_item + cli, audited, re-escalate fix) — panel 3/3 | P0 re-review | done |
| ~~FU-3~~ ✅ | approval scoping canonical key (ws+quote, case-safe) — panel 3/3, false-merge fixed | P0 re-review | done |
| ~~FU-6~~ ✅ | audit-log concurrency: append_event ครอบ _FileLock + fsync + torn-tail self-heal — ปิด hash-chain fork. panel 3/3. **Phase B audit prereq เคลียร์** | FU-2 panel | done |
| ~~FU-7~~ ✅ | append_event O(n²) → in-process last-hash cache (size+mtime key; external write=miss→FU-6 read+heal). panel 3/3 | FU-6 panel | done |
| **FU-7b** | log rotation (bound worst-case miss-path read; multi-segment verify_chain) — ก่อน sustained Phase-B | FU-7 panel | engine (deferred) |
| ~~FU-8~~ ✅ | store.save/writeback atomic+serialized (tmp+fsync+os.replace, store ล็อก) — ปิด torn/last-writer-wins. panel 3/3 | FU-6 panel | done |
| ~~FU-4~~ ✅ | dangerous-git classifier (engine/gitguard): tokenized+quote-aware(shlex)+segmented+subcommand-parsed, fail-CLOSED hook. ปิด flag-order/refspec-force/ws/=value/branch-combo/quote-wrap/cross-cmd. panel round1 FAIL→fix→round2 3/3 | P0 re-review + FU-3 panel | done |
| ~~FU-5~~ ✅ | was-configured sticky marker + commit-deletion guard (ลบ testcmd หลังตั้ง=fail-closed regression; commit ลบ=blocked; de-config ต้อง bypass=auditable) — panel 3/3 | P1 re-review | done |
| ~~RD-1~~ ✅ | merge 2 CLAUDE.md → root stub + platforms canonical (kill ~80% dup, ครบ 14 กฎ, deploy-safe) — panel 2 rounds | compliance-decay (4-lens) | done |
| ~~RD-2~~ ✅ | scenarios 298→238 (ยุบ A-G/I เป็น legend, เก็บ anchor ครบ; H/J/K/L full) — grep พิสูจน์ 12/15 ถูก ref → ลบไม่ได้ — panel 3/3 | compliance-decay | done |
| ~~RD-3~~ ✅ | ย้าย TACP/vector-memory ออกจาก bootstrap read path — panel 3/3 | compliance-decay | done |
| ~~RD-4~~ ✅ | C-codes machine-vs-advisory split (Enforce column, verified vs yaml) — panel round1 FAIL→round2 3/3 | compliance-decay | done |
| ~~OBS-1~~ ✅ | UserPromptSubmit re-inject obligations (freezes/inbox/regression/branch ทุก turn) + แก้ init_repo ไม่ ship gitguard.py/obligations.py — panel 3/3 | compliance-decay (behavior lens) | done |

> RD-1..4 = "reverse shipped behavior" (เหมือน carry-over เดิม) → ต้องผ่าน panel + คุณ approve ก่อนแตะ · DEV-FP/FU/OBS = engine/hook ทำบน feature branch ได้เลย

## ⏸️ พักไว้ (DEFERRED — ปลดเมื่อ M-A3 ผ่าน, กฎ BRD R3)

| id | งาน | เงื่อนไขปลด |
|----|-----|-----------|
| B1 | agent loop เต็ม (จาก spike → งาน arbitrary) | M-A3 + FU-2 |
| B2 | UI เต็ม (ต่อ vanilla, ไม่ rewrite SvelteKit) | M-A3 |
| B3 | model-picker UI | M-A3 |
| B4 | semantic memory (Qdrant) | dogfood พิสูจน์ lexical ไม่พอ |
| B5 | multi-repo live | ใช้จริง 2+ repos |
| B6 | specialists/multi-agent | B1 + FU-2 + FU-6 (audit-lock) ✓ prereqs เคลียร์ |
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
