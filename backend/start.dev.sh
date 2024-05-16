#!/bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input
#python manage.py collectstatic --no-input
#python manage.py createcachetable

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    (python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL) ||
        true
fi

python manage.py loaddata django_admin_theme_shop

python manage.py runserver 0.0.0.0:8001
