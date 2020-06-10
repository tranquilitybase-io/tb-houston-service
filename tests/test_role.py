import requests
import json
import logging
import os
from pprint import pprint
from tests import pytest_lib


LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/role/"
plural_url = f"http://{HOUSTON_SERVICE_URL}/api/roles/"

# Additional headers.
headers = {"Content-Type": "application/json"}
id = 0


def test_teammember():

    # Testing POST request
    id = post()
    # Testing PUT request
    put(id)
    # Test GET all teammbers with parameters
    get_all_params()
    # Testing DELETE request
    pytest_lib.delete(url, str(id))
    # Testing DELETE Request Error
    pytest_lib.delete_error(url, "-1")
    # Testing GETALL request
    pytest_lib.get_all(plural_url)


def typestest(resp):
    assert isinstance(resp["id"], int)
    assert isinstance(resp["name"], str)
    assert isinstance(resp["cloudIdentityGroup"], str)
    assert isinstance(resp["description"], str)
    pprint(resp)


def post():
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "id": 0,
        "cloudIdentityGroup": "test@gftdevgcp.com",
        "description": "eagle console test role",
        "name": "test",
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    id = str(resp_json["id"])

    # Get Request to check Post has created item as expected
    resp = requests.get(url + id, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200
    assert resp_json["name"] == "test"
    assert resp_json["cloudIdentityGroup"] == "test@gftdevgcp.com"
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return id


def put(id):
    print("Put Tests")

    # Test Update Then get new value
    newpayload = {
        "id": int(id),
        "cloudIdentityGroup": "test-change@gftdevgcp.com",
        "description": "eagle console test role changed",
        "name": "test",
    }

    resp = requests.put(
        url + id, headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(url + id, headers=headers)
    resp_json = resp.json()

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["description"] == "eagle console test role changed"
    assert resp_json["cloudIdentityGroup"] == "test-change@gftdevgcp.com"

    typestest(resp_json)


def get_all_params():

    resp = requests.get(plural_url, headers=headers)
    assert resp.status_code == 200
