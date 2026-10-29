# Desenvolvimento orientado por especificação (SDD)

Este é o fluxo compartilhado de desenvolvimento e manutenção, independente do provedor. Nesta documentação, SDD significa **spec-driven development**; a skill Superpowers `subagent-driven-development` é uma das formas de execução, não a definição do fluxo inteiro.

## Sequência mínima

1. **Pesquisa:** usar `skills/project-research/SKILL.md`. Registrar em `docs/sdd/<mudanca>/research.md` o problema, estado atual, evidências primárias, alternativas relevantes, decisão recomendada e dúvidas que mudam a implementação. Uma correção pequena pode ter uma pesquisa de poucos parágrafos. Sem código de produto nesta etapa.
2. **Plano técnico:** o papel [tech-planner](tech-planner.md) transforma a pesquisa em `spec.md`, `plan.md` e `plan.json` no mesmo diretório. A especificação descreve comportamento e critérios de aceitação; o plano escolhe a menor sequência de entregas verificáveis. Incluir arquivos, dependências, dono, verificação e condições de conclusão por tarefa. O papel [qa-test](qa-test.md) contribui com a menor matriz de testes suficiente, no plano ou em `qa-plan.md` quando extensa. Validar com `python3 scripts/check-plan.py docs/sdd/<mudanca>/plan.json`.
3. **Execução Superpowers:** ler `vendor/superpowers/skills/using-superpowers/SKILL.md` e a skill de execução registrada no plano. Para execução nativa/sequencial, `executing-plans`; para controlador com implementadores e revisão por tarefa, `subagent-driven-development`. As skills escolhidas conduzem worktrees, TDD quando pertinente, revisão, correções e verificação final. Ler somente os recursos relevantes. Não inventar ferramentas de subagentes ausentes.
4. **QA/testes:** o papel [qa-test](qa-test.md), usando `skills/project-qa/SKILL.md`, verifica os critérios no SHA estável entregue e registra `qa-report.md` com comandos, resultados e limitações. Falha retorna ao implementador; correção exige revalidação. Um check obrigatório omitido/falho impede recomendar integração. QA complementa a revisão Superpowers, sem repetir sua revisão estrutural.
5. **Integração e release:** entregar revisão, relatório QA e PR da feature para `develop`; revalidar o resultado combinado. Seguir [RELEASE.md](RELEASE.md) para estabilização, `main`, tag e publicação. O CI atual executa checks; a leitura do relatório QA é responsabilidade do coordenador, sem gate automatizado de texto.

O planejamento pode usar `writing-plans` como método, mas preserva esta ordem e estes caminhos. A análise de intenção de `brainstorming`, quando necessária, ocorre dentro da pesquisa, sem reiniciar uma descoberta já concluída. O pedido explícito do usuário e as instruções deste projeto têm precedência sobre defaults da biblioteca. Os arquivos vendorizados permanecem intactos.

## Tarefas curtas, claras e na ordem certa

- Preferir a menor solução que atende aos critérios; eliminar trabalho especulativo, etapas repetidas e abstrações sem uso.
- Cada tarefa entrega um resultado revisável; configuração e documentação pertencem à tarefa cujo resultado depende delas.
- Ordenar primeiro pelos pré-requisitos. Entre tarefas prontas, preferir as que desbloqueiam outras; depois o menor esforço. Não prometer uma otimização matemática global.
- A tabela de tarefas tem ID estável, dependências, arquivos, dono, estimativa em minutos, aceitação e comando com resultado esperado.
- Paralelizar somente tarefas sem dependência entre si **e com arquivos de escrita distintos**. Se dois trabalhos precisam do mesmo arquivo, sequenciar ou redefinir a fronteira; não confiar em ausência provável de conflito.
- Rever o plano uma vez antes da execução: cobertura da spec, interfaces, tarefas dispensáveis, dependências, conflitos de arquivos, verificações e caminho mais curto. Correções posteriores devem registrar a mudança de premissa.

O validador verifica DAG, campos, IDs e colisões de caminhos normalizados entre tarefas independentes. Use caminhos exatos ou diretórios; globs são recusadas. Efeitos indiretos, symlinks e alterações de arquivos não declaradas exigem revisão semântica do coordenador.

## Codex e Claude simultâneos

O contrato é **um agente escritor por worktree e por tarefa**. Todos compartilham Git e os artefatos versionados, mas não o diretório de trabalho. Qualquer quantidade de sessões de qualquer provedor pode participar se houver tarefas independentes e recursos suficientes.

1. Um coordenador grava e integra a pesquisa/spec/plano em `develop` antes de despachar implementadores. Somente ele atualiza o plano e integra PRs; os trabalhadores não alteram esses arquivos compartilhados.
2. Cada agente recebe mudança, tarefa, branch base e critérios. Reserve a tarefa/crie a worktree:

   ```bash
   python3 scripts/worktree.py start --change exemplo --task T01 --agent codex-1
   python3 scripts/worktree.py start --change exemplo --task T02 --agent claude-1
   ```

3. Abra Codex ou Claude no caminho impresso, em terminais/sessões próprios. O script prepara isolamento e reserva; não lança nem controla sessões. As identidades `codex-1`/`claude-1` são rótulos livres, não provedores fixos.
4. Tarefas dependentes só iniciam depois de seus pré-requisitos integrados. Atualize/fetch a base antes de abrir a próxima worktree. Integre PRs de forma serial com recomendação QA, rode verificações no resultado combinado e só então libere dependentes. A verificação final QA usa conteúdo estável; planejamento de cenários/testes pode ocorrer em paralelo com arquivos e recursos exclusivos, conforme [qa-test](qa-test.md).
5. Cada trabalhador grava sua entrega em `docs/sdd/<mudanca>/handoffs/<tarefa>-<agente>.md`: SHA, arquivos, testes/resultados, limitações, dúvidas e mudanças de escopo. O coordenador reaproveita isso na revisão/PR.
6. `python3 scripts/worktree.py list` mostra reservas em armazenamento Git compartilhado, visível a todas as worktrees. Ao encerrar uma tarefa, pare sua sessão escritora, confirme que os commits foram integrados e use `finish` com os mesmos identificadores. Não usar `--force` para remover trabalho de outra sessão.

Reservas são publicadas completas por hard link exclusivo no diretório comum de Git, evitando dupla posse e leitura de JSON parcial. São locais à máquina/clone; para múltiplos clones ou máquinas, o coordenador usa assignees/PRs como autoridade e não trata este lock local como distribuído. Uma reserva órfã exige verificar worktree, commits e sessão antes de remover manualmente seu arquivo; nunca recuperá-la por timeout automático.

O Compose tem nome padrão `local-layla`: testes de container simultâneos precisam de instalações próprias, portas diferentes **e nomes de projeto Compose diferentes** (`COMPOSE_PROJECT_NAME=local-layla-t01 ./layla up`). Dados/modelos/workspace de runtime não podem ser compartilhados entre testes escritores.

## Skills e papéis portáveis

- `AGENTS.md`: contrato para Codex e outros agentes que leem esse arquivo.
- `CLAUDE.md`: importa o mesmo contrato.
- `.agents/skills/`: skills locais descobertas pelo Codex.
- `.claude/skills/`: as mesmas skills descobertas pelo Claude Code.
- `.codex/agents/tech-planner.toml` e `.claude/agents/tech-planner.md`: adaptadores do planejador compartilhado.
- `.codex/agents/qa-test.toml` e `.claude/agents/qa-test.md`: adaptadores do QA compartilhado.
- `.codex/agents/layla-optimizer.toml` e `.claude/agents/layla-optimizer.md`: operador que cria, configura e mede uma instância Layla pelo [passo a passo](layla-optimization.md). Os papéis herdam o modelo da sessão.

Os diretórios de descoberta usam links relativos para `skills/` e `vendor/superpowers/skills/`, preservando os recursos vizinhos. Se uma plataforma não seguir links, copie as pastas para seu diretório de skills. O contrato continua disponível por leitura direta dos arquivos.

Consulte [SUPERPOWERS.md](SUPERPOWERS.md) para roteamento e atualização da cópia local. Esta integração usa skills locais; não instala hooks ou plugins globais.

Exemplo de kickoff:

```text
Leia AGENTS.md. Use project-research para investigar <problema>.
Depois use o papel tech-planner para propor a menor ordem de tarefas claras.
Registre a execução Superpowers no plano, reserve worktrees e execute o trabalho
autorizado. Codex e Claude podem assumir tarefas independentes. Use qa-test para
verificar aceitação e registrar qa-report.md antes de recomendar integração.
```

Não pedir de novo autorização já expressa na sessão. Quando houver uma decisão material pendente, apresentar primeiro o plano concreto e perguntar apenas o que muda a execução. Uma instrução de pesquisa/planejamento isolado não autoriza executar produto, merges ou releases.
