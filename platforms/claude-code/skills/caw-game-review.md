# /caw-game-review

รัน milestone gate review สำหรับ game project โดยเรียก specialist agents ที่เกี่ยวข้อง

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

### 1. Pre-flight Check (ก่อน invoke agents)

ตรวจสิ่งต่อไปนี้ก่อนส่งให้ agent:
- FDD มีอยู่ใน `CoreAiWorkspaces/08-design/` สำหรับทุก feature ที่ in_progress
- GDD อยู่ที่ `CoreAiWorkspaces/00-source/versions/v0.1/gdd.md`
- Art bible มีอยู่ที่ `CoreAiWorkspaces/08-design/art-bible.md`
- Character registry มีอยู่ที่ `CoreAiWorkspaces/08-design/character-registry.md` (ถ้ามี narrative)

ถ้าไฟล์ใดขาด → รายงานให้ผู้ใช้ทราบก่อนดำเนินการ review

### 2. Run Specialist Gates

invoke แต่ละ agent ตาม flag ที่ระบุ (default: ทั้งหมด):

| Agent | Gate Code | Focus |
|-------|-----------|-------|
| `game-designer` | `[GATE-DESIGN]` | mechanic vs. GDD pillar alignment, degenerate strategies |
| `game-art-director` | `[GATE-ART]` | asset consistency, palette compliance, VFX budget |
| `game-narrative-director` | `[GATE-NARRATIVE]` | character voice, string compliance, ludonarrative |
| `game-ux-designer` | `[GATE-UX]` | screen flow, input completeness, FTUX |
| `game-performance-analyst` | `[GATE-PERF]` | frame budget, draw calls, memory patterns |

### 3. Aggregate Report

ออก report รวมในรูปแบบ:

```
# Game Review — [Feature/Milestone Name]
Date: YYYY-MM-DD

## Gate Summary
| Gate | Verdict | Critical Issues |
|------|---------|----------------|
| DESIGN | APPROVE / CONCERNS / REJECT | [count] |
| ART | APPROVE / CONCERNS / REJECT | [count] |
| NARRATIVE | APPROVE / CONCERNS / REJECT | [count] |
| UX | APPROVE / CONCERNS / REJECT | [count] |
| PERF | APPROVE / CONCERNS / REJECT | [count] |

## Overall: APPROVE / CONCERNS / REJECT

## Issues by Priority

### 🔴 CRITICAL (block release)
[specific issues from any gate]

### 🟡 CONCERNS (fix before next milestone)
[specific issues from any gate]

### 🟢 NOTES (optional improvements)
[specific suggestions]

## Next Steps
[numbered action items]
```

### 4. Task Creation

สำหรับทุก CRITICAL และ CONCERNS issue:
- ถามผู้ใช้ว่าจะสร้าง task ใน `CoreAiWorkspaces/02-task/task-board.md` ไหม
- ถ้าใช่ → สร้าง task entries พร้อม compliance code tag

## Compliance Codes Checked

รวม compliance codes จากทุก specialist:
- Core: C-01 ถึง C-14
- Game design: G-04, G-08, G-09, G-10
- Asset: A-01 ถึง A-07
- Narrative: N-01 ถึง N-04
- UX: U-01 ถึง U-03
- Level design: L-01, L-02

## หมายเหตุ

- review ต้องได้รับ **APPROVE ทุก gate** ก่อน feature จะออกจาก `playtest` → `review`
- CONCERNS = ผ่านได้แต่ต้องมี task สำหรับ fix ก่อน milestone ถัดไป
- REJECT = block: ต้องแก้และ re-review ก่อนดำเนินการต่อ
