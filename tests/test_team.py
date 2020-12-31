import json
import logging
import os
from pprint import pprint

import requests

from tests import pytest_lib

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/team/"
plural_url = f"http://{HOUSTON_SERVICE_URL}/api/teams/"

# Additional headers.
headers = {"Content-Type": "application/json"}
id = 0


def typestest(resp):
    assert isinstance(resp["businessUnitId"], int)
    assert isinstance(resp["description"], str)
    assert isinstance(resp["id"], int)
    assert isinstance(resp["isActive"], bool)
    assert isinstance(resp["name"], str)
    pprint(resp)


def test_team():

    # Testing POST request
    id = post()
    # Testing PUT request
    put(id)
    # Testing DELETE request
    pytest_lib.logical_delete(url, str(id))
    # Testing DELETE Request Error
    pytest_lib.delete_error(url, "-1")
    # Testing GETALL request
    pytest_lib.get_all(plural_url)


def post():
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "accessRequestedById": 0,
        "businessUnitId": 1,
        "description": "Test Team",
        "id": 0,
        "isActive": True,
        "name": "Team-Test",
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    id = resp_json["id"]
    pprint(id)

    # Get Request to check Post has created item as expected
    resp = requests.get(url + str(id), headers=headers)

    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200
    assert resp_json["name"] == "Team-Test"
    assert resp_json["businessUnitId"] == 1
    assert resp_json["description"] == "Test Team"
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return id


def put(id):
    print("Put Tests")

    # Test Update Then get new value
    newpayload = {
        "accessRequestedById": 1,
        "businessUnitId": 1,
        "description": "Test Team Updated",
        "id": id,
        "isActive": False,
        "name": "Team-Test",
    }

    resp = requests.put(
        url + str(id), headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(url + str(id), headers=headers)
    resp_json = resp.json()
    id = resp_json["id"]

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["name"] == "Team-Test"
    assert resp_json["description"] == "Test Team Updated"
    assert resp_json["isActive"] is False

    typestest(resp_json)
