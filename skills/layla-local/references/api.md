# Local API contract

Default base: `http://127.0.0.1:8000`. The reference revision is `336ee4a362945b2badf8f48fcd5820cb132a7759`. The instance schema in `/openapi.json` has priority.

| Operation | Route | Notes |
| --- | --- | --- |
| Health | `GET /health` | `model_loaded` shows whether the GGUF model is in memory. HTTP 200 alone is not sufficient |
| Contract | `GET /openapi.json` | OpenAPI JSON schema of the instance |
| Chat | `POST /agent` | Body below. Full JSON response, no streaming |
| Pending actions | `GET /pending` | Object with a `pending` list |
| Greeting | `GET /wakeup` | Greeting or summary. It can update the session |
| Approve action | `POST /approve` | Body `{"id":"ID"}`. Only for a direct local connection and a matching authorization |

Example `/agent` body:

```json
{
  "message": "Analyze the file /workspace/example.py",
  "context": "I want to understand the code before I change it.",
  "conversation_id": "",
  "workspace_root": "/workspace",
  "allow_write": false,
  "allow_run": false,
  "stream": false
}
```

`response` contains the final text. Other fields, errors, or clarification requests can also occur. Keep their meaning. Do not expect `conversation_id` in every response. The API also supplies `/v1`, but the client uses `/agent` for the agent features. Do not assume that `/v1` supplies the full OpenAI contract.

## Client use

```bash
python3 scripts/layla_client.py --base-url http://127.0.0.1:8001 health
python3 scripts/layla_client.py --timeout 300 ask 'Summarize the given context.' --context 'Relevant text'
python3 scripts/layla_client.py pending
python3 scripts/layla_client.py schema > /tmp/layla-openapi.json
```

Exit code 0 means that the JSON request completed without an explicit error. Exit code 1 means one of these conditions:

- a transport or HTTP failure
- invalid JSON
- an explicit semantic error (`ok=false` or `error`)
- no loaded model for the `ready` command

Exit code 2 means invalid arguments. After a timeout, do not send the POST again until you know whether the instance processed it.

The client ignores the environment proxies and does not follow redirects. It accepts only loopback HTTP. If the LLM itself runs in a different container, `localhost` points to that container. Run the client on the host or use an explicitly configured integration. Do not silently change to a remote URL.

## Workspace and approvals in Docker

In the generated runtime, the host `workspace/` folder is at `/workspace`. Send Layla the container paths. Other host files are not automatically available.

The upstream treats calls from the Docker bridge as not local for writes, execution, and approval. This is also true when the port is published on the host loopback. Do not use proxy headers to avoid this rule. The runtime includes `./layla approve ID`, which sends the request from inside the container. Use it only after you check the action and its authorization. The HTTP client of this skill has no automatic approval subcommand.

## Diagnosis

- Connection refused: check the port and `./layla status`. Make sure that the tool runs on the correct host.
- 400 `host_not_allowed`: use `127.0.0.1` or `localhost`. Do not use an arbitrary host name.
- 401 or 403: check the access configuration of the instance. Do not disable authentication to force a request.
- 422: read `/openapi.json` and check the fields and paths that you sent.
- 5xx or a response with an error: read the logs, and check the model and the memory. Keep the original message in your report.
- Slow response: set `--timeout` explicitly. Do not send the request again automatically.

## Sources

- [AgentRequest](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/schemas/requests.py)
- [Agent routes](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/agent.py)
- [Health](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/system.py)
- [Approvals](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/approvals.py)
