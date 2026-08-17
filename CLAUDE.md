# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LenoreShop is a full-stack shopping list manager. The stack is:
- **Backend**: Django 4.2 + django-ninja (FastAPI-style API) + PostgreSQL, served via Daphne/ASGI
- **Frontend**: Vue 3 + Vite + Vuetify 3 + Pinia + TanStack Vue Query
- **Infrastructure**: Docker Compose (dev & prod), Nginx reverse proxy

## Development Commands

### Docker (recommended)

```bash
# Development (live reload, hot module replacement)
cp example.env .env.dev   # edit as needed
docker compose --env-file .env.dev -f docker-compose.yml up -d
# Frontend: http://localhost:8081  Backend: http://localhost:8001  Docs: http://localhost:8002
# Note: --env-file makes .env.dev vars available for ${VAR} substitution in the compose file
# (Docker Compose substitution reads the host shell / .env, not env_file entries)

# Production
cp example.env .env
docker compose -f docker-compose-prod.yml build
docker compose -f docker-compose-prod.yml up -d
# Nginx proxy: http://localhost:7000
```

### Frontend (from `frontend/`)

```bash
npm install
npm run dev        # Vite dev server with HMR
npm run build      # Production build
npm run lint       # ESLint --fix
npm run format     # Prettier --write src/
```

### Backend (from `backend/`, requires venv)

The project venv is `.venv/` at the repo root, on Python 3.11 to match the
`python:3.11.4-slim-bookworm` base image in the Dockerfile. Create it with:

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r backend/requirements-dev.txt
```

`requirements-dev.txt` pulls in `requirements.txt` plus a pinned `ruff`.
`mysqlclient` needs system headers — `sudo apt-get install
default-libmysqlclient-dev pkg-config` — before the install will succeed.

Note: `myenv/` is a leftover MkDocs-only environment and has no Django in it.

Django needs these env vars set or it will fail at import; the compose files
supply them in Docker, so export them by hand for a bare `manage.py` run:
`SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.

```bash
source ../.venv/bin/activate
python manage.py runserver 0.0.0.0:8001
python manage.py makemigrations && python manage.py migrate
python manage.py test                                          # all tests
python manage.py test api.tests.SomeTestClass.test_method     # single test
```

### Backend Linting

```bash
/usr/local/bin/ruff check backend/ --fix
```

Ruff is on PATH at `/usr/local/bin/ruff`, installed by the `code_server`
Ansible role. Do **not** call it by its VS Code extension path — that embeds
the extension version and breaks on every extension update. An activated
`.venv` shadows the global binary, so `backend/requirements-dev.txt` pins ruff
to the same version; check `ruff --version` on both sides before bumping.

Run before committing any Python changes. After `--fix`, manually resolve
remaining `F841` errors, then confirm `All checks passed!`.

## Architecture

### API Layer

All REST endpoints are defined in a single file: `backend/backend/api.py`, using django-ninja. They are flat `@api.<method>` handlers grouped by model (`stores`, `aisles`, `items`, `listitems`, `shoppinglists`, `freezers`, `freezeritems`, `version`) — not django-ninja `Router` objects — and the whole API is mounted at `/api/`. There are also compound read endpoints, `ShoppingListFull` and `FreezerFull`, that return a fully assembled list or freezer in one response.

Writes call `broadcast_invalidate([...])` (`backend/api/broadcast.py`) with the TanStack query keys the change affects; the frontend's `useRealtimeSync` invalidates those keys over the WebSocket. Keep the keys in a new endpoint matching the `queryKey` its composable uses.

**Data model relationships** (`backend/api/models.py`):
- `Store` → many `Aisle`, many `ShoppingList`
- `Aisle` → belongs to `Store`
- `Item` → optionally belongs to an `Aisle` (last used aisle)
- `ShoppingList` → belongs to `Store`
- `ListItem` → joins `Item` + `Aisle` + `ShoppingList`
- `Freezer` → many `FreezerItem`
- `FreezerItem` → belongs to `Freezer`; carries its own free-text `name` rather than an `Item` FK, so one-off leftovers don't pollute the shopping catalog

> A **partial freezer transfer** (`POST /api/freezeritems/{id}/transfer` with a
> `qty` below the row's) splits off a new row that **shares** the source's
> `image`/`thumbnail` path rather than copying the file. So a `FreezerItem`'s
> photo is not necessarily its own — `delete_renditions` in `api/images.py`
> checks `_still_referenced` before unlinking. Anything new that deletes image
> files must do the same, or one row's removal blanks another's photo.
- `Version` → singleton model

### Frontend Data Layer

The preferred data-fetching pattern is **TanStack Vue Query composables** in `frontend/src/composables/`. Each composable wraps axios calls to `/api/...` using `useQuery` / `useMutation`. The older `frontend/src/stores/main.js` Pinia store has direct axios fetch actions that coexist with composables — prefer composables for new code.

Pinia stores (`frontend/src/stores/`): `main`, `item`, `user` — all persisted to localStorage via `pinia-plugin-persistedstate`.

In dev, Vite proxies `/api` to the configured backend (`vite.config.js`). In production, Nginx routes `/api/` to `backend:8000`. Composables use a relative `baseURL: "/api"` that works in both.

### Router Pages

| Route | View |
|-------|------|
| `/` | HomeView |
| `/stores` | StoreView |
| `/alllists` | ListsStoreView |
| `/lists` | ListsView |
| `/list` | ListView (active shopping list) |
| `/items` | ItemView |
| `/aisles`, `/aisles/:store` | AisleView |
| `/freezers` | FreezerView |
| `/freezer` | FreezerContentsView (active freezer) |

> Dialogs must be rendered **outside** any `v-for`, as single instances driven
> by a `selected*` ref. One dialog per row shares the same ref and opens them
> all at once — on mobile that stacks into a black screen (fixed in
> `ShoppingList.vue`, see `ec3715c`).

## CI/CD & Versioning

As of 2026-08-10 this repo runs on **Forgejo Actions**, not GitHub Actions.
The forge (`lenore/LenoreShop` on `forge.lan.danielleandjohn.love`) is the
writer; GitHub is a push mirror kept for the public face and offsite DR.

- `origin` → the forge. `github` → the mirror. Land all work on `origin`.
- **Never merge on GitHub** — a merge there is a divergence, not a contribution.
- Workflows live in `.forgejo/workflows/` as thin stubs that call
  `lenore/lenore-ci/.forgejo/workflows/*@v1`, where all the real logic lives.
  See `.forgejo/workflows/README.md`.
- **`.github/workflows/` must stay deleted.** Forgejo reads both directories,
  so restoring it runs every workflow twice — including two `semantic-release`
  instances on one push.

| Stub | Fires on |
|---|---|
| `release.yml` | push to `main`/`rc`/`beta`/`alpha` |
| `build-publish.yml` | `release: published`, or dispatch by tag |
| `docs.yml` / `docs-release.yml` | push to `main` / `release: published` |
| `announce.yml` | `release: published` — **posts to Reddit** |
| `pr-title-lint.yml` | `pull_request` |
| `tests.yml` | `pull_request` |

**Forge repo settings** (configured 2026-08-11, not in version control):

- **Delete branch after merge is on.** A merged PR's head branch is pruned
  automatically — no `delete-merged-branches` workflow needed.
- **`main`, `rc`, `beta` and `alpha` are protected**, with `apply_to_admins`
  on. Force pushes and branch deletion are blocked. Normal pushes are still
  **allowed** (`enable_push: true`, no approvals, no required status checks)
  because semantic-release has to push its `chore(release):` bump commit
  directly to whichever branch it ran on. Do **not** set required approvals or
  disable push on these branches — that is what breaks the release.

Versioning is **semantic-release** (`.releaserc.json`), driven by conventional
commits, with `alpha`/`beta`/`rc` prerelease channels. `@semantic-release/exec`
runs `scripts/update-version.sh` to stamp the version into the Dockerfiles,
fixtures, `api.py`, `package.json`, and `App.vue`.

- `fix:` → patch, `feat:` → minor, `feat!:` / `BREAKING CHANGE:` → major
- `chore:`, `docs:`, `ci:`, `style:` → no release, no build, no announce

> `scripts/versioning.sh` and `ver_change.sh` are dead leftovers from the old
> GitHub-era pipeline. Nothing calls them; `update-version.sh` is the live one.

A Forgejo run reports one status per job, so a stub calling a reusable workflow
shows up as two contexts (`lint` and `lint-1`) from a single run. That is
normal and not a double execution.
