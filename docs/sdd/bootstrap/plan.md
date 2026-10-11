# Bootstrap: plano técnico

Objetivo: entregar as skills e o workflow compartilhado com a menor quantidade de mecanismos que permita usar, verificar e manter o projeto.

Pesquisa: [research.md](research.md). Especificação: [spec.md](spec.md). Execução: `executing-plans`, nativa nesta sessão; o usuário já autorizou implementação e publicação do repositório. Este plano consolida o bootstrap em andamento; não afirma que a parte Layla aguardou o pedido posterior de SDD.

1. T01 — finalizar geração e cliente Layla, validar preservação/HTTP e inicialização Docker. Arquivos sob `skills/layla-*` e `tests/test_layla.py`. Aceitação: geração independente, localhost correto, erros úteis e boot verificado. Não há modelo para teste de inferência.
2. T02 — entregar pesquisa/planejador, protocolo paralelo e biblioteca Superpowers. Arquivos `skills/project-research`, `vendor`, `docs/workflow`, adaptadores, verificadores e testes próprios. Independente de T01 em arquivos de código; execução nativa sequencial evita custo de coordenação desnecessário neste bootstrap.
3. T03 — integrar CI/release, documentação e revisão; executar o conjunto combinado e publicar main/develop na conta pessoal. Depende de T01/T02. Aceitação: checks verdes, estado remoto confirmado, nenhuma tag de versão publicada.

Verificação comum: `python3 -m unittest discover -s tests -v`, `python3 scripts/check-skills.py`, `python3 scripts/check-vendor.py`, `python3 scripts/check-plan.py docs/sdd/bootstrap/plan.json` e Compose válido. T01 acrescenta boot real; T02 acrescenta reservas concorrentes em clone temporário. Revisão: cobertura da spec, não sobrescrita, URLs locais, locks por clone, revisão vendorizada e tag pertencente a main.

- [x] T01 concluída e verificada
- [x] T02 concluída e verificada
- [ ] T03 integrada, revisada e publicada
