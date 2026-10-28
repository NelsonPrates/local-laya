---
name: layla-benchmark
description: Medir respostas de uma instância PapaKoftes/Layla antes e depois de um ajuste — tempo, carga da máquina, resposta certa, tamanho, forma de plano e chamadas de ferramenta — enviando cada pergunta uma única vez. Use para provar ou recusar uma otimização; para mudar a configuração use layla-tuning.
---

# Medir o Layla

1. Monte um arquivo de perguntas a partir de [references/questions.example.json](references/questions.example.json): poucas perguntas fechadas, reais para o uso da instância, cada uma com `id` estável e `expect` (a opção correta). As mesmas perguntas servem para todas as rodadas.
2. Rode a linha de base antes de mudar qualquer coisa, em segundo plano, porque cada pergunta leva minutos em CPU:

   ```bash
   python3 scripts/bench.py run perguntas.json --out resultados.jsonl --label antes --container local-layla-layla-1
   ```

   `--container` conta `tool=` e `hit runtime limit` nos logs do intervalo; sem acesso ao Docker, omita. O script anexa uma linha por pergunta e **nunca reenvia** uma pergunta que já tem registro naquela rodada.
3. Aplique uma única mudança (skill `layla-tuning` ou a forma do pedido em `layla-local`) e rode de novo com outro `--label`.
4. Compare: `python3 scripts/bench.py compare resultados.jsonl` imprime uma tabela Markdown por pergunta e rodada.
5. Decida pelo critério em [references/method.md](references/method.md) e registre o número, a carga e a decisão.

Não reenviar um POST que estourou o tempo: a instância pode estar respondendo, e um segundo pedido dobra a carga e contamina as duas medições. `/agent/cancel/{conversation_id}` interrompe. Não declarar ganho com uma amostra por pergunta sob carga diferente; diga a carga.
