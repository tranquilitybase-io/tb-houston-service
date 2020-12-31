import json

import requests

from tests import pytest_lib

plural_url = f"http://{pytest_lib.HOUSTON_SERVICE_URL}/api/landingzoneprogressitems/"
singular_url = f"http://{pytest_lib.HOUSTON_SERVICE_URL}/api/landingzoneprogressitem/"


def test_landingzoneprogressitem():

    # Testing POST request
    resp_json = post(singular_url)
    oid = str(resp_json["id"])
    # Testing PUT request
    put(singular_url, oid)
    # Testing DELETE request
    pytest_lib.delete(singular_url, oid)
    # Testing DELETE Request Error
    pytest_lib.delete_error(singular_url, oid)
    # Testing GETALL request
    pytest_lib.get_all(plural_url)


def post(url):

    # Test POST Then GET
    # Body
    payload = {"completed": True, "id": 0, "label": "Testing-progress-item-post"}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(
        url, headers=pytest_lib.headers, data=json.dumps(payload, indent=4)
    )

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    oid = resp_json["id"]
    assert resp.status_code == 201

    # Get Request to check Post has created item as expected
    resp = requests.get(url + str(oid), headers=pytest_lib.headers)
    resp_json = resp.json()
    # resp_headers = resp.headers
    # Validate GET response
    assert resp.status_code == 200
    # assert resp_json['completed'] == True
    # assert resp_json['label'] == 'Testing-progress-item-post'
    # assert resp_headers['content-type'] == 'application/json'

    payload["id"] = resp_json["id"]
    payload_string = json.dumps(payload)
    resp_json_string = json.dumps(resp_json)
    assert payload_string == resp_json_string

    return resp_json


def put(url, oid):

    # Test Update Then get updated value
    newpayload = {
        "completed": False,
        "id": int(oid),
        "label": "Testing-new-progress-item-post",
    }

    resp = requests.put(
        url + oid, headers=pytest_lib.headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(url + oid, headers=pytest_lib.headers)
    resp_json = resp.json()
    oid = resp_json["id"]
    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["completed"] == False
    assert resp_json["label"] == "Testing-new-progress-item-post"
