# Spec: multilingual local-layla

The user asked for a roadmap that makes local-layla multilingual, with research on tools and design patterns, and a refactoring plan in small, evolutionary deliveries. The user said that the product is "local-layla itself". The tool choice, the first locale, and the scope limits are technical decisions from [research.md](research.md).

## Behavior

- A user selects the language with `LAYLA_LANG` (for example `pt_BR` or `pt-BR`). Without it, the standard `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG` variables apply. Without any match, the text is English.
- The language applies to `setup.py`, `layla_client.py`, and the generated `./layla` script.
- `setup.py --language <value>` sets the Layla reply language. The default stays `English`.

## Acceptance

- I1: With no language variable set, or with `LAYLA_LANG=en`, every CLI output is byte-identical to the output before the change. The existing tests pass without change.
- I2: Every user-facing message in `setup.py`, `layla_client.py`, and `layla` goes through the catalog. A test fails when a message literal is not wrapped. A pseudo-locale test shows the marker on each message.
- I3: A missing catalog, a missing string, or an unknown locale shows English. No CLI fails because of the locale.
- I4: Each installed skill works alone. `install-skills.py` copies its `locales/` folder, and a copied skill shows `pt_BR` text without the repository.
- I5: `setup.py --language` accepts only values that the upstream registry at the pinned SHA supports. It rejects other values with an error and changes no file.
- I6: `pt_BR` catalogs are complete for both skills. `scripts/i18n.py check` fails in 3 cases. A catalog misses a string. A generated `.mo` or `.sh` file does not match its PO source. A translated document is older than its source. CI runs it.
- I7: `README.pt-BR.md` exists, records the hash of `README.md`, and both files link to each other.
- I8: Skills and prompts stay in English Strict STE. `check-style.py` reports 0 hard violations. `layla-docker` and `layla-local` tell the agent to reply in the user's language.
- I9: The scripts use only the Python standard library. The host needs no GNU gettext tools.

Out of scope: maintainer scripts (`scripts/*.py` other than `i18n.py`), SDD records, workflow guides, translated prompts, the upstream UI, a translation platform account, and a release or tag.
