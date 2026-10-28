# Especificação: layla-optimizer-agent

- `docs/workflow/layla-optimization.md` dá o passo a passo em ordem: quem pode mudar o quê, linha de base, dependências e imagem, configuração, projeto/aspect, memória, forma do pedido, medição e decisão, registro e reversão — com os valores medidos e os limites conhecidos.
- Papel `layla-optimizer` em `.claude/agents/` e `.codex/agents/`, com as mesmas instruções: seguir o roteiro, uma alavanca por rodada, autorização explícita para cada mudança na instância, nunca reenviar POST.
- Skill `layla-tuning`: `scripts/snapshot.py` lê somente rotas GET (`/health?deep=true`, `/health/context_budget`, `/settings`, `/settings/not_in_force`, `/projects`, `/learnings`), filtra `/settings` às chaves relevantes, e lista achados (Chroma, modelo, chaves não travadas, `not_in_force`, learnings do próprio agente, aspect `echo`, preâmbulo longo). Uma rota falha não aborta as outras; todas falhando dá código 1. Só loopback.
- Skill `layla-benchmark`: `scripts/bench.py run` envia cada pergunta uma vez por rodada (um registro existente impede o reenvio), grava JSONL com tempo, carga, resposta, palavras, `plan_shaped`, `expect_found` e contagem de logs opcional; `compare` imprime tabela Markdown. Só loopback, escrita/execução desligadas.
- Registro: `check-skills`, `install-skills`, links de descoberta, README, AGENTS.md, SDD.md e CHANGELOG.

Aceitação: testes unitários dos dois scripts contra servidor local; `check-skills` e `check-plan` passando; `snapshot.py` executado contra a instância real.
