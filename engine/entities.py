"""F9 / FR-2.3: CORE 11 entities typed schema + structural validation (ADR-009, a1-core-schema).

The invariant CORE (process layer). validate(kind, record) checks required-field presence +
declared enums (presence/structure, NOT quality — consistent with the engine thesis).
PROFILE packs extend these; this module is the canonical typed contract the audit found missing.
"""

# kind -> {required: [...], enums: {field: [allowed]}}
CORE_ENTITIES = {
    "Project":     {"required": ["id", "name"], "enums": {"status": ["active", "paused", "done", "archived"]}},
    "Requirement": {"required": ["id", "version"], "enums": {"status": ["draft", "active", "superseded"]}},
    "Plan":        {"required": ["id"], "enums": {}},
    "Task":        {"required": ["id", "title", "status", "source_ref"],
                    "enums": {"status": ["todo", "design_validate", "in_progress", "review", "done", "blocked"]}},
    "Evidence":    {"required": ["id", "task_ref", "class"], "enums": {"class": ["machine-verifiable", "human-attested"]}},
    "Decision":    {"required": ["id", "status"], "enums": {"status": ["Proposed", "Accepted", "Deprecated", "Superseded"]}},
    "TeamMember":  {"required": ["id", "role", "kind"], "enums": {"kind": ["human", "ai"]}},
    "Gate":        {"required": ["id", "trigger"], "enums": {"effect": ["auto-log", "decision-inbox", "hard-stop", "warn", "block"]}},
    "Repo":        {"required": ["id"], "enums": {}},
    "Entity":      {"required": ["id", "name", "status"], "enums": {"status": ["active", "deprecated", "superseded"]}},
    "Event":       {"required": ["id", "ts", "action"], "enums": {}},
}

CORE_KINDS = tuple(CORE_ENTITIES)  # the 11


def validate(kind, record):
    """Return (ok, errors). Structural: required fields present + enum membership."""
    errors = []
    spec = CORE_ENTITIES.get(kind)
    if spec is None:
        return False, [f"unknown CORE entity kind '{kind}'"]
    if not isinstance(record, dict):
        return False, ["record is not an object"]
    for f in spec["required"]:
        v = record.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            errors.append(f"{kind}.{f} required but missing/empty")
    for f, allowed in spec["enums"].items():
        if f in record and record[f] is not None and record[f] not in allowed:
            errors.append(f"{kind}.{f}='{record[f]}' not in {allowed}")
    return (not errors), errors
