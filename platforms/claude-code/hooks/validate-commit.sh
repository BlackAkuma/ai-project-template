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

if [ $FAIL -gt 0 ]; then
  echo ""
  echo "[BLOCKED] $FAIL critical issue(s) must be resolved before commit"
  exit 1
else
  echo "[OK] Pre-commit check passed"
fi
