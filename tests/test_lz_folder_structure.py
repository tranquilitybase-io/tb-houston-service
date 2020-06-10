"""
   Tests for the solutionresource endpoint.
"""
from pprint import pprint
import json
import os
import requests


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/lzmetadataFolderStructure/"

# Additional headers.
headers = {"Content-Type": "application/json"}


def test_main():
    """
    main test function
    """
    # Testing POST request
    post()
    # Testing GETALL request
    get()


def post():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = [
        {
            "id": 1,
            "isActive": True,
            "name": "Applications",
            "children": [
                {
                    "id": 2,
                    "isActive": True,
                    "name": "Business Unit",
                    "children": [
                        {
                            "id": 3,
                            "isActive": True,
                            "name": "Team",
                            "children": [
                                {"id": 4, "isActive": True, "name": "Solutions"}
                            ],
                        }
                    ],
                }
            ],
        }
    ]
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    print(pprint(resp))

    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    print("post")
    pprint(resp_json)


def update():
    """
    Test post endpoint.
    """
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = [
        {
            "id": 1,
            "isActive": True,
            "name": "Applications",
            "children": [
                {
                    "id": 2,
                    "isActive": True,
                    "name": "Business Unit",
                    "children": [
                        {
                            "id": 3,
                            "isActive": True,
                            "name": "Team",
                            "children": [
                                {"id": 4, "isActive": True, "name": "Solutions"}
                            ],
                        }
                    ],
                }
            ],
        }
    ]

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    print(pprint(resp))

    assert resp.status_code == 201
    pprint(resp.json())

    # Get Request to get updated values
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    pprint(resp_json)


def get():
    """
    Test get endpoint.
    """
    print("get Tests")

    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    print(f"resp_json: {resp_json}")
    # Check if valid json
    assert isinstance((resp_json[0]["id"]), int)
    assert isinstance((resp_json[0]["name"]), str)
    assert isinstance((resp_json[0]["children"]), list)
    assert isinstance((resp_json[0]["children"][0]["id"]), int)
    assert isinstance((resp_json[0]["children"][0]["name"]), str)
    assert isinstance((resp_json[0]["children"][0]["children"]), list)
    assert isinstance((resp_json[0]["children"][0]["children"][0]["id"]), int)
    assert isinstance((resp_json[0]["children"][0]["children"][0]["name"]), str)
    assert isinstance((resp_json[0]["children"][0]["children"][0]["children"]), list)
    assert isinstance(
        (resp_json[0]["children"][0]["children"][0]["children"][0]["id"]), int
    )
    assert isinstance(
        (resp_json[0]["children"][0]["children"][0]["children"][0]["name"]), str
    )
    # Validate Get All response
    assert resp.status_code == 200
