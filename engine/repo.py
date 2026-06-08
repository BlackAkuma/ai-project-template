"""F3/P9: multi-repo orchestration (BRD FR-5).

project = manifest of repos + cross-repo entity-register. When a shared entity (e.g. an
API contract) changes, detect which consumer repos are impacted and route a governed slice.
DETECT + ROUTE + SEQUENCE only — NOT atomic cross-repo refactor (human owns the seam, FR-5.3).
manifest = JSON-in-git (ADR-012). Always-in-context project_map is the coherence trick.
"""
import json
import os


def load_manifest(path):
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return {"repos": [], "entities": []}


def _entity(manifest, entity_id):
    for e in manifest.get("entities", []):
        if e["id"] == entity_id:
            return e
    return None


def impacted_by(manifest, entity_id):
    """Consumer repos impacted if this cross-repo entity changes (declared edges)."""
    e = _entity(manifest, entity_id)
    return list(e.get("consumers", [])) if e else []


def detect_drift(manifest, changed_entity_ids):
    """For each changed shared entity, flag owner + impacted consumers (detect, not refactor)."""
    out = []
    for eid in changed_entity_ids:
        e = _entity(manifest, eid)
        if not e:
            continue
        out.append({"entity": eid, "name": e.get("name"), "owner_repo": e.get("owner_repo"),
                    "impacted": list(e.get("consumers", [])), "status": e.get("status", "active")})
    return out


def deprecated_entities(manifest):
    return [e["id"] for e in manifest.get("entities", []) if e.get("status") in ("deprecated", "superseded")]


def project_map(manifest):
    """Always-in-context summary: repos + their purpose + cross-repo seams (FR-5.1)."""
    lines = ["# Project Map"]
    for r in manifest.get("repos", []):
        lines.append(f"- repo {r['id']} ({r.get('role', '?')}): {r.get('purpose', '')}")
    lines.append("# Cross-repo seams")
    for e in manifest.get("entities", []):
        cons = ",".join(e.get("consumers", []))
        lines.append(f"- {e['name']} [{e.get('status', 'active')}]: {e.get('owner_repo')} -> [{cons}]")
    return "\n".join(lines)
