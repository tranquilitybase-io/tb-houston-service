import requests
import json
import os
from pprint import pprint
from tests import pytest_lib


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/activator/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def typestest(resp):
    assert isinstance(resp["id"], int)
    assert isinstance(resp["isActive"], bool)
    assert isinstance(resp["isFavourite"], bool)
    assert isinstance(resp["lastUpdated"], str)
    assert (
        isinstance(resp["accessRequestedById"], int)
        or resp["accessRequestedById"] is None
    )
    assert (
        isinstance(resp["accessRequestedBy"], dict) or resp["accessRequestedBy"] is None
    )
    assert isinstance(resp["activator"], str)
    assert isinstance(resp["activatorLink"], str)
    assert isinstance(resp["gitRepoUrl"], str)
    assert isinstance(resp["apiManagement"], list)
    assert isinstance(resp["available"], bool)
    assert isinstance(resp["billing"], str)
    assert isinstance(resp["businessUnit"], dict)
    assert isinstance(resp["category"], str)
    assert isinstance(resp["cd"], list)
    assert isinstance(resp["description"], str)
    assert isinstance(resp["envs"], list)
    assert isinstance(resp["hosting"], list)
    assert isinstance(resp["platforms"], list)
    assert isinstance(resp["regions"], list)
    assert isinstance(resp["sensitivity"], str)
    assert isinstance(resp["serverCapacity"], int)
    assert isinstance(resp["source"], str)
    assert isinstance(resp["sourceControl"], dict)
    assert isinstance(resp["status"], str)
    assert isinstance(resp["technologyOwner"], str)
    assert isinstance(resp["technologyOwnerEmail"], str)
    assert isinstance(resp["type"], str)
    assert isinstance(resp["userCapacity"], int)
    pprint(resp)


def test_activators():
    # Testing POST request
    resp_json = post()
    oid = str(resp_json["id"])
    pprint(f"oid: {oid}")
    # Testing Set Activator Status
    set_activator_status(resp_json["id"])
    # Testing PUT request
    put(oid)
    # Testing DELETE request
    get_one(oid)
    # Test GET Activator Meta
    pytest_lib.logical_delete(url, oid)
    # Testing GETALL request
    get_all()
    # Testing GETONE request
    get_meta()
    # Test Get Activator Categories
    get_categories()


def post():
    # Test POST Then GET
    # Body
    payload = {
        "accessRequestedById": 1,
        "activator": "test-activator",
        "activatorLink": "test-post-",
        "gitRepoUrl": "test-post-",
        "apiManagement": [
            "test-post-",
            "test-post-1",
            "test-post-2",
            "test-post-3",
            "test-post-4",
            "test-post-5",
        ],
        "available": True,
        "billing": "test-post-",
        "businessUnitId": 1,
        "category": "test-post-",
        "cd": [5, 6],
        "ci": [3, 5],
        "description": "test-post-test-post-test-post-test-post-test-post-test-post-test-post-test-post-",
        "envs": [1, 2],
        "hosting": [
            "test-post-1",
            "test-post-2",
            "test-post-3",
            "test-post-4",
            "test-post-5",
        ],
        "id": 0,
        "lastUpdated": "test-post-",
        "name": "test-post-",
        "platforms": [
            "test-post-1",
            "test-post-2",
            "test-post-3",
            "test-post-4",
            "test-post-5",
            "test-post-6",
        ],
        "regions": [
            "test-post-1",
            "test-post-2",
            "test-post-3",
            "test-post-4",
            "test-post-5",
        ],
        "sensitivity": "test-post-",
        "serverCapacity": 999999999,
        "source": "test-post-",
        "sourceControlId": 3,
        "status": "Available",
        "technologyOwner": "test-post-",
        "technologyOwnerEmail": "test-post-",
        "type": "test-post-",
        "userCapacity": 999999999,
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    pprint(f"resp_json: {resp_json}")
    assert resp.status_code == 201
    assert resp_json["activator"] == "test-activator"
    
    # Validate CI 
    ci_list = resp_json["ci"]
    assert ci_list[0]["id"] == 3
    isinstance(ci_list[0]["value"], str)
    assert ci_list[1]["id"] == 5
    isinstance(ci_list[1]["value"], str)

    # Validate CD
    cd_list = resp_json["cd"]
    assert cd_list[0]["id"] == 5
    isinstance(cd_list[0]["value"], str)
    assert cd_list[1]["id"] == 6
    isinstance(cd_list[1]["value"], str)

    # Validate Envs
    envs_list = resp_json["envs"]
    assert envs_list[0]["id"] == 1
    isinstance(envs_list[0]["name"], str)
    assert envs_list[1]["id"] == 2
    isinstance(envs_list[1]["name"], str)

    oid = resp_json["id"]
    print(f"oid: {oid}")

    resp = requests.get(url + str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers

    # Validate response
    assert resp.status_code == 200
    assert resp_json["activator"] == "test-activator"
    assert resp_headers["content-type"] == "application/json"
    assert isinstance(resp_json["accessRequestedById"], int)
    assert isinstance(resp_json["accessRequestedBy"], dict)
    typestest(resp_json)
    return resp_json


def set_activator_status(oid):

    url = url = f"http://{HOUSTON_SERVICE_URL}/api/setactivatorstatus/"
    payload = {"accessRequestedById": 1, "id": oid, "status": "Locked"}
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["id"] == oid
    assert resp_json["status"] == "Locked"

    payload = {"id": oid, "status": "Available"}
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["id"] == oid
    assert resp_json["status"] == "Available"


def put(oid):

    # Test Update Then get new value
    newpayload = {
        "activator": "new-test-activator",
        "accessRequestedById": 2,
        "activatorLink": "test-put-",
        "gitRepoUrl": "test-put-",
        "apiManagement": ["test-put-6", "test-put-7", "test-put-8"],
        "available": False,
        "billing": "billing",
        "businessUnitId": 1,
        "category": "category",
        "cd": [3, 4],
        "ci": [1, 2],
        "description": "TheQuickBrownFoxJumpedOverTheLazyDogs",
        "envs": [2],
        "hosting": [
            "test-put-11",
            "test-put-22",
            "test-put-33",
            "test-put-44",
            "test-put-55",
        ],
        "lastUpdated": "fredbloggs",
        "name": "mynewactivatortest",
        "platforms": [
            "test-put-101",
            "test-put-102",
            "test-put-103",
            "test-put-104",
            "test-put-105",
            "test-put-106",
        ],
        "regions": [
            "test-put-101",
            "test-put-210",
            "test-put-310",
            "test-put-410",
            "test-put-510",
        ],
        "sensitivity": "confidential",
        "serverCapacity": 5,
        "source": "original",
        "sourceControlId": 1,
        "status": "NotAvailable",
        "technologyOwner": "me",
        "technologyOwnerEmail": "me@me.com",
        "type": "best",
        "userCapacity": 10,
    }
    resp = requests.put(
        url + oid, headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(url + oid, headers=headers)
    resp_json = resp.json()
    oid = resp_json["id"]
    # Validate CI
    ci_list = resp_json["ci"]
    assert ci_list[0]["id"] == 1
    isinstance(ci_list[0]["value"], str)
    assert ci_list[1]["id"] == 2
    isinstance(ci_list[1]["value"], str)

    # Validate CD
    cd_list = resp_json["cd"]
    assert cd_list[0]["id"] == 3
    isinstance(cd_list[0]["value"], str)
    assert cd_list[1]["id"] == 4
    isinstance(cd_list[1]["value"], str)

    # Validate Envs
    envs_list = resp_json["envs"]
    assert envs_list[0]["id"] == 2
    isinstance(envs_list[0]["name"], str)

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["activator"] == "new-test-activator"
    assert resp_json["businessUnitId"] == 1
    typestest(resp_json)


def get_all():

    geturl = f"http://{HOUSTON_SERVICE_URL}/api/activators/"
    resp = requests.get(geturl, headers=headers)
    resp_json = resp.json()
    # print(resp_json)
    assert resp.status_code == 200
    for j in resp_json:
        typestest(j)


def get_one(oid):
    print(f"get_one Test: {oid}")

    resp = requests.get(url + str(oid), headers=headers)
    resp_json = resp.json()
    # Validate Get One response
    assert resp.status_code == 200
    typestest(resp_json)


def get_meta():

    url = f"http://{HOUSTON_SERVICE_URL}/api/activator_meta/"
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    count = resp_json["count"]
    # Validate response
    assert resp.status_code == 200
    assert count >= 0


def get_categories():

    url = f"http://{HOUSTON_SERVICE_URL}/api/activatorcategories/"
    resp = requests.get(url, headers=headers)
    pprint(resp.json())
    # Validate response
    assert resp.status_code == 200


if __name__ == "__main__":
    test_activators()
