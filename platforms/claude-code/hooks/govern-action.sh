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
  # FU-3: bind approval to a canonical SCOPE (the command itself) so a reworded retry can't escape a
  # prior reject. The engine canonicalizes (whitespace/case/quoting); we pass the raw command as scope.
  state=$(python "$CLI" approval-state "$1" "$R" --scope "$2" --root "$(pwd)" 2>/dev/null | tail -1)
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
  python "$CLI" hold "$1" "$2" "$R" --scope "$2" --risk 2 --root "$(pwd)" >/dev/null 2>&1
  echo "🟡 HELD FOR YOUR APPROVAL: \"$3\" — queued to the Decision Inbox." >&2
  echo "   Review + approve/reject in the Cockpit (http://127.0.0.1:8777), then retry." >&2
  exit 2
}

# USER-ORDER BYPASS (consume-once) — แทน GOVERN_USER_ORDER env ที่ใช้ไม่ได้ผ่าน Claude Code
# (hook ไม่ inherit env ของ command). user/AI สั่งโดย: touch engine/.govern-allow-once ก่อน command
# bypass ได้เฉพาะ dev-freeze + risky-hold เท่านั้น — secret/placeholder/MASTER freeze ยัง HARD เสมอ
BYPASS=0
ALLOW_ONCE="$(pwd)/engine/.govern-allow-once"
if [ -f "$ALLOW_ONCE" ]; then BYPASS=1; rm -f "$ALLOW_ONCE"; fi

# strip quoted strings (commit messages ฯลฯ) ก่อน match — กัน false-positive จากคำใน -m "..."
CMD_NOQ=$(printf '%s' "$cmd" | sed 's/"[^"]*"//g; s/'"'"'[^'"'"']*'"'"'//g')
CURB=$(git -C "$(pwd)" branch --show-current 2>/dev/null)
# โค้ดที่ staged (นอก CoreAiWorkspaces และไม่ใช่ .md) — doc-only = ไม่นับเป็นงานฟีเจอร์
CODE_STAGED=$(git -C "$(pwd)" diff --cached --name-only 2>/dev/null | grep -vE '^CoreAiWorkspaces/|\.md$' | head -1)

# MASTER FREEZE (user rule 2026-06-11): HARD — ไม่มี bypass. precise patterns กัน false-positive
# (เดิม *push*master* จับ "git stash push -m ...master..." ผิด)
case "$CMD_NOQ" in
  *"git push"*master*|*"git checkout master"*|*"git switch master"*|*"checkout -B master"*|*"checkout -b master"*|*"git merge"*master*)
    echo "⛔ MASTER FREEZE: ห้ามแตะ master จนกว่า user สั่งปลดอย่างเป็นทางการ (rule 2026-06-11)" >&2
    exit 2 ;;
esac
case "$CMD_NOQ" in
  *"git commit"*|*"git merge"*) [ "$CURB" = "master" ] && { echo "⛔ MASTER FREEZE: ห้าม commit/merge บน master (rule 2026-06-11)" >&2; exit 2; } ;;
esac

# DEV DIRECT FREEZE (user rule 2026-06-11): งานฟีเจอร์ต้องแยก branch — แต่ doc-only commit บน dev ผ่านได้
if [ -f "$(pwd)/engine/.dev-direct-freeze" ] && [ "$BYPASS" != "1" ]; then
  case "$CMD_NOQ" in
    *"git commit"*)
      if [ "$CURB" = "dev" ] && [ -n "$CODE_STAGED" ]; then
        echo "⛔ DEV DIRECT FREEZE: ห้าม commit โค้ดตรงบน dev — แตก feature/<id> ก่อน (doc-only ผ่านได้)" >&2
        echo "   bypass มีคำสั่ง user: touch engine/.govern-allow-once แล้วรันใหม่" >&2
        exit 2
      fi ;;
  esac
fi

case "$CMD_NOQ" in
  *"git commit"*)
    run_gate secret-scan       # C-11 (L3 hard-stop): no secrets into git — HARD, no bypass
    run_gate placeholder-scan  # C-04: no unresolved placeholders
    # DEV-FP: traceability — code commit ต้องผูก task (T-xxx/BL-xx/SPIKE) — forward-port จาก master pack
    if [ -n "$CODE_STAGED" ] && [ "$BYPASS" != "1" ]; then
      MSG=$(printf '%s' "$cmd" | grep -oE "\-m[[:space:]]+\"[^\"]*\"|\-m[[:space:]]+'[^']*'" | head -1)
      if [ -n "$MSG" ] && ! printf '%s' "$MSG" | grep -qE 'T-[0-9]+|BL-[0-9]+|SPIKE|hotfix|FU-[0-9]+|DEV-FP|RD-[0-9]+|OBS-[0-9]+'; then
        echo "⛔ BLOCK: commit โค้ดต้องผูก task — ใส่ T-xxx/BL-xx/FU-x/SPIKE ใน message (traceability)" >&2
        exit 2
      fi
    fi
    ;;
esac

# RISKY GIT (FU-4): real tokenizer (engine/gitguard) instead of fragile substring globs — catches
# flag-order ('push origin main --force'), refspec-force ('push origin +master'), and ws evasion.
# Detect on CMD_NOQ (quotes stripped -> no commit-message false-positive); scope/hold on raw $cmd.
GITRISK=$(python "$CLI" git-risk "$CMD_NOQ" 2>/dev/null | tail -1)
if [ -n "$GITRISK" ]; then
  [ "$BYPASS" = "1" ] && exit 0
  hold_for_approval risky_git_op "$cmd" "$GITRISK"
fi

exit 0
