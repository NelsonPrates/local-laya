# Releases baseadas em Gitflow

## Branches e integração

| Branch | Parte de | Integra em | Responsabilidade |
| --- | --- | --- | --- |
| `main` | bootstrap | — | Código estabilizado; tags públicas |
| `develop` | `main` | `release/*` | Integração da próxima versão |
| `feature/<mudanca>/<tarefa>-<agente>` | `develop` atualizado | `develop` | Uma tarefa/entrega revisável |
| `release/X.Y.Z` | `develop` | `main`, depois `develop` | Estabilização, versão, notas e correções |
| `hotfix/X.Y.Z` | `main` | `main`, depois `develop` e release ativa | Correção urgente da linha publicada |

Um coordenador integra PRs serialmente. Preferir merge commits (`--no-ff`) para preservar proveniência e permitir ao script de worktrees confirmar ancestralidade. Se usar squash, conservar o SHA do merge e revisar a equivalência antes de limpar a worktree manualmente; `finish` recusa ancestralidade ausente.

## Release normal

1. Confirmar PRs planejados integrados e CI verde em `develop`. Criar `release/X.Y.Z` a partir de `origin/develop` atualizado; congelar features nessa branch.
2. Atualizar `VERSION` e `CHANGELOG.md` com a mesma versão. Usar SemVer: patch para correções compatíveis, minor para capacidades compatíveis, major para incompatibilidades de contrato/comandos.
3. Rodar os checks de scripts/skills, validar Compose e conferir as evidências de container/inferência pertinentes. Registrar limitações e alterações de revisão upstream/Superpowers. Abrir PR `release/X.Y.Z` → `main` e revisar o resultado.
4. Após a revisão e a autorização de merge/publicação que couber à sessão, integrar em `main`; confirmar CI verde no commit final. Criar tag anotada **`vX.Y.Z` apontando para esse commit de `main`** e enviar a tag. Não marcar a feature ou um commit anterior.
5. A Action `release.yml` valida tag/versão, ancestralidade em `main`, notas e testes antes de criar a GitHub Release com o arquivo das skills. Publicar a tag é o gatilho de publicação; não é apenas um pedido de validação.
6. Fazer backmerge de `main` para `develop` e para uma release ativa que ainda precise das correções. Rodar CI no resultado; depois remover a branch de release concluída.

## Hotfix

Criar `hotfix/X.Y.Z` de `origin/main`, manter a pesquisa e o plano proporcionais ao defeito, corrigir e verificar. Atualizar versão/notas, revisar PR para `main`, integrar e publicar tag como acima. Propagar a correção para `develop` e para qualquer release ativa antes de encerrar. Não misturar features pendentes de `develop` com a correção de produção.

## Automação e proteção

`ci.yml` valida pushes e PRs. `release.yml` executa somente em tags `v*`, com `contents: write` restrito ao job de publicação; seu check exige versão SemVer, notas correspondentes e commit ancestral de `main`.

Recomendado no GitHub: proteger `main` e `develop`, exigir PR, review e o check `skills-and-scripts`, proibir force-push/exclusão e restringir tags `v*` ao mantenedor/coordenador. Isso depende de regras da conta/repositório: documentação não significa proteção já aplicada. O workflow não consegue impedir o push inicial de uma tag inválida; ele impede sua publicação como Release.

O bootstrap entrega `main` e `develop`, mas não cria uma tag/release sem pedido. Publicação inicial do repositório e publicação de uma versão são ações distintas.

## Fontes

- [Gitflow, releases e hotfixes](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Git worktree](https://git-scm.com/docs/git-worktree)
- [GitHub Actions: eventos de push/tags](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push)
