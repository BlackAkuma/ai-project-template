"""F4/P10: retrieval interface + offline fallback (BRD FR-2 retrieval seam).

⚠️ HONEST SCOPE (panel-driven): the offline fallback is **LEXICAL token-overlap (Jaccard),
NOT semantic vector search**. Synonyms/paraphrases will NOT match. Real semantic retrieval
(embeddings) = the Qdrant backend, which is a DEFERRED seam (get_store('qdrant') raises until wired).
Do NOT market 'semantic memory' until the embedding backend lands.

Wing/Room/Drawer scoping (core/19): Wing=project, Room=repo/area, Drawer=chunk.
Retrieval is a VIEW (never authoritative — canonical truth = JSON-in-git, ADR-012).
Budget controls (k, score floor) per core/20 to bound context cost (NFR-8).
"""
import re


def _tokens(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def _sim(q, d):
    a, b = _tokens(q), _tokens(d)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)  # Jaccard (stub for embeddings; deterministic offline)


class InMemoryStore:
    """Offline fallback store. Same interface a Qdrant-backed store would expose."""

    def __init__(self):
        self._docs = []  # {text, meta, wing, room}

    def add(self, text, meta=None, wing="default", room="default"):
        self._docs.append({"text": text, "meta": meta or {}, "wing": wing, "room": room})

    def search(self, query, wing=None, room=None, k=5, floor=0.0):
        hits = []
        for d in self._docs:
            if wing is not None and d["wing"] != wing:
                continue
            if room is not None and d["room"] != room:
                continue
            score = _sim(query, d["text"])
            if score >= floor:
                hits.append({"text": d["text"], "meta": d["meta"], "score": round(score, 4)})
        hits.sort(key=lambda h: h["score"], reverse=True)
        return hits[:k]


def get_store(backend="memory"):
    """Factory. backend='memory' (offline) | 'qdrant' (real, lazy)."""
    if backend == "qdrant":
        from qdrant_client import QdrantClient  # noqa: F401  (only if installed)
        raise NotImplementedError("qdrant adapter: wire QdrantClient here (real backend)")
    return InMemoryStore()
