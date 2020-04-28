#!/bin/bash
export CODACY_PROJECT_TOKEN=${CODACY_PROJECT_TOKEN}
echo ${CODACY_PROJECT_TOKEN}
HOUSTON_SERVICE_URL=localhost:3000 coverage run venv/bin/pytest
coverage xml
coverage report
coverage html
bash <(wget -qO - https://coverage.codacy.com/get.sh) report --language Python --force-language -r coverage.xml
