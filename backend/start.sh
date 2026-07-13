#!/bin/sh
# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start server
echo "Starting Gunicorn server..."
exec gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
