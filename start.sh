#!/bin/bash

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
if [ ! -f media/dist/img/default-150x150.png ]; then
    cp static/dist/img/default-150x150.png media/dist/img/default-150x150.png
    chmod 644 media/dist/img/default-150x150.png
fi

# Copy favicon
echo "Setting up favicon..."
if [ ! -f staticfiles/dist/img/favicon.ico ]; then
    cp static/dist/img/favicon.ico staticfiles/dist/img/favicon.ico 2>/dev/null || :
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
    --log-level info \
    --error-logfile - \
    --access-logfile - \
    --capture-output \
    --enable-stdio-inheritance 