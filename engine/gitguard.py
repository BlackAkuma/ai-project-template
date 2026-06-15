"""FU-4: dangerous-git classifier — real tokenization, not fragile substring globs.

The hook used adjacent-substring case-globs (`*"push --force"*`) which were trivially bypassed:
  · `git push origin main --force`  -> "push" and "--force" not adjacent -> SKIPPED
  · `git push origin +master`       -> refspec '+' force push, no --force flag -> SKIPPED
  · `git push  --force`             -> double space -> SKIPPED
This module tokenizes the (quote-stripped, ws-normalized) command and matches by token presence,
so flag ORDER, extra whitespace, and refspec-force (`+`) variants are all caught. Conservative by
design (fail-toward-hold): if a dangerous verb+flag co-occur anywhere in the command, classify it.

classify(cmd) -> reason string (held for approval) or "" (allowed).
"""
import sys

_FORCE_PUSH_FLAGS = {"--force", "-f", "--force-with-lease", "--force-if-includes", "--mirror"}
_CLEAN_FORCE = "f"  # any -..f.. bundle


def _tokens(cmd):
    # quotes already stripped upstream (CMD_NOQ); split on any whitespace -> order/space agnostic
    return (cmd or "").split()


def classify(cmd):
    """Return a human reason if the command is a dangerous git op, else ''."""
    toks = _tokens(cmd)
    if "git" not in toks:
        return ""
    tset = set(toks)

    # --- force push: push + (force flag OR '+'-prefixed refspec) ---
    if "push" in tset:
        if tset & _FORCE_PUSH_FLAGS:
            return "force push (rewrites remote history)"
        # refspec force: a '+'-prefixed refspec like '+main' or '+HEAD:master' (forces without --force)
        if any(t.startswith("+") and len(t) > 1 for t in toks):
            return "force push via '+refspec' (rewrites remote history without --force flag)"
        # remote branch delete: 'push --delete' or colon-refspec ':branch'
        if "--delete" in tset or "-d" in tset or any(t.startswith(":") and len(t) > 1 for t in toks):
            return "remote branch delete (push --delete / ':' refspec)"

    # --- reset --hard: discards working tree + index irrecoverably ---
    if "reset" in tset and "--hard" in tset:
        return "reset --hard (discards uncommitted work)"

    # --- force-delete local branch: 'branch -D' or 'branch --delete --force' ---
    if "branch" in tset and ("-D" in tset or ("--delete" in tset and "--force" in tset)):
        return "force-delete local branch (-D)"

    # --- clean -f*: removes untracked files; any flag bundle containing 'f', or --force ---
    if "clean" in tset:
        if "--force" in tset:
            return "git clean --force (deletes untracked files)"
        for t in toks:
            if t.startswith("-") and not t.startswith("--") and _CLEAN_FORCE in t[1:]:
                return "git clean -f (deletes untracked files)"

    # --- history rewriters ---
    if "filter-branch" in tset or "filter-repo" in tset:
        return "history rewrite (filter-branch/filter-repo)"

    return ""


if __name__ == "__main__":  # CLI shim for the hook: prints reason (empty = not risky)
    print(classify(" ".join(sys.argv[1:])))
