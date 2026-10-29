# Select the smallest sufficient matrix

Use the real criteria of the change. This table is a starting point. You do not have to run every row. Use the RTK prefix when the environment requires it.

| Change | Useful check | Limit of the evidence |
| --- | --- | --- |
| Skill, contract, or documentation | Check metadata and links. Run the changed examples. Test one realistic request if the instructions are complex | Do not create tests that search for words or headings. A structural read does not prove agent decisions |
| Generator or installer | Run it in a temporary directory. Check files and values, overwrite refusal, invalid input, and preserved data | Do not use a personal runtime to prove preservation |
| HTTP client | Use a controlled local server for payloads, errors, timeouts, redirects, and forbidden effects of the changed contract | Do not call this real inference |
| Worktrees and locks | Temporary clone, concurrent tasks, exclusivity, cleanup, and ancestry | Claims are local to the clone. They are not distributed |
| Compose or Docker | Generate an isolated installation and run `docker compose --project-directory <installation> config --quiet`. If startup changes, run a real build, up, health, and down | Valid syntax or config does not prove a started container. Health does not prove a loaded model |
| Inference | Authorized GGUF model, positive ready result, and a coherent response that is not empty from the real API | Without a model, a required inference criterion is blocked. Do not download a model only to close QA |
| Changed web journey | Real browser, user steps, assertions on state or elements, and a capture of failures | Use Playwright only when it is useful and available. Fixed waits and screenshots alone do not prove success |
| Release or hotfix | Relevant checks, version and notes, CI, and the combined candidate SHA | `check-release.py` checks local consistency. Do not create a public tag as an experiment |

Usual commands in the local-layla root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-skills.py
python3 scripts/check-vendor.py
python3 scripts/check-style.py
python3 scripts/check-plan.py docs/sdd/<change>/plan.json
bash -n skills/layla-docker/assets/container/layla
```

For a parallel runtime test, use your own temporary installation, a free port, and a unique `COMPOSE_PROJECT_NAME`. Do not share the data, models, or workspace directories. Stop only the resources that the test created. An unavailable environment is not a product defect. It is also not a success.

For new tests, get the expected result from the contract. Make sure that a plausible change in behavior makes the test fail. When the implementer adds new behavior or a fix, the implementer applies TDD when it fits. QA can show a gap with a reproduction. QA does not take over the fix.

## Skills selected as models

| Primary source | Use in this skill |
| --- | --- |
| [Anthropic testing-strategy](https://github.com/anthropics/knowledge-work-plugins/blob/02ffa99ff00ce4d3046ccebabb8357cb39f3ab06/engineering/skills/testing-strategy/SKILL.md) | Select test levels by risk. Balance confidence, time, and maintenance |
| [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion/SKILL.md) | Require a run and evidence before a claim of approval |
| [Superpowers test-driven-development](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development/SKILL.md) and [writing-good-tests](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development/writing-good-tests.md) | Test behavior and real regressions. Do not mirror the implementation |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging/SKILL.md) | Reproduce failures and find the cause before the fix |
| [Anthropic webapp-testing](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing/SKILL.md) | Only for a local interface: browser observation and journey evidence |

Date of access: 2026-10-11. These are method references. The skill is self-contained and does not require their installation. In the local-layla repository, the three Superpowers skills are already in `vendor/superpowers/skills/`. Explicit session instructions and the local contract have priority. Do not copy installations or hooks. Do not add pytest or Playwright only because a reference mentions them. The full comparison of the candidates is in the SDD research of the project's qa-test-agent change.
