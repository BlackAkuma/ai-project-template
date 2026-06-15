#!/bin/bash
# UserPromptSubmit hook (OBS-1): re-inject ACTIVE obligations into context on every user prompt,
# so standing constraints (freezes, open human decisions, regressed test gate) don't decay out of
# attention over a long conversation. stdout -> added to AI context. Template-only: no engine -> silent.
_SD="$(cd "$(dirname "$0")" && pwd)"
ENGINE_ROOT="${ENGINE_DIR:-$_SD/../../..}"
[ -f "$ENGINE_ROOT/engine/obligations.py" ] || exit 0
python "$ENGINE_ROOT/engine/obligations.py" --root "$(pwd)" 2>/dev/null || exit 0
