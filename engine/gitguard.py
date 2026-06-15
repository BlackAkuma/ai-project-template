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

Quote-aware (FU-4 re-review): tokenizes with shlex so quoting is respected — 'git push origin
"+master"' is a real refspec-force (quotes are shell syntax, git sees '+master'), while a commit
message 'git commit -m "fix; git push +master"' stays a SINGLE token under subcommand 'commit' and
is correctly safe (the ';' and '+master' inside the quoted message do not split or classify). This
lets the hook pass the RAW command (no quote-stripping) without commit-message false-positives.

Out of scope (documented; need shell evaluation the hook can't do): git aliased to another name
('g push --force'), command substitution ('$(echo git) push --force'). The HOOK pairs this with a
fail-CLOSED wiring (classifier error -> hold) so these don't silently fail open.
"""
import shlex
import sys

_FORCE_PUSH_FLAGS = {"--force", "-f", "--force-with-lease", "--force-if-includes", "--mirror"}
_ARG_TAKING_GLOBAL = {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
_SEPARATORS = {";", "&", "&&", "|", "||", "\n"}


def _segments(cmd):
    """Split into per-command token-lists, quote-aware. Separators ( ; & && | || newline ) outside
    quotes delimit segments; quoted spans stay intact (so message text can't inject a fake segment).
    Newlines are hard boundaries (shell terminates a command at a newline), so we split on them first
    — shlex would otherwise treat a newline as ordinary whitespace and merge two commands."""
    segs = []
    for line in (cmd or "").split("\n"):
        try:
            lex = shlex.shlex(line, posix=True, punctuation_chars=True)
            lex.whitespace_split = True
            toks = list(lex)
        except ValueError:
            toks = line.split()  # unbalanced quotes etc -> naive split (fail-toward-detection)
        cur = []
        for t in toks:
            if t in _SEPARATORS or (t and set(t) <= {";", "&", "|"}):  # punctuation_chars groups &&,||
                if cur:
                    segs.append(cur); cur = []
            else:
                cur.append(t)
        if cur:
            segs.append(cur)
    return segs


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


def _classify_seg(toks):
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
        # force-delete = -D (or bundle with D), OR any delete form co-occurring with any force form.
        # git force-deletes an unmerged branch for ALL of: -D · -d --force · -f -d · --delete --force
        if "-D" in flagbase or _has_short_bundle(args, "D"):
            return "force-delete local branch (-D)"
        delete = "--delete" in flagbase or "-d" in flagbase or _has_short_bundle(args, "d")
        force = "--force" in flagbase or "-f" in flagbase or _has_short_bundle(args, "f")
        if delete and force:
            return "force-delete local branch (-d + --force)"
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


# NOTE: 'branch -d --force' fix above also keeps 'branch -d merged' (plain delete) safe — force
# must co-occur. _has_short_bundle is case-sensitive: lowercase 'd' = delete, uppercase 'D' = force.


if __name__ == "__main__":  # CLI shim for the hook: prints reason (empty = not risky); exit 0 = ran OK
    print(classify(" ".join(sys.argv[1:])))
