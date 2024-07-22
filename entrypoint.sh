#!/bin/bash

set -e

function wait_for_services {
    wait-for-it \
        --timeout 60 \
        --service "$POSTGRES_HOST:$POSTGRES_PORT" \
        -- echo "Services are up"
}

function init {
  echo "Run initialization scripts"
  python manage.py migrate
  python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
}

case "$1" in
    'runserver')
        wait_for_services
        init
        echo "Starting django development server"
        python manage.py collectstatic --no-input --link
        python manage.py runserver 0.0.0.0:8000
    ;;
    'test')
        echo "Running tests"
        wait_for_services
        python manage.py makemigrations --dry-run --check || echo "You have changes in models with no migrations"
        python manage.py collectstatic --no-input --link
        pytest tests/ -n auto -vv --disable-warnings
    ;;
    *)
        exec "$@"
    ;;
esac
