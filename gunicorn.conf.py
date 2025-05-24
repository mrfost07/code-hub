import multiprocessing

# Minimal worker configuration
workers = 1
worker_class = 'sync'
threads = 1

# Strict memory limits
max_requests = 100
max_requests_jitter = 10
worker_connections = 50

# Timeouts
timeout = 30
graceful_timeout = 30
keepalive = 2

# Logging
accesslog = None
errorlog = '-'
loglevel = 'warning'

# Bind
bind = "0.0.0.0:8080"

# Process naming
proc_name = 'codehub'

# Request limits - adjusted for normal HTTP traffic
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190

# Disable all extras
worker_tmp_dir = '/dev/shm'
sendfile = False
daemon = False
pidfile = None
umask = 0
user = None
group = None

# Preload for memory efficiency
preload_app = True

def on_starting(server):
    """Set memory limit to 512MB."""
    import resource
    mb = 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (512 * mb, 512 * mb))

# Additional memory optimizations
forwarded_allow_ips = '*'
worker_disable_sendfile = True

# SSL (uncomment if using HTTPS directly through Gunicorn)
# keyfile = '/etc/ssl/private/your-keyfile.key'
# certfile = '/etc/ssl/certs/your-certfile.crt' 