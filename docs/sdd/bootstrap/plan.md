# Bootstrap: technical plan

Goal: deliver the skills and the shared workflow with the fewest mechanisms that let us use, check, and maintain the project.

Research: [research.md](research.md). Spec: [spec.md](spec.md). Execution: `executing-plans`, native in this session. The user already authorized the implementation and the publication of the repository. This plan consolidates the bootstrap that was in progress. It does not claim that the Layla part waited for the later SDD request.

1. T01 — finish generation and the Layla client. Check preservation and HTTP behavior, and check Docker startup. Files under `skills/layla-*` and `tests/test_layla.py`. Acceptance: independent generation, correct localhost handling, useful errors, and a checked boot. No model is available for an inference test.
2. T02 — deliver the research skill and planner, the parallel protocol, and the Superpowers library. Files: `skills/project-research`, `vendor`, `docs/workflow`, adapters, checkers, and their tests. T02 does not share code files with T01. Native sequential execution avoids unnecessary coordination cost in this bootstrap.
3. T03 — integrate CI and release, documentation, and review. Run the combined suite and publish main/develop on the personal account. Depends on T01 and T02. Acceptance: green checks, confirmed remote state, and no published version tag.

Common checks: `python3 -m unittest discover -s tests -v`, `python3 scripts/check-skills.py`, `python3 scripts/check-vendor.py`, `python3 scripts/check-plan.py docs/sdd/bootstrap/plan.json`, and a valid Compose file. T01 adds a real boot. T02 adds concurrent claims in a temporary clone. Review: spec coverage, no overwrites, local URLs, locks for each clone, the vendored revision, and tags that belong to main.

- [x] T01 complete and checked
- [x] T02 complete and checked
- [x] T03 integrated, reviewed, and published
