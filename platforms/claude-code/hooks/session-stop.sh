#!/bin/bash
# Hook: session-stop
# รันอัตโนมัติก่อนจบ Claude Code session
# Event: PostToolUse (หลัง tool สุดท้ายของ session)

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
DOC_DIR="$PROJECT_ROOT/doc"

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

if [ $MISSING -gt 0 ]; then
  echo ""
  echo "[ACTION REQUIRED] $MISSING item(s) need attention before closing session"
  echo "Run /session-end to complete all required updates"
else
  echo "[OK] All end-of-session checks passed"
fi

echo "=== Done ==="
