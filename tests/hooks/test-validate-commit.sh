#!/bin/bash
# Test: validate-commit.sh
# ทดสอบ 5 cases สำหรับ C-11, C-14, C-04, G-06

SCRIPT="platforms/claude-code/hooks/validate-commit.sh"
PASS=0
FAIL=0

# helper
assert_contains() {
  local desc="$1" expected="$2" actual="$3"
  if echo "$actual" | grep -q "$expected"; then
    echo "[PASS] $desc"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $desc"
    echo "       expected to find: $expected"
    echo "       got: $(echo "$actual" | head -5)"
    FAIL=$((FAIL + 1))
  fi
}

assert_not_contains() {
  local desc="$1" unexpected="$2" actual="$3"
  if echo "$actual" | grep -q "$unexpected"; then
    echo "[FAIL] $desc — should NOT contain: $unexpected"
    FAIL=$((FAIL + 1))
  else
    echo "[PASS] $desc"
    PASS=$((PASS + 1))
  fi
}

assert_exit_code() {
  local desc="$1" expected="$2" actual="$3"
  if [ "$actual" -eq "$expected" ]; then
    echo "[PASS] $desc (exit $actual)"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $desc — expected exit $expected, got $actual"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Testing validate-commit.sh ==="
echo ""

# ---- setup: สร้าง temp git repo สำหรับทดสอบ ----
TMPDIR=$(mktemp -d)
cd "$TMPDIR"
git init -q
git config user.email "test@test.com"
git config user.name "Test"
# สร้าง initial commit เพื่อให้ git diff --cached ทำงานได้
touch .gitkeep && git add .gitkeep && git commit -q -m "init"
HOOK="$(cd - > /dev/null && pwd)/$SCRIPT"

# ---- Case 1: C-14 — ไฟล์มี [ENTITY:deprecated:Redux] ต้องได้ WARN ----
echo "--- Case 1: deprecated entity tag ---"
cat > test.md << 'EOF'
ใช้ [ENTITY:deprecated:Redux] สำหรับ state management
EOF
git add test.md
OUTPUT=$(bash "$HOOK" 2>&1)
assert_contains "C-14 warns on deprecated entity" "WARN" "$OUTPUT"
assert_contains "C-14 mentions entity-register" "entity-register" "$OUTPUT"
git reset HEAD test.md > /dev/null
rm test.md

# ---- Case 2: ไฟล์ปกติไม่มี deprecated tag ต้องไม่มี WARN ----
echo "--- Case 2: no deprecated tag — no warn ---"
cat > test.md << 'EOF'
ใช้ React สำหรับ UI framework
JWT สำหรับ authentication
EOF
git add test.md
OUTPUT=$(bash "$HOOK" 2>&1)
assert_not_contains "no false positive on clean file" "ENTITY" "$OUTPUT"
git reset HEAD test.md > /dev/null
rm test.md

# ---- Case 3: C-11 — hardcoded secret ต้อง FAIL และ exit 1 ----
echo "--- Case 3: hardcoded secret — must block ---"
cat > config.js << 'EOF'
const api_key = "sk-abc123def456ghi789jkl"
EOF
git add config.js
OUTPUT=$(bash "$HOOK" 2>&1)
EXIT_CODE=$?
assert_contains "C-11 detects hardcoded secret" "FAIL" "$OUTPUT"
assert_exit_code "C-11 exits with code 1" 1 $EXIT_CODE
git reset HEAD config.js > /dev/null
rm config.js

# ---- Case 4: C-04 — placeholder ต้องได้ WARN ----
echo "--- Case 4: unresolved placeholder ---"
cat > doc.md << 'EOF'
Project name: <PROJECT_NAME>
Goal: build something
EOF
git add doc.md
OUTPUT=$(bash "$HOOK" 2>&1)
assert_contains "C-04 warns on placeholder" "WARN" "$OUTPUT"
git reset HEAD doc.md > /dev/null
rm doc.md

# ---- Case 5: ไฟล์สะอาดทุกอย่าง ต้อง exit 0 ----
echo "--- Case 5: clean file — must pass ---"
cat > clean.md << 'EOF'
# Notes
Using PostgreSQL for database, JWT for auth.
All decisions documented in ADR-001.
EOF
git add clean.md
OUTPUT=$(bash "$HOOK" 2>&1)
EXIT_CODE=$?
assert_exit_code "clean file exits with code 0" 0 $EXIT_CODE
assert_contains "clean file shows OK" "OK" "$OUTPUT"
git reset HEAD clean.md > /dev/null
rm clean.md

# ---- cleanup ----
cd - > /dev/null
rm -rf "$TMPDIR"

echo ""
echo "=== Results ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "[ALL TESTS PASSED]"
  exit 0
else
  echo "[TESTS FAILED] $FAIL test(s) failed"
  exit 1
fi
