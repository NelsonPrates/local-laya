# Plan: English translation and ASD-STE100 writing rules

Goal: an English repository with an enforced writing style for prompt text. Execution: `executing-plans`, one writing coordinator. The tasks run in sequence, because T02 and T03 both use the linter from T01.

- [x] T01 — Vendor and link asd-ste100, add the lock, and make `check-vendor.py` handle each library. Add `scripts/check-style.py`. Check: `python3 scripts/check-vendor.py` shows both libraries as intact.
- [x] T02 — Translate the Strict files: the contract, skills, references, roles, adapters, script messages, comments, and tests. Check: `python3 scripts/check-style.py` exit 0, and the unittest suite passes.
- [x] T03 — Translate the human documentation and the SDD records. Add tests and CI steps for the style and vendor checks. Check: the full suite, all checks, and a search for Portuguese text.

## QA matrix

| Criterion | Check | Expected | Required |
| --- | --- | --- | --- |
| E1 | Search for Portuguese characters and words outside `vendor/` | Only the Unicode test data | Yes |
| E2 | `check-vendor.py`. Discovery test. A test that changes a vendored file | Both libraries intact. Links resolve. A changed file fails | Yes |
| E3 | `check-style.py` and its unittest | 0 hard violations | Yes |
| E4 | Coordinator review of each translated document against its source | No lost facts, links, or SHAs | Yes |
| E5 | unittest, check-skills, check-plan for each plan, `bash -n`, Compose config | Exit 0 | Yes |
| Real container and inference | Not run | Startup did not change | No |

## Delivery

See [qa-report.md](qa-report.md).
