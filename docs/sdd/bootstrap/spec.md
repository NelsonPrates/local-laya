# Especificação do bootstrap

Entregar `NelsonPrates/local-layla` público e o projeto em `~/Documentos/local-layla`.

- Skills autocontidas para gerar uma instalação Docker CPU do PapaKoftes/Layla e consultar a API local. Persistir dados/modelos/workspace e publicar porta somente no loopback.
- Gerador não sobrescreve instalação existente; cliente usa somente localhost, desativa permissões de escrita/execução e distingue API disponível de modelo pronto.
- Workflow de desenvolvimento/manutenção inicia por pesquisa, segue ao tech-planner e à execução escolhida de Superpowers; planos usam a menor ordem suficiente de tarefas claras, com dependências e verificação.
- Codex e Claude leem o mesmo contrato e podem executar tarefas independentes em worktrees diferentes; reservar tarefas, evitar arquivos compartilhados e integrar serialmente.
- Baixar as skills oficiais Superpowers com revisão fixa, licença e integridade verificável.
- Gitflow com main/develop/feature/release/hotfix, CI e automação de publicação validada por tag. Nenhuma tag de release será publicada no bootstrap.

Aceitação: skills válidas, testes de comportamento passando, Compose válido, teste real de inicialização com limite explícito de ausência de GGUF, planos validados, vendor íntegro, worktrees/reservas isoladas em teste e repositório remoto sincronizado.
