#!/usr/bin/env bash
# =============================================================================
# test-user-flows.sh — End-to-end test for both user installation flows
#
# Tests:
#   Flow A: ZIP download (extract to _template/) → bootstrap → cleanup
#   Flow B: git clone → open directly
#
# Usage:
#   bash tests/functional/test-user-flows.sh
#
# Must run from ai-project-template root
# =============================================================================

set -euo pipefail

TEMPLATE_ROOT="$(pwd)"
PASS=0
FAIL=0
ERRORS=()

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "  ${GREEN}✓${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "  ${RED}✗${NC} $1"; FAIL=$((FAIL+1)); ERRORS+=("$1"); }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
section() { echo ""; echo "━━━ $1 ━━━"; }

# ── Guard ─────────────────────────────────────────────────────────────────────

if [ ! -f "$TEMPLATE_ROOT/core/00-ai-bootstrap-master-template.md" ]; then
  echo "ERROR: must run from ai-project-template root"
  exit 1
fi

TMPDIR_BASE=$(mktemp -d)
trap "rm -rf $TMPDIR_BASE" EXIT

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  User Flow Tests — ai-project-template"
echo "  Template root: $TEMPLATE_ROOT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# =============================================================================
# FLOW A: ZIP-style install (new project)
# Simulates: user downloads ZIP → extracts to _template/ → runs new-project.sh
# =============================================================================

section "Flow A: ZIP install → new project"

PROJECT_A="$TMPDIR_BASE/test-project-a"
mkdir -p "$PROJECT_A"
mkdir -p "$PROJECT_A/_template"

# Copy template files (simulating ZIP extraction, no .git)
cp -r "$TEMPLATE_ROOT/core" "$PROJECT_A/_template/"
cp -r "$TEMPLATE_ROOT/platforms" "$PROJECT_A/_template/"
cp -r "$TEMPLATE_ROOT/skills" "$PROJECT_A/_template/"
cp -r "$TEMPLATE_ROOT/scripts" "$PROJECT_A/_template/"
cp "$TEMPLATE_ROOT/QUICKSTART.md" "$PROJECT_A/_template/"

# Verify _template structure exists
[ -d "$PROJECT_A/_template/core" ] && pass "A1: _template/core exists after extraction" || fail "A1: _template/core missing"
[ -f "$PROJECT_A/_template/core/00-ai-bootstrap-master-template.md" ] && pass "A2: core/00 accessible" || fail "A2: core/00 missing"
[ ! -d "$PROJECT_A/_template/.git" ] && pass "A3: no nested .git (ZIP simulation correct)" || fail "A3: nested .git found (ZIP simulation error)"

# Run new-project.sh from template
bash "$TEMPLATE_ROOT/scripts/new-project.sh" "TestProject" "$PROJECT_A" 2>&1 | tail -5

# Verify ai/ structure created (NOT doc/)
[ -d "$PROJECT_A/ai" ] && pass "A4: ai/ folder created" || fail "A4: ai/ folder NOT created"
[ ! -d "$PROJECT_A/doc" ] && pass "A5: no legacy doc/ folder (rename successful)" || fail "A5: old doc/ folder still created — rename incomplete"

# Verify required files
REQUIRED_A=(
  "ai/README.md"
  "ai/00-source/README.md"
  "ai/01-plan/work-status.md"
  "ai/02-task/task-board.md"
  "ai/03-log/work-log-index.md"
  "ai/04-way-of-work/way-of-work.md"
  "ai/04-way-of-work/ai-decision-protocol.md"
  "ai/04-way-of-work/compliance.md"
  "ai/07-decisions/README.md"
  "ai/07-decisions/entity-register.md"
)

for f in "${REQUIRED_A[@]}"; do
  [ -f "$PROJECT_A/$f" ] && pass "A6: $f exists" || fail "A6: $f MISSING"
done

# Verify no docs/ conflict (docs/ should NOT appear in user project)
[ ! -d "$PROJECT_A/docs" ] && pass "A7: no docs/ conflict in user project" || fail "A7: docs/ appeared in user project — conflict exists"

# Verify CLAUDE.md copy works
cp "$TEMPLATE_ROOT/platforms/claude-code/CLAUDE.md" "$PROJECT_A/CLAUDE.md"
[ -f "$PROJECT_A/CLAUDE.md" ] && pass "A8: CLAUDE.md copied to root" || fail "A8: CLAUDE.md copy failed"

# Verify CLAUDE.md references ai/ (not doc/)
if grep -q "ai/" "$PROJECT_A/CLAUDE.md" && ! grep -q "doc/" "$PROJECT_A/CLAUDE.md"; then
  pass "A9: CLAUDE.md references ai/ correctly"
elif grep -q "doc/" "$PROJECT_A/CLAUDE.md"; then
  fail "A9: CLAUDE.md still references old doc/ path"
else
  fail "A9: CLAUDE.md has no ai/ references"
fi

# Simulate cleanup (delete _template/)
rm -rf "$PROJECT_A/_template"
[ ! -d "$PROJECT_A/_template" ] && pass "A10: _template/ cleaned up successfully" || fail "A10: _template/ cleanup failed"

# After cleanup: verify ai/ still intact, no broken references
[ -d "$PROJECT_A/ai" ] && pass "A11: ai/ intact after _template/ deletion" || fail "A11: ai/ lost after _template/ deletion"

# =============================================================================
# FLOW B: git clone simulation (user clones repo directly)
# =============================================================================

section "Flow B: git clone simulation"

PROJECT_B="$TMPDIR_BASE/test-project-b"
# Simulate clone by copying entire template repo
cp -r "$TEMPLATE_ROOT" "$PROJECT_B"
cd "$PROJECT_B"

# Check: does CLAUDE.md exist at root?
if [ -f "CLAUDE.md" ]; then
  pass "B1: CLAUDE.md exists at project root"
else
  fail "B1: CLAUDE.md NOT at root — clone flow broken (user must manually copy)"
fi

# Check: docs/ must not be git-tracked on dev (must be on gh-pages only)
# Use git ls-files, NOT filesystem check — cp -r copies untracked dirs too
# but real git clone only delivers tracked files
DOCS_TRACKED_B=$(git ls-files docs/ 2>/dev/null | wc -l | tr -d ' ')
AI_EXISTS_B=$([ -d "ai" ] && echo 1 || echo 0)
if [ "$DOCS_TRACKED_B" -gt 0 ] && [ "$AI_EXISTS_B" -eq 1 ]; then
  fail "B2: COLLISION — git-tracked docs/ and ai/ both present in clone"
else
  pass "B2: no git-tracked docs/ collision with ai/ (real clone is clean)"
  if [ "$AI_EXISTS_B" -eq 1 ]; then
    warn "B2: ai/ exists in clone (template tracking) — user must rm -rf ai/ before bootstrapping own project"
  fi
fi

# Check: core/ accessible (needed for First Run Bootstrap)
[ -d "core" ] && pass "B3: core/ accessible at root — First Run Bootstrap can read templates" || fail "B3: core/ not at root"

# Check: agent paths in CLAUDE.md point to real locations
if [ -f "platforms/claude-code/CLAUDE.md" ]; then
  if grep -q "platforms/claude-code/agents/" "platforms/claude-code/CLAUDE.md"; then
    if [ -d "platforms/claude-code/agents" ]; then
      pass "B4: agent paths in CLAUDE.md exist (clone flow)"
    else
      fail "B4: CLAUDE.md references platforms/claude-code/agents/ but folder missing"
    fi
  else
    pass "B4: no dead agent paths in CLAUDE.md"
  fi
fi

# Check: skills/game/ referenced but exists?
if grep -q "skills/game/" "platforms/claude-code/CLAUDE.md" 2>/dev/null; then
  if [ -d "skills/game" ]; then
    pass "B5: skills/game/ referenced and exists (clone flow)"
  else
    fail "B5: skills/game/ referenced in CLAUDE.md but missing"
  fi
fi

cd "$TEMPLATE_ROOT"

# =============================================================================
# FLOW C: Existing project install
# =============================================================================

section "Flow C: Existing project install"

PROJECT_C="$TMPDIR_BASE/test-existing-project"
mkdir -p "$PROJECT_C/src"
echo "existing code" > "$PROJECT_C/src/main.js"
echo "node_modules/" > "$PROJECT_C/.gitignore"
cd "$PROJECT_C" && git init -q && git add . && git commit -q -m "initial commit"
cd "$TEMPLATE_ROOT"

# Simulate template extraction
mkdir -p "$PROJECT_C/_template"
cp -r "$TEMPLATE_ROOT/core" "$PROJECT_C/_template/"
cp -r "$TEMPLATE_ROOT/scripts" "$PROJECT_C/_template/"

# Run bootstrap
bash "$TEMPLATE_ROOT/scripts/new-project.sh" "ExistingProject" "$PROJECT_C" 2>&1 | tail -3

# Verify existing code untouched
[ -f "$PROJECT_C/src/main.js" ] && pass "C1: existing src/ untouched" || fail "C1: existing src/ damaged"
[ -f "$PROJECT_C/.gitignore" ] && pass "C2: existing .gitignore preserved" || fail "C2: .gitignore lost"

# Verify ai/ created
[ -d "$PROJECT_C/ai" ] && pass "C3: ai/ created in existing project" || fail "C3: ai/ not created"

# Verify no doc/ collision
[ ! -d "$PROJECT_C/doc" ] && pass "C4: no legacy doc/ created" || fail "C4: legacy doc/ created — rename incomplete"

# =============================================================================
# STRUCTURAL CHECKS
# =============================================================================

section "Structural Integrity"

cd "$TEMPLATE_ROOT"

# Check: no stray doc/ references in critical files (should be ai/ now)
if grep -q "doc/" platforms/claude-code/CLAUDE.md 2>/dev/null; then
  fail "S1: CLAUDE.md still has legacy doc/ references"
else
  pass "S1: CLAUDE.md has no legacy doc/ references"
fi

if grep -q "doc/" core/00-ai-bootstrap-master-template.md 2>/dev/null; then
  fail "S2: core/00 bootstrap template has legacy doc/ references"
else
  pass "S2: core/00 bootstrap template has no legacy doc/ references"
fi

if grep -q "TARGET/doc" scripts/new-project.sh 2>/dev/null; then
  fail "S3: new-project.sh still has legacy TARGET/doc references"
else
  pass "S3: new-project.sh has no legacy TARGET/doc references"
fi

# Check: mock-project uses ai/ not doc/
if [ -d "tests/mock-project/ai" ] && [ ! -d "tests/mock-project/doc" ]; then
  pass "S4: mock-project uses ai/ (not doc/)"
else
  fail "S4: mock-project still uses old doc/ structure"
fi

# Check: docs/ NOT tracked on dev/master (correctly moved to gh-pages branch)
DOCS_TRACKED=$(git ls-files docs/ | wc -l | tr -d ' ')
if [ "$DOCS_TRACKED" -eq 0 ]; then
  pass "S5: docs/ has no tracked files on dev — correctly on gh-pages branch only"
else
  fail "S5: docs/ has $DOCS_TRACKED tracked file(s) on dev — should be on gh-pages only"
fi

# Check: ai/ naming doesn't conflict with anything
if [ ! -d "doc" ]; then
  pass "S6: no legacy doc/ folder on dev branch"
else
  fail "S6: legacy doc/ folder found on dev — rename incomplete"
fi

# =============================================================================
# RESULTS
# =============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Results: ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}"

if [ ${#ERRORS[@]} -gt 0 ]; then
  echo ""
  echo "  Failed tests:"
  for e in "${ERRORS[@]}"; do
    echo -e "    ${RED}✗${NC} $e"
  done
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL -eq 0 ]; then
  exit 0
else
  exit 1
fi
