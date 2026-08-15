# Forgejo workflow stubs

**These are live.** This repo cut over on 2026-08-10: the forge
(`lenore/LenoreShop`) is the writer, and GitHub is a push mirror kept for the
public face and offsite DR.

All the real logic lives once in `lenore/lenore-ci`, pinned at `@v1` — a moving
major tag, following the actions convention. A fix there reaches every repo
without an edit here; a breaking change gets a deliberate `@v2`. That is why
these files are ~10 lines each.

| Stub | Calls | Fires on |
|---|---|---|
| `release.yml` | `release.yml@v1` | push to `main`/`rc`/`beta`/`alpha` |
| `build-publish.yml` | `build-publish.yml@v1` (`image_list: app`) | `release: published`, or dispatch by tag |
| `docs.yml` | `docs.yml@v1` (`mode: preview`) | push to `main` |
| `docs-release.yml` | `docs.yml@v1` (`mode: release`) | `release: published`, or dispatch by tag |
| `announce.yml` | `announce.yml@v1` (`target: reddit`) | `release: published`, or dispatch by tag |
| `pr-title-lint.yml` | `pr-title-lint.yml@v1` | `pull_request` |
| `tests.yml` | `tests.yml@v1` | `pull_request` |

`tests.yml` overrides all three of the reusable workflow's defaults, which
assume LenoreChore's setup: this repo runs Django's test runner rather than
pytest, installs `backend/requirements-test.txt` rather than `-test`'s usual
full set (mysqlclient will not build on the job image), and has no `npm test`
script, so the frontend job lints and builds instead.

## 🔴 `.github/workflows/` is gone, and it must stay gone

Forgejo reads **both** `.github/workflows/` and `.forgejo/workflows/`. With
Actions enabled on the forge, restoring that directory means every workflow runs
twice — and two `semantic-release` instances on one push is precisely the
double-changelog / double-bump anomaly this migration exists to prevent.

## 🔴 Never merge on GitHub

GitHub is a **push mirror**, so a merge performed there is not a contribution —
it is a divergence. A `non_fast_forward` ruleset guards `main`/`rc`/`beta`/
`alpha` there, which converts that mistake from silent data loss into a loud,
detectable mirror failure. Land the work on the forge and let the mirror carry
it back. Issues stay on GitHub permanently; the forge's tracker is disabled.
