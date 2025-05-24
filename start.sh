#!/bin/bash

# Set memory limit for the entire process
ulimit -v 512000  # 512MB virtual memory limit

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Start Gunicorn with strict settings
exec gunicorn swifthub.wsgi:application \
    --config gunicorn.conf.py \
    --workers 1 \
    --threads 1 \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --max-requests 100 \
    --max-requests-jitter 10 \
    --log-level warning 