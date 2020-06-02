#!/bin/bash
export SQLALCHEMY_ECHO="True"
export SQLALCHEMY_TRACK_MODIFICATIONS="True"
python -m pip install pytest
HOUSTON_SERVICE_URL=0.0.0.0:3000 "$(which pytest)" -p no:warnings
