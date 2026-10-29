# local-layla

Skills that install and use [PapaKoftes/Layla](https://github.com/PapaKoftes/Layla) in Docker on localhost, with a shared development workflow for Codex and Claude. This is an independent integration project.

| Skill | What it does |
| --- | --- |
| [layla-docker](skills/layla-docker/SKILL.md) | Generates scripts, Compose files, and configuration. Teaches installation and operation |
| [layla-local](skills/layla-local/SKILL.md) | Teaches the LLM to query the instance and chat through the local API |
| [project-research](skills/project-research/SKILL.md) | Collects evidence to develop and maintain the project |
| [project-qa](skills/project-qa/SKILL.md) | Plans tests and checks criteria with evidence before integration |

## Development with Codex and Claude

The [SDD workflow](docs/workflow/SDD.md) follows **research → technical plan → Superpowers execution → QA → integration/release**. The [tech-planner](docs/workflow/tech-planner.md) produces the smallest sufficient task order, with dependencies, owners, and acceptance criteria. The [qa-test](docs/workflow/qa-test.md) role adds to the test matrix of the plan. It then checks the delivery on a stable SHA and writes a report before it recommends integration. The plan validator rejects cycles and overlapping files in independent tasks.

The [15 official Superpowers skills](vendor/superpowers/skills/) are vendored at a fixed revision, with their license and integrity hashes. The execution skill that the plan selects drives the next implementation and review steps. The [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) contracts, the local skills, and the tech-planner and qa-test adapters work with any Codex or Claude session that supplies these capabilities.

The [QA reference selection](skills/project-qa/references/test-matrix.md) combines Anthropic's `testing-strategy` with the Superpowers skills `verification-before-completion`, `test-driven-development`, and `systematic-debugging`. `webapp-testing` applies only to interface changes. The skill is self-contained and keeps unittest. No extra framework is necessary. The report separates pass, fail, blocked, and not-run. CI runs the checks, and the coordinator evaluates the QA recommendation.

### Writing style

All files are in English. Skills, agent roles, and other LLM prompts follow [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) in Strict mode. The [asd-ste100 skill](vendor/asd-ste100/SKILL.md) is vendored at a fixed revision. Human-readable documentation uses clear, instructional language. To check the prompt files, run:

```bash
python3 scripts/check-style.py
```

### Parallel agents

Each task uses its own worktree and an exclusive claim:

```bash
python3 scripts/check-plan.py docs/sdd/<change>/plan.json
python3 scripts/worktree.py start --change <change> --task T01 --agent codex-1
python3 scripts/worktree.py start --change <change> --task T02 --agent claude-1
python3 scripts/worktree.py list
```

The plan must be merged into the `develop` base. Each task owner must be `unassigned` or the session label. Open the agents in the paths that the script prints. Run tasks in parallel only when they have no dependencies and write different files. The coordinator integrates the results one at a time and then releases the dependent tasks. Claims are local to the clone.

The [Gitflow release process](docs/workflow/RELEASE.md) defines `main`, `develop`, features, releases, hotfixes, and publication through a validated tag. The bootstrap does not publish a release automatically. See also the [initial research](docs/sdd/bootstrap/research.md) and the [review](docs/sdd/bootstrap/review.md).

## Get started

Host prerequisites: Python 3.10+, Bash, and Docker with Compose v2. Linux is the main target. On Windows, use WSL2 and Docker Desktop. On macOS, use Docker Desktop. The image uses Python 3.12 and CPU inference. The first build needs internet access and several GB of disk space. It can take several minutes.

```bash
git clone https://github.com/NelsonPrates/local-layla.git
cd local-layla

# Generate the installation and copy a GGUF model that you already have:
python3 skills/layla-docker/scripts/setup.py --output runtime --model /path/to/model.gguf

cd runtime
./layla up
./layla ready
```

Open **http://127.0.0.1:8000/ui**.

To generate the installation before you select a model, leave out `--model`. Then do one of these:

- Select or download a GGUF model in the interface.
- Copy a GGUF file to `runtime/models/`, set `model_filename` in `runtime/data/runtime_config.json`, and run `./layla restart`.

The API can start without a GGUF model, but chat needs a compatible loaded model. `./layla ready` tells you which state you are in.

If `runtime/` is already configured, edit its files or generate into a different directory. The generator refuses to overwrite files. If port 8000 is busy, add `--port 8001` when you generate.

## Chat from the terminal

From the repository root:

```bash
python3 skills/layla-local/scripts/layla_client.py health
python3 skills/layla-local/scripts/layla_client.py ready
python3 skills/layla-local/scripts/layla_client.py ask 'Hello! Reply in one short sentence.'
python3 skills/layla-local/scripts/layla_client.py pending
```

For a different port: `python3 skills/layla-local/scripts/layla_client.py --base-url http://127.0.0.1:8001 health`. The client prints the full JSON and sends `allow_write=false` and `allow_run=false`. The skill instructions and references explain context, conversation continuity, and pending actions.

## Install the skills in your agent

You can use the `SKILL.md` files in this repository directly. You can also copy the skills to the folder that your agent reads:

```bash
python3 scripts/install-skills.py
# Or select the skills directory of your agent:
python3 scripts/install-skills.py --target ~/.codex/skills
```

The default target is `~/.agents/skills`. The script copies the four project skills. It does not overwrite skills that are already installed. In this repository, `.agents/skills/` and `.claude/skills/` already link to the project skills, Superpowers, and asd-ste100. After an external installation, reload the session if necessary. Then ask:

```text
Use $layla-docker to install Layla in ~/local-layla-runtime with my GGUF model.
Use $layla-local to chat with the Layla instance on localhost:8000.
Use $project-qa to check this change and record evidence before integration.
```

Each skill includes its own scripts, references, and interface metadata. You do not need to keep the repository after you copy the skills.

## Daily operation

Run these commands in the generated directory:

| Command | Result |
| --- | --- |
| `./layla up` | Builds when necessary, starts, and waits for the API |
| `./layla status` | Shows the container state |
| `./layla health` / `./layla ready` | Shows health / checks that a model is loaded |
| `./layla logs` | Follows the logs |
| `./layla doctor` | Diagnoses Docker, the container, and the model |
| `./layla restart` | Applies changes to the app configuration |
| `./layla down` | Stops and removes the container. Keeps the files |
| `./layla approve ID` | Approves one specific authorized action from inside the container |

`data/`, `models/`, and `workspace/` persist on the host. Layla sees the work files in `/workspace`. The port is published only on `127.0.0.1`. The initial configuration limits the container to 4 CPUs and 8 GB. To change this, edit `.env` for your model and hardware, then run `./layla up`.

The upstream allows tool approval and execution only for direct local connections. A call through the Docker bridge does not get these permissions automatically. See [operation and diagnosis](skills/layla-docker/references/operations.md) and the [API contract](skills/layla-local/references/api.md).

## Development and checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-skills.py
python3 scripts/check-vendor.py
python3 scripts/check-style.py
python3 scripts/check-plan.py docs/sdd/bootstrap/plan.json
bash -n skills/layla-docker/assets/container/layla
```

The tests cover generation, data preservation, independent skill installation, vendor integrity, prompt style, and the HTTP client with a simulated local server. They need neither Docker nor a model. To test the real container:

```bash
python3 skills/layla-docker/scripts/setup.py --output runtime --port 18765
cd runtime
./layla up
./layla health
# Without a configured GGUF model, ready must return 1.
./layla ready
./layla down
```

A real inference response needs a GGUF model. This repository does not distribute models, and the generator does not download them.

## Version and license

The build pins the upstream code to SHA `336ee4a362945b2badf8f48fcd5820cb132a7759`. The build gets the code and checks the SHA. The build still resolves the base image and the Python dependencies, so a byte-for-byte reproduction is not guaranteed.

The scripts and skills of this repository use the [MIT license](LICENSE). Layla keeps its own [non-commercial license](https://github.com/PapaKoftes/Layla/blob/336ee4a362945b2badf8f48fcd5820cb132a7759/LICENSE). Superpowers keeps its [MIT license and attribution](vendor/superpowers/LICENSE), and asd-ste100 keeps its [MIT license](vendor/asd-ste100/LICENSE). Models and dependencies have their own terms. See [THIRD_PARTY.md](THIRD_PARTY.md).
