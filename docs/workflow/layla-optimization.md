# Otimizar uma instância Layla, passo a passo

Este roteiro junta o que foi medido numa instância real (PapaKoftes/Layla `336ee4a`, Qwen2.5-7B Q4_K_M, 6 CPUs compartilhadas com uma CI) e diz em que ordem mexer. O papel [layla-optimizer](../../.claude/agents/layla-optimizer.md) executa este roteiro; as skills fazem cada parte:

| Parte | Skill |
| --- | --- |
| Criar a imagem e o runtime, dependências (chromadb, GGUF, telemetria) | [layla-docker](../../skills/layla-docker/SKILL.md) |
| Fotografar e ajustar configuração, projeto, aspect, learnings | [layla-tuning](../../skills/layla-tuning/SKILL.md) |
| Formar o pedido e conversar | [layla-local](../../skills/layla-local/SKILL.md) |
| Medir antes e depois, sem reenvio | [layla-benchmark](../../skills/layla-benchmark/SKILL.md) |

A regra que atravessa tudo: **uma mudança por vez, medida antes e depois, registrada com a carga da máquina.**

## 0. Saber quem pode mudar o quê

- A API (`/settings`, `/projects`, `/learnings`) muda a instância para todos os usuários dela. Peça autorização para cada mudança num host compartilhado.
- A imagem, `compose.yaml`, `.env` e `data/runtime_config.json` pertencem ao usuário que roda o serviço (ex.: uma unit systemd `User=local-laya`). Outro usuário não reconstrói nem edita; descreve o comando para o dono rodar.
- Uma cópia instalada das skills ou do cliente (ex.: `/opt/local-laya`) só ganha opções novas quando o dono a atualiza.

## 1. Linha de base

1. `python3 skills/layla-local/scripts/layla_client.py ready` — modelo carregado. Se falhar, pare: não há o que otimizar.
2. `python3 skills/layla-tuning/scripts/snapshot.py > antes.json` — estado completo, com `findings`.
3. Escolha 2–4 perguntas fechadas do uso real (modelo em `skills/layla-benchmark/references/questions.example.json`) e rode `bench.py run … --label antes` em segundo plano. Anote a carga.

## 2. Dependências e imagem (layla-docker)

Confira no snapshot e nos logs de inicialização, nesta ordem:

1. **Chroma.** `chroma_ok: true` e `chroma_dependency: ok` em `/health?deep=true`. O `/health` simples diz `false` sempre — não diagnostique por ele. Se faltar, a imagem precisa do extra `core` (`pip install .[core,cpu,llm]`) e `ANONYMIZED_TELEMETRY=False`; o log de partida diz `No module named 'chromadb'`. Reconstruir é do dono do runtime (`./layla up`).
2. **Revisão fixa.** `LAYLA_REV` com o SHA de 40 caracteres; uma revisão nova exige revalidar `/openapi.json`, as chaves de `/settings` e este roteiro.
3. **Modelo.** O 7B Q4_K_M é o padrão medido. Baixe alternativas para `/data/models` e teste trocando `model_filename` (não `model_override`, que foi ignorado); volte o valor depois. O 3B não foi mais rápido sob carga.

## 3. Configuração (layla-tuning)

Aplique por `POST /settings`, uma alavanca por rodada, e confira `took_effect` e `/settings/not_in_force`:

1. Travar `n_ctx`, `completion_max_tokens`, `performance_mode`, `max_runtime_seconds` em `auto_tune_locked_keys` — sem isso o auto-tune volta `n_ctx` para 2048 em CPU.
2. `n_ctx=4096`, `performance_mode=mid`, `completion_max_tokens=512`, `max_runtime_seconds=900`.
3. Instância só de conselho: `max_tool_calls=1`.
4. `knowledge_min_similarity=0.6`.

Recusadas pela API nesta revisão: `prompt_optimizer_enabled`, `knowledge_max_bytes`, `prompt_budgets`. Não contorne editando o arquivo de configuração sem decisão do dono. O corte de contexto por CPU acima de 75% não tem chave.

## 4. Projeto, preâmbulo e aspect

1. Crie um projeto por uso (`POST /projects`) com um `system_preamble` de até ~150 palavras: regras fixas, quem decide, "não leia arquivos, não use ferramentas".
2. `aspect_default: nyx` para conselho. Não use `echo` (loop de `search_memories` até o limite).
3. Envie `project_id` em cada pedido daquele uso.

## 5. Memória

1. Liste `/learnings`. O agente grava sozinho `Reflection (…)` e `Tool pattern: …` a cada consulta, e cada `read_file` falho vira uma learning ruim.
2. Apresente ao dono os ids e o conteúdo; apague só os autorizados (`DELETE /learnings/{id}`). Repita depois de uma série de consultas.
3. Fatos estáveis vão no preâmbulo, não em `/learn`.

## 6. Forma do pedido (layla-local)

1. Até ~200 palavras: só identificadores e as restrições que decidem.
2. Pergunta fechada: opções A/B/C, "choose and give one line of reason".
3. "Do not read files; use only this context."
4. **Termine com `Answer in one line.`, em inglês.** O otimizador de prompt reescreve pedidos de mais de 12 palavras pela intenção ("Create a concrete plan for: … effort, dependencies, risks") e só preserva o texto diante de uma restrição de tamanho em inglês. Medido: a mesma pergunta caiu de uma resposta inteira em forma de plano para três frases.
5. Rode em segundo plano; nunca reenvie um POST que estourou o tempo.

## 7. Medir e decidir (layla-benchmark)

1. Depois de cada alavanca, `bench.py run … --label <mudança>` com as mesmas perguntas.
2. `bench.py compare resultados.jsonl` e aplique o critério de `references/method.md`: nada piorou de certo para errado, nada passou a estourar, ganho claro em um eixo, cargas comparáveis.
3. Recusou? Volte o valor anterior pela mesma rota e registre a recusa com o número.

## 8. Registrar

- No repositório que usa o Layla: uma linha por consulta (`seguida`, `rejeitada: motivo`, `indisponível (motivo)`) e a tabela de medição no artefato da mudança.
- Neste repositório: o que virou padrão de instalação entra no gerador (`setup.py`, Dockerfile) com teste, e no `CHANGELOG.md`.
- Novo snapshot (`depois.json`) junto da mudança.

## Reverter

Cada mudança de API se desfaz pela mesma rota com o valor do snapshot anterior. Uma imagem nova se desfaz voltando `LAYLA_REV`/Dockerfile e `./layla up` pelo dono; migrações de banco não voltam com a imagem — faça backup de `data/` antes (ver `skills/layla-docker/references/operations.md`). Learnings apagadas não voltam.
