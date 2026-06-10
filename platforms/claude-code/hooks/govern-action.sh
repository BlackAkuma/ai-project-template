#!/bin/bash
# Claude Code PreToolUse hook — governance on REAL agent actions (BRD-v2 A2)
# The engine (not bash) decides. Reads the tool-call JSON on stdin; if the action is risky,
# runs the matching engine gate; blocks (exit 2) when the engine returns a block verdict.
# exit 0 = allow · exit 2 = block (stderr reason is shown to the agent).
#
# Wire in .claude/settings.json:  PreToolUse → matcher "Bash" → command "bash platforms/claude-code/hooks/govern-action.sh"

input=$(cat)

# TEMPLATE-ONLY MODE: ถ้าโปรเจ็กต์นี้ไม่มี engine/ (คนเอาเฉพาะ template ไปใช้) → ผ่านเงียบๆ
# template ต้องใช้ standalone ได้เสมอ — engine เป็น optional layer (BRD-v2 N6)
_SD="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f "${ENGINE_DIR:-$_SD/../../..}/engine/check.py" ]; then
  exit 0
fi

# extract the bash command from the tool call (engine/python is required anyway)
cmd=$(printf '%s' "$input" | python -c "import sys,json
try:
    d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))
except Exception: print('')" 2>/dev/null)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE="${ENGINE_DIR:-$SCRIPT_DIR/../../..}/engine/check.py"

run_gate() {
  out=$(python "$ENGINE" "$1" --root "$(pwd)" 2>&1)
  code=$?
  if [ "$code" = "1" ]; then
    echo "🛡️ GOVERNANCE BLOCK ($1): the engine checked real state and refused this action." >&2
    echo "$out" | grep -i "fail\|missing\|block" | head -3 >&2
    exit 2
  fi
}

CLI="${ENGINE_DIR:-$SCRIPT_DIR/../../..}/engine/cli.py"

hold_for_approval() {  # risky-but-not-forbidden (L2) -> Decision Inbox, agent waits for human
  python "$CLI" hold "$1" "$2" "$3" --risk 2 --root "$(pwd)" >/dev/null 2>&1
  echo "🟡 HELD FOR YOUR APPROVAL: \"$3\" — risk action queued to the Decision Inbox." >&2
  echo "   Review + approve/reject in the Cockpit before this runs." >&2
  exit 2
}

case "$cmd" in
  *"git commit"*)
    run_gate secret-scan       # C-11 (L3 hard-stop): no secrets into git
    run_gate placeholder-scan  # C-04: no unresolved placeholders
    ;;
  *"push --force"*|*"push -f"*|*"reset --hard"*|*"branch -D"*|*"clean -fd"*|*"push --force-with-lease"*)
    hold_for_approval risky_git_op "$cmd" "dangerous git operation (rewrites/deletes history or work)"
    ;;
esac

exit 0
