#!/bin/bash
# Script for building, testing and running of mock images
ROOTDIR=$(pwd)

if [ "$1" == "pull" ]; then
  docker-compose -f docker_compose_mock.yml pull
  exit 0
fi

if [ "$1" == "down" ]; then
  docker-compose -f docker_compose_mock.yml down
  exit 0
fi

if [ "$1" == "kill" ]; then
  docker-compose -f docker_compose_mock.yml kill
  exit 0
fi

if [ "$1" == "prune" ]; then
  docker image prune -f
  exit 0
fi

if [ "$1" == "ps" ]; then
  docker-compose -f docker_compose_mock.yml ps
  exit 0
fi

if [ "$1" == "run" ]; then
  if [ -d venv ]; then
    source venv/bin/activate
  else
    echo "Please create venv directory first!" 
    exit 1
  fi
     

  python -m pip install codacy-coverage==1.3.11
  python -m pip install coverage==5.1

  nohup docker-compose -f docker_compose_mock.yml up 2>&1 &

  # Wait for system to be fully up
  start_epoch="$(date -u +%s)"
  elapsed_seconds=0
  until [ $(docker-compose -f docker_compose_mock.yml ps | grep Up | wc -l) -eq 3 ] || [ $elapsed_seconds -ge 600 ]
  do
    sleep 30
    docker-compose -f docker_compose_mock.yml ps 
    current_epoch="$(date -u +%s)"
    elapsed_seconds="$(($current_epoch-$start_epoch))"
    echo "Elapsed seconds: ${elapsed_seconds}"
  done

  cd "${ROOTDIR}/tests/"
  bash "${ROOTDIR}/tests/run_coverage.sh"

  cd "${ROOTDIR}"
  read  -n 1 -p "Press any key to shutdown? "
  docker-compose -f docker_compose_mock.yml down
  exit 0
fi

echo "Invalid or no arguement found!"
echo "Usage: $0 build | run | deploy | prune | pull | down | ps | kill"
