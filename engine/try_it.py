"""ลองใช้ A1 + A2 ในคำสั่งเดียว — narrated demo.
  python engine/try_it.py
แสดง: (A1) AI ตัวจริงในเครื่องตอบเรื่อง governance · (A2) engine บล็อก commit ที่มี secret จริง
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from llm import complete, ollama_status  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def line(c="─"):
    print(c * 60)


def a1_real_ai():
    line("="); print("  A1 — AI ตัวจริงในเครื่องคุณ (ฟรี ไม่มี key)"); line("=")
    up, info = ollama_status()
    if not up:
        print("  ⚠️  Ollama ยังไม่รัน — เปิดโปรแกรม Ollama ก่อน (หรือ `ollama serve`)")
        return
    print(f"  ✓ Ollama รันอยู่ · โมเดล: {info}")
    q = "A task is marked done but has NO test evidence and NO commit. In one short sentence: approve or block, and why?"
    print(f"\n  ❓ ถาม AI: {q}\n  ⏳ (AI ในเครื่องกำลังคิด...)")
    r = complete([{"role": "user", "content": q}], model="qwen2.5-coder:7b", role="advisory", provider_name="ollama")
    if r["ok"]:
        print(f"\n  🤖 AI ในเครื่องตอบ: \"{r['text'].strip()}\"")
        print("  → AI เล็กๆ ในเครื่อง + บริบท governance = เข้าใจงานได้ (thesis: context > model)")
    else:
        print(f"  ⚠️  {r['reason']}")


def a2_governance():
    print(); line("="); print("  A2 — governance บล็อก action จริง (commit ที่มี secret)"); line("=")
    git = _which("git")
    if not git:
        print("  ⚠️  ไม่พบ git"); return
    eng = os.path.join(REPO, "engine", "check.py")

    for label, content, expect in [
        ("commit ที่มี SECRET (api_key)", 'api_key = "sk-secret1234567890"\n', "BLOCK"),
        ("commit โค้ดสะอาด", 'def add(a, b):\n    return a + b\n', "ALLOW"),
    ]:
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([git, "init", "-q"], cwd=d)
            open(os.path.join(d, "x.py"), "w").write(content)
            subprocess.run([git, "add", "."], cwd=d)
            p = subprocess.run([sys.executable, eng, "secret-scan", "--root", d],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            blocked = p.returncode == 1
            verdict = "🔴 BLOCKED" if blocked else "✅ ALLOWED"
            ok = "✓" if ((expect == "BLOCK") == blocked) else "✗"
            print(f"\n  {ok} {label}\n      engine → {verdict}")
            if blocked:
                msg = [l for l in p.stdout.splitlines() if "->" in l or "secret" in l.lower()]
                if msg:
                    print(f"      เหตุผล: {msg[-1].strip()[:70]}")


def _which(x):
    import shutil
    return shutil.which(x) or shutil.which(x + ".exe")


if __name__ == "__main__":
    a1_real_ai()
    a2_governance()
    print(); line()
    print("  สรุป: AI ตัวจริง (A1) + governance ที่บังคับได้จริง (A2) = ทำงานบนเครื่องคุณ")
    print("  ลอง commit จริง: สร้างไฟล์ที่มี api_key=\"...\" แล้ว git commit → git hook จะบล็อก")
