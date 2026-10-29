# Research: English translation and ASD-STE100 writing rules

Date: 2026-10-29. Request: translate every local-layla file into English, written as if English were the original language. Find, install, and use an ASD-STE100 skill for skills, agents, and other LLM prompts. Use clear, instructional language for human-readable documentation.

## Current state and technical question

All project text was in Portuguese, in about 50 files (150 KB). This includes 4 skills and their references, and 2 agent roles with Codex and Claude adapters. It also includes the contract files, workflow guides, SDD records, script messages, comments, and tests. The vendored Superpowers copy is already in English and must not change. Decisions: where the ASD-STE100 skill comes from, how to install it in the repository, and how to enforce the style.

## Evidence

| Primary source or file | Revision or date | Checked finding | Implication |
| --- | --- | --- | --- |
| [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) | `8da6b6340aa22faf46fd07db8efbdea010cd38d9`, 2026-10-26 | MIT skill with Strict and STE-flavored modes and a stdlib linter (`scripts/ste-lint.py`, `--selftest` passes). The user already had an older copy in `~/.claude/skills/asd-ste100` | Vendor this revision. The linter can enforce the structural rules in CI |
| Same repository, `SKILL.md` | same SHA | The skill does not include the ASD dictionary, because ASD does not allow redistribution | Lexical rules are a direction, not a verified standard. Do not claim certified STE |
| `scripts/ste-lint.py` | same SHA | Hard rules: semicolons, sentences over 25 words, soft phrasal verbs, nominalization, marketing adjectives, synonym rotation, dangling conjunctions. Passive voice and compound tenses are advisory | Zero hard violations is a checkable target. A YAML file reads as one sentence |
| `vendor/superpowers/source.lock.json`, `scripts/check-vendor.py` | `3b38dbd` | One lock format with SHA-256 and executable modes. The checker only handles Superpowers | Use the same lock format. Make the checker handle each `vendor/*/source.lock.json` |
| `skills/layla-docker/scripts/setup.py` | `3b38dbd` | Default `response_language` is `Portuguese` | A project written in English defaults to English. This is a behavior change. Record it in the changelog |

## Alternatives and recommendation

1. Use only the user-level copy of the skill. Other agents and clones would not have it. Rejected.
2. Add the skill as a git submodule. Clones need an extra step, and the project already chose vendoring. Rejected.
3. Vendor the skill with a lock, link it in `.agents/skills/` and `.claude/skills/`, and add `scripts/check-style.py` to CI. Recommended. Cost: 7 files (about 70 KB) and one CI step.

Leave out the upstream `.claude-plugin/` metadata. It packages the skill as a plugin, and this project uses local links.

## Experiments

`python3 vendor/asd-ste100/scripts/ste-lint.py --selftest` returned OK. A first lint of the translated Strict files found semicolons, long sentences, and one synonym rotation. Each finding was fixed in the text.

## Questions that change the plan

None. Open branches in other worktrees (`feature/copilot-adapter`, `feature/layla-mcp/coordinator`, `feature/rename-local-laya`) still contain Portuguese text. They are out of scope. Their owners translate them when they merge.

## Handoff to the tech-planner

Criteria: no Portuguese text outside `vendor/`. Strict files pass the linter. Vendor checks cover both libraries. The existing tests and checks still pass. Execution: `executing-plans`, one coordinator.
