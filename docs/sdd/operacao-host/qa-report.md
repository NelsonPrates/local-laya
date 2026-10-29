# QA: operacao-host

## T01 — preparar `release/0.2.0` (2026-10-28)

Executor: o coordenador (operador do host), com autorização do dono nesta sessão.
Base: `origin/develop` `ee063f7` + merge de `feature/operacao-host` (`c08b0b4`, `--no-ff`).
Nada foi enviado ao GitHub. Não houve merge em `main`, tag nem publicação.

| Critério | Comando | Resultado |
| --- | --- | --- |
| A1 | `python3 scripts/check-release.py v0.2.0` | código 0, `Tag, versão e notas coerentes` |
| A1 | `cat VERSION` | `0.2.0`. `CHANGELOG.md`: `## Unreleased` → `## 0.2.0` |
| A2 | `git ls-tree HEAD skills/project-qa/SKILL.md` | uma linha |
| A2 | `python3 scripts/check-skills.py` | código 0 (`project-qa: OK`) |
| — | `python3 -m unittest discover -s tests` | 32 testes, `OK` |
| — | `bash -n skills/layla-docker/assets/container/layla` | código 0 |
| — | `python3 scripts/check-plan.py docs/sdd/operacao-host/plan.json` | plano válido, T01 → T02 → T03 → T04 |

Compose: esta release não altera templates de Compose. Não houve validação de container.

## Observação para T04 (P2)

`origin/develop` recebeu `fea49fb` depois da pesquisa: "chroma is probed only by `/health?deep=true`".
Assim, `chroma_ok: false` em `GET /health` pode ser só a ausência da sonda, e não uma falha.
T04 deve primeiro comparar `/health` e `/health?deep=true`.
