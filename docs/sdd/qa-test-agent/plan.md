# Plan: QA/testing agent

Goal: one shared agent, one self-contained skill, and integration into the existing workflow. Execution: `executing-plans`. Adapt its helpers to the plan format that the repository already uses, and keep the evidence and the independent review. One writing coordinator is enough: the two tasks depend on each other, so there is no parallel implementation group.

- [x] T01 — QA contract, skill, adapters, and workflow. Owner: coordinator. Files: `skills/project-qa/`, `docs/workflow/`, `AGENTS.md`, `CLAUDE.md`, `.codex/agents/qa-test.toml`, `.claude/agents/qa-test.md`, `README.md`, `CHANGELOG.md`. Result: A1/A2/A3/A5 defined without duplicating Superpowers steps. Check with the skill's quick_validate, a read of the adapters, and an independent evaluation of the behavior.
- [x] T02 — Installation, discovery, and evidence. Depends on T01. Owner: coordinator. Files: the installer and check-skills, the links `.agents/skills/project-qa` and `.claude/skills/project-qa`, installation and discovery tests, and the artifacts of this change. Result: A4 shown and A1–A5 reviewed. First, extend the installation test and watch it fail because the fourth skill is missing. Then add the skill to the installer. Run unittest, check-skills, check-vendor, check-plan, and the Bash syntax check. Record QA and review, and open a PR to develop.

## QA matrix

| Criterion | Minimum check | Expected |
| --- | --- | --- |
| A1/A2/A3 | Review of contracts, sources, and adapters | Coherent order and responsibilities. Same instructions for each provider |
| A4 | Temporary installation, preservation, links, and the unittest suite | The fourth skill works outside the repository, local references are present, nothing is overwritten |
| A5 | Independent forward test with isolated artifacts | A report with reasons, without false positives or unassigned fixes |
| Regression | Skills, vendor, and plan checks, and Bash. The full suite | Exit 0. Vendor copy intact |

Real container, GGUF, and browser: out of scope, because the runtime and UI do not change. The existing CI still checks Compose. The final QA writes `qa-report.md`. The coordinator maintains this plan. Evidence applies to the tested commit and needs a new evaluation if code, tests, or configuration change.

Pre-flight: T02 uses the self-contained project-qa directory from T01. The installation and the links use the same name. There is no interface conflict. Minimum order reviewed: no framework migration, automated gate, or wording test is necessary.

Review focus: the report of a required test that is not available, and evidence on an earlier commit. Also review concurrent writes to the QA artifacts, and portability without a checkout or vendored copy.

## Delivery

T01/T02 complete: implementation in da5272d and 550a6b4. 25 tests passed. The [QA report](qa-report.md) and the [independent forward test](forward-test.md) record evidence and a review without blockers. The PR and CI are the integration delivery, without a tag or release.
