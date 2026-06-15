#!/bin/bash
# session-debt.sh — SessionStart hook, TEMPLATE-ONLY (R6: เห็นหนี้คาตา)
# ฉีดบรรทัด "หนี้วินัย" เข้า context ทุก session — feedback loop ที่ไม่เคยมี
# stdout → ถูกเพิ่มเข้า AI context

[ -d "CoreAiWorkspaces" ] || exit 0
WL="CoreAiWorkspaces/03-log/work-log-index.md"
WS="CoreAiWorkspaces/01-plan/work-status.md"

echo "[GOVERNANCE-DEBT]"
CUR=$(git branch --show-current 2>/dev/null)
DEV=$(grep -m1 "git_dev_branch:" "$WS" 2>/dev/null | sed 's/.*://' | tr -d ' \r'); DEV=${DEV:-dev}
PROD=$(grep -m1 "git_prod_branch:" "$WS" 2>/dev/null | sed 's/.*://' | tr -d ' \r')
echo "branch: $CUR$( [ "$CUR" = "$PROD" ] && echo ' ⚠️ PROD BRANCH — หยุด แจ้ง user ก่อน' )"

if [ -f "$WL" ]; then
  LAST_LOG=$(grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' "$WL" | sort -r | head -1)
  TODAY=$(date +%Y-%m-%d)
  if [ -n "$LAST_LOG" ]; then
    DAYS=$(( ( $(date -d "$TODAY" +%s 2>/dev/null || date +%s) - $(date -d "$LAST_LOG" +%s 2>/dev/null || date +%s) ) / 86400 ))
    [ "$DAYS" -gt 1 ] && echo "log_debt: ⚠️ work-log entry ล่าสุด $LAST_LOG (ค้าง $DAYS วัน) — sync ก่อนเริ่มงานใหม่" || echo "log_debt: none (last: $LAST_LOG)"
  fi
fi
IP=$(grep -c "in_progress" CoreAiWorkspaces/02-task/task-board.md 2>/dev/null || echo 0)
echo "tasks_in_progress: $IP"
echo "rules: โค้ดใหม่=แตก feature branch · commit ต้องมี T-xxx · done ต้องมี log+evidence · ห้ามแตะ 00-source ตรง"
exit 0
