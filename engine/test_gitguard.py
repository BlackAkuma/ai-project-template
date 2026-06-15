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
check("tabs between tokens still caught (intra-segment whitespace)",
      classify("git\tpush\t\t--force") != "")
check("newline IS a command separator (shell semantics), not intra-token",
      classify("git push\n--force origin main") == "")  # two commands; '--force' alone is not git

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

# --- FU-4 re-review (panel blockers): =value forms, short-flag bundles, global-opt skip ---
check("--force-with-lease=VALUE (attached) — re-review false-neg",
      classify("git push --force-with-lease=main:abc origin main") != "")
check("--force-if-includes=VALUE", classify("git push --force-if-includes=x origin main") != "")
check("branch -fD bundle (force delete) — re-review false-neg", classify("git branch -fD feature/x") != "")
check("branch -Df bundle (reordered)", classify("git branch -Df feature/x") != "")
check("global opt 'git -c k=v push --force' parsed (sub=push)",
      classify("git -c user.name=x push --force origin main") != "")
check("global opt 'git -C path push +main' parsed", classify("git -C /repo push origin +main") != "")

# --- FU-4 re-review: segmentation — no cross-command MISATTRIBUTION (false-positive) ---
check("'echo +foo && git push origin main' -> safe (+ is not push's)",
      classify("echo +foo && git push origin main") == "")
check("'git config -f x && git push origin main' -> safe (-f is config's)",
      classify("git config -f x && git push origin main") == "")
check("'git push origin main && git log +HEAD' -> safe (+ is log's)",
      classify("git push origin main && git log +HEAD") == "")
check("'git stash push origin +foo' -> safe (sub=stash not push)",
      classify("git stash push origin +foo") == "")
# --- but a dangerous op in ANY segment is still caught ---
check("dangerous in segment 2 still caught", classify("git status && git push origin +master") != "")
check("dangerous in segment 1 still caught", classify("git reset --hard && echo done") != "")
check("pipe separator segmented", classify("echo x | git push origin +master") != "")

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
