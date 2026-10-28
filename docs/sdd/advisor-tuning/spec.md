# Especificação: advisor-tuning

- Instalação nova não deixa o auto-tune cortar o contexto: `runtime_config.json` gerado traz `performance_mode=mid` e trava `n_ctx`, `completion_max_tokens` e `performance_mode`.
- A imagem instala o chromadb (extra `core`) com telemetria anônima desligada.
- O cliente envia `aspect_id` e `project_id` apenas quando informados, lê o orçamento de contexto (`budget`) e avisa em stderr, sem bloquear, quando o pedido passa de ~600 tokens.
- A skill `layla-local` ensina a pedir conselho a um modelo pequeno: preâmbulo de projeto, pedido curto, pergunta fechada, sem leitura de arquivos, aspect de conselho, sem reenvio após timeout.

Aceitação: testes do cliente e do gerador cobrindo cada item; `check-skills` verde; dry-run de resolução do chromadb no container real. Reconstruir a imagem compartilhada é passo do operador (`local-laya`), fora desta mudança.
