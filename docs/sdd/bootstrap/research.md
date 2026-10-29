# Research: local-layla bootstrap and SDD workflow

Date: 2026-10-11. Request: publish a public personal repository with skills for the Layla Docker setup and API. Add SDD with research, a technical planner, Superpowers, parallel agents, and Gitflow.

## Checked evidence

| Primary source | Revision or date | Finding and effect |
| --- | --- | --- |
| [PapaKoftes/Layla](https://github.com/PapaKoftes/Layla) | `336ee4a362945b2badf8f48fcd5820cb132a7759` | FastAPI API with `/agent`, `/health`, `/pending`. Explicit permission fields. GGUF models |
| [Runtime config](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/runtime_safety.py) | same SHA | `LAYLA_DATA_DIR`, `models_dir`, and `sandbox_root` must point to the persistent volumes |
| [Approvals](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/agent/routers/approvals.py) | same SHA | Approval requires a direct local connection. The Docker bridge is not the same as the app loopback |
| [Superpowers](https://github.com/obra/superpowers) | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | 15 skills, MIT license. Native or subagent execution, review, and checks |
| [Codex skills](https://developers.openai.com/codex/skills/) | read 2026-10-11 | Discovery in `.agents/skills`. Content is portable as folders |
| [Codex subagents](https://developers.openai.com/codex/subagents/) | read 2026-10-11 | Custom roles in `.codex/agents/*.toml`. Availability depends on the version and harness |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents) | read 2026-10-11 | Roles in `.claude/agents/`, Markdown instructions, and tool filters |
| [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) | read 2026-10-11 | Releases from develop, hotfixes from main, tags on main, and fixes merged back |

## Decisions

Python stdlib for the generator, the client, and the checkers. Bash and Compose for operation. CPU by default, so we do not assume an available GPU. A project research skill covers the domain. Reusing the official Superpowers library for execution avoids rewriting its method. Copying the skills with a source lock, instead of a submodule, lets users clone the repository without extra setup.

Parallel work uses worktrees and an exclusive claim for each task in the common Git directory. This is local coordination, not distributed coordination. Provider sessions open separately. The project does not depend on a specific broker.

## Limits and experiments

No GGUF model was supplied. Check generation, the client against simulated local HTTP, and a real startup without a model. Do not claim that inference was tested. A CPU build was started to confirm the dependencies and the boot. Record the final results in `review.md` after the checks.

The user confirmed PapaKoftes/Layla and a public repository. No material choice is open for the bootstrap. The future workflow keeps authorization by scope and does not turn each step into a new confirmation.
