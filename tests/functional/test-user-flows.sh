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

# Verify CoreAiWorkspaces/ structure created (NOT doc/)
[ -d "$PROJECT_A/CoreAiWorkspaces" ] && pass "A4: CoreAiWorkspaces/ folder created" || fail "A4: CoreAiWorkspaces/ folder NOT created"
[ ! -d "$PROJECT_A/doc" ] && pass "A5: no legacy doc/ folder (rename successful)" || fail "A5: old doc/ folder still created — rename incomplete"

# Verify required files
REQUIRED_A=(
  "CoreAiWorkspaces/README.md"
  "CoreAiWorkspaces/00-source/README.md"
  "CoreAiWorkspaces/01-plan/work-status.md"
  "CoreAiWorkspaces/02-task/task-board.md"
  "CoreAiWorkspaces/03-log/work-log-index.md"
  "CoreAiWorkspaces/04-way-of-work/way-of-work.md"
  "CoreAiWorkspaces/04-way-of-work/ai-decision-protocol.md"
  "CoreAiWorkspaces/04-way-of-work/compliance.md"
  "CoreAiWorkspaces/04-way-of-work/tacp.md"
  "CoreAiWorkspaces/07-decisions/README.md"
  "CoreAiWorkspaces/07-decisions/entity-register.md"
)

for f in "${REQUIRED_A[@]}"; do
  [ -f "$PROJECT_A/$f" ] && pass "A6: $f exists" || fail "A6: $f MISSING"
done

# Verify no docs/ conflict (docs/ should NOT appear in user project)
[ ! -d "$PROJECT_A/docs" ] && pass "A7: no docs/ conflict in user project" || fail "A7: docs/ appeared in user project — conflict exists"

# Verify AI.md (universal protocol) was auto-installed by new-project.sh
[ -f "$PROJECT_A/AI.md" ] && pass "A8a: AI.md auto-installed at root by new-project.sh" || fail "A8a: AI.md not installed at root"

# Verify CLAUDE.md was auto-installed by new-project.sh (no manual copy needed)
[ -f "$PROJECT_A/CLAUDE.md" ] && pass "A8b: CLAUDE.md auto-installed at root by new-project.sh" || fail "A8b: CLAUDE.md not installed at root"

# Verify CLAUDE.md references CoreAiWorkspaces/ (not doc/)
if grep -q "CoreAiWorkspaces/" "$PROJECT_A/CLAUDE.md" && ! grep -q "doc/" "$PROJECT_A/CLAUDE.md"; then
  pass "A9: CLAUDE.md references CoreAiWorkspaces/ correctly"
elif grep -q "doc/" "$PROJECT_A/CLAUDE.md"; then
  fail "A9: CLAUDE.md still references old doc/ path"
else
  fail "A9: CLAUDE.md has no CoreAiWorkspaces/ references"
fi

# Simulate cleanup (delete _template/)
rm -rf "$PROJECT_A/_template"
[ ! -d "$PROJECT_A/_template" ] && pass "A10: _template/ cleaned up successfully" || fail "A10: _template/ cleanup failed"

# After cleanup: verify CoreAiWorkspaces/ still intact, no broken references
[ -d "$PROJECT_A/CoreAiWorkspaces" ] && pass "A11: CoreAiWorkspaces/ intact after _template/ deletion" || fail "A11: CoreAiWorkspaces/ lost after _template/ deletion"

# Verify .claude/commands/ installed with slash command files
if [ -d "$PROJECT_A/.claude/commands" ]; then
  pass "A12: .claude/commands/ created"
  SLASH_FILES=("caw-session-end.md" "caw-adr-create.md" "caw-compliance-check.md" "caw-scope-check.md" "caw-fdd-create.md" "caw-archive-logs.md" "caw-tool-clean.md" "caw-update.md")
  for sf in "${SLASH_FILES[@]}"; do
    [ -f "$PROJECT_A/.claude/commands/$sf" ] && pass "A13: .claude/commands/$sf installed" || fail "A13: .claude/commands/$sf missing"
  done
else
  fail "A12: .claude/commands/ NOT created — slash commands not installed"
fi

# Verify VERSION file exists and bootstrapped README embeds it
[ -f "$TEMPLATE_ROOT/VERSION" ] && pass "A14: VERSION file exists in template root" || fail "A14: VERSION file missing"
if grep -q "ai-project-template v" "$PROJECT_A/CoreAiWorkspaces/README.md" 2>/dev/null; then
  pass "A15: template version embedded in bootstrapped CoreAiWorkspaces/README.md"
else
  fail "A15: template version NOT found in CoreAiWorkspaces/README.md"
fi

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

# Check: docs/ is tracked on dev for GitHub Pages discoverability (intentional)
# CoreAiWorkspaces/ coexists — user cleans up both after bootstrap per CLAUDE.md Case 2
DOCS_TRACKED_B=$(git ls-files docs/ 2>/dev/null | wc -l | tr -d ' ')
CAW_EXISTS_B=$([ -d "CoreAiWorkspaces" ] && echo 1 || echo 0)
if [ "$DOCS_TRACKED_B" -gt 0 ]; then
  pass "B2: docs/ is git-tracked on dev (intentional — GitHub Pages discoverability)"
  warn "B2: user must run: rm -rf CoreAiWorkspaces/ docs/ tests/ CHANGELOG.md ROADMAP.md after bootstrap"
else
  pass "B2: docs/ not tracked (gh-pages-only mode)"
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
cp -r "$TEMPLATE_ROOT/platforms" "$PROJECT_C/_template/"
cp -r "$TEMPLATE_ROOT/scripts" "$PROJECT_C/_template/"

# Run bootstrap
bash "$TEMPLATE_ROOT/scripts/new-project.sh" "ExistingProject" "$PROJECT_C" 2>&1 | tail -3

# Verify existing code untouched
[ -f "$PROJECT_C/src/main.js" ] && pass "C1: existing src/ untouched" || fail "C1: existing src/ damaged"
[ -f "$PROJECT_C/.gitignore" ] && pass "C2: existing .gitignore preserved" || fail "C2: .gitignore lost"

# Verify CoreAiWorkspaces/ created
[ -d "$PROJECT_C/CoreAiWorkspaces" ] && pass "C3: CoreAiWorkspaces/ created in existing project" || fail "C3: CoreAiWorkspaces/ not created"

# Verify no doc/ collision
[ ! -d "$PROJECT_C/doc" ] && pass "C4: no legacy doc/ created" || fail "C4: legacy doc/ created — rename incomplete"

# Verify git hook installed (PROJECT_C has .git from git init above)
if [ -f "$PROJECT_C/.git/hooks/validate-commit" ]; then
  pass "C5: .git/hooks/validate-commit installed"
  [ -x "$PROJECT_C/.git/hooks/validate-commit" ] && pass "C6: .git/hooks/validate-commit is executable" || warn "C6: .git/hooks/validate-commit not executable (Windows NTFS — run: chmod +x .git/hooks/validate-commit)"
else
  fail "C5: .git/hooks/validate-commit NOT installed"
fi

# =============================================================================
# STRUCTURAL CHECKS
# =============================================================================

section "Structural Integrity"

cd "$TEMPLATE_ROOT"

# Check: no stray doc/ references in critical files (should be CoreAiWorkspaces/ now)
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

# Check: mock-project uses CoreAiWorkspaces/ not doc/
if [ -d "tests/mock-project/CoreAiWorkspaces" ] && [ ! -d "tests/mock-project/doc" ]; then
  pass "S4: mock-project uses CoreAiWorkspaces/ (not doc/)"
else
  fail "S4: mock-project still uses old doc/ structure"
fi

# Check: docs/ is tracked on dev — intentional for GitHub Pages discoverability
# (docs/ was moved from gh-pages to master/docs so users can read when browsing repo)
DOCS_TRACKED=$(git ls-files docs/ | wc -l | tr -d ' ')
if [ "$DOCS_TRACKED" -gt 0 ]; then
  pass "S5: docs/ is tracked on dev ($DOCS_TRACKED files) — intentional for GitHub Pages via master/docs"
else
  warn "S5: docs/ has no tracked files — verify GitHub Pages is configured correctly"
fi

# Check: CoreAiWorkspaces/ naming doesn't conflict with anything
if [ ! -d "doc" ]; then
  pass "S6: no legacy doc/ folder on dev branch"
else
  fail "S6: legacy doc/ folder found on dev — rename incomplete"
fi

# =============================================================================
# TACP CHECKS
# =============================================================================

section "TACP — Token-Aware Communication Protocol"

cd "$TEMPLATE_ROOT"

# Check: core/22-tacp-template.md exists
[ -f "core/22-tacp-template.md" ] && pass "T1: core/22-tacp-template.md exists" || fail "T1: core/22-tacp-template.md missing"

# Check: CLAUDE.md has TACP section
if grep -q "Token-Aware Communication Protocol" "CLAUDE.md" 2>/dev/null; then
  pass "T2: root CLAUDE.md has TACP section"
else
  fail "T2: root CLAUDE.md missing TACP section"
fi

# Check: platforms/claude-code/CLAUDE.md has TACP section
if grep -q "Token-Aware Communication Protocol" "platforms/claude-code/CLAUDE.md" 2>/dev/null; then
  pass "T3: platforms/claude-code/CLAUDE.md has TACP section"
else
  fail "T3: platforms/claude-code/CLAUDE.md missing TACP section"
fi

# Check: all caw-*.md files have AI-CONTEXT dual-block header
CAW_FILES=(
  "platforms/claude-code/skills/caw-session-end.md"
  "platforms/claude-code/skills/caw-adr-create.md"
  "platforms/claude-code/skills/caw-compliance-check.md"
  "platforms/claude-code/skills/caw-scope-check.md"
  "platforms/claude-code/skills/caw-fdd-create.md"
  "platforms/claude-code/skills/caw-archive-logs.md"
  "platforms/claude-code/skills/caw-launch-check.md"
  "platforms/claude-code/skills/caw-update.md"
  "platforms/claude-code/skills/caw-balance-check.md"
  "platforms/claude-code/skills/caw-playtest-report.md"
  "platforms/claude-code/skills/caw-game-review.md"
)

for caw_file in "${CAW_FILES[@]}"; do
  if grep -q "^<!-- AI-CONTEXT" "$caw_file" 2>/dev/null && grep -q "^<!-- HUMAN-CONTEXT" "$caw_file" 2>/dev/null; then
    pass "T4: $caw_file has dual-block format (L3)"
  else
    fail "T4: $caw_file missing dual-block format (AI-CONTEXT + HUMAN-CONTEXT)"
  fi
done

# Check: way-of-work.md has tacp config block
if grep -q "tacp:" "CoreAiWorkspaces/04-way-of-work/way-of-work.md" 2>/dev/null && grep -q "L2_LANG" "CoreAiWorkspaces/04-way-of-work/way-of-work.md" 2>/dev/null; then
  pass "T5: way-of-work.md has tacp config block with L2_LANG"
else
  fail "T5: way-of-work.md missing tacp config block"
fi

# Check: tacp.md exists in CoreAiWorkspaces/
[ -f "CoreAiWorkspaces/04-way-of-work/tacp.md" ] && pass "T6: CoreAiWorkspaces/04-way-of-work/tacp.md exists" || fail "T6: CoreAiWorkspaces/04-way-of-work/tacp.md missing"

# Check: ADR-005 exists
[ -f "CoreAiWorkspaces/07-decisions/ADR-005-tacp-token-aware-communication-protocol.md" ] && pass "T7: ADR-005-tacp exists" || fail "T7: ADR-005-tacp missing"

# Check: benchmark test document exists
[ -f "tests/token-savings/tacp-benchmark.md" ] && pass "T8: tacp-benchmark.md exists" || fail "T8: tacp-benchmark.md missing"

# Check: bootstrapped project gets tacp.md (Flow A already ran above — check PROJECT_A)
[ -f "$PROJECT_A/CoreAiWorkspaces/04-way-of-work/tacp.md" ] && pass "T9: tacp.md bootstrapped in new project (Flow A)" || fail "T9: tacp.md not bootstrapped in new project"

# Check: tacp.md in bootstrapped project has L2_LANG content
if grep -q "L2_LANG" "$PROJECT_A/CoreAiWorkspaces/04-way-of-work/tacp.md" 2>/dev/null; then
  pass "T10: bootstrapped tacp.md has L2_LANG config"
else
  fail "T10: bootstrapped tacp.md missing L2_LANG config"
fi

# Check: tacp.md header stripped correctly (no template meta-header leaked)
TACP_FIRST_LINE=$(head -1 "$PROJECT_A/CoreAiWorkspaces/04-way-of-work/tacp.md" 2>/dev/null)
if echo "$TACP_FIRST_LINE" | grep -q "^#"; then
  pass "T11: tacp.md starts with heading (template meta-header stripped correctly)"
else
  fail "T11: tacp.md has leaked template header — first line: '$TACP_FIRST_LINE'"
fi

# =============================================================================
# PROTOCOL CONTENT CHECKS — ตรวจ content ของ decision protocol + rules
# =============================================================================

section "Protocol Content — Decision Scenarios"

cd "$TEMPLATE_ROOT"

# P1: Scenario N exists in core/11
if grep -q "Scenario N" "core/11-ai-decision-protocol-template.md" 2>/dev/null; then
  pass "P1: Scenario N (ทำต่อ = per-task approval) exists in core/11"
else
  fail "P1: Scenario N missing from core/11 — blanket approval trap unaddressed"
fi

# P2: Scenario M has scope-check (step 7)
if grep -q "scope check" "core/11-ai-decision-protocol-template.md" 2>/dev/null; then
  pass "P2: Scenario M has scope-check step (entity/mechanic not in source docs)"
else
  fail "P2: Scenario M missing scope-check — scope expansion not caught"
fi

# P3: Scenario N is in Escalation table Level 2
if grep -q "Level 2" "core/11-ai-decision-protocol-template.md" 2>/dev/null && \
   grep -A2 "Level 2" "core/11-ai-decision-protocol-template.md" | grep -q "N"; then
  pass "P3: Scenario N added to Escalation Level 2 table"
else
  fail "P3: Scenario N not in Escalation table"
fi

# P4: ADR workflow has explicit blocking gate (STOP before implement)
if grep -q "STOP" "core/12-adr-template.md" 2>/dev/null && \
   grep -q "ห้าม implement" "core/12-adr-template.md" 2>/dev/null; then
  pass "P4: ADR workflow has blocking gate (STOP — ห้าม implement ก่อน Approve)"
else
  fail "P4: ADR workflow missing blocking gate — draft+implement collapse still possible"
fi

# P5: CLAUDE.md has Batch Checkpoint section
if grep -q "Batch Checkpoint" "platforms/claude-code/CLAUDE.md" 2>/dev/null; then
  pass "P5: CLAUDE.md has Batch Checkpoint section"
else
  fail "P5: CLAUDE.md missing Batch Checkpoint section"
fi

# P6: CLAUDE.md Key Rules has blanket-approval guard
if grep -q "ทำต่อ.*approve.*task" "platforms/claude-code/CLAUDE.md" 2>/dev/null || \
   grep -q "approve.*task.*ปัจจุบัน" "platforms/claude-code/CLAUDE.md" 2>/dev/null; then
  pass "P6: CLAUDE.md Key Rules has per-task approval rule (ทำต่อ ≠ blanket)"
else
  fail "P6: CLAUDE.md missing per-task approval guard in Key Rules"
fi

# P7: CLAUDE.md Branching section is reference-only (not full rules duplicated from core/21)
BRANCHING_LINES=$(grep -c "." "platforms/claude-code/CLAUDE.md" 2>/dev/null | tr -d ' ' || echo 0)
# Check that the full 9-rule table is NOT in CLAUDE.md (it should be in core/21 only)
if grep -q "| 1 |.*ก่อนเริ่มทุก task" "platforms/claude-code/CLAUDE.md" 2>/dev/null; then
  fail "P7: CLAUDE.md has duplicated 9-rule branching table — should reference core/21 only"
else
  pass "P7: CLAUDE.md Branching section is reference-only (no rule duplication)"
fi

# P8: Full branching rules exist in core/21 (the actual source)
if grep -q "Feature Branch Workflow" "core/21-git-workflow-template.md" 2>/dev/null && \
   grep -q "Promotion Pipeline" "core/21-git-workflow-template.md" 2>/dev/null; then
  pass "P8: Full branching rules exist in core/21 (single source of truth)"
else
  fail "P8: core/21 missing Feature Branch Workflow content"
fi

# P9: core/03 has Batch Checkpoint Rule
if grep -q "Batch Checkpoint" "core/03-way-of-work-template.md" 2>/dev/null; then
  pass "P9: core/03 way-of-work has Batch Checkpoint Rule (bootstraps to all projects)"
else
  fail "P9: core/03 missing Batch Checkpoint Rule"
fi

# P10: core/03 has body-first rule (body = source of truth, not AI-CONTEXT block)
if grep -q "body.*source of truth" "core/03-way-of-work-template.md" 2>/dev/null || \
   grep -q "body ของไฟล์คือ source of truth" "core/03-way-of-work-template.md" 2>/dev/null; then
  pass "P10: core/03 has body-first rule (body = source of truth, not block)"
else
  fail "P10: core/03 missing body-first rule — AI-CONTEXT reverse update still possible"
fi

# =============================================================================
# HOOK CONTENT CHECKS — ตรวจว่า hooks ทำงานถูกต้อง
# =============================================================================

section "Hook Content — session-stop + validate-commit"

cd "$TEMPLATE_ROOT"

# H1: session-stop.sh uses CoreAiWorkspaces/ not old ai/ path
if grep -q 'CoreAiWorkspaces' "platforms/claude-code/hooks/session-stop.sh" 2>/dev/null && \
   ! grep -q 'PROJECT_ROOT}/ai"' "platforms/claude-code/hooks/session-stop.sh" 2>/dev/null; then
  pass "H1: session-stop.sh uses CoreAiWorkspaces/ (not legacy ai/ path)"
else
  fail "H1: session-stop.sh still uses legacy ai/ path — checks will never find files"
fi

# H2: session-stop.sh checks task-board.md
if grep -q "task-board" "platforms/claude-code/hooks/session-stop.sh" 2>/dev/null; then
  pass "H2: session-stop.sh checks task-board.md"
else
  fail "H2: session-stop.sh does not check task-board.md — 3-file sync incomplete"
fi

# H3: session-stop.sh references /caw-session-end (not old /session-end)
if grep -q "caw-session-end" "platforms/claude-code/hooks/session-stop.sh" 2>/dev/null && \
   ! grep -q '"/session-end"' "platforms/claude-code/hooks/session-stop.sh" 2>/dev/null; then
  pass "H3: session-stop.sh references /caw-session-end (not old /session-end)"
else
  fail "H3: session-stop.sh references wrong command (/session-end instead of /caw-session-end)"
fi

# H4: session-stop.sh checks uncommitted changes (not just date)
if grep -q "DOCS_DIRTY\|diff --name-only" "platforms/claude-code/hooks/session-stop.sh" 2>/dev/null; then
  pass "H4: session-stop.sh checks uncommitted doc changes (not just date stamp)"
else
  fail "H4: session-stop.sh only checks date — uncommitted docs not caught"
fi

# H5: validate-commit.sh has doc-sync warning
if grep -q "CODE_STAGED\|DOCS_DIRTY" "platforms/claude-code/hooks/validate-commit.sh" 2>/dev/null; then
  pass "H5: validate-commit.sh has doc-sync check (warns when code staged but docs dirty)"
else
  fail "H5: validate-commit.sh missing doc-sync check — code commit without docs goes unwarned"
fi

# H6: validate-commit.sh references /caw-session-end in its warning
if grep -q "caw-session-end" "platforms/claude-code/hooks/validate-commit.sh" 2>/dev/null; then
  pass "H6: validate-commit.sh warns to run /caw-session-end"
else
  fail "H6: validate-commit.sh doc-sync warning doesn't point to /caw-session-end"
fi

# H7: validate-commit.sh escape valve logs to work-log-index.md (not just terminal)
if grep -q "SKIP_DOC_SYNC" "platforms/claude-code/hooks/validate-commit.sh" 2>/dev/null && \
   grep -q "work-log-index.md" "platforms/claude-code/hooks/validate-commit.sh" 2>/dev/null; then
  pass "H7: validate-commit.sh SKIP_DOC_SYNC escape valve logs to work-log-index.md"
else
  fail "H7: validate-commit.sh escape valve missing or doesn't log to work-log-index.md — skip leaves no audit trail"
fi

# =============================================================================
# PROTOCOL CHECKS (PART 2)
# =============================================================================

section "Protocol content — HARD RULE marker"

cd "$TEMPLATE_ROOT"

# P11: core/03 has HARD RULE classification table with ⛔ marker
if grep -q "HARD RULE" "core/03-way-of-work-template.md" 2>/dev/null && \
   grep -q "⛔" "core/03-way-of-work-template.md" 2>/dev/null; then
  pass "P11: core/03 has HARD RULE classification (⛔ marker) — AI knows what cannot be bypassed"
else
  fail "P11: core/03 missing HARD RULE classification — all rules appear equal weight to AI"
fi

# =============================================================================
# UNIVERSAL AI.md CHECKS
# =============================================================================

section "Universal AI.md — entry point completeness"

cd "$TEMPLATE_ROOT"

# U1: AI.md exists
[ -f "platforms/universal/AI.md" ] && pass "U1: platforms/universal/AI.md exists" || fail "U1: AI.md missing"

# U2: AI.md references Scenario M
if grep -q "Scenario M" "platforms/universal/AI.md" 2>/dev/null; then
  pass "U2: AI.md references Scenario M (pre-code checklist) in Session Start"
else
  fail "U2: AI.md missing Scenario M reference — new tools won't know about pre-code check"
fi

# U3: AI.md has file ownership table
if grep -q "Tool-Specific" "platforms/universal/AI.md" 2>/dev/null && \
   grep -q "System Files" "platforms/universal/AI.md" 2>/dev/null; then
  pass "U3: AI.md has file ownership table (Shared / Tool-Specific / System)"
else
  fail "U3: AI.md missing file ownership table"
fi

# U4: core/00 has architecture diagram (core/=rules, platforms/=wiring)
if grep -q "สถาปัตยกรรมของระบบ" "core/00-ai-bootstrap-master-template.md" 2>/dev/null; then
  pass "U4: core/00 has architecture diagram explaining core/ vs platforms/ roles"
else
  fail "U4: core/00 missing architecture diagram — AI may duplicate rules in platforms/"
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
