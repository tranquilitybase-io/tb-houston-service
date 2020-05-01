#!/bin/bash
if [ -z "${CODACY_PROJECT_TOKEN}" ]; then
  echo "CODACY_PROJECT_TOKEN is not set!"
  exit 1
fi
export CODACY_PROJECT_TOKEN=${CODACY_PROJECT_TOKEN}
python -m pip install pytest
HOUSTON_SERVICE_URL=localhost:3000 coverage run venv/bin/pytest
coverage xml
coverage report
coverage html
bash <(wget -qO - https://coverage.codacy.com/get.sh) report --language Python --force-language -r coverage.xml --project-token "${CODACY_PROJECT_TOKEN}"
