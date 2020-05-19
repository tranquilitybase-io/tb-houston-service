"""
   Tests for the solutionresource endpoint.
"""
from pprint import pprint
import json
import os
import requests
from urllib.parse import urlparse


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
global_url = f"http://{HOUSTON_SERVICE_URL}/api/lzmetadata/"


# Additional headers.
headers = {"Content-Type": "application/json"}


def typestest_lzmetadata(resp):
    """
    check response types
    """
    assert isinstance(resp["group"], str)
    assert isinstance(resp["name"], str)
    assert isinstance(resp["value"], str)
    assert isinstance(resp["description"], str)
    assert isinstance(resp["active"], bool)
    pprint(resp)


def test_lzmetadata():
    """
    main test function
    """
    # Testing POST request
    (group, name) = post()
    # Testing POST with Update request
    (group, name) = update()
    # Testing GETALL request
    get_all()
    # Testing DELETE request
    delete(group, name)


def post():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "description": "Landing Zone metadata for Test environment",
        "group": "test_group",
        "name": "test",
        "value": ["UAT", "Production"],
    }
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(
        global_url, headers=headers, data=json.dumps(payload, indent=4)
    )
    print(pprint(resp))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)

    assert resp_json["group"] == "test_group"
    assert resp_json["name"] == "test"
    assert resp_json["value"] == '["UAT", "Production"]'

    assert resp.status_code == 201
    assert resp.headers["content-type"] == "application/json"
    pprint(resp.json())
    typestest_lzmetadata(resp_json)

    # Get Request to get updated values
    group = str(resp_json["group"])
    name = str(resp_json["name"])
    resp = requests.get(
        urlparse(global_url + group + "/" + name).geturl(), headers=headers
    )
    resp_json = resp.json()
    print("lzmetadata_post")
    pprint(resp_json)

    return (group, name)


def update():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "description": "Landing Zone metadata for Test environment",
        "group": "test_group",
        "name": "test",
        "value": ["UAT", "Poc"],
    }
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(
        global_url, headers=headers, data=json.dumps(payload, indent=4)
    )
    print(pprint(resp))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()

    assert resp_json["group"] == "test_group"
    assert resp_json["name"] == "test"
    assert resp_json["value"] == '["UAT", "Poc"]'

    assert resp.status_code == 201
    assert resp.headers["content-type"] == "application/json"
    pprint(resp.json())
    typestest_lzmetadata(resp_json)

    # Get Request to get updated values
    group = str(resp_json["group"])
    name = str(resp_json["name"])
    resp = requests.get(
        urlparse(global_url + group + "/" + name).geturl(), headers=headers
    )
    resp_json = resp.json()
    print("lzmetadata_post")
    pprint(resp_json)

    return (group, name)


def delete(group, name):
    """
    Test delete endpoint.
    """
    print("Delete Tests")

    # Test Delete Then GET
    resp = requests.delete(
        urlparse(global_url + group + "/" + name).geturl(), headers=headers
    )
    # Validate Delete response
    assert resp.status_code == 200

    # Then GET request to check the item has been actully deleted
    resp = requests.get(
        urlparse(global_url + group + "/" + name).geturl(), headers=headers
    )
    # Validate Get response
    # resp_json = resp.json()
    assert resp.status_code == 404


def get_all():
    """
    Test getall endpoint.
    """
    print("get_all Tests")

    resp = requests.get(global_url, headers=headers)
    # Validate Get All response
    assert resp.status_code == 200
