#!/bin/bash
# govern-docs.sh — PreToolUse(Edit|Write|MultiEdit) gate, TEMPLATE-ONLY
# ปิด "ช่องทางที่ไม่มียาม": การละเมิดส่วนใหญ่เกิดผ่าน Edit/Write ไม่ใช่ Bash
#   1) แก้ source docs ตรง (CoreAiWorkspaces/00-source/**)  → BLOCK: ต้อง version ใหม่/extension doc
#   2) mark task เป็น done ใน task-board โดย work-log ไม่มี entry ของ task นั้น → BLOCK (Task Close Gate, C-03)
# exit 0 = allow · exit 2 = block · escape: GOVERN_USER_ORDER=1

input=$(cat)
[ "${GOVERN_USER_ORDER:-0}" = "1" ] && exit 0

PARSED=$(printf '%s' "$input" | python -c "import sys,json
try:
    d=json.load(sys.stdin); ti=d.get('tool_input',{})
    fp=(ti.get('file_path') or '').replace(chr(92),'/')
    new=(ti.get('new_string') or ti.get('content') or '')[:4000].replace(chr(10),' ')
    print(fp); print(new)
except Exception: print(); print()" 2>/dev/null)
FILE=$(printf '%s\n' "$PARSED" | sed -n 1p)
NEW=$(printf '%s\n' "$PARSED" | sed -n 2p)

[ -z "$FILE" ] && exit 0

# --- 1) requirement immutability ---
case "$FILE" in
  */CoreAiWorkspaces/00-source/*|CoreAiWorkspaces/00-source/*)
    case "$FILE" in
      */versions/*) ;;  # การเพิ่ม version ใหม่ = วิธีที่ถูกต้อง อนุญาต
      *)
        echo "⛔ BLOCK: ห้ามแก้ source docs ตรง — requirement เปลี่ยน = สร้าง version ใหม่ใน 00-source/versions/ หรือ extension doc (core/02)" >&2
        exit 2 ;;
    esac ;;
esac

# --- 2) Task Close Gate ที่ "มีทางเดินจริง": done ใหม่ใน task-board ต้องมี log ก่อน ---
case "$FILE" in
  */task-board.md|task-board.md|*/02-task/*)
    NEW_DONE=$(printf '%s' "$NEW" | grep -oE '(T-[0-9]+|BL-[0-9]+)[^a-zA-Z0-9-]*(\[?done\]?|→ *done|: *done)' | grep -oE 'T-[0-9]+|BL-[0-9]+' | sort -u)
    WL="$(dirname "$FILE")/../03-log/work-log-index.md"
    [ -f "$WL" ] || WL="CoreAiWorkspaces/03-log/work-log-index.md"
    if [ -n "$NEW_DONE" ] && [ -f "$WL" ]; then
      for T in $NEW_DONE; do
        if ! grep -q "$T" "$WL" 2>/dev/null; then
          echo "⛔ BLOCK (Task Close Gate): จะ mark $T = done แต่ work-log-index ไม่มี entry ของ $T" >&2
          echo "   เขียน log ก่อน (ทำอะไร + validation evidence) แล้วค่อยปิด task (core/15 C-03)" >&2
          exit 2
        fi
      done
    fi ;;
esac

exit 0
