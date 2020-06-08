"""
   Tests for the solutionresource endpoint.
"""
from pprint import pprint
import json
import os
import requests
from tests import pytest_lib


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/lzmetadata_folder_structure/"
folder_structure_name = "folder_structure"

# Additional headers.
headers = {"Content-Type": "application/json"}


def typestest_lzmetadata(resp):
    """
    check response types
    """
    assert isinstance(resp["name"], str)
    assert isinstance(resp["value"], list)
    assert isinstance(resp["isActive"], bool)
    pprint(resp)


def test_main():
    """
    main test function
    """
    # Testing POST request
    post()
    # Testing POST with Update request
    update()
    # Testing GETALL request
    get_all()
    # Testing DELETE request - blank parameter is intentional
    pytest_lib.logical_delete(url, "")


def post():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = { "value": [ {"id": 1, "isEnabled": True, "name": "Applications", "children": [{"id": 2, "isEnabled": True, "name": "Business Unit", "children": [{"id": 3, "isEnabled": True, "name": "Team", "children": [{"id": 4, "isEnabled": True, "name": "Solutions"}]}]}]} ] }
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4)
    )
    print(pprint(resp))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)

    assert resp_json["name"] == folder_structure_name

    assert resp.status_code == 201
    assert resp.headers["content-type"] == "application/json"
    pprint(resp.json())
    typestest_lzmetadata(resp_json)

    resp = requests.get(url + "/" + folder_structure_name, headers=headers)
    resp_json = resp.json()
    print("lzmetadata_post")
    pprint(resp_json)


def update():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = { "value": [ {"id": 1, "isEnabled": True, "name": "Applications", "children": [{"id": 2, "isEnabled": True, "name": "Business Unit", "children": [{"id": 3, "isEnabled": True, "name": "Team", "children": [{"id": 4, "isEnabled": True, "name": "Solutions"}]}]}]} ] } 

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    print(pprint(resp))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()

    assert resp.status_code == 201
    assert resp.headers["content-type"] == "application/json"
    pprint(resp.json())
    typestest_lzmetadata(resp_json)

    # Get Request to get updated values
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    pprint(resp_json)


def get_all():
    """
    Test getall endpoint.
    """
    print("get_all Tests")

    resp = requests.get(url, headers=headers)
    # Validate Get All response
    assert resp.status_code == 200
