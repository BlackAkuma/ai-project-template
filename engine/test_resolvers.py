"""P1-5 smoke test — verify predicate resolvers behave correctly on synthetic state.
Run: python engine/test_resolvers.py  (no pytest dep; plain asserts + exit code)
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolvers import (  # noqa: E402
    secret_absent, placeholder_absent, file_exists, entry_exists,
    status_equals, evidence_count_gte, git_staged_clean_of,
    challenge_record_valid,
)


def ctx(added="", files=None, root="."):
    return {"root": root, "staged_diff": "", "staged_files": files or [], "staged_added": added}


SECRET = r"(?i)(secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}"
cases = []


def check(name, cond):
    cases.append((name, bool(cond)))


# secret_absent
check("secret detected -> False", secret_absent(ctx('password = "hunter2xx"'), patterns=[SECRET]) is False)
check("clean -> True", secret_absent(ctx('x = 1'), patterns=[SECRET]) is True)

# placeholder_absent (also used as generic pattern matcher)
check("placeholder detected -> False", placeholder_absent(ctx('a <NEEDS_CLARIFICATION: y>'), patterns=["<NEEDS_CLARIFICATION"]) is False)
check("no placeholder -> True", placeholder_absent(ctx('clean'), patterns=["<NEEDS_CLARIFICATION"]) is True)
check("prototype marker detected -> False", placeholder_absent(ctx('// PROTOTYPE: hack'), patterns=["// PROTOTYPE:"]) is False)

# git_staged_clean_of — code staged w/o docs -> False
check("code w/o docs -> False", git_staged_clean_of(ctx(files=["src/a.py"]), glob="CoreAiWorkspaces/**") is False)
check("code+docs -> True", git_staged_clean_of(ctx(files=["src/a.py", "CoreAiWorkspaces/x.md"]), glob="CoreAiWorkspaces/**") is True)

# file_exists against a temp file
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "x.md"), "w").write("T-001 done")
    check("file_exists -> True", file_exists(ctx(root=d), path="x.md") is True)
    check("file_exists missing -> False", file_exists(ctx(root=d), path="nope.md") is False)
    check("entry_exists -> True", entry_exists(ctx(root=d), file="x.md", key="T-001") is True)
    check("entry_exists missing key -> False", entry_exists(ctx(root=d), file="x.md", key="T-999") is False)

# challenge_record_valid (P2-3) — presence/structure
_good = {"necessity": {"a_why": "build the engine validator", "b_source": "BRD FR-1.1",
         "c_simpler": "reuse validate-commit.sh generalized",
         "lenses": {"expert": "similar pattern exists in hooks", "technical": "low complexity reversible",
                    "contrarian": "could be advisory-only and skipped by weak model"}}}
check("challenge valid -> True", challenge_record_valid(ctx(), record=_good) is True)
_nocontra = {"necessity": dict(_good["necessity"], lenses={"expert": "x"*12, "technical": "y"*12, "contrarian": "no"})}
check("challenge trivial contrarian -> False", challenge_record_valid(ctx(), record=_nocontra) is False)
_nosrc = {"necessity": dict(_good["necessity"], b_source="")}
check("challenge no source -> False", challenge_record_valid(ctx(), record=_nosrc) is False)

failed = [n for n, ok in cases if not ok]
for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)} resolver tests failed")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} resolver smoke tests passed")
