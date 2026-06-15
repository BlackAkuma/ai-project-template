#!/bin/bash
# session-end-gate.sh — Stop hook, TEMPLATE-ONLY
# แก้ปัญหา "Session End Protocol ไม่เคยถูกทำ" — เพราะ 'ตอนจบ session' ไม่มีจริงสำหรับ AI
# ตรรกะ: ถ้า session นี้มีงานจริง (commit โค้ดใน 12 ชม.) แต่ work-log ไม่มี entry วันนี้
#         → block การจบ 1 ครั้ง พร้อมบอกชัดว่าขาดอะไร (AI จะ sync แล้วจบได้)
# loop-guard: stop_hook_active = จบได้เสมอ (กัน infinite loop) · trivial session (ไม่มี commit) = ผ่านเงียบ

input=$(cat)
printf '%s' "$input" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
[ "${GOVERN_USER_ORDER:-0}" = "1" ] && exit 0
[ -f "CoreAiWorkspaces/03-log/work-log-index.md" ] || exit 0

# มีงานจริงไหม? (commit ที่แตะไฟล์นอก CoreAiWorkspaces ใน 12 ชม.)
RECENT_CODE=$(git log --since="12 hours ago" --name-only --pretty=format: 2>/dev/null | grep -vE '^$|^CoreAiWorkspaces/' | head -1)
[ -z "$RECENT_CODE" ] && exit 0

TODAY=$(date +%Y-%m-%d)
if ! grep -q "$TODAY" CoreAiWorkspaces/03-log/work-log-index.md 2>/dev/null; then
  echo "⛔ ยังจบ session ไม่ได้ — มี commit โค้ดวันนี้แต่ work-log-index ไม่มี entry วันที่ $TODAY" >&2
  echo "   ทำก่อนจบ: (1) เพิ่ม entry ใน work-log-index (ทำอะไร+evidence) (2) อัปเดต work-status (3) sync task-board" >&2
  exit 2
fi
exit 0
