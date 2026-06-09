"""F1 / P7: model-agnostic adapter + role-floor (BRD FR-4.1/4.2, ADR-008 model-floor).

เสียบ model ไหนก็ได้ผ่าน provider registry (LiteLLM = real, lazy; 'stub' = offline test).
role-floor: model ที่ capability tier ต่ำกว่า floor ของ lane → ปฏิเสธ (กัน weak model ทำงาน
ที่ governance พึ่งพา — thesis "context>model" มีพื้น). enforcement = structural, ไม่เชื่อโมเดล.
"""

# Curated capability registry (tier 0-3). Extend as models are evaluated (NFR-7 additive).
MODEL_TIER = {
    "stub-weak": 0, "stub-strong": 3,
    "claude-sonnet": 3, "claude-haiku": 2, "gpt-4o": 3, "gpt-4o-mini": 2,
    "deepseek-v3": 3, "qwen2.5-7b": 1, "llama3-8b": 1, "local-3b": 0,
    # local Ollama models (run on your machine, free, no key)
    "qwen2.5-coder:7b": 2, "qwen2.5:7b": 2, "llama3.1:8b": 2,
    "qwen2.5:3b": 1, "llama3.2:3b": 1, "phi3.5": 1,
}
# Min tier per lane (FR-4.2). code/architect work needs capable models; weak → advisory only.
ROLE_FLOOR = {"read-only": 0, "advisory": 1, "code-author": 2, "architect": 3}

PROVIDERS = {}


def provider(name):
    def reg(fn):
        PROVIDERS[name] = fn
        return fn
    return reg


@provider("stub")
def _stub(messages, model, **_):
    last = messages[-1]["content"] if messages else ""
    return f"[stub:{model}] echo: {last[:60]}"


@provider("litellm")
def _litellm(messages, model, **_):  # cloud provider — lazy import, offline-safe
    import litellm  # noqa: F401  (only if installed/used)
    resp = litellm.completion(model=model, messages=messages)
    return resp["choices"][0]["message"]["content"]


@provider("ollama")
def _ollama(messages, model, **_):  # LOCAL provider — free, no key, stdlib only (no deps)
    import json as _json
    import urllib.request
    body = _json.dumps({"model": model, "messages": messages, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return _json.loads(r.read())["message"]["content"]


def ollama_status():
    """Return (up, info). Checks if the local Ollama server is running + which models are pulled."""
    import json as _json
    import urllib.request
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            models = [m["name"] for m in _json.loads(r.read()).get("models", [])]
        return True, models
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def assign(model, role):
    """Enforce role-floor BEFORE any call. Returns (ok, reason)."""
    tier = MODEL_TIER.get(model)
    if tier is None:
        return False, f"unknown model '{model}' (not in capability registry)"
    floor = ROLE_FLOOR.get(role)
    if floor is None:
        return False, f"unknown role '{role}'"
    if tier < floor:
        return False, f"{model} (tier {tier}) below '{role}' floor (tier {floor}) — refused"
    return True, "ok"


def complete(messages, model="stub-strong", role="advisory", provider_name="stub"):
    """Route a completion through role-floor enforcement + the chosen provider."""
    ok, reason = assign(model, role)
    if not ok:
        return {"ok": False, "reason": reason, "lane_refused": True}
    fn = PROVIDERS.get(provider_name)
    if fn is None:
        return {"ok": False, "reason": f"unknown provider '{provider_name}'"}
    try:
        return {"ok": True, "text": fn(messages, model), "model": model, "role": role}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "reason": f"provider error: {e}"}
