import json
import logging
import os

import requests

LOG_LEVEL = logging.DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
key_values_url = f"http://{HOUSTON_SERVICE_URL}/api/keyValues/environment/"
url = f"http://{HOUSTON_SERVICE_URL}/api/lzmetadataEnv/"
# Additional headers.
headers = {"Content-Type": "application/json"}


def test_post():
    # Test POST Then GET
    # Body
    payload = [{"id": 0, "name": "test-env", "isActive": True}]
    # convert dict to json by json.dumps() for body data.

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 201

    # Get Request to check Post has created item as expected
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200

    for j in resp_json:
        print(j)
        if j["name"] == "test-env":
            assert j["isActive"] is True
    assert resp_headers["content-type"] == "application/json"


def test_get_all():
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200


def test_get_all_key_values():
    resp = requests.get(key_values_url, headers=headers)
    assert resp.status_code == 200
