"""
   Tests for the solutionresource endpoint.
"""
from pprint import pprint
import json
import os
import requests
from urllib.parse import urlparse


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
global_url = f"http://{HOUSTON_SERVICE_URL}/api/solutionresource/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def typestest_solution_resource(resp):
    """
    check response types
    """
    assert isinstance(resp["solutionId"], int)
    assert isinstance(resp["key"], str)
    assert isinstance(resp["value"], str)
    pprint(resp)


def test_solutionresource():
    """
    main test function
    """
    # Testing POST request
    (solution_id, key) = post()
    # Testing GETALL request
    get_all()
    # Testing DELETE request
    delete(solution_id, key)


def post():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    key = 'key 1'
    payload = {"solutionId": 1, "key": key, "value": "value 1"}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(global_url, headers=headers, data=json.dumps(payload, indent=4))
    print(pprint(resp))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()

    assert resp_json["solutionId"] == 1
    assert resp_json["key"] == key
    assert resp_json["value"] == "value 1"

    assert resp.status_code == 201
    assert resp.headers["content-type"] == "application/json"
    pprint(resp.json())
    typestest_solution_resource(resp_json)

    # Get Request to get updated values
    solution_id = str(resp_json["solutionId"])
    resp = requests.get(urlparse(global_url + solution_id + '/' + key).geturl(), headers=headers)
    resp_json = resp.json()
    print("solution_post")
    pprint(resp_json)

    return (solution_id, key)


def delete(solution_id, key):
    """
    Test delete endpoint.
    """
    print("Delete Tests")

    # Test Delete Then GET
    resp = requests.delete(urlparse(global_url + solution_id + '/' + key).geturl(), headers=headers)
    # Validate Delete response
    assert resp.status_code == 200

    # Then GET request to check the item has been actully deleted
    resp = requests.get(urlparse(global_url + solution_id + '/' + key).geturl(), headers=headers)
    # Validate Get response
    # resp_json = resp.json()
    assert resp.status_code == 404


def get_all():
    """
    Test getall endpoint.
    """
    print("get_all Tests")

    url = "http://localhost:3000/api/solutionresources/"
    resp = requests.get(url, headers=headers)
    # Validate Get All response
    assert resp.status_code == 200
