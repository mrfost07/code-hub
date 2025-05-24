#!/bin/bash

# Set memory limit for the entire process
ulimit -v 512000  # 512MB virtual memory limit

# Export Django settings
export DJANGO_SETTINGS_MODULE=swifthub.settings
export PYTHONUNBUFFERED=1

# Create necessary directories with proper permissions
echo "Creating and setting up directories..."
mkdir -p media/profile
mkdir -p media/dist/img
mkdir -p staticfiles/dist/img
chmod -R 755 media
chmod -R 755 staticfiles

# Ensure default avatar exists
echo "Setting up default avatar..."
if [ ! -f media/dist/img/default-avatar.jpg ]; then
    cp static/dist/img/default-150x150.png media/dist/img/default-avatar.jpg
    chmod 644 media/dist/img/default-avatar.jpg
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