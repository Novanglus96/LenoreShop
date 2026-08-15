#!/usr/bin/env bash
# sync-live-to-sandbox.sh
#
# Copies live application data and config to the sandbox host, then starts
# the sandbox stack using the rc image.
#
# Designed to be reusable across projects — edit the Configuration block below.
#
# Prerequisites (on the machine running this script):
#   - SSH key access to both LIVE_HOST and SANDBOX_HOST
#   - docker CLI on both remote hosts
#   - The project's docker-compose-sandbox.yml in the repo root (gitignored)

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────

PROJECT_NAME="lenoreshop"
SANDBOX_COMPOSE_FILE="docker-compose-sandbox.yml"   # path relative to repo root

# Live host
LIVE_HOST="chaos.danielleandjohn.lan"
LIVE_SSH_PORT="1996"
LIVE_SSH_USER="jadams"
LIVE_COMPOSE_DIR="/Data/container/services/apps/lenoreshop"
LIVE_DB_CONTAINER="lenoreshop_db"

# Sandbox host
SANDBOX_HOST="hera.danielleandjohn.lan"
SANDBOX_SSH_PORT="22"
SANDBOX_SSH_USER="jadams"
SANDBOX_COMPOSE_DIR="/home/jadams/sand-box/lenoreshop"

# Docker named volumes to copy from live (space-separated; postgres_data is
# handled via pg_dump/restore so list only file-based volumes here)
# NOTE: These are the volume names as they exist on the live host.
#       Run `docker volume ls` on the live host to confirm names.
LIVE_VOLUMES_TO_COPY="lenoreshop_media_volume"

# Corresponding volume names on the sandbox (must match docker-compose-sandbox.yml)
# Order must match LIVE_VOLUMES_TO_COPY
SANDBOX_VOLUME_NAMES="lenoreshop_media"

# ── Helpers ────────────────────────────────────────────────────────────────────

LIVE_SSH="ssh -p ${LIVE_SSH_PORT} ${LIVE_SSH_USER}@${LIVE_HOST}"
SANDBOX_SSH="ssh -p ${SANDBOX_SSH_PORT} ${SANDBOX_SSH_USER}@${SANDBOX_HOST}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

log()  { echo "[$(date +%H:%M:%S)] $*"; }
step() { echo; echo "──────────────────────────────────────────"; log "STEP: $*"; }

# ── Resolve script location (repo root) ───────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ── Step 1: Read DB credentials from live .env ────────────────────────────────
step "Reading credentials from live .env"
ENV_CONTENT=$(${LIVE_SSH} "cat ${LIVE_COMPOSE_DIR}/.env")
SQL_USER=$(echo "${ENV_CONTENT}" | grep '^SQL_USER=' | cut -d= -f2 | tr -d '[:space:]')
SQL_DATABASE=$(echo "${ENV_CONTENT}" | grep '^SQL_DATABASE=' | cut -d= -f2 | tr -d '[:space:]')
log "DB: ${SQL_DATABASE}  User: ${SQL_USER}"

# ── Step 2: Prepare sandbox directory ────────────────────────────────────────
step "Preparing sandbox directory on ${SANDBOX_HOST}"
${SANDBOX_SSH} "mkdir -p ${SANDBOX_COMPOSE_DIR}/backup"

# ── Step 3: Sync .env from live to sandbox ────────────────────────────────────
step "Copying .env from live to sandbox"
${LIVE_SSH} "cat ${LIVE_COMPOSE_DIR}/.env" | \
  ${SANDBOX_SSH} "cat > ${SANDBOX_COMPOSE_DIR}/.env"
# Apply sandbox-specific overrides (replace existing keys or append if absent)
${SANDBOX_SSH} "
  set_env() {
    local key=\"\$1\" val=\"\$2\" file=\"\$3\"
    if grep -q \"^\${key}=\" \"\$file\"; then
      sed -i \"s|^\${key}=.*|\${key}=\${val}|\" \"\$file\"
    else
      echo \"\${key}=\${val}\" >> \"\$file\"
    fi
  }
  set_env DJANGO_ALLOWED_HOSTS 'sandbox.danielleandjohn.love' ${SANDBOX_COMPOSE_DIR}/.env
  set_env CSRF_TRUSTED_ORIGINS 'https://sandbox.danielleandjohn.love' ${SANDBOX_COMPOSE_DIR}/.env
  set_env SQL_ENGINE 'django.db.backends.postgresql' ${SANDBOX_COMPOSE_DIR}/.env
  set_env SQL_HOST 'db' ${SANDBOX_COMPOSE_DIR}/.env
  set_env REDIS_URL 'redis://redis:6379/0' ${SANDBOX_COMPOSE_DIR}/.env
"
log ".env copied and sandbox overrides applied"

# ── Step 4: Deploy sandbox docker-compose file ────────────────────────────────
step "Deploying ${SANDBOX_COMPOSE_FILE} to sandbox"
scp -P "${SANDBOX_SSH_PORT}" \
    "${REPO_ROOT}/${SANDBOX_COMPOSE_FILE}" \
    "${SANDBOX_SSH_USER}@${SANDBOX_HOST}:${SANDBOX_COMPOSE_DIR}/docker-compose.yml"
log "docker-compose.yml deployed"

# ── Step 5: Dump PostgreSQL from live ─────────────────────────────────────────
step "Dumping PostgreSQL database '${SQL_DATABASE}' from live"
DUMP_FILENAME="${PROJECT_NAME}_db_${TIMESTAMP}.sql.gz"
${LIVE_SSH} "
  docker exec ${LIVE_DB_CONTAINER} \
    pg_dump -U ${SQL_USER} ${SQL_DATABASE} | gzip > /tmp/${DUMP_FILENAME}
"
log "Dump created: /tmp/${DUMP_FILENAME}"

# ── Step 6: Transfer dump to sandbox ─────────────────────────────────────────
step "Transferring database dump to sandbox"
${LIVE_SSH} "cat /tmp/${DUMP_FILENAME}" | \
  ${SANDBOX_SSH} "cat > ${SANDBOX_COMPOSE_DIR}/backup/${DUMP_FILENAME}"
${LIVE_SSH} "rm -f /tmp/${DUMP_FILENAME}"
log "Dump transferred to ${SANDBOX_COMPOSE_DIR}/backup/${DUMP_FILENAME}"

# ── Step 7: Copy named volumes ────────────────────────────────────────────────
read -ra LIVE_VOLS <<< "${LIVE_VOLUMES_TO_COPY}"
read -ra SANDBOX_VOLS <<< "${SANDBOX_VOLUME_NAMES}"
for i in "${!LIVE_VOLS[@]}"; do
  LIVE_VOL="${LIVE_VOLS[$i]}"
  SANDBOX_VOL="${SANDBOX_VOLS[$i]}"
  step "Copying Docker volume: ${LIVE_VOL} → ${SANDBOX_VOL}"
  VOLUME_ARCHIVE="${LIVE_VOL}_${TIMESTAMP}.tar.gz"
  ${LIVE_SSH} "
    docker run --rm \
      -v ${LIVE_VOL}:/data \
      alpine tar czf - -C /data .
  " | ${SANDBOX_SSH} "cat > /tmp/${VOLUME_ARCHIVE}"
  log "Volume archive transferred"

  # Restore volume on sandbox (creates volume if it doesn't exist)
  ${SANDBOX_SSH} "
    docker volume create ${SANDBOX_VOL} 2>/dev/null || true
    docker run --rm \
      -v ${SANDBOX_VOL}:/data \
      -v /tmp:/backup \
      alpine sh -c 'rm -rf /data/* && tar xzf /backup/${VOLUME_ARCHIVE} -C /data'
    rm -f /tmp/${VOLUME_ARCHIVE}
  "
  log "Volume ${SANDBOX_VOL} restored on sandbox"
done

# ── Step 8: Start sandbox stack and restore database ─────────────────────────
step "Starting sandbox stack"
${SANDBOX_SSH} "
  cd ${SANDBOX_COMPOSE_DIR}
  docker compose down --remove-orphans 2>/dev/null || true
  docker compose pull --quiet
  docker compose up -d db
"
log "Waiting for Postgres to be ready..."
${SANDBOX_SSH} "
  cd ${SANDBOX_COMPOSE_DIR}
  for i in \$(seq 1 30); do
    docker compose exec -T db pg_isready -U ${SQL_USER} -d ${SQL_DATABASE} >/dev/null 2>&1 && break
    sleep 2
  done
"

step "Restoring database on sandbox"
${SANDBOX_SSH} "
  cd ${SANDBOX_COMPOSE_DIR}
  # Terminate existing connections and drop/recreate the database
  docker compose exec -T db psql -U ${SQL_USER} -d postgres -c \
    \"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='${SQL_DATABASE}' AND pid <> pg_backend_pid();\"
  docker compose exec -T db psql -U ${SQL_USER} -d postgres -c \
    \"DROP DATABASE IF EXISTS ${SQL_DATABASE};\"
  docker compose exec -T db psql -U ${SQL_USER} -d postgres -c \
    \"CREATE DATABASE ${SQL_DATABASE};\"
  gunzip -c backup/${DUMP_FILENAME} | \
    docker compose exec -T db psql -U ${SQL_USER} -d ${SQL_DATABASE}
  rm -f backup/${DUMP_FILENAME}
"
log "Database restored"

step "Starting remaining sandbox services"
${SANDBOX_SSH} "
  cd ${SANDBOX_COMPOSE_DIR}
  docker compose up -d
"

log "Done! Sandbox is running at http://${SANDBOX_HOST}:8080"
