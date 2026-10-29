# Pesquisa: agente de QA/testes

Data: 2026-10-11. Pedido: adicionar QA ao workflow compartilhado e escolher as melhores skills de inspiração. O repo usa Python stdlib/unittest, scripts Bash, templates Compose e documentação/skills; não mantém uma aplicação frontend própria. Há 24 testes e 15 skills Superpowers já vendorizadas. A mudança não altera Layla, container ou API.

## Evidências e seleção

Consultados o catálogo [skills.sh](https://skills.sh/), `npx --yes skills find testing-strategy` e os arquivos primários das candidatas. Popularidade ajuda a descobrir opções; adequação ao repo determina a seleção.

| Candidata | Evidência e adequação | Decisão |
| --- | --- | --- |
| [Anthropic testing-strategy](https://github.com/anthropics/knowledge-work-plugins/blob/02ffa99ff00ce4d3046ccebabb8357cb39f3ab06/engineering/skills/testing-strategy/SKILL.md) | Estratégia por componente/risco, equilíbrio entre cobertura, velocidade e manutenção; sem exigir framework. Repo Apache-2.0. | Base da escolha da menor matriz suficiente. |
| [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion/SKILL.md) | Exige evidência atual antes de alegar sucesso; já disponível localmente, MIT. | Base do relatório e decisão de QA. |
| [Superpowers test-driven-development](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development/SKILL.md), recurso writing-good-tests | Testar comportamento e detectar regressão real; descarta testes que apenas espelham código/prosa. | Base da qualidade dos testes novos; TDD quando muda comportamento executável. |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging/SKILL.md) | Reprodução, hipótese e causa antes da correção. | Base do encaminhamento de defeitos ao implementador. |
| [Anthropic webapp-testing](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing/SKILL.md) | Browser/Playwright e evidência da interface local. A stack atual não precisa disso para toda mudança. | Referência condicional se mudar jornada web; não instalar browser/Playwright agora. |
| [python-testing-patterns](https://github.com/wshobson/agents/blob/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/python-development/skills/python-testing-patterns/SKILL.md) | Descrição e exemplos iniciais centrados em pytest, fixtures e mocks; repo MIT. | Adiada: unittest já atende; não migrar stack para adotar uma skill. |

As revisões externas são as consultadas, não dependências instaladas. Superpowers permanece inalterado. As instruções próprias serão originais, com atribuição por links; não copiar helpers ou presumir uma licença única para o repo misto anthropics/skills. Não é necessário baixar mais bibliotecas para inspiração.

## Compatibilidade dos agentes

- [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): TOML de projeto em `.codex/agents/`, com name, description e developer_instructions. O repo já usa esse formato. Herdar modelo/permissões da sessão.
- [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents): Markdown em `.claude/agents/`, frontmatter com nome, descrição e ferramentas. QA precisa de Bash para executar testes e escrita para seus artefatos; as instruções delimitam o escopo, sem alegar sandbox somente leitura.
- Contrato comum em `docs/workflow/qa-test.md`; uma skill autocontida com referências relativas pode ser copiada pelo instalador existente.

## Decisão

Pesquisa continua primeiro, seguida de plano técnico com contribuição de QA à matriz, execução Superpowers, verificação de QA e integração/release. QA compara critérios com comportamento e evidências; a revisão de código existente continua responsável por qualidade estrutural. QA não faz merges, releases ou correções silenciosas de produto.

Dois modos bastam: planejar testes e verificar entrega. Uma matriz pequena pode ficar no plano; mudanças maiores usam `qa-plan.md`. Registrar SHA, comandos, exit codes, esperado/obtido e limitações em `qa-report.md`. Teste obrigatório indisponível bloqueia o critério; teste fora do escopo não deve criar trabalho artificial. Smoke de container, inferência real e browser são condicionais ao que mudou. CI existente valida execução, não interpreta aprovação textual de QA.

Não há decisão do usuário pendente. Confirmar portabilidade por instalação em diretório temporário, links dos dois provedores e avaliação independente da skill com tarefa realista isolada.
