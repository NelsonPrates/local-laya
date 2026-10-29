# Changelog

## 0.2.0

- Papel `layla-optimizer` (Claude e Codex) e passo a passo de otimização em `docs/workflow/layla-optimization.md`.
- Skill `layla-tuning`: alavancas medidas e `snapshot.py`, fotografia somente leitura com achados.
- Skill `layla-benchmark`: `bench.py` envia cada pergunta uma vez, registra tempo, carga, resposta, forma de plano e ferramentas, e compara rodadas.
- Configuração gerada trava `n_ctx`, `completion_max_tokens` e `performance_mode=mid` contra o auto-tune, que cortava o contexto para 2048 em CPU.
- Imagem instala o extra `core` (chromadb), com telemetria anônima desligada.
- Cliente: `--aspect`, `--project-id`, subcomando `budget` e aviso de pedido longo; skill layla-local ensina a pedir conselho a um modelo pequeno.
- Agente QA/testes compartilhado por Codex e Claude, skill project-qa autocontida e seleção de referências primárias.
- Matriz de testes no planejamento SDD e relatório com evidências antes da integração Gitflow.

## 0.1.0

- Skills de geração/instalação Docker, uso da API local e pesquisa do projeto.
- Workflow SDD compartilhado por Codex e Claude, papel tech-planner e worktrees com reservas.
- Superpowers vendorizado em revisão fixa e fluxo Gitflow de release/hotfix.

Versão preparada no bootstrap; a existência desta seção não implica tag ou release publicada.
