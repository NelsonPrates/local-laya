# local-layla: contrato dos agentes

Projeto: duas skills de instalação/uso de PapaKoftes/Layla e skills de pesquisa e QA para manutenção. Não alterar o produto upstream sem pedido correspondente.

- Começar cada mudança de desenvolvimento/manutenção com `skills/project-research/SKILL.md`; depois usar o papel `docs/workflow/tech-planner.md` com matriz QA proporcional. Seguir `docs/workflow/SDD.md`: pesquisa → plano técnico → execução Superpowers → QA → integração/release.
- Usar `docs/workflow/qa-test.md` e `skills/project-qa/SKILL.md` no planejamento dos testes e na verificação final. Registrar evidência por critério/SHA em `qa-report.md`; check obrigatório falho ou indisponível impede recomendar integração. Revalidar o conteúdo combinado e alterações que afetem evidências.
- Usar a revisão local de Superpowers em `vendor/superpowers/skills/`. Depois do plano, a próxima skill é a execução registrada (`executing-plans` ou `subagent-driven-development`), com seus recursos pertinentes. Instruções explícitas do usuário prevalecem; não solicitar novamente autorização já existente. Não alterar arquivos vendorizados para mudar o processo.
- Toda tarefa deve ter resultado observável, arquivos, dependências, verificação e dono. Preferir a menor ordem suficiente; revisar e eliminar tarefas desnecessárias antes de executar.
- Trabalho simultâneo: um escritor por worktree/tarefa; reservar com `scripts/worktree.py`. Paralelizar apenas tarefas independentes com arquivos distintos. Somente o coordenador altera plano/spec compartilhados e integra branches.
- Respeitar mudanças de outros agentes. Não fazer reset, clean, force-push ou exclusão de worktrees/reservas de terceiros para resolver conflitos.
- Gitflow: `feature/*` → `develop`; `release/*` parte de `develop` → `main` e retorna a `develop`; `hotfix/*` parte de `main` → `main` e retorna a `develop`/release ativa. Seguir `docs/workflow/RELEASE.md`.
- Verificação usual: `python3 -m unittest discover -s tests -v`, `python3 scripts/check-skills.py`, `bash -n skills/layla-docker/assets/container/layla`. Validar Compose para mudanças nos templates e o container real quando a mudança altera inicialização. Só afirmar inferência real quando houver GGUF carregado e resposta verificada.
- Não versionar dados, modelos, `.env`, tokens, runtime ou estado de sessão. O repositório é público. Preservar licenças e locks de origem ao atualizar dependências vendorizadas.
- Se o ambiente exige RTK, prefixar comandos de shell com `rtk` (`rtk proxy` para comandos sem adaptação).

Pesquisa, planos e entregas vivem em `docs/sdd/<mudanca>/`. O bootstrap inicial consolida trabalho já autorizado pelo usuário; não representa autorização permanente para publicar futuras releases.
