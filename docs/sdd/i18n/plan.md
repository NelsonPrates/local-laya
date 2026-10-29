# Plan: multilingual local-layla

Goal: local-layla shows its CLI messages and its main document in the user's language, with English as the default and the fallback. Research: [research.md](research.md). Acceptance: [spec.md](spec.md). Tasks: [plan.json](plan.json).

Execution: `subagent-driven-development`. Several tasks write different files and can run in parallel worktrees. One coordinator integrates them one at a time.

## Deliveries

Each delivery ships alone and keeps English output byte-identical. A user sees a new language only from D5.

| Delivery | Tasks | Result after the merge | Time |
| --- | --- | --- | --- |
| D1 Foundation | T01, T02 | The tool and the helper exist. No visible change | 65 min (45 min in parallel) |
| D2 Python CLIs | T03, T04 | Every Python message goes through a catalog. English stays the same | 55 min (30 min in parallel) |
| D3 Bash CLI | T05 | `./layla` reads generated message files | 35 min |
| D4 Reply language | T06, T07 | `setup.py --language` sets the Layla reply language | 50 min |
| D5 First locale | T08, T09 | `LAYLA_LANG=pt_BR` shows Portuguese. CI checks the catalogs | 65 min |
| D6 Docs and prompts | T10, T11, T12 | `README.pt-BR.md`. Agents reply in the user's language | 65 min |

Total: about 5 hours and 35 minutes of work, or about 4 hours with parallel worktrees. Add one D5-style step, about 1 hour, for each new locale after `pt_BR`.

## Tasks

The full fields are in `plan.json`. Summary:

- [ ] **T01** `scripts/i18n.py` with 4 commands. `extract` scans `_()` calls with `ast` and writes a `.pot`. `build` compiles `.po` to `.mo` from the documented GNU format, and writes `messages/<locale>.sh` for Bash with `printf %q`. `pseudo` writes a test catalog that marks each string as `[!! … !!]`. `check` fails on missing strings, stale generated files, and stale document markers. Test: `tests/test_i18n_tool.py`.
- [ ] **T02** `_i18n.py` in `skills/layla-docker/scripts/` and `skills/layla-local/scripts/`. Signature: `translator(domain, localedir=None) -> gettext.NullTranslations`. It reads `LAYLA_LANG` and changes `-` to `_`. Then it lets gettext read the standard variables, with `fallback=True`. A test checks that the two copies are identical. Parallel with T01.
- [ ] **T03** Wrap the `setup.py` strings with `_ = translator("layla-docker").gettext`. Create `skills/layla-docker/locales/layla-docker.pot`. Add a test that fails on an unwrapped `print`, `parser.error`, `ArgumentTypeError`, or `help=` literal, and a pseudo-locale test.
- [ ] **T04** The same work for `layla_client.py` with the domain `layla-local`. Do not change the JSON that the client prints. Parallel with T03.
- [ ] **T05** `layla` sources `"$ROOT/messages/${locale}.sh"` when that file exists. The locale is `LAYLA_LANG` or the first locale variable. Each message keeps its English default, for example `printf '%s\n' "${MSG_MISSING_ENV:-Missing configuration. Run setup.py first.}"`. `setup.py` copies `messages/`. The `compose.yaml` interpolation message stays in English, because Compose cannot translate it.
- [ ] **T06** Coordinator research note: the full `response_language` key list after the tutor merge at `336ee4a`, and where the UI interface language is stored (Q1, Q2). Parallel with D1 to D3.
- [ ] **T07** `setup.py --language` with an allowlist from T06. It writes the canonical value and rejects other values before the first write. The default stays `English`. Document the flag in `references/operations.md`.
- [ ] **T08** Change the writing rule in `AGENTS.md`: English is the source, and translated catalogs and human docs are allowed. Run `check-style.py`. Add `pt_BR` `.po` files for both skills, then build. Test an installed copy of each skill with `LAYLA_LANG=pt_BR` outside the repository.
- [ ] **T09** Add `python scripts/i18n.py check` to `ci.yml` and `release.yml`. Write `docs/workflow/I18N.md`: extract, copy the `.pot` file to `<locale>.po`, translate, build, check, and open a PR.
- [ ] **T10** `README.pt-BR.md` with `<!-- source: README.md sha256:<hash> -->` on the first line. Add language links at the top of both files. Document `LAYLA_LANG` and `--language` in `README.md`.
- [ ] **T11** Add a Strict STE rule to the two Layla skills: "Reply in the language of the user. Do not translate commands, paths, or API fields." Run `check-style.py`. Parallel with T08 to T10.
- [ ] **T12** Changelog entry under Unreleased.

## Order and parallel work

```text
T01 ─┬─ T03 ── T05 ─┐
T02 ─┴─ T04 ────────┼─ T07 ─ T08 ─ T09 ─ T10 ─┐
T06 ────────────────┘    └──── T11 ──────────┴─ T12
```

`python3 scripts/check-plan.py docs/sdd/i18n/plan.json` checks the order and the file collisions. T03, T05, and T07 all write `setup.py`, so they run in sequence. T08 and T09 write the generated files and the CI that checks them, so they run in sequence.

## Review of the plan

- Removed: translation of the maintainer scripts and SDD records, po4a, Babel, translated prompts, and a translation platform. The research gives the reasons.
- Kept small: the helper is about 20 lines in each skill, and there is no shared package. Installed skills stay self-contained.
- Risk: a hand-written `.mo` compiler. T01 tests a round trip through `gettext.GNUTranslations`, including plural forms and a non-ASCII string.
- Risk: the Bash message files are code that `layla` runs. `build` writes only `MSG_*=` assignments with `printf %q`. T01 tests a translation that contains `$(…)`, quotes, and a newline.

## QA matrix

| Criterion | Check | Expected | Required |
| --- | --- | --- | --- |
| I1 | The existing suite, plus a comparison of the output of `setup.py --help`, `layla_client.py --help`, and `./layla help` before and after | Byte-identical without a locale | Yes |
| I2 | The unwrapped-literal tests and the pseudo-locale tests | Each message has the marker | Yes |
| I3 | Helper and Bash tests with `LAYLA_LANG=xx_YY` and no catalog | English, exit code unchanged | Yes |
| I4 | `install-skills.py --target <tmp>`, then run the copies with `LAYLA_LANG=pt_BR` | Portuguese text, no repository path | Yes |
| I5 | `tests/test_language_flag.py` | A valid value is written. An invalid value exits 2 and writes no file | Yes |
| I6 | `scripts/i18n.py check` on a clean tree and on 3 changed trees (missing string, stale `.mo`, stale marker) | Exit 0, then a failure for each case | Yes |
| I7 | Check the marker and both links | Present and current | Yes |
| I8 | `check-style.py`, `check-skills.py` | 0 hard violations, exit 0 | Yes |
| I9 | A test that reads the imports of `scripts/i18n.py` and the two helpers | Standard library only | Yes |
| Container start | `./layla up` and `./layla ready` with `LAYLA_LANG=pt_BR` | Portuguese messages. The container starts the same way | Yes for T05 |
| Real inference in Portuguese | `layla_client.py ask` with a loaded GGUF model and `--language pt` | A reply in Portuguese | No. Only with a model |

## Delivery

Each delivery gets a QA report in `qa-report.md` for its target SHA before the merge into `develop`.
