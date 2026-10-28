# Handoff J2: tech-planner para operacao-host

- Job: J2
- Result: done
- Commits: feature/operacao-host (SHA do commit que contém este arquivo; ver `git log -1 -- docs/sdd/operacao-host/handoffs/J2-planner.md`)
- Checks run:
  - `python3 scripts/check-plan.py docs/sdd/operacao-host/plan.json` → `Plano válido. Ordem sugerida: T01 -> T02 -> T03 -> T04`
  - `python3 -m unittest discover -s tests -v` → `Ran 32 tests`, `OK`
- Open questions:
  1. P3: é aceitável alterar o comportamento do upstream, ou só a configuração gerada por `setup.py`? (bloqueia P3)
  2. P4: quantas cópias guardar e em qual pasta? (não bloqueia T03: o dono dá `DEST` e `--keep N` na linha de agendamento)
  3. P1: o dono autoriza o merge de `release/0.2.0` em `main`, a tag `v0.2.0` e a publicação? (bloqueia T02, e por isso T03 e T04)
- Next step: o coordenador integra estes artefatos em `develop` e executa T01 com `executing-plans`.

## Artefatos

- [spec.md](../spec.md): comportamento, critérios A1–A8, perguntas abertas.
- [plan.md](../plan.md): tarefas, riscos, matriz QA.
- [plan.json](../plan.json): `execution_skill: executing-plans`.

## Ordem

T01 (preparar `release/0.2.0`) → T02 (merge, tag, backmerge, atualizar a cópia instalada; dono) → T03 (`./layla backup DEST [--keep N]`) → T04 (diagnóstico de `chroma_ok: false`, somente leitura). Não há grupo paralelo. P3 não tem tarefa.

## Decisões técnicas do planejador

- Versão `0.2.0` (minor): capacidades compatíveis em `develop`.
- `backup` não usa Docker e não para o container. Ele copia `data/` sem `models/`. `DEST` é obrigatório; `--keep` é opcional. Sem `--keep`, nada é removido.
- T03 depende de T02 por causa de `CHANGELOG.md`. Se o dono quer T03 antes da release, o coordenador remove essa dependência.

## Limites

- Esta sessão não fez merge, tag, push nem release. Não usou Docker.
- Nenhum host, IP ou dado de usuário foi registrado.
