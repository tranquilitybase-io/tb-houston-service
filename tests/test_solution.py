import requests
import json
import os
from pprint import pprint
from tests import pytest_lib


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/solution/"

# Additional headers.
headers = {"Content-Type": "application/json"}
id = 0


def typestest(resp):
    assert isinstance(resp["isActive"], bool)
    assert isinstance(resp["isFavourite"], bool)
    assert isinstance(resp["lastUpdated"], str)
    assert isinstance(resp["applications"], list)
    assert isinstance(resp["businessUnit"], str)
    assert isinstance(resp["ci"], str)
    assert isinstance(resp["cd"], str)
    assert isinstance(resp["costCentre"], str)
    assert isinstance(resp["description"], str)
    assert isinstance(resp["id"], int)
    assert isinstance(resp["name"], str)
    assert isinstance(resp["sourceControl"], str)
    assert isinstance(resp["teamId"], int)
    pprint(resp)


def test_solution():

    # Testing POST request
    oid = post()
    # Testing PUT request
    put(oid)
    # Testing DELETE request
    pytest_lib.logical_delete(url, oid)
    # Test GETALL test
    get_all()
    # Test GETONE test
    get_one(oid)


def post():
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "isActive": True,
        "businessUnit": "test",
        "cd": "test",
        "ci": "test",
        "costCentre": "test",
        "description": "test",
        "isFavourite": True,
        "id": 0,
        "name": "test",
        "sourceControl": "test",
        "teamId": 1,
        "environments": [1, 2, 3]
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = str(resp_json["id"])
    assert resp.status_code == 201

    # Get Request to check Post has created item as expected
    resp = requests.get(url + id, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200
    assert resp_json["name"] == "test"
    assert resp_json["businessUnit"] == "test"
    assert resp_json["description"] == "test"
    assert len(resp_json["environments"]) == 3
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return id


def put(id):
    print("Put Tests")

    # Test Update Then get new value
    newpayload = {
        "id": int(id),
        "isActive": True,
        "businessUnit": "test put",
        "cd": "test put",
        "ci": "test put",
        "costCentre": "test put",
        "description": "test put",
        "isFavourite": True,
        "name": "test put",
        "sourceControl": "test put",
        "environments": [1, 3]
    }

    resp = requests.put(
        url + id, headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(url + id, headers=headers)
    resp_json = resp.json()
    id = resp_json["id"]

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["name"] == "test put"
    assert resp_json["description"] == "test put"
    assert resp_json["businessUnit"] == "test put"
    assert resp_json["ci"] == "test put"
    assert resp_json["cd"] == "test put"
    assert resp_json["sourceControl"] == "test put"
    assert len(resp_json["environments"]) == 2
    typestest(resp_json)


def get_all():
    print("get_all Tests")

    url = f"http://{HOUSTON_SERVICE_URL}/api/solutions/"
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    # Validate Get All response
    assert resp.status_code == 200
    for r in resp_json:
        typestest(r)


def get_one(oid):
    print("get_one Test")

    resp = requests.get(url+str(oid), headers=headers)
    resp_json = resp.json()
    # Validate Get One response
    assert resp.status_code == 200
    typestest(resp_json)


if __name__ == "__main__":
    test_solution()
