#!/bin/bash
# Hook: pre-compact
# รันอัตโนมัติก่อน context ถูกบีบ
# Event: PreCompact

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
DOC_DIR="$PROJECT_ROOT/doc"

echo "=== Pre-Compact Checkpoint ==="
echo "Context is about to be compacted. Ensure checkpoint is saved."
echo ""
echo "Required before compact:"
echo "  1. Add checkpoint entry to work-log with current progress"
echo "  2. Update work-status with current state"
echo "  3. Mark active task as [IN_PROGRESS: checkpoint saved — <summary>]"
echo ""
echo "After compact, run /session-start equivalent to reload context:"
echo "  - Read work-status AI-CONTEXT block"
echo "  - Read work-log-index AI-CONTEXT block"
echo "  - Read task-board AI-CONTEXT block"
echo ""

# ตรวจ task ที่ in_progress ไม่มี checkpoint
BOARD_FILE="$DOC_DIR/02-task/task-board.md"
if [ -f "$BOARD_FILE" ]; then
  IN_PROGRESS=$(grep "in_progress" "$BOARD_FILE" | grep -v "checkpoint saved" | head -5)
  if [ -n "$IN_PROGRESS" ]; then
    echo "[WARN] Tasks in_progress without checkpoint:"
    echo "$IN_PROGRESS"
  fi
fi

echo "=== Compact will proceed ==="
