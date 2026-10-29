# Pesquisa: Layla como conselheira de fluxo em CPU

Evidência colhida em 2026-10-27 na instância compartilhada (revisão `336ee4a`, Qwen2.5-7B Q4_K_M, 6 CPUs, 12 GB) usada pelo langerie-store.

- `GET /health/context_budget`: `n_ctx` efetivo 2048 com 8192 configurado; total a 103%, `system_instructions` e `memory` truncados. Os pedidos com estado de roadmap perdiam parte do texto.
- Causa em duas camadas (`agent/services/infrastructure/system_optimizer.py`): o auto-tune grava `performance_mode=low` em CPU (`auto_tune_owned_keys` inclui `performance_mode`, `n_ctx`, `completion_max_tokens`), e `low` aplica `min(2048, n_ctx)`; depois, independente do modo, CPU > 75% corta para 3072 e > 90% para 2048.
- `POST /settings` com `auto_tune_locked_keys` + `performance_mode=mid` entra em vigor sem reinício (`report[].outcome=took_effect`); o efetivo passou a 3072 com a CPU em 80% (CI no mesmo host).
- `chroma_ok=false`: o log diz `No module named 'chromadb'`. O Dockerfile instala `[cpu,llm]`; `chromadb>=0.6.0,<1` está no extra `core` de `pyproject.toml`. `pip install --dry-run` no container resolve `chromadb-0.6.3` só com wheels (inclui `posthog`, telemetria do Chroma).
- `/history`: todas as perguntas de fluxo saíram com a aspect `morrigan` (implementação). `/aspects/echo` descreve "workflow alignment, session continuity".
- `/learnings`: a learning de estratégia registra `read_file: failed` ×3 — o modelo tentou ler o repositório, que não está em `/workspace`.
- `routers/agent.py`: `project_id` antepõe `system_preamble` ao contexto e aplica `aspect_default` quando o pedido não traz aspect. O cliente não expunha `aspect_id` nem `project_id`.
- Teste real pelo projeto: aspect `echo` estourou `max_runtime_seconds=600` (703 s) em loop de `search_memories`; `nyx` com `max_tool_calls=1` respondeu em 738 s.
