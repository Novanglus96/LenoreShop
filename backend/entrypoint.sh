#!/bin/sh

# Wait for external database if configured
if [ "$SQL_ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Waiting for PostgreSQL at $SQL_HOST:$SQL_PORT..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do sleep 0.1; done
    echo "PostgreSQL is ready."
elif [ "$SQL_ENGINE" = "django.db.backends.mysql" ]; then
    echo "Waiting for MySQL at $SQL_HOST:$SQL_PORT..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do sleep 0.1; done
    echo "MySQL is ready."
else
    echo "Using SQLite — no external database required."
fi

# Django setup
cd /home/app/web || exit 1
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py loaddata version

if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

# Build supervisord config
SUPERVISOR_CONF=/tmp/supervisord.conf

cat > "$SUPERVISOR_CONF" << 'EOF'
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0
pidfile=/tmp/supervisord.pid

[program:nginx]
command=nginx -g "daemon off;"
autostart=true
autorestart=true
priority=10
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:daphne]
command=daphne -b 127.0.0.1 -p 8000 backend.asgi:application
directory=/home/app/web
autostart=true
autorestart=true
priority=20
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
EOF

# Add Celery worker only if Redis is configured
if [ -n "$REDIS_URL" ]; then
    echo "Redis configured — enabling cache and background worker."
    cat >> "$SUPERVISOR_CONF" << 'EOF'

[program:celery]
command=celery -A backend worker --loglevel=info
directory=/home/app/web
autostart=true
autorestart=true
priority=30
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
EOF
else
    echo "No REDIS_URL — starting without cache or background worker."
fi

exec supervisord -c "$SUPERVISOR_CONF"
