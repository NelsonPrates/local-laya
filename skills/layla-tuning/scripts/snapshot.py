#!/usr/bin/env python3
"""Fotografia somente leitura de uma instância Layla: saúde, configuração, orçamento, projetos e learnings."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# As chaves que decidiram o resultado nas medições; o resto de /settings é ruído para esta tarefa.
SETTINGS_KEYS = (
    "model_filename", "n_ctx", "completion_max_tokens", "performance_mode", "max_runtime_seconds",
    "max_tool_calls", "auto_tune_enabled", "auto_tune_locked_keys", "knowledge_min_similarity",
    "knowledge_max_bytes", "prompt_optimizer_enabled", "use_chroma", "n_threads", "n_batch", "temperature",
)
LOCKED = ("n_ctx", "completion_max_tokens", "performance_mode", "max_runtime_seconds")
# Learnings que o próprio agente grava a cada consulta; acumulam sem informar nada sobre o projeto.
NOISE_PREFIXES = ("Reflection (", "Tool pattern:")


def local_url(value):
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise argparse.ArgumentTypeError("use uma URL http de loopback")
    return value.rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get(base_url, path, timeout):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(urllib.request.Request(base_url + path, headers={"Accept": "application/json"}), timeout=timeout) as response:
        return json.load(response)


def load_average():
    try:
        with open("/proc/loadavg", encoding="ascii") as handle:
            return [float(value) for value in handle.read().split()[:3]]
    except OSError:
        return None


def collect(base_url, timeout):
    """Cada rota é lida uma vez; uma rota que falha vira `error` naquela seção, sem abortar as outras."""
    sections = {
        "health": "/health?deep=true",
        "context_budget": "/health/context_budget",
        "settings": "/settings",
        "not_in_force": "/settings/not_in_force",
        "projects": "/projects",
        "learnings": "/learnings?limit=100",
    }
    raw = {}
    for name, path in sections.items():
        try:
            raw[name] = get(base_url, path, timeout)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            raw[name] = {"error": str(exc)}
    return raw


def summarise(raw):
    health = raw["health"]
    settings = raw["settings"]
    learnings = raw["learnings"].get("items", []) if "error" not in raw["learnings"] else []
    projects = raw["projects"].get("projects", []) if "error" not in raw["projects"] else []
    out = {
        "load_average": load_average(),
        "health": {key: health.get(key) for key in ("status", "model_loaded", "chroma_ok", "vector_store", "learnings", "error") if key in health},
        "chroma_dependency": (health.get("dependencies") or {}).get("chroma"),
        "settings": {key: settings[key] for key in SETTINGS_KEYS if key in settings},
        "not_in_force": [item.get("key") for item in raw["not_in_force"].get("not_in_force", [])],
        "head_budget_tokens": raw["context_budget"].get("n_ctx"),
        "projects": [
            {"id": item.get("id"), "name": item.get("name"), "aspect_default": item.get("aspect_default"),
             "preamble_words": len((item.get("system_preamble") or "").split())}
            for item in projects
        ],
        "learnings": [{"id": item.get("id"), "type": item.get("type"), "content": (item.get("content") or "")[:100]} for item in learnings],
    }
    out["findings"] = findings(out, raw)
    return out


def findings(out, raw):
    notes = []
    for name, data in raw.items():
        if "error" in data:
            notes.append(f"{name}: rota indisponível ({data['error']})")
    if out["health"].get("model_loaded") is False:
        notes.append("model_loaded=false: nenhuma resposta virá do modelo")
    if "chroma_ok" in out["health"] and out["health"]["chroma_ok"] is not True:
        notes.append("chroma_ok não é true na sondagem profunda: imagem sem o extra core ou Chroma quebrado")
    locked = out["settings"].get("auto_tune_locked_keys")
    if locked is not None:
        missing = [key for key in LOCKED if key not in locked]
        if missing:
            notes.append("auto-tune ainda controla: " + ", ".join(missing))
    if out["not_in_force"]:
        notes.append("gravado mas não em vigor: " + ", ".join(map(str, out["not_in_force"])))
    noise = [item["id"] for item in out["learnings"] if item["content"].startswith(NOISE_PREFIXES)]
    if noise:
        notes.append(f"learnings gravadas pelo próprio agente (ids {noise}): revisar com o dono antes de apagar")
    for project in out["projects"]:
        if project["aspect_default"] == "echo":
            notes.append(f"projeto {project['name']}: aspect echo entrou em loop de search_memories em teste real")
        if project["preamble_words"] > 200:
            notes.append(f"projeto {project['name']}: preâmbulo de {project['preamble_words']} palavras pode ser truncado")
    return notes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", type=local_url, default=local_url(os.environ.get("LAYLA_BASE_URL", "http://127.0.0.1:8000")))
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--raw", action="store_true", help="imprimir também as respostas completas das rotas")
    args = parser.parse_args(argv)
    raw = collect(args.base_url, args.timeout)
    result = summarise(raw)
    if args.raw:
        result["raw"] = raw
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 1 if all("error" in data for data in raw.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
