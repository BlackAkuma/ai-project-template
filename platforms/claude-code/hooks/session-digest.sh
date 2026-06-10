#!/bin/bash
# SessionStart hook (BL-2/A5): inject project-memory digest into every new Claude Code session.
# stdout -> added to AI context. Template-only mode: no engine/ -> silent pass.
_SD="$(cd "$(dirname "$0")" && pwd)"
ENGINE_ROOT="${ENGINE_DIR:-$_SD/../../..}"
[ -f "$ENGINE_ROOT/engine/digest.py" ] || exit 0
python "$ENGINE_ROOT/engine/digest.py" --root "$(pwd)" 2>/dev/null || exit 0
