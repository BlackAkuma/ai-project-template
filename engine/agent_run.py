"""BL-12/B1-spike: ONE governed agent run — think→act→gate→evidence, fully recorded (G5).

First step from "silent guard" to "assistant that works for you": the LOCAL model proposes
code; the ENGINE decides (deterministic gates only — LLM never judges, per panel dissent #5):
  1. PLAN   — LLM proposes (advisory, recorded)
  2. WRITE  — proposed content passes deterministic gates (secret/placeholder) BEFORE touching disk
  3. TEST   — real test run, real exit code = machine evidence
  4. DONE   — mark_done through the Task Close Gate (worklog + evidence + tests green)
Every step lands in the tamper-evident event chain + a human-readable transcript.

  python engine/agent_run.py            # live run with Ollama (if up)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from llm import complete  # noqa: E402
from events import append_event  # noqa: E402
from govern import mark_done  # noqa: E402
from testrun import run_tests  # noqa: E402

SECRET_PAT = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}")
PLACEHOLDER_PAT = re.compile(r"<NEEDS_CLARIFICATION|TODO_REPLACE|XXX_FILL")
LOG = "engine/events.log.jsonl"

TEST_TEMPLATE = '''import calc
assert calc.add(2, 3) == 5
assert calc.add(-1, 1) == 0
assert calc.add(0, 0) == 0
print("OK")
'''


def _extract_code(text):
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()


def run_task(workdir, task_id="SPIKE-1", model="stub-strong", provider="stub",
             inject_content=None, ts=5000):
    """One governed run in `workdir` (sandbox). Returns record dict + writes transcript."""
    os.makedirs(os.path.join(workdir, "engine"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "CoreAiWorkspaces/02-task"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "CoreAiWorkspaces/03-log"), exist_ok=True)
    bp = os.path.join(workdir, "CoreAiWorkspaces/02-task/task-board.md")
    if not os.path.exists(bp):
        open(bp, "w", encoding="utf-8").write("<!-- AI-CONTEXT\ndone: []\n-->\n")
    steps = []

    def rec(step, status, detail=""):
        steps.append({"step": step, "status": status, "detail": str(detail)[:300]})
        append_event(model, f"agent_run.{step}", task_id, f"{status}: {str(detail)[:120]}",
                     ts=ts + len(steps), root=workdir, log=LOG)

    # 1) PLAN (LLM advisory — recorded, never authoritative)
    plan = complete([{"role": "user", "content":
                      "Plan in 2 short steps: write python function add(a,b) in calc.py, then test it."}],
                    model=model, role="advisory", provider_name=provider)
    rec("plan", "ok" if plan["ok"] else "llm-error", plan.get("text", plan.get("reason")))

    # 2) WRITE — model proposes code; DETERMINISTIC gates check content BEFORE disk
    if inject_content is not None:
        code = inject_content
    else:
        r = complete([{"role": "user", "content":
                       "Write ONLY python code for calc.py: function add(a, b) returning a+b, with a one-line docstring. No explanation."}],
                     model=model, role="advisory", provider_name=provider)
        code = _extract_code(r.get("text", "")) if r["ok"] else ""
        source = "model"
        if "def add" not in code:  # stub/weak fallback keeps loop mechanics testable
            code = 'def add(a, b):\n    """Return a + b."""\n    return a + b\n'
            source = "FALLBACK-template (model output unusable)"  # panel: must be distinguishable
        rec("propose", "ok", f"source={source}")
    if SECRET_PAT.search(code) or PLACEHOLDER_PAT.search(code):
        rec("write", "BLOCKED", "deterministic gate: proposed content contains secret/placeholder")
        _save(workdir, task_id, steps, done=False)
        return {"done": False, "blocked_at": "write", "steps": steps}
    open(os.path.join(workdir, "calc.py"), "w", encoding="utf-8").write(code)
    rec("write", "ok", f"calc.py {len(code)}B (gated before write)")

    # 3) TEST — real run, real exit code = machine evidence
    open(os.path.join(workdir, "test_calc.py"), "w", encoding="utf-8").write(TEST_TEMPLATE)
    open(os.path.join(workdir, "engine", "testcmd.txt"), "w", encoding="utf-8").write(
        f'"{sys.executable}" test_calc.py')
    tr = run_tests(workdir, use_cache=False)
    rec("test", "green" if tr["green"] else "RED", f"exit={tr['exit']}")
    if not tr["green"]:
        _save(workdir, task_id, steps, done=False)
        return {"done": False, "blocked_at": "test", "steps": steps}

    # 4) DONE — through the real Task Close Gate (no shortcut)
    open(os.path.join(workdir, "CoreAiWorkspaces/03-log/work-log-index.md"), "a", encoding="utf-8").write(
        f"- {task_id} done: calc.add implemented, test exit=0 evidence ✓\n")
    md = mark_done(task_id, root=workdir, ts=ts + 50, log=LOG)
    rec("done", "ok" if md["ok"] else "blocked", md.get("missing", "closed via Task Close Gate"))
    _save(workdir, task_id, steps, done=md["ok"])
    return {"done": md["ok"], "steps": steps, "test_exit": tr["exit"]}


def _save(workdir, task_id, steps, done):
    p = os.path.join(workdir, "agent-run-report.md")
    L = [f"# Governed Agent Run — {task_id}", ""]
    for s in steps:
        icon = {"ok": "✅", "green": "✅", "BLOCKED": "🔴", "RED": "🔴", "blocked": "🟡", "llm-error": "⚠️"}.get(s["status"], "·")
        L.append(f"- {icon} **{s['step']}** [{s['status']}] {s['detail']}")
    L.append(f"\nresult: {'DONE (closed via Task Close Gate)' if done else 'NOT DONE (governance held the line)'}")
    open(p, "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    from llm import ollama_status, MODEL_TIER
    up, info = ollama_status()
    wd = os.path.join("engine", "agent_runs", "live")
    live = [m for m in (info if isinstance(info, list) else []) if m in MODEL_TIER and MODEL_TIER[m] >= 2]
    if up and live:
        print(f"live run with {live[0]} ...")
        r = run_task(wd, model=live[0], provider="ollama")
    else:
        print("Ollama/known model not available — stub run (mechanics only)")
        r = run_task(wd)
    print(json.dumps(r, ensure_ascii=False, indent=1)[:800])
    print(f"\ntranscript: {wd}/agent-run-report.md")
