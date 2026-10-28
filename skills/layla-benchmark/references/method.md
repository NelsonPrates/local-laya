# Método de medição

## O que cada linha registra

`label`, `id`, `started_at`, `load_before`/`load_after` (load average de 1, 5 e 15 min do host), `seconds`, `aspect`, `response`, `error`, `words`, `plan_shaped`, `expect_found` (quando a pergunta tem `expect`) e `log` (contagem de `tool=…` e `hit runtime limit` no container, ou `null`).

`plan_shaped` procura as marcas do formato que o otimizador de prompt impõe a pedidos classificados como `planning` — *estimated effort*, *success criteria*, *mitigation*, passos numerados. Achar essas marcas diz que o pedido perdeu a forma; corrija o pedido antes de culpar o modelo. `expect_found` é a letra esperada isolada no texto: uma resposta que cita A, B e C ao justificar pode marcar certo por acaso, por isso leia a resposta antes de registrar.

## Critério para adotar uma mudança

Adote quando, nas mesmas perguntas:

1. nenhuma resposta passou de certa para errada;
2. nenhuma estourou o tempo que antes não estourava;
3. e houve ganho claro em pelo menos um eixo — menos tempo com carga parecida, menos palavras, sumiu `plan_shaped`, menos `tool=`.

Tempo em CPU compartilhada varia com a carga: uma diferença menor que ~20% com cargas distintas não é ganho. Quando a carga de uma rodada passou do dobro da outra, repita a rodada mais tarde em vez de concluir. Uma mudança que só piora o tempo sob carga, sem ganho de qualidade, é recusada e registrada assim — foi o caso do modelo 3B.

## Referência medida (2026-10-27/28, 7B em CPU, nyx)

| Pergunta | Rodada | Segundos | Resultado |
| --- | --- | --- | --- |
| Branch para uma mudança de convenção | aspect echo, sem projeto | 703 | limite de execução; loop de `search_memories` |
| mesma | projeto + `max_tool_calls=1` | 738 | B certa, uma ferramenta; inventou números de plano |
| mesma | modelo 3B | 945 / 998 | limite de execução nas duas |
| mesma | após reconstruir a imagem | 773 | B certa, inteira em forma de plano |
| *Proven by* sem teste | idem | 384 | B certa, prolixa |
| branch + `Answer in one line.` | idem | 587 | B certa, três frases, sem plano |

A carga média subiu de ~2 para 7–11 em todas as rodadas do dia 28 por causa de uma CI no mesmo host; os tempos absolutos dependem disso.

## Registro

Registre cada consulta numa linha estável onde o projeto que usa o Layla possa contá-la, por exemplo `- Layla (AAAA-MM-DD): <conselho> — seguida | rejeitada: <motivo> | indisponível (<motivo>)`. Uma rodada de medição registra a tabela de `compare`, a carga e a decisão no artefato da mudança.
