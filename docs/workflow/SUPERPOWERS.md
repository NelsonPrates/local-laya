# Superpowers local

Origem: [obra/superpowers](https://github.com/obra/superpowers), revisão
`bb92a77741419a4ab5f06e711a283343f1ada0c3`, consultada/baixada em 2026-10-11.
Foram incluídas as 15 skills completas, seus recursos e executáveis, README e licença MIT.
`vendor/superpowers/source.lock.json` registra SHA-256 de cada arquivo. Os links
de descoberta não duplicam ou reescrevem os arquivos upstream.

## Roteamento do projeto

| Situação | Skill local |
| --- | --- |
| Começar a execução após pesquisa/plano | `using-superpowers`, depois a execução do plano |
| Executar diretamente na sessão | `executing-plans` |
| Controlar implementadores e revisão por tarefa | `subagent-driven-development` |
| Isolar workspace | `using-git-worktrees` + reserva de `scripts/worktree.py` |
| Paralelizar investigações/tarefas independentes | `dispatching-parallel-agents`, com os limites de arquivos/worktrees do projeto |
| Investigar falha | `systematic-debugging` |
| Implementar comportamento verificável | `test-driven-development`, proporcional à mudança |
| Revisar | `requesting-code-review` / `receiving-code-review` |
| Declarar conclusão | `verification-before-completion` |
| Encerrar feature | `finishing-a-development-branch`, integrando em `develop` conforme Gitflow |

`writing-plans` apoia o tech-planner, sem deslocar a pesquisa da primeira etapa.
O texto upstream pode sugerir modelos, ferramentas, caminhos, gates e opções de
merge genéricos; prevalecem as instruções explícitas da sessão e o contrato local.
Use as ferramentas realmente disponíveis e preserve escolhas já autorizadas.
Não pedir uma segunda autorização para o mesmo escopo por causa de um default.

As referências do upstream descrevem instalações por plugin em alguns harnesses.
Esta cópia disponibiliza as skills como arquivos locais; não instala os hooks nem
promete todos os comportamentos do plugin. A ativação do processo é explícita em
`AGENTS.md`/`CLAUDE.md`. Em ferramentas sem descoberta, abrir diretamente `SKILL.md`.

## Atualização

Abrir uma mudança SDD: pesquisar a revisão desejada, diferenças de fluxo, licença e
compatibilidade com Codex/Claude. Baixar as pastas completas de `skills/` no SHA
selecionado; preservar bytes e modos executáveis do Git de origem. Atualizar também
README e LICENSE, conferir diferenças e regenerar o lock conscientemente a partir
da árvore verificada. Não regenerar hashes apenas para esconder uma alteração local.

Executar `python3 scripts/check-vendor.py`, validar os links locais e revisar o
roteamento acima. O verificador detecta mudança de arquivos contra o lock, mas não
é uma assinatura criptográfica do autor; a revisão do download/origem continua
sendo parte da manutenção.
