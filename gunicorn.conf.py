import multiprocessing

# Reduce number of workers for Railway's memory constraints
workers = 2  # Using fixed number instead of CPU-based calculation

# Type of worker processes
worker_class = 'sync'

# Reduce max simultaneous clients
worker_connections = 100

# Tune worker lifecycle to prevent memory leaks
max_requests = 500
max_requests_jitter = 50

# Reduce timeout
timeout = 30

# Memory optimization
worker_tmp_dir = '/dev/shm'
preload_app = True

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Bind
bind = "0.0.0.0:8080"

# Process naming
proc_name = 'codehub'

# Graceful timeout
graceful_timeout = 30

# Memory limits (in MB)
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# SSL (uncomment if using HTTPS directly through Gunicorn)
# keyfile = '/etc/ssl/private/your-keyfile.key'
# certfile = '/etc/ssl/certs/your-certfile.crt' 