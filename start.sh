#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.vercel}"

echo "==> Running collectstatic..."
python manage.py collectstatic --noinput --clear

echo "==> Starting server..."
exec "$@"
