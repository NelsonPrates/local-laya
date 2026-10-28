# layla-optimizer-agent: plano técnico

Pesquisa: [research.md](research.md). Especificação: [spec.md](spec.md). Execução: `executing-plans`, sequencial — os arquivos de registro são compartilhados entre as partes.

1. T01 — scripts, skills, roteiro, agente, registros e testes. Aceitação: spec acima. Verificação: `python3 -m unittest discover -s tests -v`, `python3 scripts/check-skills.py`, `python3 scripts/check-plan.py docs/sdd/layla-optimizer-agent/plan.json`, `snapshot.py` contra `127.0.0.1:8000`.

- [x] T01 concluída e verificada
