"""DEV-FP regression — secret-scan exclusion scope (panel dissent: must not blanket-exclude tests/hooks).
Real secret in a test/non-scanner file = CAUGHT · only scanner-def files + allowlist-tagged lines skip.
Run: python engine/test_secretscan_scope.py
"""
import os
import subprocess
import sys
import tempfile

ENGINE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(ENGINE, "check.py")
git = __import__("shutil").which("git")
cases = []
def check(name, cond): cases.append((name, bool(cond)))

SECRET = 'api_key = "sk-realleak1234567890"\n'  # allowlist-secret (fixture constant; written into temp repos, not a real leak)


def scan(repo):
    p = subprocess.run([sys.executable, CHECK, "secret-scan", "--root", repo],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode  # 1 = caught/blocked, 0 = clean


def repo_with(path, content):
    d = tempfile.mkdtemp()
    subprocess.run([git, "init", "-q"], cwd=d)
    subprocess.run([git, "config", "user.email", "t@t"], cwd=d)
    subprocess.run([git, "config", "user.name", "t"], cwd=d)
    full = os.path.join(d, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    subprocess.run([git, "add", "."], cwd=d)
    return d


if not git:
    print("[SKIP] git not available"); sys.exit(0)

# real secret in a TEST file (no pragma) -> CAUGHT (the panel security concern)
check("secret in tests/ file -> CAUGHT", scan(repo_with("tests/leak.py", SECRET)) == 1)
# real secret in a normal code file -> CAUGHT
check("secret in app code -> CAUGHT", scan(repo_with("src/app.py", SECRET)) == 1)
# real secret in a NON-scanner hook -> CAUGHT (not blanket-excluding hooks/)
check("secret in non-scanner hook -> CAUGHT", scan(repo_with("platforms/claude-code/hooks/custom.sh", SECRET)) == 1)
# allowlist-tagged fixture line -> SKIPPED (intentional fake)
check("allowlist-tagged line -> skipped", scan(repo_with("tests/fixture.py", 'api_key = "sk-fake1234567890"  # allowlist-secret\n')) == 0)
# scanner-definition file (gate yaml) -> SKIPPED (it DEFINES the pattern)
check("engine/gates yaml -> skipped (self-def)", scan(repo_with("engine/gates/x.yaml", 'patterns:\n  - api_key.*sk-[a-z0-9]{16}\n')) == 0)

for n, ok in cases:
    print(f"  {'PASS' if ok else 'FAIL'}  {n}")
failed = [n for n, ok in cases if not ok]
if failed:
    print(f"\n[FAIL] {len(failed)}/{len(cases)}")
    sys.exit(1)
print(f"\n[OK] {len(cases)}/{len(cases)} secret-scan scope tests passed")
