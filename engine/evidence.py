"""F11 / FR-2.4: evidence 2-class verification — machine-verifiable vs human-attested (ADR-009 D2).

machine-verifiable: Engine checks the artifact deterministically (commit SHA / test exit / file).
human-attested: Engine checks PRESENCE of a sign-off only — the truth is trust-based, recorded,
auditable (NOT judged by the Engine). This is the functional 2-class path the audit found stubbed.
"""
import os
import re


def verify(ev, root="."):
    """Return (verified, how). ev = {class, type, ref, exit?, signoff?}."""
    cls = ev.get("class")
    if cls == "machine-verifiable":
        typ = ev.get("type")
        ref = ev.get("ref", "")
        if typ == "commit":
            return bool(re.match(r"^[0-9a-f]{7,40}$", str(ref))), "commit-sha-valid"
        if typ == "test":
            return str(ev.get("exit", "")) == "0", "test-exit-0"
        if typ == "artifact":
            return os.path.exists(os.path.join(root, ref)), "artifact-exists"
        return bool(ref), "ref-present"
    if cls == "human-attested":
        # presence of a sign-off only; Engine does not judge correctness (truth = human)
        return bool(ev.get("signoff")), "human-signoff-present"
    return False, f"unknown-class:{cls}"
