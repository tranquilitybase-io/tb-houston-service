#!/bin/bash
# Log Level Numeric value
# CRITICAL 50
# ERROR 40
# WARNING 30
# INFO 20
# DEBUG 10
# NOTSET 0

LOGLEVEL=10

NUMBER_OF_WORKERS=5
PORT=3000

if [ ! -z "${1}" ]; then
	PORT=${1}
fi

GCP_DAC_URL='localhost:3100' SQLALCHEMY_TRACK_MODIFICATIONS='False' SQLALCHEMY_ECHO='False' SQLALCHEMY_DATABASE_URI="${SQLALCHEMY_DATABASE_URI}" DEBUG="${LOGLEVEL}" gunicorn --workers="${NUMBER_OF_WORKERS}" --bind="0.0.0.0:${PORT}" --log-level="${LOGLEVEL}" --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' app:connex_app
