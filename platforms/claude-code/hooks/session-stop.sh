#!/bin/bash
# Hook: session-stop
# รันอัตโนมัติก่อนจบ Claude Code session
# Event: PostToolUse (หลัง tool สุดท้ายของ session)

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
DOC_DIR="$PROJECT_ROOT/CoreAiWorkspaces"

echo "=== Session End Check ==="

MISSING=0

# ตรวจว่า work-status อัปเดตวันนี้
STATUS_FILE="$DOC_DIR/01-plan/work-status.md"
if [ -f "$STATUS_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  if grep -q "updated: $TODAY" "$STATUS_FILE"; then
    echo "[OK] work-status updated today"
  else
    echo "[WARN] work-status may not be updated today — check before closing"
    MISSING=$((MISSING + 1))
  fi
fi

# ตรวจว่า work-log-index มี entry วันนี้
LOG_FILE="$DOC_DIR/03-log/work-log-index.md"
if [ -f "$LOG_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  if grep -q "$TODAY" "$LOG_FILE"; then
    echo "[OK] work-log-index has entry for today"
  else
    echo "[WARN] No log entry for today — add session summary before closing"
    MISSING=$((MISSING + 1))
  fi
fi

# ตรวจว่า task-board ไม่มี task ที่ status ยังไม่ sync
TASK_FILE="$DOC_DIR/02-task/task-board.md"
if [ -f "$TASK_FILE" ]; then
  # ตรวจ uncommitted changes ใน task-board
  if git -C "$PROJECT_ROOT" diff --name-only -- "CoreAiWorkspaces/02-task/task-board.md" 2>/dev/null | grep -q "task-board"; then
    echo "[WARN] task-board.md has uncommitted changes — commit หรือ sync ก่อนปิด"
    MISSING=$((MISSING + 1))
  else
    echo "[OK] task-board is committed"
  fi
fi

# ตรวจว่า core docs ไม่มี uncommitted changes ค้าง
DOCS_DIRTY=$(git -C "$PROJECT_ROOT" diff --name-only -- \
  "CoreAiWorkspaces/01-plan/work-status.md" \
  "CoreAiWorkspaces/02-task/task-board.md" \
  "CoreAiWorkspaces/03-log/work-log-index.md" 2>/dev/null | wc -l | tr -d ' ')

if [ "$DOCS_DIRTY" -gt 0 ]; then
  echo "[WARN] Core docs have uncommitted changes — รัน /caw-session-end แล้ว commit ก่อนปิด"
  MISSING=$((MISSING + 1))
fi

if [ $MISSING -gt 0 ]; then
  echo ""
  echo "[ACTION REQUIRED] $MISSING item(s) need attention before closing session"
  echo "รัน /caw-session-end เพื่อ sync work-status + work-log + task-board ครบในขั้นตอนเดียว"
else
  echo "[OK] All end-of-session checks passed"
fi

echo "=== Done ==="
