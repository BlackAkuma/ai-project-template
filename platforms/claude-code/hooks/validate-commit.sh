#!/bin/bash
# Hook: validate-commit
# รันอัตโนมัติก่อน git commit
# Event: PreToolUse (Bash tool ที่มี "git commit")

echo "=== Pre-Commit Compliance Check ==="

FAIL=0

# C-11 Security — ห้าม commit secrets
echo "Checking for hardcoded secrets..."
SECRET_PATTERNS="(password|secret|api_key|apikey|token|private_key)[[:space:]]*=[[:space:]]*[\"'][^\"']{8,}"
if git diff --cached | grep -iE "$SECRET_PATTERNS" > /dev/null 2>&1; then
  echo "[FAIL] Possible hardcoded secret detected in staged changes"
  git diff --cached | grep -iE "$SECRET_PATTERNS"
  FAIL=$((FAIL + 1))
else
  echo "[OK] No hardcoded secrets found"
fi

# C-04 — ห้าม commit placeholder
echo "Checking for unresolved placeholders..."
if git diff --cached | grep -E '<NEEDS_CLARIFICATION|<PROJECT_NAME>|<CURRENT_DATE>' > /dev/null 2>&1; then
  echo "[WARN] Unresolved placeholders in staged changes — review before commit"
fi

# C-14 — warn เมื่อ commit มี reference ถึง deprecated entity
echo "Checking for deprecated entity references..."
if git diff --cached | grep -E '\[ENTITY:deprecated:' > /dev/null 2>&1; then
  echo "[WARN] Deprecated entity tag found in staged changes"
  echo "       ตรวจ CoreAiWorkspaces/07-decisions/entity-register.md ว่าใช้ entity ที่ถูกต้องหรือไม่"
  git diff --cached | grep -E '\[ENTITY:deprecated:'
fi

# G-06 — ห้าม commit prototype code เข้า main
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  echo "Checking for prototype code on main branch..."
  if git diff --cached | grep "// PROTOTYPE:" > /dev/null 2>&1; then
    echo "[FAIL] Prototype code found in commit to $CURRENT_BRANCH"
    git diff --cached | grep "// PROTOTYPE:"
    FAIL=$((FAIL + 1))
  else
    echo "[OK] No prototype code"
  fi
fi

# Doc Sync Check — ถ้า commit มี code files แต่ core docs มี unstaged changes
CODE_STAGED=$(git diff --cached --name-only | grep -v "^CoreAiWorkspaces/" | grep -c "." 2>/dev/null || echo 0)
DOCS_DIRTY=$(git diff --name-only -- \
  "CoreAiWorkspaces/01-plan/work-status.md" \
  "CoreAiWorkspaces/02-task/task-board.md" \
  "CoreAiWorkspaces/03-log/work-log-index.md" 2>/dev/null | wc -l | tr -d ' ')

if [ "$CODE_STAGED" -gt 0 ] && [ "$DOCS_DIRTY" -gt 0 ]; then
  # Escape valve: SKIP_DOC_SYNC=1 git commit ... อนุญาตให้ข้ามได้ แต่ต้อง log ไว้เสมอ
  if [ "${SKIP_DOC_SYNC:-0}" = "1" ]; then
    echo "[SKIP] Doc sync check bypassed via SKIP_DOC_SYNC=1"
    LOG_FILE="CoreAiWorkspaces/03-log/work-log-index.md"
    if [ -f "$LOG_FILE" ]; then
      SKIP_ENTRY="- [SKIP_DOC_SYNC] $(date '+%Y-%m-%d %H:%M') — doc sync check bypassed; docs still dirty at commit"
      echo "$SKIP_ENTRY" >> "$LOG_FILE"
      echo "       Logged skip entry to $LOG_FILE"
    else
      echo "[WARN] work-log-index.md not found — skip not logged (audit trail missing)"
    fi
  else
    echo "[WARN] Code staged but CoreAiWorkspaces docs have pending changes:"
    git diff --name-only -- \
      "CoreAiWorkspaces/01-plan/work-status.md" \
      "CoreAiWorkspaces/02-task/task-board.md" \
      "CoreAiWorkspaces/03-log/work-log-index.md" 2>/dev/null
    echo "       รัน /caw-session-end เพื่อ sync docs ก่อน push"
    echo "       (หรือใช้ SKIP_DOC_SYNC=1 git commit ... เพื่อข้าม — จะ log ไว้ใน work-log-index.md)"
  fi
fi

if [ $FAIL -gt 0 ]; then
  echo ""
  echo "[BLOCKED] $FAIL critical issue(s) must be resolved before commit"
  exit 1
else
  echo "[OK] Pre-commit check passed"
fi
