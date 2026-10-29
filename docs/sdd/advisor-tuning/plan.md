# advisor-tuning: plano técnico

Pesquisa: [research.md](research.md). Especificação: [spec.md](spec.md). Execução: `executing-plans`, sequencial — uma tarefa pequena, sem paralelismo útil.

1. T01 — gerador, Dockerfile, cliente, skill e testes. Aceitação: spec acima. Verificação: `python3 -m unittest discover -s tests -v`, `python3 scripts/check-skills.py`, `python3 scripts/check-plan.py docs/sdd/advisor-tuning/plan.json`.

- [x] T01 concluída e verificada
