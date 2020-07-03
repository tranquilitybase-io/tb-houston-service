import requests
import json
import logging
import os

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/cd/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def test_cd():
    # Testing POST request
    resp_json = post()
    id = str(resp_json["id"])
    # Testing PUT request
    put(id)
    # Testing DELETE request
    delete(id)
    # Testing DELETE Request Error
    delete_error(id)
    # Testing GETALL request
    get_all()

def post():

    # Test POST Then GET
    # Body
    payload = {"id":10000, "value": "test-post-value"}
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = str(resp_json["id"])
    assert resp.status_code == 201
    assert resp_json["value"] == "test-post-value"

    # Get Request to check Post has created item as expected
    resp = requests.get(url + id, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200
    assert resp_json["value"] == "test-post-value"
    assert resp_headers["content-type"] == "application/json"
    return resp_json


def put(id):

    # Test Update Then get new value
    newpayload = {"id": id, "value": "new-test-value"}
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
    assert resp_json["id"] == 10000
    assert resp_json["value"] == "new-test-value"


def delete(id):

    # Test Delete Then GET
    resp = requests.delete(url + id, headers=headers)
    assert resp.status_code == 200


def get_error():

    resp = requests.get(url + id, headers=headers)
    # resp_json = resp.json()
    assert resp.status_code == 404


def get_all():

    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
