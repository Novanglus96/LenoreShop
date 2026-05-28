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
cp example.env.db .env.db # set DB credentials — never change after first run
docker compose -f docker-compose.yml up -d
# Frontend: http://localhost:8081  Backend: http://localhost:8001  Docs: http://localhost:8002

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

```bash
source ../myenv/bin/activate
python manage.py runserver 0.0.0.0:8001
python manage.py makemigrations && python manage.py migrate
python manage.py test                                          # all tests
python manage.py test api.tests.SomeTestClass.test_method     # single test
```

### Backend Linting

```bash
/home/jadams/.local/share/code-server/extensions/charliermarsh.ruff-2026.46.0-linux-x64/bundled/libs/bin/ruff check backend/ --fix
```

Ruff is not on PATH — use the full path above. Run before committing any Python changes. After `--fix`, manually resolve remaining `F841` errors, then confirm `All checks passed!`.

## Architecture

### API Layer

All REST endpoints are defined in a single file: `backend/backend/api.py`, using django-ninja. Endpoints are organized into routers by model (`stores`, `aisles`, `items`, `listitems`, `shoppinglists`, `version`) and mounted on the Django app at `/api/`. There is also a compound `ShoppingListFull` read endpoint that returns a fully assembled list (aisles + items) in one response.

**Data model relationships** (`backend/api/models.py`):
- `Store` → many `Aisle`, many `ShoppingList`
- `Aisle` → belongs to `Store`
- `Item` → optionally belongs to an `Aisle` (last used aisle)
- `ShoppingList` → belongs to `Store`
- `ListItem` → joins `Item` + `Aisle` + `ShoppingList`
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

## CI/CD & Versioning

Workflows run on **self-hosted GitHub Actions runners**. The pipeline chain on push to `main`:

1. **`deploy-docs.yml`** → publishes MkDocs API docs to GitHub Pages
2. **`versioning.yml`** → runs `scripts/versioning.sh` to auto-bump version (skipped for `docs:` and `ci:` commit prefixes). Updates version in both Dockerfiles, fixtures, `api.py`, `package.json`, `AppNavigation.vue`, and `App.vue`, then commits, tags, and creates a GitHub release.
3. **`docker.yml`** → builds and pushes to Docker Hub as `novanglus96/lenoreshop_frontend` and `novanglus96/lenoreshop_backend` (only if commit message contains the word `publish`)

**Version bump rules** (in commit message):
- Default → patch bump
- Include `[minor]`, `minor:`, or start with `minor` → minor bump
- Include `[major]`, `major:`, or start with `major` → major bump
- Prefix `docs:` or `ci:` → skip versioning and Docker publish entirely
- Include `publish` → trigger Docker Hub push

> Note: This project uses its own versioning script (`scripts/versioning.sh`), not semantic-release. The branch/PR conventions from the global CLAUDE.md still apply for branch protection and PR title linting.
