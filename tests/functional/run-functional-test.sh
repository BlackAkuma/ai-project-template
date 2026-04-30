#!/usr/bin/env bash
# =============================================================================
# run-functional-test.sh — Functional Bootstrap Test
# ทดสอบว่าการ bootstrap project จาก template ทำงานได้จริง
# รันจาก project root: bash tests/functional/run-functional-test.sh
# =============================================================================

set -euo pipefail

PASS=0; FAIL=0
FAIL_LIST=()

pass() { echo "[PASS] $1"; PASS=$((PASS+1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL+1)); FAIL_LIST+=("$1"); }
header() { echo ""; echo "══════════════════════════════════════════"; echo "  $1"; echo "══════════════════════════════════════════"; }

assert_file() {
  local desc="$1" file="$2"
  [ -f "$file" ] && pass "$desc" || fail "$desc — missing: $file"
}

assert_dir() {
  local desc="$1" dir="$2"
  [ -d "$dir" ] && pass "$desc" || fail "$desc — missing dir: $dir"
}

assert_grep() {
  local desc="$1" pattern="$2" file="$3"
  if grep -qE "$pattern" "$file" 2>/dev/null; then
    pass "$desc"
  else
    fail "$desc — pattern '$pattern' not found in $file"
  fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Functional Bootstrap Test"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# =============================================================================
header "P1: ShopFlow — Software Project Bootstrap"
# =============================================================================

BASE="tests/functional/shopflow"

# P1-1: doc/ structure
assert_dir  "P1-1: doc/ exists"           "$BASE/doc"
assert_dir  "P1-2: doc/00-source/ exists" "$BASE/doc/00-source"
assert_dir  "P1-3: doc/01-plan/ exists"   "$BASE/doc/01-plan"
assert_dir  "P1-4: doc/02-task/ exists"   "$BASE/doc/02-task"
assert_dir  "P1-5: doc/03-log/ exists"    "$BASE/doc/03-log"
assert_dir  "P1-6: doc/04-way-of-work/ exists" "$BASE/doc/04-way-of-work"
assert_dir  "P1-7: doc/07-decisions/ exists"   "$BASE/doc/07-decisions"

# P1-8: no doc/08-design (not a game project)
if [ ! -d "$BASE/doc/08-design" ]; then
  pass "P1-8: no doc/08-design (correct — software project)"
else
  fail "P1-8: doc/08-design exists in software project — should not be here"
fi

# P1-9: required files
assert_file "P1-9:  work-status.md"         "$BASE/doc/01-plan/work-status.md"
assert_file "P1-10: task-board.md"          "$BASE/doc/02-task/task-board.md"
assert_file "P1-11: work-log-index.md"      "$BASE/doc/03-log/work-log-index.md"
assert_file "P1-12: way-of-work.md"         "$BASE/doc/04-way-of-work/way-of-work.md"
assert_file "P1-13: ai-decision-protocol.md" "$BASE/doc/04-way-of-work/ai-decision-protocol.md"
assert_file "P1-14: ADR index README.md"    "$BASE/doc/07-decisions/README.md"
assert_file "P1-15: entity-register.md"     "$BASE/doc/07-decisions/entity-register.md"
assert_file "P1-16: source requirements"    "$BASE/doc/00-source/versions/v0.1/product-requirements.md"

# P1-17: AI-CONTEXT blocks present
assert_grep "P1-17: work-status has AI-CONTEXT block"  "AI-CONTEXT" "$BASE/doc/01-plan/work-status.md"
assert_grep "P1-18: task-board has AI-CONTEXT block"   "AI-CONTEXT" "$BASE/doc/02-task/task-board.md"
assert_grep "P1-19: work-log has AI-CONTEXT block"     "AI-CONTEXT" "$BASE/doc/03-log/work-log-index.md"
assert_grep "P1-20: entity-register has AI-CONTEXT"    "AI-CONTEXT" "$BASE/doc/07-decisions/entity-register.md"

# P1-21: task board has source references
assert_grep "P1-21: tasks reference source docs"  "v0.1" "$BASE/doc/02-task/task-board.md"

# P1-22: ADR exists and linked from index
assert_file "P1-22: ADR-001 file exists"    "$BASE/doc/07-decisions/ADR-001-nextjs-frontend.md"
assert_grep "P1-23: ADR-001 linked in index" "ADR-001" "$BASE/doc/07-decisions/README.md"
assert_grep "P1-24: ADR-001 has Context"     "Context"  "$BASE/doc/07-decisions/ADR-001-nextjs-frontend.md"
assert_grep "P1-25: ADR-001 has status Accepted" "Accepted" "$BASE/doc/07-decisions/ADR-001-nextjs-frontend.md"

# P1-26: entity-register has active entities
assert_grep "P1-26: entity-register has Next.js"  "Next.js" "$BASE/doc/07-decisions/entity-register.md"
assert_grep "P1-27: entity-register has ADR ref"  "ADR-"    "$BASE/doc/07-decisions/entity-register.md"

# P1-28: decision protocol has all 11 scenarios
assert_grep "P1-28: protocol has Scenario H" "Scenario H" "$BASE/doc/04-way-of-work/ai-decision-protocol.md"
assert_grep "P1-29: protocol has Scenario J" "Scenario J" "$BASE/doc/04-way-of-work/ai-decision-protocol.md"
assert_grep "P1-30: protocol has Scenario K" "Scenario K" "$BASE/doc/04-way-of-work/ai-decision-protocol.md"

# =============================================================================
header "P2: HexGame — Game Project Bootstrap"
# =============================================================================

BASE="tests/functional/hexgame"

# P2-1: core structure
assert_dir "P2-1: doc/ exists"           "$BASE/doc"
assert_dir "P2-2: doc/08-design/ exists" "$BASE/doc/08-design"

# P2-3: game-specific files
assert_file "P2-3: doc/08-design/README.md"         "$BASE/doc/08-design/README.md"
assert_file "P2-4: FDD-001 movement-system.md"       "$BASE/doc/08-design/movement-system.md"
assert_file "P2-5: work-status.md"                   "$BASE/doc/01-plan/work-status.md"
assert_file "P2-6: task-board.md"                    "$BASE/doc/02-task/task-board.md"
assert_file "P2-7: entity-register.md"               "$BASE/doc/07-decisions/entity-register.md"

# P2-8: FDD structure (sections 1–8)
assert_grep "P2-8:  FDD has section 1"  "ส่วนที่ 1"  "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-9:  FDD has section 2"  "ส่วนที่ 2"  "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-10: FDD has section 4"  "ส่วนที่ 4"  "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-11: FDD has section 8"  "ส่วนที่ 8"  "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-12: FDD has MDA table"  "Mechanics"   "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-13: FDD has Dynamics"   "Dynamics"    "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-14: FDD has Aesthetics" "Aesthetics"  "$BASE/doc/08-design/movement-system.md"

# P2-15: FDD status Approved
assert_grep "P2-15: FDD is Approved" "Approved" "$BASE/doc/08-design/movement-system.md"

# P2-16: config values (no hardcoded magic numbers — all have config: reference)
assert_grep "P2-16: FDD section 4 has config references" "config:" "$BASE/doc/08-design/movement-system.md"
assert_grep "P2-17: FDD has range defined"               "range:"  "$BASE/doc/08-design/movement-system.md"

# P2-18: task lifecycle
assert_grep "P2-18: task board has playtest lifecycle"   "playtest"        "$BASE/doc/02-task/task-board.md"
assert_grep "P2-19: task board references FDD"           "FDD-"            "$BASE/doc/02-task/task-board.md"
assert_grep "P2-20: work-status has read_more"           "read_more"       "$BASE/doc/01-plan/work-status.md"
assert_grep "P2-21: work-status read_more includes FDD"  "08-design"       "$BASE/doc/01-plan/work-status.md"

# P2-22: entity-register for game
assert_grep "P2-22: entity-register has Phaser"  "Phaser" "$BASE/doc/07-decisions/entity-register.md"
assert_grep "P2-23: entity-register has AI-CONTEXT" "AI-CONTEXT" "$BASE/doc/07-decisions/entity-register.md"

# =============================================================================
header "P3: Cross-Check — Template Consistency"
# =============================================================================

# P3-1: both projects use same AI-CONTEXT block format
assert_grep "P3-1: shopflow work-status has phase field"    "phase:"        "tests/functional/shopflow/doc/01-plan/work-status.md"
assert_grep "P3-2: hexgame work-status has phase field"     "phase:"        "tests/functional/hexgame/doc/01-plan/work-status.md"
assert_grep "P3-3: shopflow work-log has last_session"      "last_session"  "tests/functional/shopflow/doc/03-log/work-log-index.md"
assert_grep "P3-4: shopflow task-board has in_progress"     "in_progress"   "tests/functional/shopflow/doc/02-task/task-board.md"
assert_grep "P3-5: hexgame task-board has in_progress"      "in_progress"   "tests/functional/hexgame/doc/02-task/task-board.md"

# P3-6: ADR format consistency
assert_grep "P3-6: shopflow ADR has Context section"    "## Context"  "tests/functional/shopflow/doc/07-decisions/ADR-001-nextjs-frontend.md"
assert_grep "P3-7: shopflow ADR has Options section"    "Options"     "tests/functional/shopflow/doc/07-decisions/ADR-001-nextjs-frontend.md"
assert_grep "P3-8: shopflow ADR has Source Reference"   "Source Reference" "tests/functional/shopflow/doc/07-decisions/ADR-001-nextjs-frontend.md"

# P3-9: entity-register format consistency
assert_grep "P3-9:  shopflow entity-register has Active Entities"  "Active Entities" "tests/functional/shopflow/doc/07-decisions/entity-register.md"
assert_grep "P3-10: hexgame entity-register has Active Entities"   "Active Entities" "tests/functional/hexgame/doc/07-decisions/entity-register.md"

# =============================================================================
header "FINAL RESULTS"
# =============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PASS : $PASS"
echo "  FAIL : $FAIL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL -gt 0 ]; then
  echo ""
  echo "Failed checks:"
  for item in "${FAIL_LIST[@]}"; do
    echo "  ✗ $item"
  done
  echo ""
  exit 1
else
  echo ""
  echo "  ALL FUNCTIONAL TESTS PASSED ✓"
  echo ""
  exit 0
fi
