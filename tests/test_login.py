import json
import os

import requests


def test_login():
    HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
    url = f"http://{HOUSTON_SERVICE_URL}/api/login"

    headers = {"Content-Type": "application/json"}

    payload = {"username": "test@testmail.com", "password": "string"}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate Response
    assert resp.status_code == 401
