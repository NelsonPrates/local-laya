# Spec: English translation and ASD-STE100 writing rules

The user asked for three things:

1. Translate all project files into natural English.
2. Install and use an ASD-STE100 skill for prompt text.
3. Use clear, instructional language for documentation.

The file scope, the lint gate, and the default language are local technical decisions.

## Acceptance

- E1: No file outside `vendor/` contains Portuguese text. The only exception is test data that checks Unicode handling.
- E2: `vendor/asd-ste100/` holds the upstream skill at a fixed revision, with its MIT license and a SHA-256 lock. `.agents/skills/asd-ste100` and `.claude/skills/asd-ste100` link to it. `scripts/check-vendor.py` checks both vendored libraries and fails on a changed file.
- E3: Skills, skill references, agent roles, adapters, and `AGENTS.md`/`CLAUDE.md` use Strict mode. `scripts/check-style.py` reports zero hard violations, and CI runs it.
- E4: README, workflow guides, changelog, attribution, and SDD records use clear, instructional English. They keep every fact, number, link, and SHA from the source.
- E5: Behavior does not change, except for messages and the default `response_language`, which is now `English`. All existing tests and checks pass.

Out of scope: changes to vendored upstream files, branches that other agents own, and a release or tag.
