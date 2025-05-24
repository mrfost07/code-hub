import multiprocessing

# Absolute minimum worker configuration
workers = 1  # Single worker
threads = 4  # Use threads instead of multiple workers

# Type of worker processes
worker_class = 'gthread'  # Using threads instead of processes

# Reduce max simultaneous clients
worker_connections = 50

# Aggressive memory settings
max_requests = 250
max_requests_jitter = 25

# Reduce timeout
timeout = 29
keepalive = 2

# Memory optimization
worker_tmp_dir = '/dev/shm'
preload_app = True

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'warning'  # Reduce logging overhead

# Bind
bind = "0.0.0.0:8080"

# Process naming
proc_name = 'codehub'

# Graceful timeout
graceful_timeout = 30

# Memory limits (in MB)
limit_request_line = 1024
limit_request_fields = 50
limit_request_field_size = 4096

# Additional memory optimizations
forwarded_allow_ips = '*'
worker_disable_sendfile = True

# SSL (uncomment if using HTTPS directly through Gunicorn)
# keyfile = '/etc/ssl/private/your-keyfile.key'
# certfile = '/etc/ssl/certs/your-certfile.crt' 