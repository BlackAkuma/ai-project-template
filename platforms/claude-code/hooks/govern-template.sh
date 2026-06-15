#!/bin/bash
# govern-template.sh — PreToolUse(Bash) gate, TEMPLATE-ONLY (ไม่ต้องมี engine/)
# แก้ปัญหาจริงจากผู้ใช้: AI ละเลยกฎ prose → เปลี่ยนกฎสำคัญเป็น "ด่านที่เครื่องบังคับ"
#   1) commit ที่มี secret/placeholder           → BLOCK (C-11/C-04)
#   2) commit "โค้ด" ตรงบน dev branch            → BLOCK: แตก feature/<id> ก่อน (doc-only ผ่านได้)
#   3) commit โค้ดโดย message ไม่มี T-xxx/SPIKE   → BLOCK: ผูกงานกับ task เสมอ (C-02/C-03)
# exit 0 = allow · exit 2 = block (เหตุผลทาง stderr → AI เห็นและแก้ถูกจุด)
# escape เฉพาะมีคำสั่ง user ชัดเจน: GOVERN_USER_ORDER=1 (ทุกการ bypass ควรถูกบันทึกใน work-log)

input=$(cat)
[ "${GOVERN_USER_ORDER:-0}" = "1" ] && exit 0

cmd=$(printf '%s' "$input" | python -c "import sys,json
try: print(json.load(sys.stdin).get('tool_input',{}).get('command',''))
except Exception: print('')" 2>/dev/null)
case "$cmd" in *"git commit"*) ;; *) exit 0 ;; esac

# --- เก็บข้อมูล staged ---
STAGED=$(git diff --cached --name-only 2>/dev/null)
[ -z "$STAGED" ] && exit 0
CODE_STAGED=$(printf '%s\n' "$STAGED" | grep -vE '^CoreAiWorkspaces/|\.md$' | head -1)

# --- 1) secrets / placeholders ใน staged diff ---
SECRET_PAT='(api[_-]?key|secret|password|passwd|token|private[_-]?key)[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']{8,}'
if git diff --cached | grep -qiE "$SECRET_PAT" 2>/dev/null; then
  echo "⛔ BLOCK: พบ hardcoded secret ใน staged diff — ย้ายไป env/secret store ก่อน commit (C-11)" >&2
  exit 2
fi
if git diff --cached | grep -qE '<NEEDS_CLARIFICATION|<PROJECT_NAME>|<CURRENT_DATE>' 2>/dev/null; then
  echo "⛔ BLOCK: placeholder ยังค้างใน staged diff — แก้ให้เสร็จก่อน commit (C-04)" >&2
  exit 2
fi

# --- 2) branch-per-feature: โค้ดห้าม commit ตรงบน dev (doc/CoreAiWorkspaces ผ่านได้) ---
DEV_BRANCH=$(grep -m1 "git_dev_branch:" CoreAiWorkspaces/01-plan/work-status.md 2>/dev/null | sed 's/.*git_dev_branch:[[:space:]]*//' | tr -d ' \r')
DEV_BRANCH=${DEV_BRANCH:-dev}
CUR=$(git branch --show-current 2>/dev/null)
if [ "$CUR" = "$DEV_BRANCH" ] && [ -n "$CODE_STAGED" ]; then
  echo "⛔ BLOCK: ห้าม commit โค้ดตรงบน '$DEV_BRANCH' — แตก branch ก่อน: git checkout -b feature/<task-id>-<ชื่อ>" >&2
  echo "   (commit เฉพาะ docs/CoreAiWorkspaces = ผ่านได้ · มีคำสั่ง user: GOVERN_USER_ORDER=1)" >&2
  exit 2
fi

# --- 3) traceability: โค้ด commit ต้องอ้าง task ---
MSG=$(printf '%s' "$cmd" | grep -oE '\-m[[:space:]]+"[^"]*"|\-m[[:space:]]+'"'"'[^'"'"']*'"'"'' | head -1)
if [ -n "$CODE_STAGED" ] && [ -n "$MSG" ] && ! printf '%s' "$MSG" | grep -qE 'T-[0-9]+|SPIKE|BL-[0-9]+|hotfix'; then
  echo "⛔ BLOCK: commit โค้ดต้องผูกกับ task — ใส่ T-xxx / BL-xx / SPIKE ใน message (เช่น \"T-041: ...\")" >&2
  echo "   ยังไม่มี task? ลงทะเบียนใน CoreAiWorkspaces/02-task/task-board.md ก่อน (กันงานหลุด tracking)" >&2
  exit 2
fi

exit 0
