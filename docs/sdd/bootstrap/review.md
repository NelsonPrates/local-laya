# Revisão do bootstrap

Data: 2026-10-11. Escopo: skills Docker/API/pesquisa, workflow SDD, worktrees paralelas, Superpowers vendorizado e Gitflow.

## Resultado

Revisão independente somente leitura concluída, seguida de correções e re-revisão. Nenhum achado remanescente no escopo revisto. A validação é de scripts, workflow e inicialização; inferência real continua sem teste por ausência de GGUF fornecido.

## Achados corrigidos

1. P2: comparação literal de caminhos permitia conflitos como `src/./client.py` e `src/client.py`, ou raiz `.` versus um arquivo. O validador agora normaliza caminhos, considera a raiz e recusa globs. Testes cobrem aliases, raiz, diretórios e tarefas sequenciais.
2. P3: uma listagem simultânea podia ler JSON de reserva ainda incompleto. A reserva agora é escrita em arquivo temporário e publicada completa por hard link exclusivo; a listagem tolera remoção depois do glob. Testes determinísticos cobrem escrita parcial, remoção concorrente e disputa por dupla posse.

A re-revisão confirmou ambas as correções e não encontrou regressões relacionadas.

## Verificação

- 24 testes passaram: geração, preservação de arquivos/configuração/symlink, cópias independentes das skills, cliente HTTP, URLs locais, erros, DAG, colisões, reservas paralelas, cleanup seguro e metadados de release.
- As três skills próprias passaram no validador `quick_validate.py` de skill-creator, além do verificador do projeto.
- Superpowers: 76 arquivos de origem com hashes e 9 arquivos executáveis conferidos contra o lock; 15 skills disponíveis por links locais para Codex/Claude.
- Bash e YAML válidos; Compose gerado validado.
- Imagem CPU compilada e container iniciado em `127.0.0.1:18765`. `/health` retornou 200, banco disponível, 207 ferramentas registradas e `model_loaded=false`; `/ui` e `/openapi.json` responderam 200, com 351 rotas no schema.
- `ready` retornou 1 pela ausência do GGUF, conforme esperado. Nenhuma resposta de inferência real é reivindicada.
- Neste host, `no-new-privileges` impediu a execução de processos no Docker. Um teste controlado isolou essa opção como causa; ela foi removida do template. O usuário não recebeu alterações de daemon/host.
- O container de teste foi parado/removido; dados locais foram preservados e a porta do runtime foi restaurada para 8000. Dados/modelos/runtime são ignorados pelo Git.

## Revisão da ordem e autorização

Pesquisa → tech-planner → skill de execução Superpowers → revisão/verificação → Gitflow. A biblioteca não altera essa ordem nem repete autorizações já expressas. Tarefas independentes só são paralelas com arquivos distintos; integração e atualização de plano ficam com um coordenador. As reservas são locais ao clone e não substituem coordenação entre máquinas.

A publicação inicial do repositório foi autorizada pelo usuário. Tags/releases futuras têm o fluxo documentado e não são publicadas como efeito do bootstrap. Branch protections estão descritas como recomendação, sem alegação de aplicação automática.
