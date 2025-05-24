#!/bin/bash

# Set memory limit for the entire process
ulimit -v 512000  # 512MB virtual memory limit

# Export Django settings
export DJANGO_SETTINGS_MODULE=swifthub.settings
export PYTHONUNBUFFERED=1

# Create necessary directories
echo "Creating media directories..."
mkdir -p media/dist/img
mkdir -p media/profile
mkdir -p staticfiles/dist/img

# Copy default images if they don't exist
echo "Setting up default images..."
if [ ! -f media/dist/img/default-avatar.jpg ]; then
    cp static/dist/img/default-150x150.png media/dist/img/default-avatar.jpg
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run migrations
echo "Running migrations..."
python manage.py migrate --no-input

# Start Gunicorn with strict settings
echo "Starting Gunicorn..."
exec gunicorn swifthub.wsgi:application \
    --config gunicorn.conf.py \
    --workers 1 \
    --threads 1 \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --log-level info \
    --error-logfile - \
    --access-logfile - \
    --capture-output \
    --enable-stdio-inheritance 