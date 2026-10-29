# operacao-host: plano técnico

Pesquisa: [research.md](research.md). Especificação: [spec.md](spec.md). Tabela verificável: [plan.json](plan.json).

Execução: `executing-plans`, sequencial. As tarefas formam uma cadeia (ver dependências). Não há grupo paralelo.

## Objetivo

Corrigir P1 (skill `project-qa` ausente em `main`), adicionar P4 (`./layla backup`) e diagnosticar P2 (`chroma_ok: false`). P3 espera a resposta do dono (pergunta 1 em `spec.md`).

## Pré-requisito

O coordenador integra esta pasta (`research.md`, `spec.md`, `plan.md`, `plan.json`) em `develop` antes de T01. Assim `release/0.2.0` contém os artefatos e o `qa-report.md` desta mudança.

## Arquivos e interfaces

| Arquivo | Mudança | Tarefa |
| --- | --- | --- |
| `VERSION` | `0.1.0` → `0.2.0` | T01 |
| `CHANGELOG.md` | seção `Unreleased` → `## 0.2.0` (T01); nova entrada `Unreleased` para `backup` (T03) | T01, T03 |
| `skills/layla-docker/assets/container/layla` | comando `backup DEST [--keep N]`, antes da verificação do Docker e depois da verificação de `.env` | T03 |
| `skills/layla-docker/references/operations.md` | uso de `backup`, exemplo de agendamento sem host nem caminho de usuário, limite da cópia com container em execução, cópia do script para instalação antiga | T03 |
| `tests/test_layla.py` | testes de `backup` sobre uma instalação gerada por `setup.py` em pasta temporária | T03 |
| `docs/sdd/operacao-host/qa-report.md` | evidências por critério e SHA | T01, T03 |
| `docs/sdd/operacao-host/handoffs/T02-owner.md` | SHA do merge, tag, resultado de `find -xtype l` sem caminhos de usuário | T02 |
| `docs/sdd/operacao-host/chroma-diagnosis.md` | causa de `chroma_ok: false` e evidências | T04 |

Interface de T03: `./layla backup DEST [--keep N]`. Saída padrão: o caminho do arquivo criado. Códigos: 0 sucesso; 2 uso inválido; outro código para falha do `tar`. O nome usa a hora UTC, então duas execuções no mesmo segundo colidem: o comando falha em vez de sobrescrever.

## Restrições

- Não alterar o upstream nem os arquivos vendorizados.
- Não registrar endereço IP, nome de host, caminho de usuário, dados de usuário nem segredos. O repositório é público.
- O comando `backup` não usa Docker e não para o container.
- Merge, tag, push e publicação precisam de autorização do dono (pergunta 3 em `spec.md`).

## Riscos

- Cópia com container em execução pode ficar inconsistente (SQLite/Chroma). Mitigação: documentar o horário sem uso e a cópia com container parado. Não é um bloqueio.
- `--keep` remove arquivos. Mitigação: só remove nomes `layla-data-*.tgz` dentro de `DEST`, e só depois de criar o novo arquivo com sucesso.
- T02 depende de uma ação humana. Se o dono não autoriza, T03 e T04 esperam, porque T03 escreve em `CHANGELOG.md` depois do backmerge.

## Tarefas

- [x] **T01 — Preparar `release/0.2.0`** (dono: coordenador; 20 min; depende de: —)
  - Criar `release/0.2.0` de `origin/develop`. Atualizar `VERSION` e `CHANGELOG.md`. Rodar os checks. Registrar QA em `qa-report.md`. Abrir o PR para `main` só com autorização.
  - Resultado: A1, A2.
  - Verificação: `python3 scripts/check-release.py v0.2.0` → `Tag, versão e notas coerentes`; `python3 scripts/check-skills.py` → código 0; `python3 -m unittest discover -s tests -v` → `OK`; `bash -n skills/layla-docker/assets/container/layla` → código 0.
- [ ] **T02 — Integrar a release e atualizar a cópia instalada** (dono: dono do repositório e operador do host; 20 min; depende de: T01)
  - Merge `release/0.2.0` → `main` (`--no-ff`), tag anotada `v0.2.0` no commit de `main`, backmerge para `develop`. O operador do host atualiza a cópia instalada a partir de `main`.
  - Resultado: A3.
  - Verificação: `git merge-base --is-ancestor v0.2.0 origin/main` → código 0; `git ls-tree origin/main skills/project-qa/SKILL.md` → uma linha; `find <pasta de skills> -xtype l` → nenhum link deste projeto.
- [ ] **T03 — Comando `./layla backup`** (dono: unassigned; 40 min; depende de: T02)
  - TDD: primeiro os testes de A4 a A7 em `tests/test_layla.py`, depois o comando e a documentação. Entrada em `CHANGELOG.md` (`Unreleased`). QA em `qa-report.md`.
  - Resultado: A4, A5, A6, A7.
  - Verificação: `python3 -m unittest discover -s tests -v` → `OK` com os testes de `backup`; `bash -n skills/layla-docker/assets/container/layla` → código 0; `python3 scripts/check-skills.py` → código 0.
- [ ] **T04 — Diagnóstico de `chroma_ok: false`** (dono: layla-optimizer com o operador do host; 30 min; depende de: T03)
  - O operador faz `./layla backup DEST` com a instalação atual (cópia do script novo). Depois o diagnóstico lê `/health` (`./layla health`), `data/logs/layla.log` e o código de saúde do upstream em `336ee4a`. Somente leitura.
  - Resultado: A8. Se a causa exige mudança, o coordenador revisa este plano.
  - Verificação: o arquivo cita `/health`, `layla.log` e `336ee4a`; `grep -En '([0-9]{1,3}\.){3}[0-9]{1,3}' docs/sdd/operacao-host/chroma-diagnosis.md` → sem saída.
- [ ] **P3 — espera a pergunta 1.** Sem tarefa até a resposta do dono.

Ordem: T01 → T02 → T03 → T04. Razões: T03 escreve `CHANGELOG.md` na seção `Unreleased` criada pelo backmerge de T02. T04 precisa de um backup feito por T03 antes de ler a instância.

## Matriz QA

| Critério | Cenário/check | Esperado | Pré-requisito | Situação |
| --- | --- | --- | --- | --- |
| A1 | `check-release.py v0.2.0` em `release/0.2.0` | mensagem de coerência, código 0 | T01 | obrigatório |
| A2 | `check-skills.py`; `git ls-tree` de `skills/project-qa/SKILL.md` | código 0; uma linha | T01 | obrigatório |
| A3 | `find <pasta de skills> -xtype l` depois da atualização | nenhum link deste projeto | T02, acesso do operador | obrigatório (evidência do operador) |
| A4 | `backup DEST` em instalação temporária; `tar -tzf` | contém `data/runtime_config.json`; sem `models/` | T03 | obrigatório |
| A5 | três arquivos antigos; `backup DEST --keep 2` | ficam os dois mais novos (um antigo e o novo) | T03 | obrigatório |
| A6 | `DEST` em `data/`; `--keep 0`; `--keep x` | código 2; nenhum `.tgz` novo | T03 | obrigatório |
| A7 | `backup` com `PATH` sem `docker` | código 0 | T03 | obrigatório |
| A8 | leitura de `chroma-diagnosis.md`; `grep` de IP | três evidências citadas; sem IP | T04 | obrigatório |
| — | backup com container real em execução | arquivo criado; container continua `running` | T04, instância real | opcional (evidência do operador) |
| — | correção de P2 e de P3 | — | causa (P2); pergunta 1 (P3) | fora do escopo |

## Revisão do plano

- Cobertura: A1–A8 têm tarefa e check.
- Tarefa removida: um script separado de agendamento. O agendamento é do operador; um exemplo na documentação basta.
- Premissa aberta: autorização de T02 (pergunta 3). Ela bloqueia T03 e T04 só por causa de `CHANGELOG.md` e da ordem pedida. Se o dono quer T03 antes da release, T03 pode partir de `develop` sem depender de T02; o coordenador revisa a dependência.
