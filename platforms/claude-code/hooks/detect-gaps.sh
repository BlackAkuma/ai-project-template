#!/bin/bash
# Hook: detect-gaps
# ตรวจ gap ระหว่าง task board กับ source docs
# รันอัตโนมัติตอน session start หรือเรียกด้วย /scope-check

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
DOC_DIR="$PROJECT_ROOT/ai"

echo "=== Gap Detection ==="

GAPS=0

BOARD_FILE="$DOC_DIR/02-task/task-board.md"
SOURCE_DIR="$DOC_DIR/00-source/versions"

if [ ! -f "$BOARD_FILE" ]; then
  echo "[SKIP] task-board.md not found"
  exit 0
fi

# ตรวจ task in_progress ที่ไม่มี source reference
echo "Checking tasks for missing source references..."
while IFS= read -r line; do
  if echo "$line" | grep -q "in_progress"; then
    if ! echo "$line" | grep -q "CoreAiWorkspaces/00-source"; then
      TASK_ID=$(echo "$line" | grep -oE 'T-[0-9]+' | head -1)
      if [ -n "$TASK_ID" ]; then
        echo "[GAP] $TASK_ID is in_progress but has no source reference"
        GAPS=$((GAPS + 1))
      fi
    fi
  fi
done < "$BOARD_FILE"

# ตรวจว่า source version ที่ board อ้างถึงยังมีอยู่
BOARD_SRC=$(grep "^src:" "$BOARD_FILE" | head -1 | awk '{print $2}')
if [ -n "$BOARD_SRC" ] && [ -n "$SOURCE_DIR" ]; then
  if [ ! -d "$SOURCE_DIR/$BOARD_SRC" ]; then
    echo "[GAP] task-board references source $BOARD_SRC but directory not found"
    GAPS=$((GAPS + 1))
  fi
fi

if [ $GAPS -eq 0 ]; then
  echo "[OK] No gaps detected"
else
  echo ""
  echo "[ACTION] $GAPS gap(s) found — see Scenario H in ai-decision-protocol.md"
fi

echo "=== Done ==="
