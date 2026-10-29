# Escolher a menor matriz suficiente

Use critérios reais da mudança; esta tabela é um ponto de partida, não uma obrigação de rodar todas as linhas. Respeite o prefixo RTK quando exigido pelo ambiente.

| Mudança | Verificação útil | Limite da evidência |
| --- | --- | --- |
| Skill/contrato/documentação | Validar metadados/links, executar exemplos alterados e testar uma solicitação realista se instruções forem complexas | Não criar testes que procuram palavras ou headings; leitura estrutural não prova decisões do agente |
| Gerador/instalador | Rodar em diretório temporário; conferir arquivos/valores, recusa de sobrescrita, entradas inválidas e dados preservados | Não usar runtime pessoal para provar preservação |
| Cliente HTTP | Servidor local controlado para payload, erros, timeout, redirecionamento e efeitos proibidos conforme o contrato alterado | Não chamar isso de inferência real |
| Worktrees/locks | Clone temporário, tarefas concorrentes, exclusividade, limpeza/ancestralidade | Reservas são locais ao clone, não distribuídas |
| Compose/Docker | Gerar instalação isolada e `docker compose --project-directory <instalacao> config --quiet`; se muda inicialização, build/up/health/down reais | Sintaxe/config não prova container iniciado; health não prova modelo carregado |
| Inferência | GGUF autorizado, ready positivo e resposta não vazia coerente na API real | Sem modelo, critério de inferência obrigatório fica blocked; não baixar um modelo só para encerrar QA |
| Jornada web alterada | Browser real, passos do usuário, assertions por estado/elemento e captura de falha | Aplicar Playwright apenas se útil/disponível; esperas fixas e prints sozinhos não provam sucesso |
| Release/hotfix | Checks relevantes, versão/notas, CI e SHA candidato combinado | `check-release.py` verifica consistência local; não criar tag pública como experimento |

Comandos usuais na raiz do local-layla:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-skills.py
python3 scripts/check-vendor.py
python3 scripts/check-plan.py docs/sdd/<mudanca>/plan.json
bash -n skills/layla-docker/assets/container/layla
```

Em teste de runtime paralelo, use instalação temporária própria, porta livre, `COMPOSE_PROJECT_NAME` exclusivo e diretórios de data/models/workspace não compartilhados. Finalize apenas recursos que o teste criou. Não confundir ambiente indisponível com defeito de produto nem com sucesso.

Para testes novos, derive esperado do contrato; confira se uma mudança plausível no comportamento os faria falhar. Na implementação de comportamento novo/correção, o implementador aplica TDD quando pertinente. QA pode evidenciar lacuna com uma reprodução sem assumir a correção.

## Skills selecionadas como inspiração

| Fonte primária | Aplicação nesta skill |
| --- | --- |
| [Anthropic testing-strategy](https://github.com/anthropics/knowledge-work-plugins/blob/02ffa99ff00ce4d3046ccebabb8357cb39f3ab06/engineering/skills/testing-strategy/SKILL.md) | Selecionar níveis por risco e equilibrar confiança, tempo e manutenção |
| [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion/SKILL.md) | Exigir execução/evidência antes de alegar aprovação |
| [Superpowers test-driven-development](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development/SKILL.md) e [writing-good-tests](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development/writing-good-tests.md) | Testar comportamento e regressões reais sem espelhar implementação |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging/SKILL.md) | Reproduzir falhas e investigar causa antes da correção |
| [Anthropic webapp-testing](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing/SKILL.md) | Condicional para interface local: observação no browser e evidências de jornada |

Consulta: 2026-10-11. São referências de método; a skill é autocontida e não exige instalá-las. No repo local-layla as três skills Superpowers já estão em `vendor/superpowers/skills/`. A instrução explícita da sessão e o contrato local prevalecem. Não copiar instalações/hooks nem adicionar pytest/Playwright por associação. A comparação completa das candidatas fica na pesquisa SDD da mudança qa-test-agent do projeto.
