# Pesquisa: agente e passo a passo para otimizar o Layla

Pedido do dono (2026-10-28): documentar o passo a passo das otimizações feitas na instância compartilhada e criar neste repositório um agente com skills especializadas em criar, configurar e otimizar os resultados do Layla e de suas dependências.

- O que já existe: `layla-docker` cobre imagem, Compose, GGUF, chromadb e telemetria; `layla-local` cobre o cliente e a forma do pedido (inclui `Answer in one line.`). Faltam o diagnóstico da configuração viva e a medição antes/depois, feitos até aqui à mão com `curl` e um script temporário.
- Evidência de [advisor-tuning](../advisor-tuning/research.md) e das rodadas de 2026-10-27/28: auto-tune corta `n_ctx` sem `auto_tune_locked_keys`; corte por CPU não configurável; `/health` simples sempre `chroma_ok=false`; `echo` em loop; 3B não mais rápido sob carga; `model_override` ignorado; `prompt_optimizer` reescreve pedidos e só respeita restrição de tamanho em inglês; `POST /settings` recusa `prompt_optimizer_enabled`, `knowledge_max_bytes`, `prompt_budgets`.
- Novo nesta pesquisa (`/openapi.json` e rotas vivas): `/settings/not_in_force` nomeia chaves sobrescritas pelo auto-tune (`n_batch` hoje); `/health/context_budget` informa o cabeçalho (1146 tokens); `/learnings` mostra que cada consulta grava sozinha uma `Reflection (…)` e um `Tool pattern: …` (ids 6, 8, 10).
- Agentes do repositório seguem o par `.claude/agents/*.md` + `.codex/agents/*.toml`; skills são validadas por `scripts/check-skills.py`, instaladas por `scripts/install-skills.py` e descobertas por links em `.agents/skills` e `.claude/skills`.

Alternativas: (A) um agente e duas skills novas, `layla-tuning` e `layla-benchmark`, reaproveitando as duas existentes; (B) um agente e uma skill única; (C) só o documento. Recomendado: A — cada skill tem um script testável e um gatilho distinto, e as existentes não crescem.
