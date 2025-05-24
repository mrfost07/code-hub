import multiprocessing

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Type of worker processes
worker_class = 'sync'

# Maximum number of simultaneous clients
worker_connections = 1000

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Timeout for worker processes
timeout = 30

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Bind
bind = "0.0.0.0:8080"

# Process naming
proc_name = 'codehub'

# SSL (uncomment if using HTTPS directly through Gunicorn)
# keyfile = '/etc/ssl/private/your-keyfile.key'
# certfile = '/etc/ssl/certs/your-certfile.crt' 