# Plano: agente QA/testes

Objetivo: um agente comum, uma skill autocontida e integração ao fluxo existente. Execução: `executing-plans`; adaptar seus helpers ao formato de plano já usado pelo repo, mantendo evidência e revisão independente. Um coordenador escritor basta: as duas tarefas são dependentes, sem grupo paralelo de implementação.

- [ ] T01 — Contrato QA, skill, adaptadores e workflow. Dono: coordinator. Arquivos: `skills/project-qa/`, `docs/workflow/`, `AGENTS.md`, `CLAUDE.md`, `.codex/agents/qa-test.toml`, `.claude/agents/qa-test.md`, `README.md`, `CHANGELOG.md`. Resultado: A1/A2/A3/A5 definidos sem duplicar etapas Superpowers. Verificar com quick_validate da skill, leitura dos adaptadores e avaliação independente do comportamento.
- [ ] T02 — Instalação, descoberta e evidência. Depende de T01. Dono: coordinator. Arquivos: instalador/check-skills, links `.agents/skills/project-qa` e `.claude/skills/project-qa`, testes de instalação/descoberta e artefatos desta mudança. Resultado: A4 demonstrado e A1–A5 revisados. Primeiro estender teste de instalação e observar falha pela ausência da quarta skill; depois incluir a skill no instalador. Rodar unittest/check-skills/check-vendor/check-plan e sintaxe Bash; registrar QA/revisão e abrir PR para develop.

## Matriz QA

| Critério | Verificação mínima | Esperado |
| --- | --- | --- |
| A1/A2/A3 | Revisão de contratos, fontes e adaptadores | Ordem e responsabilidades coerentes; mesmas instruções nos provedores |
| A4 | Instalação temporária, preservação, links; suíte unittest | Quarta skill utilizável fora do repo, referências locais presentes, sem sobrescrita |
| A5 | Forward-test independente com artefatos isolados | Relatório fundamentado sem falso positivo ou correção não atribuída |
| Regressão | Checks de skills/vendor/plan e Bash; suíte inteira | Exit 0; vendor intacto |

Container real, GGUF e browser: fora do escopo, sem mudança de runtime/UI. Compose continua validado pelo CI existente. QA final escreve `qa-report.md`; o coordenador mantém este plano. Evidências referem-se ao commit testado e são reavaliadas se código/testes/configuração mudarem.

Pre-flight: T02 consome o diretório autocontido project-qa de T01; instalação e links usam o mesmo nome. Não há conflito de interface. Ordem mínima revisada: nenhuma migração de framework, automação de gate ou teste de redação é necessária.

Review Focus: relato de teste obrigatório indisponível; evidência em commit anterior; escrita concorrente dos artefatos QA; portabilidade sem checkout/vendored presente.
