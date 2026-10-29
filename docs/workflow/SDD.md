# Spec-driven development (SDD)

This is the shared development and maintenance workflow. It does not depend on one provider. In this documentation, SDD means **spec-driven development**. The Superpowers skill `subagent-driven-development` is one way to execute a plan. It is not the name of the whole workflow.

## Minimum sequence

1. **Research:** use `skills/project-research/SKILL.md`. In `docs/sdd/<change>/research.md`, record the problem, the current state, the primary evidence, the relevant alternatives, the recommended decision, and the open questions that change the implementation. A small fix can have a research note of a few paragraphs. Do not write product code in this step.
2. **Technical plan:** the [tech-planner](tech-planner.md) role turns the research into `spec.md`, `plan.md`, and `plan.json` in the same directory. The spec describes behavior and acceptance criteria. The plan selects the smallest sequence of verifiable deliveries. For each task, include the files, dependencies, owner, check, and completion conditions. The [qa-test](qa-test.md) role adds the smallest sufficient test matrix, in the plan or in `qa-plan.md` when it is long. Validate the plan with `python3 scripts/check-plan.py docs/sdd/<change>/plan.json`.
3. **Superpowers execution:** read `vendor/superpowers/skills/using-superpowers/SKILL.md` and the execution skill that the plan records. For native, sequential execution, use `executing-plans`. For a controller with implementers and a review for each task, use `subagent-driven-development`. The selected skills drive worktrees, TDD where it applies, review, fixes, and the final check. Read only the relevant resources. Do not invent subagent tools that are not available.
4. **QA and tests:** the [qa-test](qa-test.md) role uses `skills/project-qa/SKILL.md` to check the criteria on the delivered stable SHA. It writes `qa-report.md` with the commands, results, and limits. A failure goes back to the implementer, and a fix needs a new check. A required check that is missing or fails blocks an integration recommendation. QA adds to the Superpowers review. It does not repeat the structural review.
5. **Integration and release:** deliver the review, the QA report, and the feature PR to `develop`. Check the combined result again. Follow [RELEASE.md](RELEASE.md) for stabilization, `main`, tags, and publication. The current CI runs the checks. The coordinator reads the QA report. No automated gate reads its text.

Planning can use `writing-plans` as a method, but keep this order and these paths. If you need the intent analysis from `brainstorming`, do it inside the research step. Do not restart a discovery that is already complete. The explicit user request and the instructions of this project have priority over the library defaults. Do not change the vendored files.

## Short, clear tasks in the right order

- Use the smallest solution that meets the criteria. Remove speculative work, repeated steps, and unused abstractions.
- Each task delivers a result that someone can review. Configuration and documentation belong to the task whose result depends on them.
- Order the tasks by prerequisites first. Among ready tasks, prefer the ones that unblock other tasks, then the ones with the least effort. Do not promise a global mathematical optimum.
- The task table has a stable ID, dependencies, files, an owner, an estimate in minutes, acceptance criteria, and a command with its expected result.
- Run tasks in parallel only when they do not depend on each other **and write different files**. If two tasks need the same file, run them in sequence or change the task boundary. Do not rely on a conflict being unlikely.
- Review the plan once before execution. Check spec coverage, interfaces, unnecessary tasks, dependencies, file conflicts, checks, and the shortest path. If you correct the plan later, record the changed assumption.

The validator checks the DAG, the fields, the IDs, and collisions of normalized paths between independent tasks. Use exact paths or directories. The validator rejects globs. Indirect effects, symlinks, and changes to files that a task does not declare need a semantic review by the coordinator.

## Codex and Claude at the same time

The rule is **one writing agent for each worktree and each task**. All agents share Git and the committed artifacts, but not the working directory. Any number of sessions from any provider can take part when there are independent tasks and enough resources.

1. One coordinator writes the research, spec, and plan and merges them into `develop` before dispatching implementers. Only the coordinator updates the plan and integrates PRs. Workers do not change these shared files.
2. Each agent receives a change, a task, a base branch, and criteria. Claim the task and create the worktree:

   ```bash
   python3 scripts/worktree.py start --change example --task T01 --agent codex-1
   python3 scripts/worktree.py start --change example --task T02 --agent claude-1
   ```

3. Open Codex or Claude in the printed path, each in its own terminal or session. The script prepares isolation and the claim. It does not start or control sessions. The labels `codex-1` and `claude-1` are free text. They do not fix a provider.
4. A dependent task starts only after its prerequisites are integrated. Update or fetch the base before you open the next worktree. Integrate PRs one at a time with a QA recommendation. Run the checks on the combined result before you release dependent tasks. The final QA check uses stable content. Scenario and test planning can run in parallel with exclusive files and resources, as [qa-test](qa-test.md) describes.
5. Each worker writes a handoff in `docs/sdd/<change>/handoffs/<task>-<agent>.md`: SHA, files, tests and results, limits, questions, and scope changes. The coordinator uses this file in the review and the PR.
6. `python3 scripts/worktree.py list` shows the claims. They are stored in shared Git storage that all worktrees can see. To finish a task, stop its writing session, make sure that its commits are integrated, and run `finish` with the same identifiers. Do not use `--force` to remove the work of another session.

The script publishes each claim complete through an exclusive hard link in the common Git directory. This prevents double ownership and partial JSON reads. Claims are local to the machine and the clone. For several clones or machines, the coordinator uses assignees and PRs as the authority. Do not treat this local lock as a distributed lock. Before you manually remove an orphan claim, check its worktree, its commits, and its session. Never release a claim automatically after a timeout.

The default Compose project name is `local-layla`. Concurrent container tests need their own installations, different ports, **and different Compose project names** (`COMPOSE_PROJECT_NAME=local-layla-t01 ./layla up`). Tests that write must not share runtime data, models, or workspaces.

## Portable skills and roles

- `AGENTS.md`: the contract for Codex and other agents that read this file.
- `CLAUDE.md`: imports the same contract.
- `.agents/skills/`: local skills that Codex discovers.
- `.claude/skills/`: the same skills, for Claude Code.
- `.codex/agents/tech-planner.toml` and `.claude/agents/tech-planner.md`: adapters for the shared planner.
- `.codex/agents/qa-test.toml` and `.claude/agents/qa-test.md`: adapters for the shared QA role. Both roles inherit the session model.

The discovery directories use relative links to `skills/`, `vendor/superpowers/skills/`, and `vendor/asd-ste100/`. The links keep the neighboring resources available. If a platform does not follow links, copy the folders to its skills directory. Agents can always read the contract files directly.

See [SUPERPOWERS.md](SUPERPOWERS.md) for routing and for updates to the local copy. This integration uses local skills. It does not install global hooks or plugins.

## Writing style

Write all files in English. Use the vendored `asd-ste100` skill:

- **Strict mode** for skills, agent roles, adapters, prompts, error messages, help text, and code comments.
- **STE-flavored mode** for human-readable documentation such as this guide. Use clear, instructional language: short sentences, active voice, and one idea for each sentence.

Run `python3 scripts/check-style.py` before you commit prompt text. The check covers the Strict Markdown and TOML files and must report zero hard violations. Review `agents/openai.yaml` files manually, because the linter reads a YAML file as one sentence.

Example kickoff:

```text
Read AGENTS.md. Use project-research to investigate <problem>.
Then use the tech-planner role to propose the smallest order of clear tasks.
Record the Superpowers execution in the plan, claim worktrees, and execute the
authorized work. Codex and Claude can take independent tasks. Use qa-test to
check acceptance and record qa-report.md before you recommend integration.
```

Do not ask again for an authorization that the session already gave. When a material decision is open, present the concrete plan first, and ask only what changes the execution. An instruction to only research or plan does not authorize product execution, merges, or releases.
