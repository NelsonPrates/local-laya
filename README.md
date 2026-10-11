# local-layla

Skills para instalar e usar [PapaKoftes/Layla](https://github.com/PapaKoftes/Layla) em Docker pelo localhost, com um workflow compartilhado de desenvolvimento para Codex e Claude. Projeto independente de integração.

| Skill | O que faz |
| --- | --- |
| [layla-docker](skills/layla-docker/SKILL.md) | Gera scripts, Compose e configuração; ensina instalação e operação |
| [layla-local](skills/layla-local/SKILL.md) | Ensina a LLM a consultar a instância e conversar pela API local |
| [project-research](skills/project-research/SKILL.md) | Pesquisa evidências para desenvolver e manter o projeto |

## Desenvolvimento com Codex e Claude

O [workflow SDD](docs/workflow/SDD.md) segue **pesquisa → plano técnico → execução Superpowers → integração/release**. O [tech-planner](docs/workflow/tech-planner.md) produz a menor ordem suficiente de tarefas com dependências, donos e aceitação. O validador rejeita ciclos e arquivos sobrepostos em tarefas independentes.

As [15 skills oficiais Superpowers](vendor/superpowers/skills/) estão baixadas em revisão fixa, com licença e hashes de integridade. Os próximos passos de implementação/revisão são conduzidos pela skill de execução escolhida no plano. Os contratos [AGENTS.md](AGENTS.md) e [CLAUDE.md](CLAUDE.md), skills locais e adaptadores do planejador permitem trabalhar com qualquer sessão Codex/Claude que ofereça essas capacidades.

Para agentes simultâneos, cada tarefa usa uma worktree própria e uma reserva exclusiva:

```bash
python3 scripts/check-plan.py docs/sdd/<mudanca>/plan.json
python3 scripts/worktree.py start --change <mudanca> --task T01 --agent codex-1
python3 scripts/worktree.py start --change <mudanca> --task T02 --agent claude-1
python3 scripts/worktree.py list
```

O plano deve estar integrado na base `develop`, com dono `unassigned` ou o rótulo da sessão. Abra os agentes nos caminhos retornados. Execute em paralelo somente tarefas sem dependência e com arquivos distintos. O coordenador integra resultados serialmente e libera tarefas dependentes; as reservas são locais ao clone.

O [Gitflow de releases](docs/workflow/RELEASE.md) define `main`, `develop`, features, releases, hotfixes e publicação por tag validada. O bootstrap não publica uma release automaticamente. Veja também a [pesquisa inicial](docs/sdd/bootstrap/research.md) e a [revisão](docs/sdd/bootstrap/review.md).

## Começar

Pré-requisitos no host: Python 3.10+, Bash e Docker com Compose v2. Linux é o alvo principal; Windows via WSL2 e Docker Desktop; macOS via Docker Desktop. A imagem usa Python 3.12 e inferência CPU. A compilação inicial requer internet, vários GB de disco e pode levar vários minutos.

```bash
git clone https://github.com/NelsonPrates/local-layla.git
cd local-layla

# Gere a instalação e copie um modelo GGUF que você já possui:
python3 skills/layla-docker/scripts/setup.py --output runtime --model /caminho/modelo.gguf

cd runtime
./layla up
./layla ready
```

Abra **http://127.0.0.1:8000/ui**. Para gerar a instalação antes de escolher o modelo, omita `--model`; selecione/baixe um GGUF pela interface ou copie-o para `runtime/models/`, ajuste `model_filename` em `runtime/data/runtime_config.json` e rode `./layla restart`. A API pode iniciar sem GGUF, mas conversar exige um modelo compatível carregado. `./layla ready` diferencia esses estados.

Se `runtime/` já estiver configurado, edite seus arquivos ou gere em outro diretório; o gerador recusa sobrescrita. Use `--port 8001` na geração se a porta 8000 estiver ocupada.

## Conversar pelo terminal

Na raiz do repositório:

```bash
python3 skills/layla-local/scripts/layla_client.py health
python3 skills/layla-local/scripts/layla_client.py ready
python3 skills/layla-local/scripts/layla_client.py ask 'Olá! Responda em português.'
python3 skills/layla-local/scripts/layla_client.py pending
```

Para outra porta: `python3 skills/layla-local/scripts/layla_client.py --base-url http://127.0.0.1:8001 health`. O cliente imprime o JSON completo e envia `allow_write=false`/`allow_run=false`; instruções e referências da skill explicam contexto, continuidade da conversa e pendências.

## Instalar as skills no agente

É possível usar diretamente os arquivos `SKILL.md` deste repositório ou copiar as skills para a pasta descoberta pelo seu agente:

```bash
python3 scripts/install-skills.py
# Ou escolha explicitamente o diretório de skills do seu agente:
python3 scripts/install-skills.py --target ~/.codex/skills
```

O destino padrão do instalador é `~/.agents/skills`. O script copia as três skills próprias; não sobrescreve versões já instaladas. Neste repositório, `.agents/skills/` e `.claude/skills/` já apontam para as skills próprias e Superpowers. Após a instalação externa, recarregue a sessão se necessário e invoque:

```text
Use $layla-docker para instalar o Layla em ~/local-layla-runtime usando meu GGUF.
Use $layla-local para conversar com o Layla disponível em localhost:8000.
```

Cada skill inclui seus próprios scripts, referências e metadados de interface. Não é preciso manter o repositório presente depois de copiar as skills.

## Operação diária

Execute no diretório gerado:

| Comando | Resultado |
| --- | --- |
| `./layla up` | Compila quando necessário e inicia aguardando a API |
| `./layla status` | Consulta estado do container |
| `./layla health` / `./layla ready` | Consulta saúde / verifica modelo carregado |
| `./layla logs` | Acompanha logs |
| `./layla doctor` | Diagnostica Docker, container e modelo |
| `./layla restart` | Aplica mudanças na configuração do app |
| `./layla down` | Para e remove o container, mantendo os arquivos |
| `./layla approve ID` | Aprova uma ação específica autorizada, de dentro do container |

`data/`, `models/` e `workspace/` persistem no host. O Layla vê os arquivos de trabalho em `/workspace`. A porta é publicada apenas em `127.0.0.1`. A configuração inicial limita o container a 4 CPUs e 8 GB; ajuste `.env` conforme modelo/hardware e rode `./layla up`.

O upstream restringe aprovação e execução de ferramentas a conexões locais diretas; uma chamada pelo bridge Docker não recebe automaticamente essas permissões. Consulte [operação e diagnóstico](skills/layla-docker/references/operations.md) e [contrato da API](skills/layla-local/references/api.md).

## Desenvolvimento e validação

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-skills.py
python3 scripts/check-vendor.py
python3 scripts/check-plan.py docs/sdd/bootstrap/plan.json
bash -n skills/layla-docker/assets/container/layla
```

Os testes cobrem geração, preservação de dados, instalação independente das skills e cliente HTTP com servidor local simulado. Não precisam de Docker nem de um modelo. Para validar o container real:

```bash
python3 skills/layla-docker/scripts/setup.py --output runtime --port 18765
cd runtime
./layla up
./layla health
# Sem um GGUF configurado, ready deve retornar 1.
./layla ready
./layla down
```

Uma resposta de inferência real exige disponibilizar um GGUF. Este repositório não distribui nem baixa modelos automaticamente pelo gerador.

## Versão e licença

O build fixa o código upstream no SHA `336ee4a362945b2badf8f48fcd5820cb132a7759`. O código é obtido durante o build e o SHA é conferido. A imagem base e dependências Python ainda são resolvidas no build, portanto não há promessa de reprodução byte a byte.

Os scripts e skills próprios deste repositório usam [MIT](LICENSE). O Layla mantém sua [licença própria para uso não comercial](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/LICENSE). Superpowers mantém sua [MIT e atribuição](vendor/superpowers/LICENSE); modelos/dependências têm termos próprios. Veja [THIRD_PARTY.md](THIRD_PARTY.md).
