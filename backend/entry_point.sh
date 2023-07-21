#!/bin/sh

echo Running as PID $PUID and GID $PGID.
echo Starting drg_backend ...
export DJANGO_SETTINGS_MODULE=backend.settings
chown $PUID:$PGID .  # for sqlite journal
su-exec python ./manage.py migrate
su-exec $PUID:$PGID gunicorn --bind 0.0.0.0:8000 backend.wsgi --access-logfile -