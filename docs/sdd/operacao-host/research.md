# Pesquisa: problemas de operação encontrados pelo operador do host

Data: 2026-10-28. Pedido: o operador do host (root) registrou quatro problemas desta instalação. Cada problema segue este fluxo SDD. Esta etapa é só pesquisa. Não há código de produto.

O repositório é público. Este documento não registra endereço IP, nome de host nem segredos.

## Problemas e evidências

| ID | Problema | Evidência (2026-10-28) | Causa provável |
| --- | --- | --- | --- |
| P1 | `local-laya-skills` cria um link `project-qa` que aponta para uma pasta que não existe | `find ~/.claude/skills -xtype l` mostra `project-qa` quebrado em três pastas de skills de outro usuário | `project-qa` está em `develop` (PR #1, `3b38dbd`). A cópia instalada usa `main` (`0ef523f`), que não tem a skill |
| P2 | `GET /health` retorna `chroma_ok: false` com `vector_store: enabled` e `use_chroma: true` | resposta de `/health` | Desconhecida. Um backup `data-pre-chroma-*.tgz` mostra uma mudança recente no Chroma |
| P3 | A API recusa pedidos: `System is under load (CPU or RAM). Try again in a moment.` | dois pedidos recusados. CPU do host 92% e 83%. Limite `hard_cpu_percent=85` | O governador mede a CPU do host inteiro, não a do container (limite `cpus: 4`). Outros projetos ocupam a CPU e bloqueiam Layla |
| P4 | Não há backup agendado de `runtime/data` | sem crontab e sem timer. Só existe um backup manual | O instalador não cria rotina de backup |

## Alternativas e decisão recomendada

- P1: fazer a release `develop` → `main` conforme `docs/workflow/RELEASE.md` e atualizar a cópia instalada. Alternativa recusada: remover `project-qa` do instalador, porque a skill já foi aceita em `develop`.
- P2: reproduzir com o container atual. Ler o log `data/logs/layla.log` e o código de saúde do upstream na revisão `336ee4a`. Decidir depois da causa.
- P3: medir a CPU do container (cgroup) em vez da CPU do host, ou expor o limite como configuração. A escolha muda o upstream ou só a configuração local. Pergunta ao dono.
- P4: um script em `skills/layla-docker/assets/container/layla` (`./layla backup`), com o agendamento feito pelo operador do host.

## Dúvidas que mudam a implementação

1. P3: é aceitável alterar o comportamento do upstream, ou só a configuração gerada por `setup.py`?
2. P4: quantas cópias guardar e em qual pasta?

## Próxima etapa

Papel `tech-planner`: `spec.md`, `plan.md` e `plan.json` nesta pasta. Validar com `python3 scripts/check-plan.py docs/sdd/operacao-host/plan.json`.
