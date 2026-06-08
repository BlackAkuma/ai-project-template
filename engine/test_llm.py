"""F1/P7 test — model-agnostic adapter + role-floor enforcement (FR-4.1/4.2).
Run: python engine/test_llm.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm import assign, complete  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

# role-floor enforcement (the moat-floor — structural, not model goodwill)
check("strong model + architect -> ok", assign("claude-sonnet", "architect")[0] is True)
check("weak model + code-author -> REFUSED", assign("local-3b", "code-author")[0] is False)
check("mid model + advisory -> ok", assign("claude-haiku", "advisory")[0] is True)
check("weak model + read-only -> ok", assign("local-3b", "read-only")[0] is True)
check("unknown model -> refused", assign("mystery-llm", "advisory")[0] is False)
check("unknown role -> refused", assign("gpt-4o", "wizard")[0] is False)

# model-agnostic completion via stub (offline)
r = complete([{"role": "user", "content": "hello"}], model="stub-strong", role="advisory", provider_name="stub")
check("complete via stub -> text", r["ok"] is True and "echo" in r["text"])
# swap model -> still works (agnostic)
r2 = complete([{"role": "user", "content": "x"}], model="gpt-4o", role="architect", provider_name="stub")
check("swap model (gpt-4o) -> still works", r2["ok"] is True)
# sub-floor model blocked at completion time
r3 = complete([{"role": "user", "content": "x"}], model="local-3b", role="code-author", provider_name="stub")
check("sub-floor completion -> blocked (lane_refused)", r3["ok"] is False and r3.get("lane_refused") is True)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} model-agnostic + role-floor tests passed")
