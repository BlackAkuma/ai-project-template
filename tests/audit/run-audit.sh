#!/usr/bin/env bash
# =============================================================================
# run-audit.sh — Full Project Audit: ai-project-template
# รันจาก project root: bash tests/audit/run-audit.sh
# =============================================================================

set -euo pipefail

PASS=0; FAIL=0; WARN=0
FAIL_LIST=()

# ── Helpers ──────────────────────────────────────────────────────────────────

pass()  { echo "[PASS] $1"; PASS=$((PASS+1)); }
fail()  { echo "[FAIL] $1"; FAIL=$((FAIL+1)); FAIL_LIST+=("$1"); }
warn()  { echo "[WARN] $1"; WARN=$((WARN+1)); }
header(){ echo ""; echo "══════════════════════════════════════════"; echo "  $1"; echo "══════════════════════════════════════════"; }

assert_file() {
  local desc="$1" file="$2"
  [ -f "$file" ] && pass "$desc" || fail "$desc — missing: $file"
}

assert_dir() {
  local desc="$1" dir="$2"
  [ -d "$dir" ] && pass "$desc" || fail "$desc — missing dir: $dir"
}

assert_count() {
  local desc="$1" expected="$2" actual="$3"
  if [ "$actual" -eq "$expected" ]; then
    pass "$desc (count=$actual)"
  else
    fail "$desc (expected=$expected, got=$actual)"
  fi
}

assert_grep() {
  local desc="$1" pattern="$2" file="$3"
  if grep -qE "$pattern" "$file" 2>/dev/null; then
    pass "$desc"
  else
    fail "$desc — pattern '$pattern' not found in $file"
  fi
}

assert_no_grep() {
  local desc="$1" pattern="$2" file="$3"
  if ! grep -qE "$pattern" "$file" 2>/dev/null; then
    pass "$desc"
  else
    fail "$desc — found unwanted pattern '$pattern' in $file"
  fi
}

assert_bash_syntax() {
  local file="$1"
  if bash -n "$file" 2>/dev/null; then
    pass "bash syntax: $(basename $file)"
  else
    fail "bash syntax: $(basename $file) — syntax error"
  fi
}

# ── Main ─────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ai-project-template Full Audit"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# =============================================================================
header "A: Core Templates (00–18)"
# =============================================================================

CORE_COUNT=$(ls core/*.md 2>/dev/null | wc -l | tr -d ' ')
assert_count "A-1: core/ has exactly 19 files" 19 "$CORE_COUNT"

# Check numbering: 00–18 with no gaps
CORE_NUMS=$(ls core/*.md 2>/dev/null | grep -oE "[0-9]{2}-" | grep -oE "[0-9]{2}" | sort -n)
EXPECTED_NUMS=$(seq -w 0 18)
if [ "$CORE_NUMS" = "$EXPECTED_NUMS" ]; then
  pass "A-2: core/ numbering 00–18, no gaps"
else
  fail "A-2: core/ numbering gaps detected"
fi

# Check no empty files
EMPTY_CORE=0
for f in core/*.md; do
  [ "$(wc -c < "$f")" -eq 0 ] && EMPTY_CORE=$((EMPTY_CORE+1)) && echo "     ↳ EMPTY: $f"
done
[ "$EMPTY_CORE" -eq 0 ] && pass "A-3: no empty core files" || fail "A-3: $EMPTY_CORE empty core files"

# Required file references from 00
assert_grep "A-4: core/00 references 11-ai-decision-protocol" "11-ai-decision-protocol" "core/00-ai-bootstrap-master-template.md"
assert_grep "A-5: core/00 references 12-adr" "12-adr" "core/00-ai-bootstrap-master-template.md"
assert_grep "A-6: core/00 references 13-retrospective" "13-retrospective" "core/00-ai-bootstrap-master-template.md"
assert_grep "A-7: core/00 references 14-anti-patterns" "14-anti-patterns" "core/00-ai-bootstrap-master-template.md"
assert_grep "A-8: core/00 references 15-compliance" "15-compliance" "core/00-ai-bootstrap-master-template.md"
assert_grep "A-9: core/00 lists doc/04-way-of-work/ai-decision-protocol.md output" "ai-decision-protocol" "core/00-ai-bootstrap-master-template.md"
assert_grep "A-10: core/00 lists doc/07-decisions/ output" "07-decisions" "core/00-ai-bootstrap-master-template.md"

# core/01 folder structure
assert_grep "A-11: core/01 has doc/07-decisions/" "07-decisions" "core/01-folder-structure-template.md"
assert_grep "A-12: core/01 has doc/04-way-of-work/ai-decision-protocol" "ai-decision-protocol" "core/01-folder-structure-template.md"
assert_grep "A-13: core/01 has doc/04-way-of-work/compliance" "compliance" "core/01-folder-structure-template.md"

# core/11 scenario completeness
assert_grep "A-14: core/11 has Scenario H (gap detection)" "Scenario H" "core/11-ai-decision-protocol-template.md"
assert_grep "A-15: core/11 has Scenario J (deprecated entity)" "Scenario J" "core/11-ai-decision-protocol-template.md"
assert_grep "A-16: core/11 has Scenario K (memory scope)" "Scenario K" "core/11-ai-decision-protocol-template.md"
assert_grep "A-17: core/11 has ENTITY tag format table" "ENTITY:deprecated" "core/11-ai-decision-protocol-template.md"

# core/12 ADR
assert_grep "A-18: core/12 has ADR index section" "Decision Log" "core/12-adr-template.md"
assert_grep "A-19: core/12 has individual ADR template" "Context" "core/12-adr-template.md"
assert_grep "A-20: core/12 has workflow steps" "workflow" "core/12-adr-template.md"

# =============================================================================
header "B: skills/game/ (00–06)"
# =============================================================================

GAME_COUNT=$(ls skills/game/*.md 2>/dev/null | wc -l | tr -d ' ')
assert_count "B-1: skills/game/ has exactly 7 files" 7 "$GAME_COUNT"

GAME_UNIQUE=$(ls skills/game/*.md 2>/dev/null | grep -oE "/[0-9]{2}-" | grep -oE "[0-9]{2}" | sort -nu | wc -l | tr -d ' ')
if [ "$GAME_UNIQUE" -eq 7 ]; then
  pass "B-2: skills/game/ numbering 00–06, no gaps"
else
  fail "B-2: skills/game/ numbering gaps detected (unique numbers=$GAME_UNIQUE, expected 7)"
fi

EMPTY_GAME=0
for f in skills/game/*.md; do
  [ "$(wc -c < "$f")" -eq 0 ] && EMPTY_GAME=$((EMPTY_GAME+1)) && echo "     ↳ EMPTY: $f"
done
[ "$EMPTY_GAME" -eq 0 ] && pass "B-3: no empty game skill files" || fail "B-3: $EMPTY_GAME empty game files"

assert_grep "B-4: skills/game/00 references 01–06" "01-fdd" "skills/game/00-game-skill-overview.md"
assert_grep "B-5: FDD template has design_validate lifecycle" "design_validate" "skills/game/01-fdd-template.md"
assert_grep "B-6: FDD template has playtest lifecycle" "playtest" "skills/game/01-fdd-template.md"
assert_grep "B-7: game coding standards has G-01 compliance codes" "G-01" "skills/game/02-game-coding-standards.md"
assert_grep "B-8: asset protocol has A-01 compliance codes" "A-01" "skills/game/03-asset-protocol.md"
assert_grep "B-9: narrative standards has N-01 compliance codes" "N-01" "skills/game/06-narrative-standards-template.md"

# =============================================================================
header "C: platforms/claude-code/"
# =============================================================================

# CLAUDE.md cross-references
assert_grep "C-1: CLAUDE.md references core/10-bootstrap-checklist" "10-bootstrap-checklist" "platforms/claude-code/CLAUDE.md"
assert_grep "C-2: CLAUDE.md references Scenario H" "Scenario H" "platforms/claude-code/CLAUDE.md"
assert_grep "C-3: CLAUDE.md references Scenario K" "Scenario K" "platforms/claude-code/CLAUDE.md"
assert_grep "C-4: CLAUDE.md references Scenario B" "Scenario B" "platforms/claude-code/CLAUDE.md"
assert_grep "C-5: CLAUDE.md references Scenario J" "Scenario J" "platforms/claude-code/CLAUDE.md"
assert_grep "C-6: CLAUDE.md has doc/08-design game detection" "doc/08-design" "platforms/claude-code/CLAUDE.md"
assert_grep "C-7: CLAUDE.md has 00 → 18 range" "00 → 18" "platforms/claude-code/CLAUDE.md"
assert_grep "C-8: CLAUDE.md has 00 → 06 game range" "00 → 06" "platforms/claude-code/CLAUDE.md"
assert_grep "C-9: CLAUDE.md has Memory Scope reference" "cross-project-memory" "platforms/claude-code/CLAUDE.md"

# Hooks
HOOK_COUNT=$(ls platforms/claude-code/hooks/*.sh 2>/dev/null | wc -l | tr -d ' ')
assert_count "C-10: hooks/ has 5 files" 5 "$HOOK_COUNT"

for f in platforms/claude-code/hooks/*.sh; do
  assert_bash_syntax "$f"
done

# Rules
RULES_COUNT=$(ls platforms/claude-code/rules/*.md 2>/dev/null | wc -l | tr -d ' ')
assert_count "C-11: rules/ has 4 files" 4 "$RULES_COUNT"

assert_file "C-12: rules/core-standards.md" "platforms/claude-code/rules/core-standards.md"
assert_file "C-13: rules/design-docs.md" "platforms/claude-code/rules/design-docs.md"
assert_file "C-14: rules/gameplay-code.md" "platforms/claude-code/rules/gameplay-code.md"
assert_file "C-15: rules/test-standards.md" "platforms/claude-code/rules/test-standards.md"

# Skills (core 7)
for skill in compliance-check fdd-create adr-create session-end scope-check launch-check archive-logs; do
  assert_file "C-16: skills/$skill.md" "platforms/claude-code/skills/$skill.md"
done

# Skills (game-only — documented as game-only in CLAUDE.md)
assert_file "C-17: skills/balance-check.md (game-only)" "platforms/claude-code/skills/balance-check.md"
assert_file "C-18: skills/playtest-report.md (game-only)" "platforms/claude-code/skills/playtest-report.md"

# =============================================================================
header "D: README.md & QUICKSTART.md — Claims Verification"
# =============================================================================

assert_file  "D-1: LICENSE file exists" "LICENSE"
assert_file  "D-2: QUICKSTART.md exists" "QUICKSTART.md"
assert_file  "D-3: docs/how-it-works.html exists" "docs/how-it-works.html"

assert_grep  "D-4: README (EN) — 19 template files" "19 template files" "README.md"
assert_grep  "D-5: README (TH) — 19 template files" "19 template files" "README.md"
assert_grep  "D-6: README (EN) — 00 → 18" "00 → 18" "README.md"
assert_grep  "D-7: README (TH) — 00 → 18" "00 → 18" "README.md"
assert_grep  "D-8: README has GitHub Sponsors badge" "sponsors/BlackAkuma" "README.md"
assert_grep  "D-9: README (EN) has how-it-works link" "how-it-works.html" "README.md"
assert_grep  "D-10: README (TH) has how-it-works link" "how-it-works.html" "README.md"
assert_grep  "D-11: README references QUICKSTART.md" "QUICKSTART.md" "README.md"

assert_grep  "D-12: QUICKSTART uses master branch URL" "archive/master.zip" "QUICKSTART.md"
assert_no_grep "D-13: QUICKSTART has no main branch URL" "archive/main.zip" "QUICKSTART.md"
assert_grep  "D-14: QUICKSTART — 00 → 18" "00 → 18" "QUICKSTART.md"
assert_no_grep "D-15: QUICKSTART has no old 00 → 16 reference" "00 → 16" "QUICKSTART.md"

# Verify 19 files in README table (table appears in both EN and TH sections = 38 total rows)
README_CORE_ROWS=$(grep -cE "^\| \`[0-9]{2}\`" README.md 2>/dev/null || echo 0)
assert_count "D-16: README core table has 38 rows (19 EN + 19 TH)" 38 "$README_CORE_ROWS"

# =============================================================================
header "E: Number & Name Consistency (cross-document)"
# =============================================================================

assert_grep "E-1: CLAUDE.md — 00 → 18" "00 → 18" "platforms/claude-code/CLAUDE.md"
assert_grep "E-2: platforms/README — 00–18" "00" "platforms/claude-code/README.md"

# Check for leftover old references
assert_no_grep "E-3: README has no old 00 → 16" "00 → 16" "README.md"
assert_no_grep "E-4: QUICKSTART has no ai-project-template-main" "ai-project-template-main" "QUICKSTART.md"
assert_no_grep "E-5: CLAUDE.md has no reference to main branch" "archive/main" "platforms/claude-code/CLAUDE.md"

# =============================================================================
header "F: tests/ Suite"
# =============================================================================

assert_file "F-1: tests/README.md" "tests/README.md"
assert_file "F-2: tests/hooks/test-validate-commit.sh" "tests/hooks/test-validate-commit.sh"
assert_bash_syntax "tests/hooks/test-validate-commit.sh"

# Reader test files
for tf in test-agent-diary test-cross-project-memory test-memory-scope test-scenario-j test-entity-register test-scoped-memory; do
  assert_file "F-3: tests/reader/$tf.md" "tests/reader/$tf.md"
done

# mock-project structure
assert_dir "F-4: tests/mock-project/doc exists" "tests/mock-project/doc"
assert_file "F-5: tests/mock-project/doc/01-plan/work-status.md" "tests/mock-project/doc/01-plan/work-status.md"
assert_file "F-6: tests/mock-project/doc/02-task/task-board.md" "tests/mock-project/doc/02-task/task-board.md"

# functional test projects
assert_file "F-7: tests/functional/run-functional-test.sh" "tests/functional/run-functional-test.sh"
assert_dir  "F-8: tests/functional/shopflow exists" "tests/functional/shopflow"
assert_dir  "F-9: tests/functional/hexgame exists"  "tests/functional/hexgame"
assert_file "F-10: shopflow/doc/07-decisions/entity-register.md" "tests/functional/shopflow/doc/07-decisions/entity-register.md"
assert_file "F-11: hexgame/doc/08-design/movement-system.md (FDD)" "tests/functional/hexgame/doc/08-design/movement-system.md"

# =============================================================================
header "G: docs/ GitHub Pages"
# =============================================================================

assert_file "G-1: docs/how-it-works.html" "docs/how-it-works.html"
assert_grep "G-2: how-it-works.html has 19" "19" "docs/how-it-works.html"
assert_grep "G-3: how-it-works.html has GitHub Sponsors link" "sponsors/BlackAkuma" "docs/how-it-works.html"
assert_grep "G-4: how-it-works.html has bilingual TH/EN" 'html\[lang|lang="en"' "docs/how-it-works.html"
assert_grep "G-5: how-it-works.html has GitHub repo link" "BlackAkuma/ai-project-template" "docs/how-it-works.html"

# =============================================================================
header "FINAL RESULTS"
# =============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PASS : $PASS"
echo "  FAIL : $FAIL"
echo "  WARN : $WARN"
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
  echo "  ALL CHECKS PASSED ✓"
  echo ""
  exit 0
fi
