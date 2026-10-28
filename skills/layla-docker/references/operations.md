# Operação da instalação gerada

## Dependências e primeiro uso

- Python 3.10+ e Bash no host. Linux é o alvo principal; no Windows use WSL2 com integração Docker Desktop. No macOS use Docker Desktop e Python 3.
- [Docker Engine](https://docs.docker.com/engine/install/) ou [Docker Desktop](https://docs.docker.com/desktop/) com [Compose v2](https://docs.docker.com/compose/install/).
- Git e compiladores ficam na imagem, não são necessários no host para o runtime gerado.
- A imagem CPU inclui dependências de memória/inferência. Reserve vários GB de disco e tempo para a compilação. A memória necessária depende do GGUF; `8g` é um limite inicial, não garantia de que qualquer modelo cabe.

Gere sem `--model` para usar o fluxo de configuração em `/ui`. O app poderá baixar um modelo e modelos de embeddings durante o setup/primeiro uso. Ter a inferência local não significa que a instalação inicial dispense internet.

Para um GGUF existente, `--model` copia o arquivo para `models/` e configura seu nome. O cabeçalho GGUF é validado, mas só carregar o modelo confirma compatibilidade. Também é possível copiar um GGUF manualmente para `models/`, definir `model_filename` em `data/runtime_config.json` e reiniciar.

## Caminhos e configuração

| Host (diretório gerado) | Container | Uso |
| --- | --- | --- |
| `data/` | `/data` | Banco, configuração, cache e estado persistente |
| `models/` | `/data/models` | Modelos GGUF, inclusive downloads da interface |
| `workspace/` | `/workspace` | Arquivos que você deseja disponibilizar ao Layla |

Edite `.env` para `LAYLA_PORT`, `LAYLA_CPUS` e `LAYLA_MEMORY`. Rode `./layla up` para recriar o container com esses valores. Edite `data/runtime_config.json` para `model_filename`, `n_ctx`, `n_threads` e idioma; rode `./layla restart`. A configuração existente é mantida pelo app, que completa defaults ausentes.

O gerador grava `performance_mode=mid` e trava `n_ctx`, `completion_max_tokens`, `performance_mode` e `max_runtime_seconds` (900) em `auto_tune_locked_keys`. Sem isso o auto-tune do upstream grava `low` em CPU, o que corta `n_ctx` para 2048 a cada carga de configuração. `GET /settings/not_in_force` lista o que o auto-tune ainda sobrescreve. Uma instalação anterior a esta versão recebe o mesmo efeito com `POST /settings` `{"auto_tune_locked_keys": [...], "performance_mode": "mid"}`, sem reiniciar. Independente disso, o otimizador reduz `n_ctx` enquanto a CPU passa de 75%; não há chave para desligar esse corte.

A imagem instala o extra `core` (chromadb). Uma imagem construída antes disso usa o fallback sem busca vetorial até `./layla up` reconstruí-la. Verifique com `curl -s 'http://127.0.0.1:8000/health?deep=true'`: só a sondagem profunda testa o Chroma (`chroma_ok`, `dependencies.chroma`); o `/health` simples informa `chroma_ok=false` sempre.

Os UID/GID gerados correspondem ao usuário do host. Não execute `setup.py` com sudo. Em Linux com Docker rootless/user namespaces, confira as permissões dos bind mounts para o UID efetivo do container. No macOS/Windows, Docker Desktop gerencia os compartilhamentos.

## API e operações autorizadas

O cliente de rede entra pelo bridge do Docker; algumas rotas do upstream verificam conexão diretamente de loopback. Em especial, `POST /approve` pode retornar 403 mesmo quando chamado pelo localhost do host. `./layla approve ID` consulta `/approve` por dentro do container. Isso é uma aprovação efetiva, e só deve ser usado para a ação específica autorizada pelo usuário.

O comando Uvicorn desativa processamento de cabeçalhos de proxy. Não tente simular localhost com `X-Forwarded-For` nem habilitar `remote_enabled` para contornar restrições. Pedidos `/agent` via bridge também têm escrita/execução desabilitadas pelo upstream. O cliente da outra skill já envia ambos como `false`.

## Problemas comuns

- Docker não responde: iniciar Engine/Desktop, conferir `docker info` e acesso do usuário ao daemon. Não alterar grupos ou permissões automaticamente só para executar um diagnóstico.
- Porta ocupada: alterar `LAYLA_PORT` no `.env` e rodar `./layla up`. Atualizar `LAYLA_BASE_URL` do cliente no host.
- Container encerra ou demora: `./layla status`, `docker compose logs --tail 100 layla`. O build inicial pode demorar; o limite de 600 segundos de `up` é para a inicialização, após o build.
- `model_loaded=false`: conferir nome do arquivo, montagem, formato suportado, logs e memória. `./layla ready` retorna código 1 nesse caso.
- OOM: usar GGUF menor, diminuir `n_ctx`/`n_batch` ou ajustar memória disponível e `LAYLA_MEMORY`.
- Caminho do host inexistente dentro do app: copiar o arquivo para `workspace/` e referir `/workspace/arquivo` na conversa.
- Build falha em uma dependência: preservar o erro, conferir suporte de arquitetura e versões upstream; não declarar a instalação concluída.
- `exec ... operation not permitted` antes do app iniciar: em alguns hosts o Docker não consegue executar imagens com `no-new-privileges`. O template não ativa essa opção; verificar overrides locais antes de mudar o daemon/host.

## Parar, backup e atualizar

`./layla down` remove o container e a rede e mantém os diretórios. Para backup consistente, pare o container e arquive `data/`, `models/`, `workspace/`, `.env`, `compose.yaml` e `Dockerfile`. Cópias do banco com o app gravando não garantem consistência. Confirme que o backup pode ser lido antes de remover uma instalação.

Para atualizar: faça backup, confira a revisão desejada no upstream, substitua `LAYLA_REV` em `.env` por seu SHA completo de 40 caracteres e execute `./layla up`. Valide `/openapi.json`, `/health` e uma conversa. Em caso de regressão, restaure a revisão e os dados do backup compatível; voltar a imagem não desfaz migrações de banco.

## Fontes verificadas

Revisão base: `336ee4a362945b2badf8f48fcd5820cb132a7759`.

- [Dockerfile upstream](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/Dockerfile)
- [Extras CPU/LLM](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/pyproject.toml)
- [Configuração e caminhos persistentes](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/runtime_safety.py)
- [Licença do Layla](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/LICENSE): uso não comercial; conferir os termos antes de uso comercial.
