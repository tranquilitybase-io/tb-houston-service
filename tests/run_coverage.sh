#!/bin/bash
if [ -z "${CODACY_PROJECT_TOKEN}" ]; then
  echo "CODACY_PROJECT_TOKEN is not set!"
  exit 1
fi
export CODACY_PROJECT_TOKEN=${CODACY_PROJECT_TOKEN}
export SQLALCHEMY_ECHO="True"
export SQLALCHEMY_TRACK_MODIFICATIONS="True"
python -m pip install pytest
python -m pip install codacy-coverage==1.3.11
python -m pip install coverage==5.1
HOUSTON_SERVICE_URL=0.0.0.0:3000 coverage run "$(which pytest)"
coverage xml
coverage report
coverage html
bash <(wget -qO - https://coverage.codacy.com/get.sh) report --language Python --force-language -r coverage.xml --project-token "${CODACY_PROJECT_TOKEN}"
