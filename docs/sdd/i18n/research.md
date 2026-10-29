# Research: make local-layla multilingual

Date: 2026-10-29. Base: `feature/english-ste/coordinator` at `bb48d81`. Upstream Layla: `336ee4a362945b2badf8f48fcd5820cb132a7759`.

## Problem

All local-layla text is in English. The user wants a roadmap that makes local-layla itself available in more than one language. English stays the default and the fallback. The roadmap must split the refactoring into small deliveries that each ship on their own.

## Current state

Text that a user of the skills sees:

| Surface | Where | Size | Notes |
| --- | --- | --- | --- |
| Python CLI messages | `skills/layla-docker/scripts/setup.py` | 81 lines, about 14 messages | argparse help, `parser.error`, `print` |
| Python CLI messages | `skills/layla-local/scripts/layla_client.py` | 79 lines, about 12 messages | argparse help, errors |
| Bash CLI messages | `skills/layla-docker/assets/container/layla` | 50 lines, 1 help block and 4 messages | `setup.py` copies it to the runtime directory. It runs on the host |
| Compose error | `skills/layla-docker/assets/container/compose.yaml` | 1 message | `${LAYLA_REV:?Run setup.py first}` |
| Layla reply language | `setup.py` writes `"response_language": "English"` | 1 value | Upstream reads it. See below |
| Human docs | `README.md`, skill references | 1 main document | The workflow docs are for maintainers |
| Agent prompts | `SKILL.md`, references, roles, `agents/openai.yaml` | 4 skills, 2 roles | Strict ASD-STE100 English |

Text that only maintainers see: `scripts/*.py` messages, the SDD records, and the workflow guides. Maintainers work in English (`AGENTS.md`).

Constraints that apply to every option:

- Each skill must be self-contained. `scripts/install-skills.py` copies one skill folder, and the copy must work without the repository.
- The scripts use only the Python standard library. The host needs Python 3.10+, Bash, and Docker. GNU gettext tools are not a host prerequisite. On this machine `gettext` and `envsubst` exist, but `msgfmt`, `xgettext`, and `po4a` do not. macOS does not ship GNU gettext by default.
- `AGENTS.md` says "All repository text is in English". A translation needs an explicit exception in that rule.
- ASD-STE100 defines only English. The Strict style check cannot check a translated prompt.

## Evidence

### Python gettext (standard library)

Source: [gettext, Python 3 docs](https://docs.python.org/3/library/gettext.html), read 2026-10-29.

- `gettext.translation(domain, localedir, languages=None, fallback=True)` returns a translation object. With `fallback=True` it returns `NullTranslations` when no catalog exists, so the English source string is shown.
- When `languages` is `None`, `find()` reads `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG`. The first non-empty one wins. It looks for `localedir/<language>/LC_MESSAGES/<domain>.mo`.
- The docs recommend the class-based API for modules and libraries. A module must not call the global `install()`.
- `ngettext` handles plurals. `pgettext` and `npgettext` (context) exist since Python 3.8.
- `pygettext.py` and `msgfmt.py` are in CPython `Tools/i18n`. The docs say that "some Python distributions will install" them. On this machine they are not installed. The project needs its own way to extract strings and compile `.mo` files.
- `GNUTranslations` reads only binary `.mo` files.

### Bash locale translation

Source: [Bash manual, Locale-Specific Translation](https://www.gnu.org/software/bash/manual/html_node/Locale-Translation.html), read 2026-10-29.

- `$"..."` translates a string through gettext with `TEXTDOMAIN` and `TEXTDOMAINDIR`. In the C or POSIX locale, or when no translation exists, Bash uses the original string.
- It needs compiled `.mo` catalogs and the gettext library on the host. The `noexpand_translation` option exists.
- A `$"..."` string is a security risk when it contains expansions, because the translation can add command substitutions. The help heredoc in `layla` is not a `$"..."` candidate.

### Documentation translation

Sources: [po4a-gettextize(1p)](https://man.archlinux.org/man/po4a-gettextize.1p.en), [po4a project](https://po4a.org/), and real configurations such as wesnoth `doc/man/po4a.cfg` and ansible/workshops `po4a.cfg`. Read 2026-10-29.

- po4a keeps translations in PO files and builds the translated documents from the source structure. It supports Markdown through its text module.
- It is a Perl tool and is not installed here. The one-time migration of an existing translation (`po4a-gettextize`) is fragile.
- For one document with frequent edits, a parallel file (`README.pt-BR.md`) with a source marker is simpler. A check can compare the marker with the current source.

### Upstream Layla at the pinned SHA

Sources: `agent/services/prompts/response_language.py`, `agent/routers/language.py`, and `README.md` at [`336ee4a`](https://github.com/PapaKoftes/Layla/tree/336ee4a362945b2badf8f48fcd5820cb132a7759). Read 2026-10-29.

- `response_language.py` has a registry with the base entries english, dutch, japanese, arabic, and mandarin. It merges the tutor `LANGUAGES` registry into it.
- `normalize_language` accepts a code, an English name, or a native name, case-insensitive. An empty value, `auto`, or `default` gives no language block. **An unsupported value is ignored without an error.**
- The upstream README says that the web UI has 11 interface languages: English, Spanish, German, French, Italian, Portuguese, Russian, Japanese, Chinese, Korean, and Arabic (RTL). The user selects it in Settings → Interface language. Untranslated strings fall back to English.
- Effect for local-layla: Layla can already reply in other languages and show its UI in other languages. local-layla only needs to write a valid `response_language`, and it must reject a value that upstream would ignore.

### Agent Skills and prompt language

Sources: [Agent Skills specification](https://agentskills.io/specification), read 2026-10-29. Studies: [Is Translation All You Need?](https://arxiv.org/abs/2403.10258), [Cross-Lingual Prompt Steerability](https://arxiv.org/abs/2512.02841), [CulturALL](https://arxiv.org/abs/2604.19262). Opinion: [The localized system prompt your model performs worse against](https://tianpan.co/blog/2026-06-02-the-localized-system-prompt-your-model-performs-worse-against-than-the-english-original).

- The spec has no language or localization field. `name` must match the folder name. Two language copies of one skill need two names and two folders, and an agent can load both.
- 2512.02841 found that English system prompts did slightly worse than same-language prompts, and the authors call the drop marginal. 2403.10258 and CulturALL found that native-language prompts help on culture-specific tasks. local-layla prompts are operational instructions, not culture tasks.
- No study isolates the system-prompt language for tool-use instructions. The evidence does not justify the cost of translated prompt copies.

## Alternatives

### Message catalogs for the Python CLIs

| Option | For | Against |
| --- | --- | --- |
| **A. gettext with PO sources and committed `.mo` files** | Standard format. Translator tools (Poedit, Weblate) read PO. `ngettext` for plurals. Locale lookup from the environment is built in | Needs a local extract and compile script, because the CPython tools are not installed |
| B. JSON catalog per locale and a dictionary lookup | Smallest code. No binary files | Custom format. No plural rules. No translator tooling. Own locale logic |
| C. Python dictionaries in a module per locale | No parser | Translators must edit code. Same gaps as B |
| D. Babel | Full CLDR data | A third-party dependency. The project is stdlib-only |

### Messages in the Bash script

| Option | For | Against |
| --- | --- | --- |
| A. `$"..."` and gettext | Native Bash feature | Needs gettext on the host and `.mo` files in the runtime. Injection risk with expansions. No support on a default macOS |
| **B. Generated message files (`messages/<locale>.sh`) that the script sources** | No host dependency. The build script generates them from the same PO files, with `printf %q` quoting | A small generator to write. The script must keep English defaults inline |

### Human documentation

| Option | For | Against |
| --- | --- | --- |
| **A. Parallel files (`README.pt-BR.md`) with a source hash marker and a staleness check** | No tool. Easy to review | A translator rewrites changed sections by hand |
| B. po4a | Paragraph-level updates | Perl dependency. Fragile migration. Too much for one document |
| C. A translation platform (Weblate, Crowdin) | Community workflow | An external account and service. Later option, when there are contributors. It reads PO files from option A |

### Agent prompts

| Option | For | Against |
| --- | --- | --- |
| **A. Keep English Strict prompts and add one rule: reply in the user's language** | One source. The STE check stays valid. No duplicate skill names | The agent's own reasoning stays in English. This is acceptable |
| B. Translated skill copies | Native prompt text | Duplicate `name` values or folders. No STE check. Copies drift |

## Design patterns

- **Message catalog (resource bundle):** each user-facing string is a key in a per-locale catalog. The source English string is the key (gettext style), so a missing translation shows English.
- **Locale fallback chain:** `LAYLA_LANG` > `LANGUAGE` > `LC_ALL` > `LC_MESSAGES` > `LANG` > English. gettext already does every step after `LAYLA_LANG`.
- **Strangler migration:** wrap strings file by file. English output stays byte-identical, so each step ships alone.
- **Externalize and enforce:** a test finds message literals that are not wrapped in `_()`. Pseudo-localization in the test (each translated string gets markers) shows strings that bypass the catalog.
- **Single source, generated targets:** one PO file for each skill and locale. The build script makes the `.mo` file for Python and the `.sh` file for Bash. A check fails when a generated file does not match its source.
- **Staleness marker:** a translated document records the SHA-256 of its English source. A check fails when the source changed.

## Recommendation

1. Use gettext with PO sources (option A). Add `scripts/i18n.py` with two commands: `extract` (an `ast` scan for `_()` calls that writes a `.pot` file) and `build` (compile `.mo` and generate the Bash message files). Use only the standard library. Write the compiler from the published `.mo` format. Do not copy CPython code, so no new license applies.
2. Each skill has its own `locales/` folder and its own copy of a small helper (`_i18n.py`, about 20 lines). A test checks that the copies are identical. This keeps each installed skill self-contained.
3. The Bash script sources a generated message file, with English defaults inline.
4. Add `setup.py --language`, checked against the upstream registry at the pinned SHA. The default stays `English`.
5. Translate `README.md` as a parallel file with a staleness marker.
6. Keep prompts in English Strict STE. Add a rule to the two Layla skills: reply in the user's language.
7. Start with one real locale, `pt_BR`, because the project started in Portuguese. Other locales use the same steps.
8. Leave the maintainer scripts (`scripts/*.py`) and the SDD records in English. Maintainers use English by the project contract.

## Open questions that change the implementation

- Q1: Which keys does the upstream tutor `LANGUAGES` registry add at the pinned SHA? Task T07 reads them and fixes the allowed `--language` values.
- Q2: Can `setup.py` preset the upstream UI interface language, or does the browser store it? If the browser stores it, it stays out of scope. Task T07 answers this too.
- Q3: Does Codex read localized interface strings in `agents/openai.yaml`? No source says so. They stay in English until a source does.
- Known limit: argparse's own words ("usage:", "error:") come from the Python `argparse` domain. Python ships no translations for them, so they stay in English.
