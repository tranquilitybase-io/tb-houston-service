import os

import requests

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/keyValues/teamsByUserId/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def test_folder():
    get_all()


def get_all():
    oid = "1"
    resp = requests.get(url + oid, headers=headers)
    assert resp.status_code == 200
