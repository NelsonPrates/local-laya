# Research: QA/testing agent

Date: 2026-10-11. Request: add QA to the shared workflow and select the best skills to use as models. The repository uses Python stdlib and unittest, Bash scripts, Compose templates, and documentation and skills. It has no frontend application of its own. It has 24 tests and 15 vendored Superpowers skills. The change does not affect Layla, the container, or the API.

## Evidence and selection

Sources read: the [skills.sh](https://skills.sh/) catalog, `npx --yes skills find testing-strategy`, and the primary files of the candidates. Popularity helps to find options. Fit with the repository decides the selection.

| Candidate | Evidence and fit | Decision |
| --- | --- | --- |
| [Anthropic testing-strategy](https://github.com/anthropics/knowledge-work-plugins/blob/02ffa99ff00ce4d3046ccebabb8357cb39f3ab06/engineering/skills/testing-strategy/SKILL.md) | Strategy by component and risk. Balances coverage, speed, and maintenance. Requires no framework. Apache-2.0 repository. | Basis for the smallest sufficient matrix. |
| [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion/SKILL.md) | Requires current evidence before a success claim. Already available locally, MIT. | Basis for the QA report and decision. |
| [Superpowers test-driven-development](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development/SKILL.md), writing-good-tests resource | Test behavior and find real regressions. Rejects tests that only mirror code or prose. | Basis for the quality of new tests. TDD when executable behavior changes. |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging/SKILL.md) | Reproduction, hypothesis, and cause before the fix. | Basis for sending defects to the implementer. |
| [Anthropic webapp-testing](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing/SKILL.md) | Browser, Playwright, and evidence of the local interface. The current stack does not need this for every change. | Conditional reference for a changed web journey. Do not install a browser or Playwright now. |
| [python-testing-patterns](https://github.com/wshobson/agents/blob/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/python-development/skills/python-testing-patterns/SKILL.md) | Description and first examples center on pytest, fixtures, and mocks. MIT repository. | Deferred: unittest is sufficient. Do not migrate the stack to adopt a skill. |

The external revisions are the ones that were read. They are not installed dependencies. Superpowers stays unchanged. The project instructions will be original, with attribution through links. Do not copy helpers, and do not assume one license for the mixed anthropics/skills repository. No more libraries need to be downloaded as models.

## Agent compatibility

- [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): project TOML in `.codex/agents/`, with name, description, and developer_instructions. The repository already uses this format. Inherit the model and permissions from the session.
- [Claude Code: sub-agents](https://code.claude.com/docs/en/sub-agents): Markdown in `.claude/agents/`, with frontmatter for the name, description, and tools. QA needs Bash to run tests and write access for its artifacts. The instructions limit the scope, with no claim of a read-only sandbox.
- Common contract in `docs/workflow/qa-test.md`. The existing installer can copy one self-contained skill with relative references.

## Decision

Research stays first. Then come the technical plan with a QA contribution to the matrix, the Superpowers execution, the QA check, and the integration or release. QA compares the criteria with behavior and evidence. The existing code review stays responsible for structural quality. QA does not merge, release, or silently fix the product.

Two modes are enough: plan the tests and check the delivery. A small matrix can stay in the plan. Larger changes use `qa-plan.md`. Record the SHA, commands, exit codes, expected and actual results, and limits in `qa-report.md`. A required test that is not available blocks the criterion. An out-of-scope test must not create artificial work. Container smoke tests, real inference, and browser tests depend on what changed. The existing CI checks execution. It does not read the text QA approval.

No user decision is open. Confirm portability with an installation in a temporary directory and the links for both providers. Evaluate the skill independently with a realistic isolated task.
