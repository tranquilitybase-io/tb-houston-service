import json
import requests
from tests import pytest_lib

url = f"http://{pytest_lib.HOUSTON_SERVICE_URL}/api/lzmetadataLanVpc/"
test_name = "testing_999999999"


def test_main():
    post1()
    post2()


def post1():

    # Test POST1 Then GET
    # Body
    payload = [ { "environments": [1,2,3], "isActive": True, "name": "Test Development VPC" }, { "environments": [1,2], "isActive": True, "name": "Test Production VPC" } ]
    print(f"url: {url}")
    print(f"payload: {json.dumps(payload)}")

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url+"?readActiveOnly=true&bulkDelete=true", headers=pytest_lib.headers, data=json.dumps(payload))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 201
    resp_json = resp.json()
    for j in resp_json:
        assert isinstance(j["id"], int)
        assert isinstance(j["name"], str)
        assert isinstance(j["isActive"], bool)
        if j['name'] == "Test Development VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 3
        if j['name'] == "Test Production VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 2


    # Get Request to check Post has created item as expected
    resp1 = requests.get(url+"?readActiveOnly=true", headers=pytest_lib.headers)
    # resp_headers = resp.headers
    # Validate GET response
    resp_json1 = resp1.json()
    assert resp1.status_code == 200
    for j in resp_json1:
        assert isinstance(j["id"], int)
        assert isinstance(j["name"], str)
        assert isinstance(j["isActive"], bool)
        if j['name'] == "Test Development VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 3
        if j['name'] == "Test Production VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 2


def post2():

    # Test POST2 Then GET
    # Body
    payload = [ { "environments": [1,3], "isActive": True, "name": "Test Development VPC" }, { "environments": [1], "isActive": True, "name": "Test Production VPC" } ]
    print(f"url: {url}")
    print(f"payload: {json.dumps(payload)}")

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url+"?readActiveOnly=true&bulkDelete=true", headers=pytest_lib.headers, data=json.dumps(payload))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    for j in resp_json:
        assert isinstance(j["id"], int)
        assert isinstance(j["name"], str)
        assert isinstance(j["isActive"], bool)
        if j['name'] == "Test Development VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 2
        if j['name'] == "Test Production VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 1

    # Get Request to check Post has created item as expected
    resp1 = requests.get(url+"?readActiveOnly=true", headers=pytest_lib.headers)
    # resp_headers = resp.headers
    # Validate GET response
    resp_json1 = resp1.json()
    assert resp1.status_code == 200
    for j in resp_json1:
        assert isinstance(j["id"], int)
        assert isinstance(j["name"], str)
        assert isinstance(j["isActive"], bool)
        if j['name'] == "Test Development VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 2
        if j['name'] == "Test Production VPC":
            print(f"{j['name']} environments: {len(j['environments'])}")
            assert len(j["environments"]) == 1


if __name__ == "__main__":
    test_main()
