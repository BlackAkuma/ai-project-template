"""F5/P5: Cockpit renderer — read-only project view (BRD FR-3, P5 read-only Cockpit).

Renders project state (canonical store) + Decision Inbox + recent audit events as a dashboard.
Read-only: NEVER mutates state/engine (preserves the proven moat). This is the headless/CLI
renderer; the full interactive SvelteKit web Cockpit needs a frontend env (flagged, not built here).
It is the demand-harvest 'visible surface' (ADR-013 C-fallback) over the same data contract.
"""


def _counts(state):
    by = {}
    for t in state.get("tasks", []):
        by[t.get("status", "todo")] = by.get(t.get("status", "todo"), 0) + 1
    return by


def render_cockpit(state, open_items=None, recent_events=None):
    """Pure read-only render. state=store dict; open_items=inbox list_open; recent_events=tail."""
    open_items = open_items or []
    recent_events = recent_events or []
    p = state.get("project", {})
    c = _counts(state)
    L = []
    L.append("=" * 56)
    L.append("  COCKPIT — Governed Project Memory")
    L.append("=" * 56)
    L.append(f"phase: {p.get('phase', '-')}   branch: {p.get('active_branch', '-')}")
    L.append(f"tasks: done={c.get('done', 0)} in_progress={c.get('in_progress', 0)} "
             f"blocked={c.get('blocked', 0)} todo={c.get('todo', 0)}")
    L.append(f"blocker: {p.get('blocker', 'none')}")
    L.append("")
    L.append(f"DECISION INBOX ({len(open_items)} open) — needs human:")
    if open_items:
        for it in open_items:
            L.append(f"  [{it['id']}] L{it.get('risk_level')} {it.get('gate')}: {it.get('reason', '')[:50]}")
    else:
        L.append("  (none — all clear)")
    L.append("")
    L.append("recent activity:")
    for e in recent_events[-5:]:
        L.append(f"  {e.get('action')} {e.get('target')} -> {e.get('result')}")
    if not recent_events:
        L.append("  (no events)")
    return "\n".join(L)
