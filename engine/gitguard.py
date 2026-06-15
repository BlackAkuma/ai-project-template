"""FU-4: dangerous-git classifier — real tokenization + subcommand grammar, not substring globs.

The hook used adjacent-substring case-globs (`*"push --force"*`) which were trivially bypassed:
  · `git push origin main --force`  -> "push"/"--force" not adjacent -> SKIPPED
  · `git push origin +master`       -> refspec '+' force push, no --force flag -> SKIPPED
  · `git push  --force`             -> double space -> SKIPPED
This module:
  1. SEGMENTS the command on shell separators (; && || | &) so a flag from one segment can't be
     misattributed to a git verb in another ('echo +foo && git push origin main' is NOT a force push);
  2. parses each segment's git SUBCOMMAND (skipping global opts like -c X / -C path) so 'git stash
     push origin +foo' is judged as 'stash', not 'push';
  3. matches flags by their base name (split on '=') so the attached-value form
     '--force-with-lease=main' is caught, and short-flag BUNDLES ('-fD', 'clean -df') are caught.
Conservative by design (fail-toward-hold): a segment with a dangerous verb+flag co-occurring -> hold.

classify(cmd) -> reason string (held for approval) or "" (allowed).

Out of scope (documented; need shell evaluation the hook can't do): git aliased to another name
('g push --force'), command substitution ('$(echo git) push --force'). The HOOK pairs this with a
fail-CLOSED wiring (classifier error -> hold) so these don't silently fail open.
"""
import re
import sys

_FORCE_PUSH_FLAGS = {"--force", "-f", "--force-with-lease", "--force-if-includes", "--mirror"}
_ARG_TAKING_GLOBAL = {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
_SEG_SPLIT = re.compile(r"\|\||&&|[;|&\n]")


def _segments(cmd):
    return [s for s in _SEG_SPLIT.split(cmd or "") if s.strip()]


def _subcommand(rest):
    """First non-option token = the git subcommand; skip global opts (and their args)."""
    i = 0
    while i < len(rest):
        t = rest[i]
        if t.startswith("-"):
            base = t.split("=", 1)[0]
            if base in _ARG_TAKING_GLOBAL and "=" not in t and i + 1 < len(rest):
                i += 2  # consumes the option's separate argument (e.g. -c key=val)
            else:
                i += 1
            continue
        return t, rest[i + 1:]
    return None, []


def _has_short_bundle(args, letter):
    """True if any short-flag bundle (-xyz, not --long) contains `letter` (case-sensitive)."""
    for a in args:
        if a.startswith("-") and not a.startswith("--") and letter in a[1:]:
            return True
    return False


def _classify_seg(seg):
    toks = seg.split()
    if "git" not in toks:
        return ""
    rest = toks[toks.index("git") + 1:]
    sub, args = _subcommand(rest)
    if not sub:
        return ""
    flagbase = {a.split("=", 1)[0] for a in args}  # base name so '--force-with-lease=x' matches

    if sub == "push":
        if flagbase & _FORCE_PUSH_FLAGS:
            return "force push (rewrites remote history)"
        if any(a.startswith("+") and len(a) > 1 for a in args):
            return "force push via '+refspec' (rewrites remote history without --force flag)"
        if "--delete" in flagbase or "-d" in flagbase or any(a.startswith(":") and len(a) > 1 for a in args):
            return "remote branch delete (push --delete / ':' refspec)"
        return ""

    if sub == "reset":
        return "reset --hard (discards uncommitted work)" if "--hard" in flagbase else ""

    if sub == "branch":
        if "-D" in flagbase or ("--delete" in flagbase and "--force" in flagbase) or _has_short_bundle(args, "D"):
            return "force-delete local branch (-D)"
        return ""

    if sub == "clean":
        if "--force" in flagbase or _has_short_bundle(args, "f"):
            return "git clean -f (deletes untracked files)"
        return ""

    if sub in ("filter-branch", "filter-repo"):
        return "history rewrite (filter-branch/filter-repo)"

    return ""


def classify(cmd):
    """Return a human reason if ANY segment is a dangerous git op, else ''."""
    for seg in _segments(cmd):
        r = _classify_seg(seg)
        if r:
            return r
    return ""


if __name__ == "__main__":  # CLI shim for the hook: prints reason (empty = not risky); exit 0 = ran OK
    print(classify(" ".join(sys.argv[1:])))
