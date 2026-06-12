#!/bin/bash
# test-enforcement-pack.sh — เทส Enforcement Pack (template-only) ครบทุกด่าน
# รัน: bash tests/hooks/test-enforcement-pack.sh
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
GT="$ROOT/platforms/claude-code/hooks/govern-template.sh"
GD="$ROOT/platforms/claude-code/hooks/govern-docs.sh"
SE="$ROOT/platforms/claude-code/hooks/session-end-gate.sh"
SD="$ROOT/platforms/claude-code/hooks/session-debt.sh"
PASS=0; FAIL=0
ok(){ echo "  PASS  $1"; PASS=$((PASS+1)); }
no(){ echo "  FAIL  $1"; FAIL=$((FAIL+1)); }
check(){ [ "$2" = "$3" ] && ok "$1" || no "$1 (got exit $2, want $3)"; }
bashcall(){ printf '{"tool_name":"Bash","tool_input":{"command":"%s"}}' "$1"; }
editcall(){ printf '{"tool_name":"Edit","tool_input":{"file_path":"%s","new_string":"%s"}}' "$1" "$2"; }

mkrepo(){
  D=$(mktemp -d); cd "$D"
  git init -q -b dev; git config user.email t@t; git config user.name t
  mkdir -p CoreAiWorkspaces/01-plan CoreAiWorkspaces/02-task CoreAiWorkspaces/03-log
  printf '<!-- AI-CONTEXT\ngit_dev_branch: dev\ngit_prod_branch: master\n-->\n' > CoreAiWorkspaces/01-plan/work-status.md
  printf '<!-- AI-CONTEXT\ndone: []\n-->\n' > CoreAiWorkspaces/02-task/task-board.md
  printf '# Work Log\n' > CoreAiWorkspaces/03-log/work-log-index.md
  git add .; git commit -qm "T-000: init"
}

echo "=== govern-template.sh (Bash gate) ==="
mkrepo
echo 'x = 1' > app.py; git add app.py
bashcall "git commit -m 'T-001: add app'" | bash "$GT"; check "secret-free code + T-ref + feature... wait on dev -> BLOCK" $? 2
git checkout -q -b feature/T-001-app
bashcall "git commit -m 'T-001: add app'" | bash "$GT"; check "same commit on feature branch -> ALLOW" $? 0
bashcall "git commit -m 'add app no ref'" | bash "$GT"; check "code commit without T-ref -> BLOCK" $? 2
echo 'api_key = "sk-secret12345678"' > leak.py; git add leak.py
bashcall "git commit -m 'T-002: leak'" | bash "$GT"; check "secret staged -> BLOCK" $? 2
git reset -q leak.py; rm leak.py
git checkout -q dev
git reset -q app.py 2>/dev/null; rm -f app.py
echo 'note' > CoreAiWorkspaces/03-log/note.md; git add CoreAiWorkspaces/
bashcall "git commit -m 'sync docs'" | bash "$GT"; check "doc-only commit on dev -> ALLOW" $? 0
GOVERN_USER_ORDER=1 bashcall "git commit -m 'x'" | GOVERN_USER_ORDER=1 bash "$GT"; check "user-order bypass -> ALLOW" $? 0

echo "=== govern-docs.sh (Edit/Write gate) ==="
mkdir -p CoreAiWorkspaces/00-source/versions/v1
editcall "$D/CoreAiWorkspaces/00-source/brd.md" "changed requirement" | bash "$GD"; check "edit source doc directly -> BLOCK" $? 2
editcall "$D/CoreAiWorkspaces/00-source/versions/v1/brd.md" "new version" | bash "$GD"; check "add new VERSION -> ALLOW" $? 0
editcall "$D/CoreAiWorkspaces/02-task/task-board.md" "T-123 [done] finished" | bash "$GD"; check "mark done WITHOUT log entry -> BLOCK" $? 2
echo "- T-123 done: built X, tests green" >> CoreAiWorkspaces/03-log/work-log-index.md
editcall "$D/CoreAiWorkspaces/02-task/task-board.md" "T-123 [done] finished" | bash "$GD"; check "mark done WITH log entry -> ALLOW" $? 0
editcall "$D/src/main.py" "print(1)" | bash "$GD"; check "normal code edit -> ALLOW" $? 0

echo "=== session-end-gate.sh (Stop gate) ==="
git checkout -q -b feature/T-009-work
echo 'y=2' > code.py; git add code.py; git commit -qm "T-009: work"
printf '{}' | bash "$SE"; check "code committed today + NO log today -> BLOCK stop" $? 2
echo "- $(date +%Y-%m-%d) T-009: did work, evidence ok" >> CoreAiWorkspaces/03-log/work-log-index.md
printf '{}' | bash "$SE"; check "log entry today exists -> ALLOW stop" $? 0
printf '{"stop_hook_active": true}' | bash "$SE"; check "loop-guard stop_hook_active -> ALLOW" $? 0

echo "=== session-debt.sh (SessionStart debt line) ==="
OUT=$(bash "$SD")
echo "$OUT" | grep -q "GOVERNANCE-DEBT" && ok "debt header present" || no "debt header missing"
echo "$OUT" | grep -q "branch:" && ok "branch line present" || no "branch line missing"

cd "$ROOT"; rm -rf "$D"
echo ""
echo "ผล: $PASS PASS / $FAIL FAIL"
[ "$FAIL" = "0" ] && echo "[OK] enforcement-pack tests passed" || exit 1
