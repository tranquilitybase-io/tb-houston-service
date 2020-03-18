LOGLEVEL=debug
NUMBER_OF_WORKERS=5
CONFIGFILE="config/local_development.py" DEBUG="${LOGLEVEL}" gunicorn --workers=${NUMBER_OF_WORKERS} --bind=0.0.0.0:3000 --log-level="${LOGLEVEL}" --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' app:connex_app
