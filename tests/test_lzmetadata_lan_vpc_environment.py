import requests
import json
from tests import pytest_lib

url = f"http://{pytest_lib.HOUSTON_SERVICE_URL}/api/lzmetadataLanVpcEnvironment/"


def test_main():
    post()


def post():

    # Test POST Then GET
    # Body
    payload = [ { "environmentId": 2, "id": 0, "lzlanvpcId": 1 } ] 
    print(f"url: {url}")
    print(f"payload: {json.dumps(payload)}")

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=pytest_lib.headers, data=json.dumps(payload))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 201

    # Get Request to check Post has created item as expected
    resp1 = requests.get(url, headers=pytest_lib.headers)
    # resp_headers = resp.headers
    # Validate GET response
    resp_json1 = resp1.json()
    assert resp1.status_code == 200
    for j in resp_json1:
        assert isinstance(j["id"], int)
        assert isinstance(j["environmentId"], int)
        assert isinstance(j["lzlanvpcId"], int)
