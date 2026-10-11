# Contrato da API local

Base padrão: `http://127.0.0.1:8000`. A revisão de referência é `336ee4a362945b2badf8f48fcd5820cb132a7759`; o schema da instância em `/openapi.json` prevalece.

| Operação | Rota | Observações |
| --- | --- | --- |
| Saúde | `GET /health` | `model_loaded` identifica se o GGUF está em memória; HTTP 200 sozinho não basta |
| Contrato | `GET /openapi.json` | Schema OpenAPI JSON da instância |
| Conversar | `POST /agent` | Corpo abaixo; resposta JSON completa, sem streaming |
| Pendências | `GET /pending` | Objeto com lista `pending` |
| Saudação | `GET /wakeup` | Saudação/resumo, pode atualizar sessão |
| Aprovar ação | `POST /approve` | Corpo `{"id":"ID"}`; apenas conexão local direta e autorização correspondente |

Exemplo de corpo `/agent`:

```json
{
  "message": "Analise o arquivo /workspace/exemplo.py",
  "context": "Quero entender o código antes de alterá-lo.",
  "conversation_id": "",
  "workspace_root": "/workspace",
  "allow_write": false,
  "allow_run": false,
  "stream": false
}
```

`response` contém o texto final. Podem existir outros campos, erros ou solicitações de esclarecimento; preservar seu significado. Não depender da presença de `conversation_id` em toda resposta. A API também oferece `/v1`, mas o cliente usa `/agent` para os recursos do agente; não assumir que `/v1` reproduz todo o contrato OpenAI.

## Uso do cliente

```bash
python3 scripts/layla_client.py --base-url http://127.0.0.1:8001 health
python3 scripts/layla_client.py --timeout 300 ask 'Resuma o contexto fornecido.' --context 'Texto relevante'
python3 scripts/layla_client.py pending
python3 scripts/layla_client.py schema > /tmp/layla-openapi.json
```

Código de saída 0 significa requisição JSON concluída sem erro explícito. Código 1 indica falha de transporte/HTTP, JSON inválido, erro semântico explícito (`ok=false`/`error`) ou modelo não carregado no comando `ready`; código 2 indica argumentos inválidos. Não repetir um POST após timeout sem investigar se a instância já o processou.

O cliente desabilita proxies do ambiente e redirects, e aceita apenas HTTP loopback. Se a própria LLM roda em outro container, `localhost` aponta para esse container. Execute o cliente no host ou use uma integração explicitamente configurada; não trocar silenciosamente para uma URL remota.

## Workspace e aprovações no Docker

No runtime gerado, `workspace/` do host fica em `/workspace`. Os caminhos enviados ao Layla são os do container. Outros arquivos do host não ficam automaticamente disponíveis.

O upstream considera chamadas vindas da bridge Docker como não locais para escrita/execução e aprovação, mesmo com porta publicada no loopback do host. Não contornar com headers de proxy. O runtime inclui `./layla approve ID` que faz a requisição de dentro do container, somente após verificar a ação e sua autorização. O cliente HTTP desta skill não tem subcomando de aprovação automática.

## Diagnóstico

- Conexão recusada: conferir porta, `./layla status` e se a ferramenta executa no host correto.
- 400 `host_not_allowed`: usar `127.0.0.1` ou `localhost`, sem hostname arbitrário.
- 401/403: verificar configuração de acesso da instância; não desabilitar autenticação para forçar uma requisição.
- 422: conferir `/openapi.json` e os campos/caminhos enviados.
- 5xx ou resposta com erro: consultar logs, modelo e memória; manter a mensagem original no relato.
- Resposta lenta: ajustar `--timeout` de forma explícita, sem reenviar automaticamente.

## Fontes

- [AgentRequest](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/schemas/requests.py)
- [Rotas do agente](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/agent.py)
- [Saúde](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/system.py)
- [Aprovações](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/approvals.py)
