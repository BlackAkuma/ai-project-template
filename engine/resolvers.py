"""Predicate resolver vocabulary (P1-2).

Vetted, fixed set of predicates. Each checks REAL state (git/file), never agent claims.
Engineers extend the vocabulary; gate authors compose from it (engine/gates/_grammar.md).
"""
import os
import re
import fnmatch

RESOLVERS = {}


def resolver(name):
    def reg(fn):
        RESOLVERS[name] = fn
        return fn
    return reg


@resolver("file_exists")
def file_exists(ctx, path=None, **_):
    return os.path.exists(os.path.join(ctx["root"], path))


@resolver("secret_absent")
def secret_absent(ctx, patterns=None, **_):
    added = ctx["staged_added"]
    for p in (patterns or []):
        if re.search(p, added):
            return False
    return True


@resolver("placeholder_absent")
def placeholder_absent(ctx, patterns=None, **_):
    added = ctx["staged_added"]
    for p in (patterns or [r"<[A-Z_]{3,}>"]):
        if re.search(p, added):
            return False
    return True


@resolver("git_staged_clean_of")
def git_staged_clean_of(ctx, glob=None, **_):
    """Fail if non-glob (code) files are staged while glob (docs) files are NOT."""
    files = ctx["staged_files"]
    docs = [f for f in files if fnmatch.fnmatch(f, glob)]
    code = [f for f in files if not fnmatch.fnmatch(f, glob)]
    if code and not docs:
        return False
    return True


@resolver("entry_exists")
def entry_exists(ctx, file=None, key=None, **_):
    p = os.path.join(ctx["root"], file)
    if not os.path.exists(p) or key is None:
        return False
    with open(p, encoding="utf-8") as fh:
        return key in fh.read()


@resolver("status_equals")
def status_equals(ctx, file=None, key=None, value=None, **_):
    p = os.path.join(ctx["root"], file)
    if not os.path.exists(p) or key is None:
        return False
    with open(p, encoding="utf-8") as fh:
        txt = fh.read()
    if value == "done":
        # task id present in the AI-CONTEXT done:[...] list
        return re.search(r"done:\s*\[[^\]]*\b" + re.escape(key) + r"\b", txt) is not None
    return key in txt


@resolver("evidence_count_gte")
def evidence_count_gte(ctx, task=None, n=1, **_):
    """Presence heuristic (pre canonical-store): work-log line w/ task + evidence marker."""
    p = os.path.join(ctx["root"], "CoreAiWorkspaces/03-log/work-log-index.md")
    if not os.path.exists(p) or task is None:
        return False
    with open(p, encoding="utf-8") as fh:
        txt = fh.read()
    cnt = sum(
        1 for line in txt.splitlines()
        if task in line and re.search(r"(✓|test|commit|evidence|[0-9a-f]{7,})", line, re.I)
    )
    return cnt >= int(n)


@resolver("human_signoff")
def human_signoff(ctx, ref=None, **_):
    return False  # stub — needs Decision Inbox (P6)


@resolver("challenge_record_valid")
def challenge_record_valid(ctx, record=None, min_len=10, **_):
    """P2-3: validate challenge-necessity record presence/structure (not quality).
    `record` = dict (inline) or path to JSON. Required: a_why/b_source/c_simpler + 3 lenses;
    contrarian lens must be non-trivial (บังคับ produce real objection)."""
    import json as _json
    rec = record
    if isinstance(record, str):
        p = os.path.join(ctx["root"], record)
        if not os.path.exists(p):
            return False
        try:
            rec = _json.load(open(p, encoding="utf-8"))
        except Exception:
            return False
    if not isinstance(rec, dict):
        return False
    nec = rec.get("necessity", rec)

    def ok(v, n=min_len):
        return isinstance(v, str) and len(v.strip()) >= n

    if not all(ok(nec.get(k)) for k in ("a_why", "c_simpler")):
        return False
    if not ok(nec.get("b_source"), 5):
        return False
    lenses = nec.get("lenses", {})
    if not all(ok(lenses.get(k)) for k in ("expert", "technical", "contrarian")):
        return False
    return True


@resolver("tests_green")
def tests_green(ctx, **_):
    """BL-6: REAL test evidence — runs the project's configured test command (engine/testcmd.txt),
    consumes the actual exit code (cached by git HEAD). Policy: configured -> enforced;
    not configured -> pass-with-note (BL-7 init writes a default; digest surfaces the gap)."""
    from testrun import run_tests
    r = run_tests(ctx.get("root", "."))
    if not r["configured"]:
        return True  # not enforced until configured (logged decision, see BL-6)
    return bool(r["green"])
