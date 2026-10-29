# Local Superpowers

Source: [obra/superpowers](https://github.com/obra/superpowers), revision
`bb92a77741419a4ab5f06e711a283343f1ada0c3`, read and downloaded on 2026-10-11.
The copy includes the 15 complete skills, their resources and executables, the
README, and the MIT license. `vendor/superpowers/source.lock.json` records the
SHA-256 of each file. The discovery links do not duplicate or rewrite the
upstream files.

## Project routing

| Situation | Local skill |
| --- | --- |
| Start execution after research and planning | `using-superpowers`, then the plan's execution skill |
| Execute directly in the session | `executing-plans` |
| Control implementers with a review for each task | `subagent-driven-development` |
| Isolate the workspace | `using-git-worktrees` and a claim from `scripts/worktree.py` |
| Run independent investigations or tasks in parallel | `dispatching-parallel-agents`, within the project's file and worktree limits |
| Investigate a failure | `systematic-debugging` |
| Implement verifiable behavior | `test-driven-development`, in proportion to the change |
| Review | `requesting-code-review` / `receiving-code-review` |
| Claim completion | `verification-before-completion` |
| Check acceptance after execution and review | `project-qa`, with `verification-before-completion`. Investigate with `systematic-debugging` |
| Finish a feature | `finishing-a-development-branch`, merging into `develop` per Gitflow |
| Write or review prompt text | `asd-ste100` (vendored in `vendor/asd-ste100/`), then `python3 scripts/check-style.py` |

`writing-plans` supports the tech-planner. It does not move research out of the
first step. The upstream text can suggest generic models, tools, paths, gates,
and merge options. The explicit session instructions and the local contract have
priority. Use the tools that are actually available, and keep the choices that
the user already authorized. Do not ask for a second authorization of the same
scope because of a library default.

Some upstream references describe plugin installations for specific harnesses.
This copy supplies the skills as local files. It does not install the hooks, and
it does not promise every plugin behavior. `AGENTS.md` and `CLAUDE.md` activate
the process explicitly. In tools without skill discovery, open `SKILL.md`
directly.

## Update a vendored library

This procedure applies to `vendor/superpowers/` and `vendor/asd-ste100/`.

1. Open an SDD change. Research the new revision, the workflow differences, the
   license, and the compatibility with Codex and Claude.
2. Download the complete skill folders at the selected SHA. Keep the bytes and
   the executable modes from the source Git repository.
3. Update the README and LICENSE too. Review the differences.
4. Generate the lock again from the reviewed tree. Never generate hashes only to
   hide a local change.
5. Run `python3 scripts/check-vendor.py`, check the local links, and review the
   routing above.

The checker detects file changes against the lock. It is not a cryptographic
signature of the author. Review of the download and its source is still part of
the maintenance.
