#!/usr/bin/env bash
# =============================================================================
# new-project.sh — Bootstrap a new project from ai-project-template
#
# Usage:
#   bash scripts/new-project.sh <PROJECT_NAME> <TARGET_DIR> [--game]
#
# Examples:
#   bash scripts/new-project.sh "ShopFlow" "../shopflow"
#   bash scripts/new-project.sh "HexGame"  "../hexgame" --game
#
# ต้องรันจาก project root ของ ai-project-template
# =============================================================================

set -euo pipefail

# ── Args ─────────────────────────────────────────────────────────────────────

if [ $# -lt 2 ]; then
  echo "Usage: bash scripts/new-project.sh <PROJECT_NAME> <TARGET_DIR> [--game]"
  exit 1
fi

PROJECT_NAME="$1"
TARGET="$2"
IS_GAME=0
GAME_PROJECT=false
if [ "${3:-}" = "--game" ]; then IS_GAME=1; GAME_PROJECT=true; fi

TEMPLATE_ROOT="$(pwd)"
DATE="$(date '+%Y-%m-%d')"
YEAR="$(date '+%Y')"
MONTH="$(date '+%m')"

# ── Guard ────────────────────────────────────────────────────────────────────

if [ ! -f "$TEMPLATE_ROOT/core/00-ai-bootstrap-master-template.md" ]; then
  echo "ERROR: รันจาก ai-project-template root เท่านั้น"
  exit 1
fi

if [ -d "$TARGET/CoreAiWorkspaces" ]; then
  echo "ERROR: $TARGET/CoreAiWorkspaces มีอยู่แล้ว — ไม่ overwrite"
  exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Bootstrap: $PROJECT_NAME"
echo "  Target:    $TARGET"
echo "  Type:      $([ $IS_GAME -eq 1 ] && echo 'game' || echo 'software')"
echo "  Date:      $DATE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Helper ───────────────────────────────────────────────────────────────────

make_file() {
  # make_file <path> <content>
  local path="$1"; shift
  mkdir -p "$(dirname "$path")"
  printf '%s\n' "$@" > "$path"
  echo "  created: $path"
}

sub() {
  # substitute PROJECT_NAME and DATE placeholders in template
  sed \
    -e "s/<PROJECT_NAME>/$PROJECT_NAME/g" \
    -e "s/<CURRENT_DATE>/$DATE/g" \
    -e "s/<YYYY-MM-DD>/$DATE/g" \
    -e "s/YYYY-MM-DD/$DATE/g" \
    -e "s/<CURRENT_SOURCE_VERSION>/v0.1/g" \
    "$1"
}

# ── 1. Create directory structure (core/01) ──────────────────────────────────

echo "[1/6] Creating directory structure..."

dirs=(
  "$TARGET/CoreAiWorkspaces/00-source/versions/v0.1"
  "$TARGET/CoreAiWorkspaces/01-plan"
  "$TARGET/CoreAiWorkspaces/02-task"
  "$TARGET/CoreAiWorkspaces/03-log"
  "$TARGET/CoreAiWorkspaces/04-way-of-work"
  "$TARGET/CoreAiWorkspaces/05-summary/$YEAR/$MONTH"
  "$TARGET/CoreAiWorkspaces/06-extensions"
  "$TARGET/CoreAiWorkspaces/07-decisions"
)
if [ $IS_GAME -eq 1 ]; then
  dirs+=("$TARGET/CoreAiWorkspaces/08-design")
fi

for d in "${dirs[@]}"; do
  mkdir -p "$d"
done
echo "  directories created"

# ── 2. CoreAiWorkspaces/README.md ─────────────────────────────────────────────────────────

echo "[2/6] Creating core files..."

TYPE_LABEL=$([ $IS_GAME -eq 1 ] && echo "game" || echo "software")
SKILLS_NOTE=$([ $IS_GAME -eq 1 ] && echo "Template version: ai-project-template (core 00–18 + skills/game 00–06)" || echo "Template version: ai-project-template (core 00–18)")
DESIGN_ROW=$([ $IS_GAME -eq 1 ] && echo "| \`08-design/\` | Feature Design Documents (FDD) — game-only |" || echo "")

make_file "$TARGET/CoreAiWorkspaces/README.md" \
"# CoreAiWorkspaces/ — $PROJECT_NAME

โครงสร้างเอกสารโปรเจ็กต์ $PROJECT_NAME (${TYPE_LABEL})
Bootstrap date: $DATE
$SKILLS_NOTE

| โฟลเดอร์ | เนื้อหา |
|----------|--------|
| \`00-source/\` | Source docs ต้นฉบับ versioned |
| \`01-plan/\` | Project plan + work status |
| \`02-task/\` | Task board |
| \`03-log/\` | Work log index |
| \`04-way-of-work/\` | Working agreements + protocols |
| \`05-summary/\` | Monthly summaries |
| \`06-extensions/\` | Extension docs |
| \`07-decisions/\` | ADR index + entity register |
$DESIGN_ROW"

# ── 3. Source docs placeholder ────────────────────────────────────────────────

make_file "$TARGET/CoreAiWorkspaces/00-source/README.md" \
"# Source Documents — $PROJECT_NAME

| Version | Date | Status | หมายเหตุ |
|---------|------|--------|---------|
| [v0.1](versions/v0.1/README.md) | $DATE | Active | initial version |

**กฎ:** ห้ามแก้ไขไฟล์ใน versions/ โดยตรง — ถ้า requirement เปลี่ยนให้สร้าง versions/v0.2/ แทน"

make_file "$TARGET/CoreAiWorkspaces/00-source/versions/v0.1/README.md" \
"# Source Documents v0.1 — $PROJECT_NAME

วางไฟล์ source docs ของโปรเจ็กต์ไว้ในโฟลเดอร์นี้

| ไฟล์ | เนื้อหา |
|------|--------|
| *(เพิ่มไฟล์ source doc ของโปรเจ็กต์ที่นี่)* | |

**กฎ:** ห้ามแก้ไฟล์ใน v0.1/ โดยตรง — ถ้า requirement เปลี่ยนให้สร้าง versions/v0.2/ แทน"

# ── 4. 01-plan/ ───────────────────────────────────────────────────────────────

make_file "$TARGET/CoreAiWorkspaces/01-plan/project-plan.md" \
"# Project Plan — $PROJECT_NAME

**Source:** CoreAiWorkspaces/00-source/versions/v0.1/
**Created:** $DATE

## Milestone 1 — <MILESTONE_NAME>

**Entry Gate:** <เงื่อนไขที่ต้องครบก่อนเริ่ม milestone นี้>
**Exit Gate:** <เงื่อนไขที่ต้องครบก่อนถือว่า milestone เสร็จ>

| Task | Status |
|------|--------|
| T-001: <FIRST_TASK> | todo |"

make_file "$TARGET/CoreAiWorkspaces/01-plan/work-status.md" \
"<!-- AI-CONTEXT
phase: bootstrap
active_task: none
blocker: none
last_updated: $DATE
read_more: []
-->

# Work Status — $PROJECT_NAME

อัปเดตล่าสุด: $DATE

## สถานะปัจจุบัน

**Phase:** bootstrap
**Active Task:** none — รอกรอก task แรก
**Blocker:** none

## Next Actions

1. เพิ่ม source docs ใน \`CoreAiWorkspaces/00-source/versions/v0.1/\`
2. กรอก project plan ใน \`CoreAiWorkspaces/01-plan/project-plan.md\`
3. สร้าง task แรกใน task board"

# ── 5. 02-task/ ───────────────────────────────────────────────────────────────

make_file "$TARGET/CoreAiWorkspaces/02-task/task-board.md" \
"<!-- AI-CONTEXT
total_tasks: 0
in_progress: []
blocked: []
done: []
last_updated: $DATE
-->

# Task Board — $PROJECT_NAME

## In Progress

*(ยังไม่มี task)*

## Todo

*(เพิ่ม task หลังจากมี source docs แล้ว)*

## Done

*(ยังไม่มี)*"

# ── 6. 03-log/ ────────────────────────────────────────────────────────────────

make_file "$TARGET/CoreAiWorkspaces/03-log/work-log-index.md" \
"<!-- AI-CONTEXT
last_session: $DATE
tool: Claude Code
completed: []
checkpoint: none
next_from_last: none
notes: bootstrap session
deep_context: none
-->

# Work Log Index — $PROJECT_NAME

## Milestone Summary

*(ยังไม่มี milestone เสร็จ — โปรเจ็กต์เพิ่งเริ่ม)*

## Recent Sessions

### $DATE — [Bootstrap]

**สิ่งที่ทำ:**
- Bootstrap project structure จาก ai-project-template
- สร้าง CoreAiWorkspaces/ โครงสร้างทั้งหมด
- Next: เพิ่ม source docs และ task แรก"

# ── 7. 04-way-of-work/ ────────────────────────────────────────────────────────

make_file "$TARGET/CoreAiWorkspaces/04-way-of-work/way-of-work.md" \
"# Way of Work — $PROJECT_NAME

## ภาษา

- สื่อสารกัน: <ระบุภาษา — กรอกตอน session แรก>
- Code / identifiers / comments: English

## Project Type

$TYPE_LABEL

## Session Protocol

ใช้ ai-project-template session protocol
- Session Start: อ่าน AI-CONTEXT block ของ work-status + log-index + task-board
- Session End: รัน /session-end หรือ Session End Protocol ด้วยมือ

## Compliance Status

สถานะ: active"

# ai-decision-protocol: copy from core/11, strip template meta-header, set project title
{
  echo "# AI Decision Protocol — $PROJECT_NAME"
  echo ""
  # skip first 4 lines (template title + description + "นำไปวางใน..." + blank)
  tail -n +5 "$TEMPLATE_ROOT/core/11-ai-decision-protocol-template.md" \
    | sed \
        -e "s/<PROJECT_NAME>/$PROJECT_NAME/g" \
        -e "s/<CURRENT_DATE>/$DATE/g"
} > "$TARGET/CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md"
echo "  created: $TARGET/CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md (from core/11)"

# compliance: copy from core/15, strip template meta-header, strip fictional example data
{
  echo "# Compliance — $PROJECT_NAME"
  echo ""
  # skip first line (template title), strip fictional example rows in Tech Debt Register
  tail -n +2 "$TEMPLATE_ROOT/core/15-compliance-check-template.md" \
    | sed \
        -e "s/<PROJECT_NAME>/$PROJECT_NAME/g" \
        -e "s/<CURRENT_DATE>/$DATE/g" \
        -e '/src\/game\/player\.ts/d' \
        -e '/src\/enemy\/ai\.ts/d'
} > "$TARGET/CoreAiWorkspaces/04-way-of-work/compliance.md"
echo "  created: $TARGET/CoreAiWorkspaces/04-way-of-work/compliance.md (from core/15)"

make_file "$TARGET/CoreAiWorkspaces/04-way-of-work/coding-standards.md" \
"# Coding Standards — $PROJECT_NAME

นำมาจาก core/04-coding-standards-template.md
ปรับตามโปรเจ็กต์ได้ในส่วน Project-Specific ด้านล่าง

## Core Standards

- ทุก function ≤ 50 บรรทัด (C-05)
- ไฟล์ > 500 บรรทัด → แตกไฟล์ (C-01)
- ห้าม magic numbers — ทุกค่าต้องอยู่ใน config/constant
- dependency ใหม่ต้องมี ADR (C-06)

## Project-Specific

*(เพิ่มกฎเฉพาะโปรเจ็กต์ที่นี่)*"

# ── 8. 03-log/ README + templates/ ───────────────────────────────────────────

make_file "$TARGET/CoreAiWorkspaces/03-log/README.md" \
"# Log — $PROJECT_NAME

| ไฟล์/โฟลเดอร์ | เนื้อหา |
|----------------|--------|
| \`work-log-index.md\` | index ของทุก session (AI อ่านทุกครั้ง) |
| \`templates/\` | template สำหรับ daily log |
| \`YYYY/MM/\` | daily log files (optional, local-only) |
| \`agents/\` | AI tool diaries — สร้างเมื่อใช้ AI มากกว่า 1 ตัว |"

mkdir -p "$TARGET/CoreAiWorkspaces/03-log/templates"
make_file "$TARGET/CoreAiWorkspaces/03-log/templates/daily-log-template.md" \
"# Daily Log — $DATE

**Task ที่ทำ:** T-XXX
**เวลา:** HH:MM — HH:MM

## สิ่งที่ทำ

- ...

## สิ่งที่ยังค้าง

- ...

## Decision / Note สำคัญ

- ..."

# 05-summary/ + 06-extensions/ placeholder files

make_file "$TARGET/CoreAiWorkspaces/05-summary/README.md" \
"# Summaries — $PROJECT_NAME

Monthly summaries เก็บใน \`YYYY/MM/\`
ใช้ template จาก \`templates.md\`"

make_file "$TARGET/CoreAiWorkspaces/05-summary/templates.md" \
"# Summary Templates — $PROJECT_NAME

## Monthly Summary Template

\`\`\`md
# Summary — YYYY-MM

**Period:** YYYY-MM-01 to YYYY-MM-DD
**Tasks completed:** T-XXX, T-XXX
**Milestones reached:** ...

## ภาพรวม

...

## Lessons / Decisions

...
\`\`\`"

make_file "$TARGET/CoreAiWorkspaces/06-extensions/README.md" \
"# Extension Docs — $PROJECT_NAME

Extension docs ใช้เพื่อขยาย requirement โดยไม่แก้ source docs ต้นฉบับ

| ไฟล์ | เนื้อหา |
|------|--------|
| *(เพิ่มเมื่อมี requirement เพิ่มเติม)* | |"

make_file "$TARGET/CoreAiWorkspaces/06-extensions/extension-template.md" \
"# Extension: <EXTENSION_TITLE>

**วันที่:** $DATE
**Source Reference:** CoreAiWorkspaces/00-source/versions/v0.1/<filename>.md §<section>
**Related Tasks:** T-XXX
**Author:** <ชื่อ>

## เหตุผลที่สร้าง Extension

อธิบายว่าทำไมถึงต้องเพิ่มเติม และ source doc เดิมไม่ครอบคลุมส่วนไหน

## เนื้อหา Extension

...

## ข้อจำกัด

Extension นี้ใช้ได้จนกว่า source doc จะถูก update เป็น version ใหม่"

# ── 9. 07-decisions/ ──────────────────────────────────────────────────────────

# ADR index — write live content directly (not copy meta-template instructions)
mkdir -p "$TARGET/CoreAiWorkspaces/07-decisions"
cat > "$TARGET/CoreAiWorkspaces/07-decisions/README.md" <<EOF
<!-- AI-CONTEXT
total_adrs: 0
accepted: []
proposed: []
last_updated: $DATE
-->

# Decision Log — $PROJECT_NAME

บันทึก architectural decisions ทั้งหมดของโปรเจ็กต์
ADR ที่ถูก accept แล้วถือเป็น source of truth สำหรับทิศทาง technical

## กฎการใช้งาน

- AI ทุก session ต้องอ่าน index นี้ก่อนทำการตัดสินใจเชิง architecture
- ห้ามลบ ADR — เปลี่ยนสถานะเป็น Deprecated หรือ Superseded แทน
- AI สามารถสร้าง ADR ในสถานะ Proposed ได้ — มนุษย์เป็นผู้ Approve

## Status ที่ใช้ได้

| Status | ความหมาย |
|--------|----------|
| Proposed | เสนอโดย AI หรือทีม รอการ approve |
| Accepted | ตัดสินใจแล้ว ใช้เป็นแนวทาง |
| Deprecated | ไม่ใช้แล้ว แต่ยังมีประวัติ |
| Superseded | ถูกแทนที่โดย ADR อื่น |

## Decision Log

| ID | Title | Status | Date | Supersedes |
|----|-------|--------|------|------------|
| *(ยังไม่มี ADR — สร้างด้วย /adr-create)* | | | | |
EOF
echo "  created: $TARGET/CoreAiWorkspaces/07-decisions/README.md (live ADR index)"

# entity-register — write live content directly (not extract from meta-template)
cat > "$TARGET/CoreAiWorkspaces/07-decisions/entity-register.md" <<EOF
<!-- AI-CONTEXT
entities_active: []
entities_deprecated: []
last_updated: $DATE
-->

# Entity Register — $PROJECT_NAME

อัปเดตล่าสุด: $DATE

## Active Entities

| Entity | Type | Status | Since | ADR | Notes |
|--------|------|--------|-------|-----|-------|
| *(เพิ่มเมื่อมี tech/integration ใหม่ — รัน /adr-create แล้วอัปเดตที่นี่)* | | | | | |

## Deprecated / Removed Entities

| Entity | Type | Status | Since | Until | ADR | Replaced By |
|--------|------|--------|-------|-------|-----|-------------|
| *(ยังไม่มี)* | | | | | | |
EOF
echo "  created: $TARGET/CoreAiWorkspaces/07-decisions/entity-register.md (live entity register)"

# ── 9. Game-only: 08-design/ ──────────────────────────────────────────────────

if [ $IS_GAME -eq 1 ]; then
  echo "[3/6] Creating game-specific files (skills/game/)..."

  make_file "$TARGET/CoreAiWorkspaces/08-design/README.md" \
"# Design Documents — $PROJECT_NAME

Index ของ Feature Design Documents ทั้งหมด

| FDD | Feature | Status | Task |
|-----|---------|--------|------|
| *(สร้าง FDD แรกด้วย /fdd-create)* | | | |

**กฎ:** ทุก feature ใหม่ต้องมี FDD ที่ Approved ก่อน task จะออกจาก design_validate"

  make_file "$TARGET/CoreAiWorkspaces/08-design/asset-registry.md" \
"<!-- AI-CONTEXT
total_assets: 0
last_updated: $DATE
-->

# Asset Registry — $PROJECT_NAME

| Asset | Type | Path | Status | FDD |
|-------|------|------|--------|-----|
| *(เพิ่ม asset เมื่อมีใน FDD)* | | | | |

**กฎ:** ทุก asset ต้องตั้งชื่อตาม naming convention ใน \`skills/game/03-asset-protocol.md\`"

fi

# ── 10. Install platform files ────────────────────────────────────────────────

echo "[$([ $IS_GAME -eq 1 ] && echo '3' || echo '3')/6] Installing platform files..."

# Install slash commands
mkdir -p "$TARGET/.claude/commands"
cp "$TEMPLATE_ROOT/platforms/claude-code/skills/"*.md "$TARGET/.claude/commands/" 2>/dev/null || true
echo "  installed: .claude/commands/ (slash commands)"

# Install agents (game projects get game agents; all projects get base agents)
mkdir -p "$TARGET/.claude/agents"
if [ "$GAME_PROJECT" = true ]; then
  cp "$TEMPLATE_ROOT/platforms/claude-code/agents/"*.md "$TARGET/.claude/agents/" 2>/dev/null || true
  echo "  installed: .claude/agents/ (game agents)"
fi

# Install git hooks (only if .git exists in target)
if [ -d "$TARGET/.git" ]; then
  cp "$TEMPLATE_ROOT/platforms/claude-code/hooks/validate-commit.sh" "$TARGET/.git/hooks/validate-commit" 2>/dev/null || true
  chmod +x "$TARGET/.git/hooks/validate-commit" 2>/dev/null || true
  echo "  installed: .git/hooks/validate-commit"
fi

# Copy CLAUDE.md to root
cp "$TEMPLATE_ROOT/platforms/claude-code/CLAUDE.md" "$TARGET/CLAUDE.md"
echo "  installed: CLAUDE.md → root"

# ── 11. Summary ───────────────────────────────────────────────────────────────

echo ""
echo "[$([ $IS_GAME -eq 1 ] && echo '5' || echo '4')/6] Verifying output..."

REQUIRED=(
  "CoreAiWorkspaces/README.md"
  "CoreAiWorkspaces/00-source/README.md"
  "CoreAiWorkspaces/00-source/versions/v0.1/README.md"
  "CoreAiWorkspaces/01-plan/project-plan.md"
  "CoreAiWorkspaces/01-plan/work-status.md"
  "CoreAiWorkspaces/02-task/task-board.md"
  "CoreAiWorkspaces/03-log/README.md"
  "CoreAiWorkspaces/03-log/work-log-index.md"
  "CoreAiWorkspaces/03-log/templates/daily-log-template.md"
  "CoreAiWorkspaces/04-way-of-work/way-of-work.md"
  "CoreAiWorkspaces/04-way-of-work/coding-standards.md"
  "CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md"
  "CoreAiWorkspaces/04-way-of-work/compliance.md"
  "CoreAiWorkspaces/05-summary/README.md"
  "CoreAiWorkspaces/05-summary/templates.md"
  "CoreAiWorkspaces/06-extensions/README.md"
  "CoreAiWorkspaces/06-extensions/extension-template.md"
  "CoreAiWorkspaces/07-decisions/README.md"
  "CoreAiWorkspaces/07-decisions/entity-register.md"
)
if [ $IS_GAME -eq 1 ]; then
  REQUIRED+=("CoreAiWorkspaces/08-design/README.md" "CoreAiWorkspaces/08-design/asset-registry.md")
fi

MISSING=0
for f in "${REQUIRED[@]}"; do
  if [ ! -f "$TARGET/$f" ]; then
    echo "  MISSING: $f"
    MISSING=$((MISSING+1))
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "  All required files present ✓"
else
  echo "  ERROR: $MISSING required file(s) missing"
  exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Bootstrap complete: $PROJECT_NAME"
echo "  Path: $TARGET/CoreAiWorkspaces/"
echo ""
echo "  Next steps:"
echo "  1. เพิ่ม source docs ใน CoreAiWorkspaces/00-source/versions/v0.1/"
echo "  2. กรอก project-plan.md"
if [ $IS_GAME -eq 1 ]; then
  echo "  3. รัน /fdd-create เพื่อสร้าง FDD แรก"
else
  echo "  3. สร้าง task แรกใน task-board.md"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
