#!/usr/bin/env bash
# verify-install.sh — Verify that ai-project-template was fully installed
# Run from the TARGET project root (not the template root)
# Usage: bash verify-install.sh

set -euo pipefail

PASS=0
FAIL=0
ERRORS=()

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "  ${GREEN}✓${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "  ${RED}✗${NC} $1"; FAIL=$((FAIL+1)); ERRORS+=("$1"); }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
section() { echo ""; echo "━━━ $1 ━━━"; }

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  verify-install.sh — ai-project-template post-install check"
echo "  Project root: $(pwd)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# =============================================================================
# Section 1: CoreAiWorkspaces/ structure
# =============================================================================

section "CoreAiWorkspaces/ structure"

[ -d "CoreAiWorkspaces" ]                                             && pass "CoreAiWorkspaces/ exists"                                       || fail "CoreAiWorkspaces/ does NOT exist"
[ -f "CoreAiWorkspaces/00-source/README.md" ]                        && pass "CoreAiWorkspaces/00-source/README.md exists"                    || fail "CoreAiWorkspaces/00-source/README.md missing"
[ -f "CoreAiWorkspaces/01-plan/work-status.md" ]                     && pass "CoreAiWorkspaces/01-plan/work-status.md exists"                 || fail "CoreAiWorkspaces/01-plan/work-status.md missing"
[ -d "CoreAiWorkspaces/01-plan" ]                                     && pass "CoreAiWorkspaces/01-plan/ exists"                               || fail "CoreAiWorkspaces/01-plan/ missing"
[ -f "CoreAiWorkspaces/02-task/task-board.md" ]                      && pass "CoreAiWorkspaces/02-task/task-board.md exists"                  || fail "CoreAiWorkspaces/02-task/task-board.md missing"
[ -f "CoreAiWorkspaces/03-log/work-log-index.md" ]                   && pass "CoreAiWorkspaces/03-log/work-log-index.md exists"               || fail "CoreAiWorkspaces/03-log/work-log-index.md missing"
[ -f "CoreAiWorkspaces/04-way-of-work/way-of-work.md" ]              && pass "CoreAiWorkspaces/04-way-of-work/way-of-work.md exists"          || fail "CoreAiWorkspaces/04-way-of-work/way-of-work.md missing"
[ -f "CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md" ]     && pass "CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md exists" || fail "CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md missing"
[ -f "CoreAiWorkspaces/04-way-of-work/compliance.md" ]               && pass "CoreAiWorkspaces/04-way-of-work/compliance.md exists"           || fail "CoreAiWorkspaces/04-way-of-work/compliance.md missing"
[ -f "CoreAiWorkspaces/07-decisions/README.md" ]                     && pass "CoreAiWorkspaces/07-decisions/README.md exists"                 || fail "CoreAiWorkspaces/07-decisions/README.md missing"
[ -f "CoreAiWorkspaces/07-decisions/entity-register.md" ]            && pass "CoreAiWorkspaces/07-decisions/entity-register.md exists"        || fail "CoreAiWorkspaces/07-decisions/entity-register.md missing"

# =============================================================================
# Section 2: CLAUDE.md at root
# =============================================================================

section "CLAUDE.md at root"

if [ -f "CLAUDE.md" ]; then
  pass "CLAUDE.md exists at root"
  if grep -q "CoreAiWorkspaces/" "CLAUDE.md" && ! grep -qP '(?<![a-zA-Z0-9_\-])ai/' "CLAUDE.md" 2>/dev/null; then
    pass "CLAUDE.md references CoreAiWorkspaces/ (not ai/)"
  elif grep -qP '(?<![a-zA-Z0-9_\-])ai/' "CLAUDE.md" 2>/dev/null; then
    fail "CLAUDE.md still references legacy ai/ path"
  else
    warn "CLAUDE.md has no CoreAiWorkspaces/ references — may need review"
  fi
else
  fail "CLAUDE.md NOT found at root"
fi

# =============================================================================
# Section 3: Slash commands installed
# =============================================================================

section "Slash commands installed"

if [ -d ".claude/commands" ]; then
  pass ".claude/commands/ exists"
  EXPECTED_SKILLS=("session-end.md" "adr-create.md" "compliance-check.md" "scope-check.md" "fdd-create.md" "archive-logs.md")
  for skill in "${EXPECTED_SKILLS[@]}"; do
    [ -f ".claude/commands/$skill" ] && pass ".claude/commands/$skill installed" || fail ".claude/commands/$skill missing"
  done
else
  fail ".claude/commands/ does NOT exist — slash commands not installed"
fi

# =============================================================================
# Section 4: Git hooks
# =============================================================================

section "Git hooks"

if [ -d ".git" ]; then
  if [ -f ".git/hooks/validate-commit" ]; then
    pass ".git/hooks/validate-commit exists"
    if [ -x ".git/hooks/validate-commit" ]; then
      pass ".git/hooks/validate-commit is executable"
    else
      fail ".git/hooks/validate-commit is NOT executable"
    fi
  else
    fail ".git/hooks/validate-commit NOT installed"
  fi
else
  warn ".git/ not found — git hooks check skipped (not a git repo)"
fi

# =============================================================================
# Section 5: No legacy ai/ folder
# =============================================================================

section "No legacy ai/ folder"

if [ ! -d "ai" ]; then
  pass "ai/ folder does NOT exist (clean project)"
else
  fail "ai/ folder EXISTS — legacy folder should be removed (rm -rf ai/)"
fi

# =============================================================================
# Section 6: Summary
# =============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  Results: ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}"

if [ ${#ERRORS[@]} -gt 0 ]; then
  echo ""
  echo "  Failed checks:"
  for e in "${ERRORS[@]}"; do
    echo -e "    ${RED}✗${NC} $e"
  done
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL -eq 0 ]; then
  echo "  Install verified successfully."
  exit 0
else
  echo "  Install verification FAILED — fix the issues above."
  exit 1
fi
