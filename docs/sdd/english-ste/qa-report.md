# QA report: english-ste

Date and agent: 2026-10-29 (local time), coordinator session. Mode: self-assessment. No independent QA delegation was used.
Target: `6b965b099e897b15572f07c9074c749aafa1fb9d`. Base: `3b38dbdc83161285b9dacc2d0acfa1399df3f920` (`develop`). Worktree: clean at the target.
Environment: Linux, Python 3.10.12, Docker 29.1.3 with Compose v2. Tests use local temporary resources.
Scope: E1–E5 from [spec.md](spec.md). Out of scope: a real container start and inference, because startup did not change.

| Criterion or check | Required? | Real command or procedure | Expected | Actual result and exit code | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| E1: no Portuguese text | Yes | `grep -P '[ãõçáéíóúâêôà]'` and a search for common Portuguese words, outside `vendor/` and `.git` | Only Unicode test data | Only `café` in `tests/test_layla.py`, which tests Unicode handling | pass | Search output |
| E2: vendor and links | Yes | `python3 scripts/check-vendor.py` | Both libraries intact | `asd-ste100 is intact: 8da6b63… (7 files)`, `superpowers is intact: bb92a77… (76 files)`, exit 0 | pass | Checker output |
| E2: changed vendor file fails | Yes | `test_changed_vendor_file_fails_integrity_check` | Non-zero exit that names asd-ste100 | Pass in the suite | pass | unittest |
| E2: discovery | Yes | `test_skill_discovery_links_and_vendor_integrity` | `asd-ste100/SKILL.md` resolves in `.agents/skills` and `.claude/skills` | Pass in the suite | pass | unittest |
| E3: Strict style | Yes | `python3 scripts/check-style.py` | 0 hard violations | `STE check passed: 17 files`, exit 0. 5 advisory passive-voice findings remain | pass | Linter output |
| E4: documentation keeps every fact | Yes | Coordinator review of each document against its Portuguese source. STE-flavored lint with lexical rules disabled | No lost facts, links, numbers, or SHAs. 0 structural violations | Review found no lost content. Lint: 0 violations | pass | Review in this session |
| E5: tests | Yes | `rtk proxy python3 -m unittest discover -s tests` | All pass | 27 tests, OK, exit 0 | pass | unittest |
| E5: skills, plans, Bash | Yes | `check-skills.py`, `check-plan.py` for each plan, `bash -n …/layla` | Exit 0 | 4 skills OK. 3 valid plans. Bash exit 0 | pass | Checker output |
| E5: Compose and generator | Yes, because the templates changed | `setup.py --output <tmp>` and `docker compose --project-directory <tmp> config --quiet`. `./layla help` | Exit 0. English help. `response_language` is `English` | Exit 0 for all. Help and config show the expected text | pass | Command output |
| Real container and inference | No, startup did not change | Not run | — | — | not-run | Only messages and comments changed in the templates |

## Defects and blocks

None open. During execution, the linter found semicolons, long sentences, and one synonym rotation in the first translation. Each finding was fixed before the target commit. The linter reads a YAML file as one sentence, so `scripts/check-style.py` leaves out `agents/openai.yaml`. The coordinator reviewed those files manually.

## Decision

**pass** for integration into `develop`: all required criteria passed and no blocker is open. Residual risks:

- This is a self-assessment, not an independent review.
- The STE lexical rules have no ASD dictionary. The text follows plain-word guidance but is not certified STE.
- Branches outside this change still contain Portuguese: `feature/copilot-adapter` (uncommitted work in the main checkout), `feature/layla-mcp/coordinator`, and `feature/rename-local-laya`. A merge of those branches conflicts with this change in `docs/workflow/SDD.md` and possibly other files. The copilot-adapter test requires `.github/agents/*.agent.md` to match the now-English `.claude/agents/*.md`.

## New check

This report is the only change after the target commit. It does not affect the evidence.
