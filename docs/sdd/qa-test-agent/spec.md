# Spec: QA/testing agent

Add the shared `qa-test` role, Codex and Claude adapters, and the project skill `project-qa`. The user asked for the agent and for a selection of skills to use as models. The names, artifacts, and strategy below are local technical decisions.

## Acceptance

- A1: QA takes part in the plan after the research and checks the delivery after the Superpowers execution, before Gitflow integration. Define the responsibility, the handoff, and the return path for defects, without replacing code review.
- A2: The selection is based on primary sources: testing-strategy and three Superpowers skills, with webapp-testing as a conditional reference. Keep the unittest stack and the vendored copy.
- A3: The Codex and Claude agents point to the same contract and do not set a model. QA runs tests and writes only assigned artifacts and tests, with isolation and one writer for each file.
- A4: The copied skill is self-contained. The installation includes its resources and keeps existing targets. Discovery works for both providers.
- A5: The report separates pass, fail, blocked, and not-run, links evidence to the commit and environment, and does not approve a missing required test. Define the new check after a fix or integration, and separate a healthy API from real inference.

Out of scope: changes to the Layla product or to Superpowers, new frameworks or a browser, and running a GGUF model. Publishing a version or tag and remote protection settings are also out of scope. The QA requirement is an agent contract. This change does not create an automated gate that reads the report.
