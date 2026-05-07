#!/bin/bash
# Hook: session-start
# รันอัตโนมัติเมื่อเริ่ม Claude Code session
# Event: PreToolUse (ก่อน tool แรกของ session)

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
DOC_DIR="$PROJECT_ROOT/ai"

echo "=== Session Start Check ==="

# ตรวจว่า ai/ มีอยู่
if [ ! -d "$DOC_DIR" ]; then
  echo "[WARN] ai/ not found at $DOC_DIR"
  echo "       Run bootstrap setup first"
  exit 0
fi

# ตรวจ work-status
STATUS_FILE="$DOC_DIR/01-plan/work-status.md"
if [ -f "$STATUS_FILE" ]; then
  echo "[OK] work-status found"
  # Extract AI-CONTEXT block และแสดง
  awk '/^<!-- AI-CONTEXT/,/^-->/' "$STATUS_FILE" | head -20
else
  echo "[WARN] work-status.md not found — create it first"
fi

# ตรวจ task-board
BOARD_FILE="$DOC_DIR/02-task/task-board.md"
if [ -f "$BOARD_FILE" ]; then
  # นับ task ที่ in_progress
  IN_PROGRESS=$(grep -c "in_progress" "$BOARD_FILE" 2>/dev/null || echo "0")
  echo "[OK] task-board found — $IN_PROGRESS task(s) in_progress"
else
  echo "[WARN] task-board.md not found"
fi

# ตรวจ work-log-index
LOG_FILE="$DOC_DIR/03-log/work-log-index.md"
if [ -f "$LOG_FILE" ]; then
  echo "[OK] work-log-index found"
else
  echo "[WARN] work-log-index.md not found"
fi

echo "=== Ready ==="
