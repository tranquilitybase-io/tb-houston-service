import json
import os
from pprint import pprint

import requests

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/solutionresourcejson/"
urls = f"http://{HOUSTON_SERVICE_URL}/api/solutionresourcejsons/"

# Additional headers.
headers = {"Content-Type": "application/json"}
id = 0

with open("solution_response_example.json", "r") as fh:
    my_json_s = json.dumps(json.load(fh).get("payload"))
    print(my_json_s)

with open("solution_response_example2.json", "r") as fh:
    my_json_s2 = json.dumps(json.load(fh).get("payload"))
    print(my_json_s2)


def typestest_solution_resource_json(resp):
    assert isinstance(resp["solutionId"], int)
    assert isinstance(resp["json"], str)
    pprint(resp)


def test_solutionresourcejson():

    # Testing POST request - create + update existing row
    id1 = post()
    # Testing GET ALL request
    get_all()
    # Testing DELETE request
    delete(id1)
    post2()
    post3()
    post4()


def post():
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "solutionId": 1,
        "json": my_json_s,
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(pprint(resp_json))

    assert resp_json["solutionId"] == 1
    assert resp_json["json"] == my_json_s

    assert resp.status_code == 201
    assert resp.headers["content-type"] == "application/json"
    pprint(resp.json())
    typestest_solution_resource_json(resp_json)

    # Get Request to get updated values
    solutionId = str(resp_json["solutionId"])
    resp = requests.get(url + solutionId, headers=headers)
    resp_json = resp.json()
    assert resp_json["solutionId"] == 1
    assert resp_json["json"] == my_json_s
    print("solution_response_json_post")
    pprint(resp_json)

    return solutionId


def post2():
    print("Post 2 Test")

    # Test Update
    payload = {"solutionId": 2, "json": my_json_s}

    print("url: " + url)
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json["solutionId"] == 2
    assert resp_json["json"] == my_json_s

    # Validate update/Put response
    assert resp.status_code == 201

    # Get Request to get updated values
    solutionId = str(resp_json["solutionId"])
    resp = requests.get(url + solutionId, headers=headers)
    resp_json = resp.json()

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["solutionId"] == 2
    assert resp_json["json"] == my_json_s
    typestest_solution_resource_json(resp_json)


def post3():
    print("Post 3 Test")

    # Test Update
    payload = {"solutionId": 3, "json": my_json_s}

    print("url: " + url)
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json["solutionId"] == 3
    assert resp_json["json"] == my_json_s

    # Validate update/Put response
    assert resp.status_code == 201

    # Get Request to get updated values
    solutionId = str(resp_json["solutionId"])
    resp = requests.get(url + solutionId, headers=headers)
    resp_json = resp.json()

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["solutionId"] == 3
    assert resp_json["json"] == my_json_s
    typestest_solution_resource_json(resp_json)


def post4():
    print("Post 4 Test")

    # Test Update
    payload = {"solutionId": 4, "json": my_json_s2}

    print("url: " + url)
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json["solutionId"] == 4
    assert resp_json["json"] == my_json_s2

    # Validate update/Put response
    assert resp.status_code == 201

    # Get Request to get updated values
    solutionId = str(resp_json["solutionId"])
    resp = requests.get(url + solutionId, headers=headers)
    resp_json = resp.json()

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["solutionId"] == 4
    assert resp_json["json"] == my_json_s2
    typestest_solution_resource_json(resp_json)


def delete(solutionId):
    print("Delete Tests")

    # Test Delete Then GET
    resp = requests.delete(url + solutionId, headers=headers)
    # Validate Delete response
    assert resp.status_code == 200

    # Then GET request to check the item has been actully deleted
    resp = requests.get(url + solutionId, headers=headers)
    # Validate Get response
    # resp_json = resp.json()
    assert resp.status_code == 404


def get_all():
    print("get_all Tests")

    resp = requests.get(urls, headers=headers)
    # Validate Get All response
    assert resp.status_code == 200
