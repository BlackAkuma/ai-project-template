"""F4/P10: vector memory interface + in-memory fallback (BRD FR-2 cross-session retrieval).

Wing/Room/Drawer scoping (core/19): Wing=project, Room=repo/area, Drawer=chunk.
Real backend = Qdrant (lazy import); fallback = in-memory token-overlap similarity (offline,
deterministic, testable). Retrieval is a VIEW (never authoritative — canonical truth = JSON-in-git).
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
