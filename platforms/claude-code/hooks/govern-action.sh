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

hold_for_approval() {  # risky-but-not-forbidden (L2) -> Decision Inbox; human decision is CAUSAL:
  # approved (unconsumed) -> allow ONCE · pending -> keep blocked, NO duplicate · rejected -> blocked
  # approval is scoped to THIS exact command (reason includes the command string)
  R="$3 :: $2"
  state=$(python "$CLI" approval-state "$1" "$R" --root "$(pwd)" 2>/dev/null | tail -1)
  case "$state" in
    approved)
      echo "✅ APPROVED in Decision Inbox — allowing this action once (approval consumed, audited)." >&2
      exit 0 ;;
    pending)
      echo "🟡 STILL WAITING: \"$3\" is already in the Decision Inbox — approve/reject in the Cockpit first." >&2
      exit 2 ;;
    rejected)
      echo "🔴 REJECTED earlier in the Decision Inbox — this action stays blocked." >&2
      exit 2 ;;
  esac
  python "$CLI" hold "$1" "$2" "$R" --risk 2 --root "$(pwd)" >/dev/null 2>&1
  echo "🟡 HELD FOR YOUR APPROVAL: \"$3\" — queued to the Decision Inbox." >&2
  echo "   Review + approve/reject in the Cockpit (http://127.0.0.1:8777), then retry." >&2
  exit 2
}

# DEV DIRECT FREEZE (user rule 2026-06-11): งานฟีเจอร์ทุกชนิดต้องอยู่บน branch แยก —
# ห้าม commit ตรงบน dev (merge จาก feature branch ทำได้). เปิดใช้เมื่อมี marker engine/.dev-direct-freeze
# bypass เฉพาะมีคำสั่ง user ชัดเจน: GOVERN_USER_ORDER=1
if [ -f "$(pwd)/engine/.dev-direct-freeze" ] && [ "${GOVERN_USER_ORDER:-0}" != "1" ]; then
  case "$cmd" in
    *"git commit"*)
      CURB=$(git -C "$(pwd)" branch --show-current 2>/dev/null)
      if [ "$CURB" = "dev" ]; then
        echo "⛔ DEV DIRECT FREEZE: ห้าม commit ตรงบน dev — แตก feature/<id> ก่อนเสมอ (user rule 2026-06-11)" >&2
        echo "   (merge จาก feature branch = ทำได้ปกติ · มีคำสั่ง user: ใส่ GOVERN_USER_ORDER=1)" >&2
        exit 2
      fi ;;
  esac
fi

# MASTER FREEZE (user rule 2026-06-11): ห้ามอัปเดต master ทุกกรณีจนกว่า user สั่งอย่างเป็นทางการ
# hard block — ไม่มีทาง approve ผ่าน Inbox (ปลดได้ทางเดียว: user สั่ง + แก้กฎนี้อย่างเป็นทางการ)
case "$cmd" in
  *"push"*master*|*"push origin master"*|*"checkout master"*|*"switch master"*|*"merge"*" master"*)
    echo "⛔ MASTER FREEZE: user ห้ามอัปเดต/แตะ master ทุกกรณีจนกว่าจะสั่งอย่างเป็นทางการ (rule 2026-06-11)" >&2
    exit 2 ;;
esac

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
