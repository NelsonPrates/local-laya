---
name: layla-tuning
description: Diagnosticar e ajustar a configuração de uma instância PapaKoftes/Layla já instalada — contexto travado contra o auto-tune, limites de execução, modelo GGUF, projeto com preâmbulo e aspect, learnings e limiar de conhecimento. Use para otimizar uma instância existente; para criar a imagem use layla-docker, para medir o efeito use layla-benchmark.
---

# Ajustar uma instância Layla

Trabalhe sempre na ordem fotografar → mudar uma coisa → medir → registrar. Uma mudança sem medição antes e depois é palpite.

1. Fotografe o estado com `python3 scripts/snapshot.py` (somente leitura: `/health?deep=true`, `/health/context_budget`, `/settings`, `/settings/not_in_force`, `/projects`, `/learnings`). Guarde o JSON junto da mudança. `findings` aponta o que costuma estragar respostas; não é uma ordem para agir.
2. Escolha **uma** alavanca de [references/settings.md](references/settings.md) e confira quem pode aplicá-la: rotas HTTP mudam a instância de todos que a usam; arquivos do runtime e a imagem pertencem ao usuário dono do serviço.
3. Aplique pela API quando ela aceitar (`POST /settings`, `POST`/`PATCH /projects`) e leia o retorno: cada chave diz `took_effect` ou é recusada. Uma chave recusada não é contornada editando `runtime_config.json` sem decisão do dono.
4. Confira com `GET /settings/not_in_force`: uma chave gravada que o auto-tune sobrescreve aparece ali. Fotografe de novo.
5. Meça com a skill `layla-benchmark` antes de declarar ganho, e registre a mudança, o número e se foi adotada.

## Limites

- Apagar learnings, trocar o modelo padrão, mudar o aspect de um projeto compartilhado e reconstruir a imagem exigem autorização explícita para aquela ação. Liste os ids e o motivo; não apague em lote por heurística.
- O corte de contexto por CPU (`n_ctx` 3072 acima de 75%, 2048 acima de 90%) não tem chave. Sob carga, o remédio é um pedido mais curto, não uma configuração.
- `prompt_optimizer_enabled`, `knowledge_max_bytes` e `prompt_budgets` foram recusados por `POST /settings` na revisão `336ee4a`. A correção do otimizador vive na forma do pedido (skill `layla-local`).
- O `/health` simples sempre informa `chroma_ok=false`; só `?deep=true` testa o Chroma.
- Não publicar a API fora do loopback nem desligar autenticação para facilitar um ajuste.
