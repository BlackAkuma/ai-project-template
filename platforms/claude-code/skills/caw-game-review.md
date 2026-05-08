<!-- AI-CONTEXT
cmd: caw-game-review
requires: CoreAiWorkspaces/08-design/ (game projects only)
flags: [--design, --art, --narrative, --ux, --performance, feature_path]
steps: [preflight_check_docs, invoke_specialist_agents_per_flag, aggregate_report, create_tasks_for_critical_concerns]
agents: [game-designer, game-art-director, game-narrative-director, game-ux-designer, game-performance-analyst]
verdicts: [APPROVE, CONCERNS, REJECT]
rule: all_gates_APPROVE_before_playtest_to_review | CONCERNS_needs_task | REJECT_blocks
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-game-review

รัน milestone gate review สำหรับ game project โดยเรียก specialist agents ที่เกี่ยวข้อง
-->

## วิธีใช้

```
/caw-game-review                    ← full review (design + art + narrative + ux + performance)
/caw-game-review --design           ← เฉพาะ game-designer gate
/caw-game-review --art              ← เฉพาะ game-art-director gate
/caw-game-review --narrative        ← เฉพาะ game-narrative-director gate
/caw-game-review --ux               ← เฉพาะ game-ux-designer gate
/caw-game-review --performance      ← เฉพาะ game-performance-analyst gate
/caw-game-review feature/jump       ← review เฉพาะ feature ที่ระบุ
```

## สิ่งที่ทำ

### 1. Pre-flight Check

ตรวจก่อนส่งให้ agent:
- FDD มีอยู่ใน `CoreAiWorkspaces/08-design/` สำหรับทุก feature ที่ in_progress
- GDD อยู่ที่ `CoreAiWorkspaces/00-source/versions/v0.1/gdd.md`
- Art bible มีอยู่ที่ `CoreAiWorkspaces/08-design/art-bible.md`

### 2. Specialist Gates

| Agent | Gate Code | Focus |
|-------|-----------|-------|
| `game-designer` | `[GATE-DESIGN]` | mechanic vs. GDD pillar, degenerate strategies |
| `game-art-director` | `[GATE-ART]` | asset consistency, palette, VFX budget |
| `game-narrative-director` | `[GATE-NARRATIVE]` | character voice, string compliance |
| `game-ux-designer` | `[GATE-UX]` | screen flow, input completeness, FTUX |
| `game-performance-analyst` | `[GATE-PERF]` | frame budget, draw calls, memory |

### 3. Output Format

```
# Game Review — [Feature/Milestone]
Date: YYYY-MM-DD

| Gate | Verdict | Critical Issues |
|------|---------|----------------|
| DESIGN | APPROVE / CONCERNS / REJECT | [count] |
...

## Overall: APPROVE / CONCERNS / REJECT

### 🔴 CRITICAL (block release)
### 🟡 CONCERNS (fix before next milestone)
### 🟢 NOTES (optional)
```

### 4. Task Creation

สำหรับทุก CRITICAL และ CONCERNS — ถามว่าจะสร้าง task ใน task-board ไหม

## กฎ

- ทุก gate APPROVE → ผ่าน
- CONCERNS → ผ่านได้ แต่ต้องมี task สำหรับ fix ก่อน milestone ถัดไป
- REJECT → block — ต้องแก้และ re-review
