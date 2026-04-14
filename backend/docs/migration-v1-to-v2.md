# Migrating from v1 to v2 (Single Container)

Starting with **v1.7.0**, LenoreShop ships as a single self-contained Docker image instead of four separate containers (frontend, backend, nginx, db). This guide walks through migrating an existing v1 installation to the new architecture.

---

## What Changed

| | v1 (old) | v2 (new) |
|---|---|---|
| **Containers** | `lenoreshop_frontend`, `lenoreshop_backend`, `lenoreshop_nginx`, `lenoreshop_db` | Single `lenoreshop` container |
| **Database** | PostgreSQL required | SQLite (default) or PostgreSQL/MySQL (optional) |
| **Redis** | Not included | Optional (enable with `REDIS_URL`) |
| **Image** | `novanglus96/lenoreshop_frontend` + `novanglus96/lenoreshop_backend` | `novanglus96/lenoreshop` |
| **Media volume** | `media_volume` | `lenoreshop_media` |
| **Static volume** | `static_volume` | `lenoreshop_static` (rebuilt automatically) |

---

## Before You Start

Back up your data first.

```bash
# Export PostgreSQL database
docker exec lenoreshop_db pg_dump -U $SQL_USER $SQL_DATABASE > lenoreshop_backup.sql

# Export media files
docker run --rm \
  -v $(docker inspect lenoreshop_backend --format '{{range .Mounts}}{{if eq .Destination "/home/app/web/mediafiles"}}{{.Name}}{{end}}{{end}}'):/data \
  alpine tar czf - -C /data . > lenoreshop_media_backup.tar.gz

echo "Backup complete."
```

---

## Migration Paths

Choose based on your preferred database for v2:

- **[Path A — Keep PostgreSQL](#path-a-keep-postgresql)**: Migrate existing data, keep PostgreSQL
- **[Path B — Switch to SQLite](#path-b-switch-to-sqlite)**: Simpler setup, migrate data via Django fixtures

---

## Path A: Keep PostgreSQL

### Step 1: Stop the old stack

```bash
docker compose down
# Do NOT use --volumes — this preserves your data
```

### Step 2: Get the new compose file

Download [`docker-compose-full.yml`](https://github.com/Novanglus96/LenoreShop/blob/main/docker-compose-full.yml) and save it as `docker-compose.yml` in your deployment directory.

### Step 3: Update your `.env`

The v2 image reads the same database variables but adds new optional ones. Update your `.env`:

```env
# Required
DEBUG=0
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=your-host-or-ip
CSRF_TRUSTED_ORIGINS=https://your-domain

# Database (keep your existing values)
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=lenoreshop
SQL_USER=lenoreshopuser
SQL_PASSWORD=somepassword
SQL_HOST=db
SQL_PORT=5432

# Optional: Redis (enables caching and background worker)
# REDIS_URL=redis://redis:6379/0

# Optional: exposed port (default 7000)
# APP_PORT=7000

# Optional: superuser created on first run
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=changeme
```

**Remove** any old v1-only variables (`DATABASE=postgres` is no longer used).

### Step 4: Migrate the media volume

The media volume was renamed from `media_volume` to `lenoreshop_media`. Copy its contents across:

```bash
# Determine the old volume name (usually <project>_media_volume)
docker volume ls | grep media

# Copy from old volume to new
docker volume create lenoreshop_media
docker run --rm \
  -v <old_media_volume>:/source \
  -v lenoreshop_media:/dest \
  alpine sh -c "cp -a /source/. /dest/"
```

> Static files (`static_volume`) do **not** need migrating — they are regenerated automatically by `collectstatic` on container startup.

### Step 5: Start the new stack

```bash
docker compose up -d
```

The container will run migrations and start serving automatically. Access the app at `http://your-host:7000` (or your configured `APP_PORT`).

---

## Path B: Switch to SQLite

### Step 1: Export data from PostgreSQL

```bash
# Export all application data as Django fixtures
docker exec lenoreshop_backend \
  python manage.py dumpdata \
    --exclude auth.permission \
    --exclude contenttypes \
    --indent 2 > lenoreshop_data.json
```

### Step 2: Stop the old stack

```bash
docker compose down
```

### Step 3: Get the new compose file

Download [`docker-compose-prod.yml`](https://github.com/Novanglus96/LenoreShop/blob/main/docker-compose-prod.yml) and save it as `docker-compose.yml` in your deployment directory.

### Step 4: Create your `.env`

```env
DEBUG=0
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=your-host-or-ip
CSRF_TRUSTED_ORIGINS=https://your-domain
APP_PORT=7000
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=changeme
```

No database variables are needed — SQLite is the default.

### Step 5: Start the stack and load data

```bash
docker compose up -d

# Wait for the container to finish startup (~15s), then load fixtures
docker exec lenoreshop python manage.py loaddata /path/to/lenoreshop_data.json
```

### Step 6: Migrate media files

```bash
docker run --rm \
  -v <old_media_volume>:/source \
  -v lenoreshop_media:/dest \
  alpine sh -c "cp -a /source/. /dest/"
```

---

## Verify the Migration

1. Open the app in your browser
2. Confirm your stores, lists, and items are present
3. Check the version shown in the nav bar matches the release version

---

## Rollback

If anything goes wrong, your old containers and volumes are still intact (as long as you didn't run `docker compose down --volumes`). Restore your original `docker-compose.yml` and start the old stack:

```bash
docker compose up -d
```

Your data was never modified — the old volumes are untouched.

---

## Removing Old Images

Once you've confirmed the migration is successful, clean up the old images:

```bash
docker image rm novanglus96/lenoreshop_frontend novanglus96/lenoreshop_backend
```
