LOGLEVEL=debug
PORT=3000
FLASK_RUN_PORT="${PORT}"
CONFIGFILE="config/gcp_development.py" DEBUG="True" gunicorn --workers=5 --bind=0.0.0.0:3000 --log-level="${LOGLEVEL}" --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' app:connex_app
