"""F4/P10 test — vector memory retrieval + Wing/Room scoping + budget (FR-2).
Run: python engine/test_memory.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory import get_store  # noqa: E402

cases = []
def check(name, cond): cases.append((name, bool(cond)))

s = get_store("memory")
s.add("the governance gate blocks fake done with no evidence", {"id": "d1"}, wing="proj", room="engine")
s.add("the canonical store renders prose views from json", {"id": "d2"}, wing="proj", room="engine")
s.add("marketing outreach for design partners willingness to pay", {"id": "d3"}, wing="proj", room="gtm")

# relevance ranking
top = s.search("gate blocks fake done evidence", wing="proj")
check("most relevant doc ranked #1", top[0]["meta"]["id"] == "d1")
check("scores descending", all(top[i]["score"] >= top[i + 1]["score"] for i in range(len(top) - 1)))

# Wing/Room scoping
eng = s.search("store", wing="proj", room="engine")
check("room scoping excludes gtm", all(h["meta"]["id"] != "d3" for h in eng))
gtm = s.search("partners", wing="proj", room="gtm")
check("gtm room returns d3", any(h["meta"]["id"] == "d3" for h in gtm))

# budget: k limit + score floor
check("k=1 returns one", len(s.search("the", wing="proj", k=1)) == 1)
check("score floor filters weak matches", all(h["score"] >= 0.5 for h in s.search("gate evidence done", wing="proj", floor=0.5)))
check("no-match query -> empty", s.search("zzz nonexistent qqq", wing="proj", floor=0.1) == [])

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} vector-memory tests passed")
