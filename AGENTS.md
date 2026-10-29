# local-layla: agent contract

Project: two skills that install and use PapaKoftes/Layla, plus research and QA skills for maintenance. Do not change the upstream product unless the user asks for it.

- Start each development or maintenance change with `skills/project-research/SKILL.md`. Then use the `docs/workflow/tech-planner.md` role with a QA matrix that fits the change. Follow `docs/workflow/SDD.md`: research → technical plan → Superpowers execution → QA → integration/release.
- Use `docs/workflow/qa-test.md` and `skills/project-qa/SKILL.md` to plan the tests and to do the final check. Record evidence for each criterion and SHA in `qa-report.md`. A required check that fails or is not available blocks an integration recommendation. Check the combined content again after a merge. Check again after each change that affects the evidence.
- Use the local Superpowers revision in `vendor/superpowers/skills/`. After the plan, the next skill is the execution skill that the plan records (`executing-plans` or `subagent-driven-development`). Use only its relevant resources. Explicit user instructions have priority. Do not ask again for an authorization that the user already gave. Do not change vendored files to change the process.
- Each task must have an observable result, files, dependencies, a check, and an owner. Use the smallest sufficient order. Review the tasks and remove unnecessary tasks before execution.
- Concurrent work: one writer for each worktree and task. Claim the task with `scripts/worktree.py`. Run tasks in parallel only when they are independent and write different files. Only the coordinator changes the shared plan or spec. Only the coordinator integrates branches.
- Respect changes from other agents. Do not use reset, clean, or force-push to solve a conflict. Do not remove worktrees or claims that belong to other agents.
- Gitflow: `feature/*` → `develop`. `release/*` starts from `develop`, goes to `main`, and returns to `develop`. `hotfix/*` starts from `main`, goes to `main`, and returns to `develop` and to the active release. Follow `docs/workflow/RELEASE.md`.
- Usual checks: `python3 -m unittest discover -s tests -v`, `python3 scripts/check-skills.py`, `python3 scripts/check-vendor.py`, `bash -n skills/layla-docker/assets/container/layla`. Check the generated Compose file when a template changes. Test the real container when a change affects startup. Claim real inference only when a GGUF model is loaded and you checked a model response.
- Do not commit data, models, `.env`, tokens, runtime files, or session state. The repository is public. Keep the source licenses and locks when you update vendored dependencies.
- If the environment requires RTK, put `rtk` before shell commands. Use `rtk proxy` for commands that RTK does not adapt.

## Writing rules

All repository text is in English.

- Skills, agent roles, adapters, and other LLM prompts: use the `asd-ste100` skill in Strict mode (`vendor/asd-ste100/SKILL.md`). This scope includes `AGENTS.md`, `CLAUDE.md`, `skills/`, `.claude/agents/`, `.codex/agents/`, and the role files `docs/workflow/tech-planner.md` and `docs/workflow/qa-test.md`.
- Error messages, help text, and code comments: use Strict mode.
- Human-readable documentation (README, workflow guides, SDD records, changelog): use clear instructional language. Apply the STE-flavored mode of the same skill.
- Before you commit prompt text, run `python3 scripts/check-style.py`. It must report zero hard violations.

Research, plans, and deliverables are in `docs/sdd/<change>/`. The initial bootstrap records work that the user already authorized. It is not a permanent authorization to publish future releases.
