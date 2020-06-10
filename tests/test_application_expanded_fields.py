import requests
import os
from pprint import pformat
from tests import pytest_lib


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]

# Additional headers.
headers = {"Content-Type": "application/json"}
id = 0


def test_main():
    get_all()
    get()


def get_all():
    print("get_all Tests")

    url = f"http://{HOUSTON_SERVICE_URL}/api/applications/"
    resp = requests.get(url, headers=headers)
    # Validate Get All response
    assert resp.status_code == 200

    resp_json = resp.json()
    for resp_j in resp_json:
        pytest_lib.typestest_application(resp_j)


def get():
    print("get Tests")

    url = f"http://{HOUSTON_SERVICE_URL}/api/application/"
    resp = requests.get(url+"1", headers=headers)
    # Validate Get All response
    assert resp.status_code == 200

    resp_json = resp.json()
    print(f"resp_json: {pformat(resp_json)}")
    pytest_lib.typestest_application(resp_json)


if __name__ == "__main__":
    test_main()
