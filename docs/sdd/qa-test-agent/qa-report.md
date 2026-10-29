# QA report: qa-test-agent

Date: 2026-10-11 (UTC). Mode: independent review and forward test, consolidated by the coordinator.
Target: `550a6b4ee135e4bba8b039b5ea7695e30e31f698`. Base: `0ef523ff86f68ef4fe3b5a953235deb95bcdc833`.
The worktree was clean during the independent review. Environment: Linux, Python 3.10.12. HTTP, installation, and worktree tests use local temporary resources. The Layla runtime did not change.

| Criterion or check | Required? | Real command or procedure | Expected | Actual and exit | Status |
| --- | --- | --- | --- | --- | --- |
| A1/A2: workflow and references | Yes | Independent review of the diff, spec, plan, and research | QA after execution, proportional planning, suitable sources | No findings. Primary references at fixed revisions | pass |
| A3: adapters | Yes | Parse TOML with the tomli copy already present in the host pip, and YAML with the installed parser. Compare with the official contract | Name, description, instructions, Claude Bash access, inherited model | Parse and assertions exit 0. Both read the common contract | pass |
| A4: portability and preservation | Yes | `rtk proxy python3 -m unittest discover -s tests -v` | Independent installation, copied resources, preserved targets, valid links | 25 tests, exit 0. The independent reviewer repeated the run | pass |
| A5: skill decisions | Yes | Independent agent with a realistic isolated fixture | Evidence for each criterion, no false positives | Found data loss despite a green test. Required unavailable check blocked. Recommended fail | pass |
| Metadata and links | Yes | `rtk proxy python3 scripts/check-skills.py` and skill-creator quick_validate.py for project-qa | Four valid skills with their resources | Exit 0 for both | pass |
| Vendor | Yes | `rtk proxy python3 scripts/check-vendor.py` | Intact copy | 76 intact files. Exit 0 | pass |
| Plan | Yes | `rtk proxy python3 scripts/check-plan.py docs/sdd/qa-test-agent/plan.json` | Valid DAG T01 → T02 | Exit 0 | pass |
| Bash | Yes, usual regression | `rtk proxy bash -n skills/layla-docker/assets/container/layla` | Valid syntax | Exit 0 | pass |
| Real Docker, GGUF, browser | No, the runtime, API, and UI did not change | Not run | Out of scope for this change | No claim about a real container, inference, or interface | not-run |
| Native Codex and Claude sessions | No, not in this configuration delivery | Not started | Check files and the contract without external sessions | Formats checked. The evaluation uses a subagent available in this session | not-run |

## Defects and blocks

None open in the changed product. In the RED phase, both installation scenarios failed. The installer did not copy the fourth skill. Its presence also did not prevent a partial installation of the other skills. Adding project-qa to the pre-checked list fixed both. GREEN and the full suite confirmed the fix.

The first TOML parse failed, because neither tomllib nor a standalone tomli was available in the host Python 3.10. The check used the tomli copy that pip already supplies, without adding a project dependency. The parser is only a local check tool.

The forward-test fixture defect is intentionally outside the product and does not affect this recommendation. See [forward-test.md](forward-test.md).

## Independent review

Agent `qa_workflow_review` worked in a new context. It reviewed `0ef523f..550a6b4`, ran the 25 tests and the checks, and confirmed that HEAD and the checkout did not change. It returned "Ready to merge: Yes", with no critical, important, or minor findings. It asked to consolidate the report and the forward test. Both are in this directory.

Items the reviewer declined to judge, and the coordinator decision: the runtime, GGUF, and browser did not change and are out of scope. The spec excluded an automated text gate. Version publication and remote protection are not part of the request. None of these exclusions hides a required check of this change.

## Decision and new check

**pass** for integration of the feature into develop: all required criteria and checks of this change passed, and no blocker is open. The report requirement is a process contract, without a new automated gate in CI.

The later consolidation commits of this directory change only administrative artifacts. Review the diff to use the results of 550a6b4 again. Before integration, confirm that CI is green on the published head. If code, tests, configuration, or the integration base change, repeat the affected checks on the combined content and record the new SHA.
