# Alavancas de configuração

Revisão de referência: `336ee4a362945b2badf8f48fcd5820cb132a7759`, CPU de 6 núcleos, Qwen2.5-7B-Instruct Q4_K_M. Os números foram medidos em 2026-10-27/28 e servem de ponto de partida, não de garantia.

| Alavanca | Como aplicar | Valor que funcionou | Por quê |
| --- | --- | --- | --- |
| Travar o contexto | `POST /settings` `{"auto_tune_locked_keys": ["n_ctx","completion_max_tokens","performance_mode","max_runtime_seconds"]}` | as quatro chaves | Sem a trava o auto-tune grava `performance_mode=low` em CPU e corta `n_ctx` para 2048 a cada carga de configuração |
| Janela | `n_ctx`, `performance_mode` | 4096, `mid` | Acima de 4096 o prompt cresce e o CPU fica mais lento sem melhorar a resposta curta |
| Saída | `completion_max_tokens` | 512 | Uma linha de conselho cabe; respostas longas consomem minutos |
| Tempo | `max_runtime_seconds` | 900 | 703–998 s foram medidos sob carga; menos que isso corta a resposta |
| Ferramentas | `max_tool_calls` | 1 | Para uma instância que só aconselha; cada passo de ferramenta custa 1–2 min |
| Conhecimento | `knowledge_min_similarity` | 0,6 (padrão 0,40) | Corta documentos sem relação na recuperação; com `n_ctx` ≤ 4096 a seção já recebe 0 tokens |
| Lote | `n_batch` | deixar com o auto-tune | Gravar sem travar aparece em `not_in_force`; não mediu ganho |
| Modelo | `model_filename` (reinicia o modelo) | 7B Q4_K_M | O 3B (`qwen2.5-coder-3b`) não foi mais rápido sob carga: 945 e 998 s, ambos no limite |
| Override por pedido | `model_override` em `/agent` | não usar | Foi ignorado: o modelo recarregou duas vezes |

## Projeto, preâmbulo e aspect

`POST /projects` com `name`, `system_preamble` e `aspect_default`; `PATCH /projects/{id}` corrige. O preâmbulo entra em todo pedido com `project_id` (`[Active project: …]`), por isso leva só fatos estáveis em até ~150 palavras: regras fixas, quem decide, "não leia arquivos, não use ferramentas". Fatos que mudam vão no pedido.

Aspects: `nyx` para conselho/análise; `morrigan` para implementação. `echo` entrou em loop de `search_memories` até o limite de 703 s. Uma aspect de projeto vale para todos que usam o projeto.

## Learnings

`GET /learnings?limit=100` lista; `DELETE /learnings/{id}` apaga e responde `{"ok":true}`. O agente grava sozinho uma `Reflection (…)` e um `Tool pattern: …` por consulta, e um `read_file` falho vira learning ruim; essas entradas voltam na recuperação e puxam o modelo para o que deu errado. Revise periodicamente, apresente ids e conteúdo ao dono e apague só os autorizados. Fatos estáveis do projeto pertencem ao preâmbulo, não a `/learn`: uma learning só entra no prompt se a busca a recuperar.

## O que não se configura

- Corte por CPU de `n_ctx` (75% → 3072, 90% → 2048), mesmo travado.
- Orçamento por seção para modelo pequeno (`n_ctx` ≤ 4096): `knowledge 0`, `pinned_context 0`, `agent_state 0`, `system_instructions 600`, `memory 300`, `conversation 400`. O cabeçalho fica perto de 1146 tokens (`/health/context_budget`), e seções são truncadas sem erro.
- O otimizador de prompt e o classificador de raciocínio: o primeiro reescreve pedidos de mais de 12 palavras pela intenção; o segundo manda para `deep` qualquer goal+contexto acima de 350 caracteres. Ambos se contornam pela forma do pedido.

## Dono das mudanças

API (`/settings`, `/projects`, `/learnings`): qualquer usuário local com acesso à porta, com efeito para todos. Runtime (`runtime_config.json`, `.env`, `compose.yaml`) e imagem: o usuário do serviço que roda o container; num host compartilhado, peça a ele. Uma cópia instalada do cliente (ex.: `/opt/local-laya`) só ganha opções novas quando o dono a atualiza.
