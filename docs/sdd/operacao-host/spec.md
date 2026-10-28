# operacao-host: especificação

Pesquisa: [research.md](research.md). Plano: [plan.md](plan.md).

## Problema

O operador do host registrou quatro problemas desta instalação (P1 a P4 em `research.md`). Esta especificação cobre P1, P4 e P2. P3 espera a resposta do dono à pergunta 1.

## Pedido do usuário

- Ordem: P1, depois P4, depois P2.
- P3 espera a resposta do dono à pergunta 1 de `research.md`.
- Execução: `executing-plans`.

## Comportamento esperado

### P1: release `develop` → `main`

- A branch `main` contém a skill `project-qa`.
- Depois da atualização da cópia instalada, a instalação não tem links quebrados para skills deste projeto.
- A release segue `docs/workflow/RELEASE.md`: `release/0.2.0` parte de `origin/develop`, com `VERSION` e `CHANGELOG.md` na mesma versão.

Decisão técnica: a versão é `0.2.0` (minor). `develop` adiciona capacidades compatíveis (skills `project-qa`, `layla-tuning`, `layla-benchmark` e o papel `layla-optimizer`). Não há mudança incompatível de comando.

### P4: comando `./layla backup DEST [--keep N]`

- O comando grava um arquivo `layla-data-<UTC AAAAMMDDTHHMMSSZ>.tgz` em `DEST`. O arquivo contém a pasta `data/` da instalação.
- O comando não inclui `models/` nem `workspace/`. Um GGUF é grande e pode ser obtido de novo.
- `DEST` é obrigatório. O comando cria `DEST` se não existir.
- O comando recusa `DEST` dentro de `data/` (código de saída 2). Um backup não pode conter a si mesmo.
- Com `--keep N` (N inteiro ≥ 1), o comando remove os arquivos `layla-data-*.tgz` mais antigos em `DEST` e guarda os N mais novos. Sem `--keep`, o comando não remove arquivos.
- O comando grava primeiro um arquivo temporário em `DEST` e depois o renomeia. Uma falha não deixa um arquivo `layla-data-*.tgz` incompleto.
- O comando não usa Docker. Ele não para nem reinicia o container. Ele funciona sem Docker instalado, mas precisa de `.env` (instalação gerada por `setup.py`).
- `./layla help` mostra o comando.
- O agendamento (cron ou timer) é do operador do host. A skill `layla-docker` mostra um exemplo de linha de agendamento sem nome de host nem caminho de usuário.

Decisão técnica: `DEST` e `N` são argumentos. Assim o comando não fixa a resposta à pergunta 2 de `research.md`. O dono escolhe os valores na linha de agendamento.

Limite: o comando copia `data/` com o container em execução. Um arquivo SQLite ou Chroma em escrita pode ficar inconsistente na cópia. A skill recomenda agendar o backup num horário sem uso. Uma cópia consistente com o container parado é uma ação do operador (`./layla down`, backup, `./layla up`).

### P2: diagnóstico de `chroma_ok: false`

- Um documento `docs/sdd/operacao-host/chroma-diagnosis.md` registra a causa de `chroma_ok: false`, ou registra que a causa não foi encontrada e quais evidências faltam.
- O documento cita: a resposta de `/health`, as linhas pertinentes de `data/logs/layla.log` e o código de saúde do upstream na revisão `336ee4a`.
- O diagnóstico é somente leitura. Ele não muda a instância nem o produto. Antes do diagnóstico, o operador faz um backup com `./layla backup`.
- A correção é uma revisão deste plano depois da causa.
- O documento não registra endereço IP, nome de host, caminho de usuário nem segredos.

## Critérios de aceitação

| ID | Critério |
| --- | --- |
| A1 | Na branch `release/0.2.0`, `VERSION` é `0.2.0` e `CHANGELOG.md` tem a seção `## 0.2.0`. `python3 scripts/check-release.py v0.2.0` passa |
| A2 | `skills/project-qa/SKILL.md` existe em `release/0.2.0`. `python3 scripts/check-skills.py` passa |
| A3 | Depois do merge e da atualização da cópia instalada, `find <pasta de skills> -xtype l` não mostra skills deste projeto |
| A4 | `./layla backup DEST` cria um `.tgz` em `DEST` com `data/runtime_config.json`, sem `models/` |
| A5 | `./layla backup DEST --keep 2` com três arquivos anteriores deixa os dois mais novos |
| A6 | `DEST` dentro de `data/`, `--keep 0` ou `--keep x` falham com código 2 e não criam arquivo |
| A7 | `./layla backup` funciona sem `docker` no `PATH` |
| A8 | `chroma-diagnosis.md` existe, cita as três evidências e não contém endereço IP nem nome de host |

## Compatibilidade

- Os comandos atuais de `./layla` não mudam.
- Uma instalação antiga recebe `backup` só quando o operador gera o script de novo. `setup.py` recusa uma segunda geração sobre configuração existente. A skill explica como copiar só o script `layla`.

## Perguntas abertas

Copiadas de `research.md`.

1. P3: é aceitável alterar o comportamento do upstream, ou só a configuração gerada por `setup.py`? Bloqueia P3.
2. P4: quantas cópias guardar e em qual pasta? Não bloqueia a tarefa de P4: o dono dá os valores na linha de agendamento (`DEST`, `--keep N`).
3. P1: o dono autoriza o merge de `release/0.2.0` em `main`, a tag `v0.2.0` e a publicação? Bloqueia a tarefa T02. Esta sessão não faz merge, tag nem push.
4. T01 (J4, 2026-10-28): o pré-requisito de `plan.md` não está cumprido. `origin/develop` (`ee063f7`) não contém `docs/sdd/operacao-host/`. Um job agendado não pode fazer merge, e só pode escrever em branches `feature/*`. O dono deve decidir:
   a. integrar `feature/operacao-host` em `develop` antes de T01 (o plano supõe isto); e
   b. autorizar a criação de `release/0.2.0` por um job agendado, ou executar T01 pessoalmente.
   Bloqueia T01, e por isso T02, T03 e T04.
