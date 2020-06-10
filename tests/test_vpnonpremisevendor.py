import requests
import json
import os


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/keyValues/vpnonpremisevendor/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def test_vpnonpremisevendor():

    # Testing POST request
    resp_json = post()
    oid = str(resp_json["id"])
    # Testing PUT request
    put(oid)
    # Testing DELETE request
    delete(oid)
    # Testing DELETE Request Error
    delete_error(oid)
    # Testing GETALL request
    get_all()


def post():

    # Test POST Then GET
    # Body
    payload = {"key": "test", "value": "test-value"}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    oid = resp_json["id"]
    assert resp.status_code == 201
    assert resp_json["key"] == "test"
    assert resp_json["value"] == "test-value"

    resp = requests.get(url + str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers

    # Validate response
    assert resp.status_code == 200
    assert resp_json["key"] == "test"
    assert resp_headers["content-type"] == "application/json"
    return resp_json


def put(oid):

    # Test Update Then get updated value
    newpayload = {"key": "test", "value": "new-test-value"}
    resp = requests.put(
        url + oid, headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(url + oid, headers=headers)
    resp_json = resp.json()
    # oid = resp_json['id']

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["value"] == "new-test-value"


def delete(oid):

    # Delete Request
    resp = requests.delete(url + oid, headers=headers)
    # Validate Delete response
    assert resp.status_code == 200
    # Then Get request to check the item has been actully deleted
    resp = requests.get(url + oid, headers=headers)
    # Validate Get response
    # resp_json = resp.json()
    assert resp.status_code == 404


def delete_error(oid):

    # Delete Request for a non existing item
    resp = requests.delete(url + oid, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response ; expect Not found
    assert resp.status_code == 404
    assert resp_json["detail"] == "VPNOnPremiseVendor " + str(oid) + " not found"
    assert resp_headers["content-type"] == "application/problem+json"


def get_all():

    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
