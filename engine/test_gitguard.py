"""FU-4 — dangerous-git classifier: real tokenization closes the substring-glob bypasses.
Run: python engine/test_gitguard.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gitguard import classify  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

# --- force push: every flag ORDER + spacing must be caught (the old glob missed these) ---
check("push --force adjacent", classify("git push --force origin main") != "")
check("push --force NON-adjacent (flag at end) — old glob MISSED this",
      classify("git push origin main --force") != "")
check("push -f", classify("git push -f origin main") != "")
check("push --force-with-lease", classify("git push --force-with-lease") != "")
check("push double-space before flag — old glob MISSED this",
      classify("git push  --force") != "")
check("tabs/newlines between tokens still caught",
      classify("git\tpush\n  --force") != "")

# --- refspec force '+': forces WITHOUT a --force flag (the named FU-4 bypass) ---
check("refspec force '+branch'", classify("git push origin +main") != "")
check("refspec force '+src:dst'", classify("git push origin +HEAD:master") != "")

# --- remote branch delete via refspec/flag ---
check("push --delete", classify("git push origin --delete oldbranch") != "")
check("push ':branch' delete refspec", classify("git push origin :oldbranch") != "")

# --- other destructive ops, order-independent ---
check("reset --hard", classify("git reset --hard HEAD~3") != "")
check("reset --hard flag-first", classify("git reset HEAD~3 --hard") != "")
check("branch -D", classify("git branch -D feature/x") != "")
check("branch --delete --force", classify("git branch --delete --force feature/x") != "")
check("clean -fd", classify("git clean -fd") != "")
check("clean -df (reordered bundle)", classify("git clean -df") != "")
check("clean -fdx", classify("git clean -fdx") != "")
check("clean --force", classify("git clean --force") != "")
check("filter-branch", classify("git filter-branch --tree-filter x HEAD") != "")

# --- NEGATIVES: must NOT block ordinary safe commands ---
check("plain push -> safe", classify("git push origin main") == "")
check("plain commit -> safe", classify("git commit -m 'fix'") == "")
check("plain branch -d (lowercase, normal delete merged) -> NOT -D",
      classify("git branch -d merged-branch") == "")
check("status -> safe", classify("git status") == "")
check("pull -> safe", classify("git pull --ff-only") == "")
check("non-git command -> safe", classify("rm -f notes.txt") == "")
check("branch --force-with... not a delete (no -D) -> safe (only -D/-D+--force blocks)",
      classify("git branch feature/new") == "")
# 'push' word appearing in a non-push context must not trip force (no push subcommand)
check("'+' token without push -> safe", classify("git log +main") == "")

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} gitguard tests passed")
