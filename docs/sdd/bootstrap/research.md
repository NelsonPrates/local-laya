# Pesquisa: bootstrap local-layla e workflow SDD

Data: 2026-10-11. Pedido: publicar um repositório pessoal público com skills para Docker/API Layla e acrescentar SDD com pesquisa, planejador técnico, Superpowers, agentes paralelos e Gitflow.

## Evidências verificadas

| Fonte primária | Revisão/data | Achado e efeito |
| --- | --- | --- |
| [PapaKoftes/Layla](https://github.com/PapaKoftes/Layla) | `336ee4a362945b2badf8f48fcd5820cb132a7759` | API FastAPI, `/agent`, `/health`, `/pending`; campos de permissões explícitos; modelos GGUF |
| [Config runtime](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/runtime_safety.py) | mesmo SHA | `LAYLA_DATA_DIR`, `models_dir` e `sandbox_root` precisam apontar aos volumes persistentes |
| [Aprovações](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/approvals.py) | mesmo SHA | Aprovação exige conexão local direta; bridge Docker não equivale a loopback do app |
| [Superpowers](https://github.com/obra/superpowers) | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | 15 skills, licença MIT; execução nativa ou por subagentes, revisão e verificação |
| [Codex skills](https://developers.openai.com/codex/skills/) | consulta 2026-10-11 | Descoberta em `.agents/skills`; conteúdo portável por pastas |
| [Codex subagents](https://developers.openai.com/codex/subagents/) | consulta 2026-10-11 | Papéis customizados em `.codex/agents/*.toml`; disponibilidade depende da versão/harness |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents) | consulta 2026-10-11 | Papéis em `.claude/agents/`, instruções Markdown e filtros de tools |
| [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) | consulta 2026-10-11 | Releases de develop, hotfix de main, tags em main e retorno das correções |

## Decisões

Python stdlib para gerador, cliente e verificadores; Bash/Compose para operação. CPU por padrão evita presumir GPU disponível. Skill própria de pesquisa cobre o domínio; reutilizar a biblioteca oficial Superpowers para execução evita reescrever sua metodologia. Copiar skills com origem/lock em vez de submodule permite clonar o repo sem preparação extra.

Paralelismo usa worktrees e reserva exclusiva por tarefa no diretório Git comum; esta é uma coordenação local, não distribuída. As sessões dos provedores são abertas separadamente, sem dependência de um broker específico no projeto.

## Limites e experimentos

Modelo GGUF não foi fornecido. Validar geração, cliente com HTTP local simulado e inicialização real sem modelo; não declarar inferência testada. Build CPU foi iniciado para confirmar dependências e boot. Registrar resultados finais em `review.md` após os checks.

O usuário confirmou PapaKoftes/Layla e repositório público. Não há escolha material pendente para criar o bootstrap. O fluxo futuro preserva autorização por escopo, sem transformar cada etapa em nova confirmação.
