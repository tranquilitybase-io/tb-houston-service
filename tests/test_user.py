import requests
import json
import logging
import os
from pprint import pprint
from tests import pytest_lib

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/user/"
urls = f"http://{HOUSTON_SERVICE_URL}/api/users/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def typestest(resp):
    assert isinstance(resp["id"], int)
    assert isinstance(resp["email"], str)
    assert isinstance(resp["firstName"], str)
    assert isinstance(resp["lastName"], str)
    assert isinstance(resp["isAdmin"], bool)
    assert isinstance(resp["isActive"], bool)
    assert isinstance(resp["showWelcome"], bool)
    pprint(resp)


def test_user():
    # Testing POST request
    oid = post()
    # Testing PUT request
    put(oid)
    # Testing logical DELETE request
    pytest_lib.logical_delete(url, str(oid))
    # Testing DELETE Request Error
    pytest_lib.delete_error(url, str(-1))
    # Testing GETALL request
    pytest_lib.get_all(urls)

def post():
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "firstName": "test",
        "lastName": "test",
        "email": "test_email_account",
        "isActive": True
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(f"resp_json: {resp_json}")    
    assert resp.status_code == 201
    oid = resp_json["id"]

    # Get Request to check Post has created item as expected
    resp = requests.get(url + str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers

    print(f"resp_json: {resp_json}")
    # Validate response
    assert resp.status_code == 200
    assert resp_json["firstName"] == "test"
    assert resp_json["lastName"] == "test"
    assert resp_json["email"] == "test_email_account"
    assert resp_json["isActive"] == True
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return oid


def put(oid):
    print("Put Tests")

    # Test Update Then get new value
    newpayload = {
        "id": oid,
        "firstName": f"test{str(oid)}",
        "lastName": "test",
        "email": f"test{str(oid)}@test.com",
        "isActive": False,
        "showWelcome": True
    }

    resp = requests.put(
        url + str(oid), headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Get Request to get updated values
    resp = requests.get(url + str(oid), headers=headers)
    resp_json = resp.json()    
    print(f"resp_json: {resp_json}")    

    # Validate update/Put response
    assert resp.status_code == 200

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["firstName"] == f"test{str(oid)}"
    assert resp_json["lastName"] == "test"    
    assert resp_json["isActive"] == False
    assert resp_json["email"] == f"test{str(oid)}@test.com"

    typestest(resp_json)


if __name__ == "__main__":
    test_user()
