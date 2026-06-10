#!/bin/bash
# SessionEnd hook (BL-3/A5): auto write-back session facts (git commits, branch) to the store.
# Deterministic, machine-fact keys only. Template-only mode: no engine/ -> silent pass.
_SD="$(cd "$(dirname "$0")" && pwd)"
ENGINE_ROOT="${ENGINE_DIR:-$_SD/../../..}"
[ -f "$ENGINE_ROOT/engine/writeback.py" ] || exit 0
python "$ENGINE_ROOT/engine/writeback.py" --root "$(pwd)" >/dev/null 2>&1 || true
exit 0
