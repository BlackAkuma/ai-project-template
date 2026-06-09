"""Launch the engine API + web Cockpit against the seeded demo project (for preview/first-run).
Run seed_demo first. Used by .claude/launch.json 'engine-demo'."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed_demo import seed  # noqa: E402
from api import serve  # noqa: E402

if __name__ == "__main__":
    seed()  # ensure demo scenario is populated
    serve(port=int(os.environ.get("PORT", "8777")), root="engine/demo_data")
