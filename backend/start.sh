#!/bin/sh

set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting Gunicorn server..."
exec gunicorn app.main:app \
    -w 1 \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:${PORT:-8080} \
    --timeout 120
