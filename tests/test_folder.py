import requests
import json
import os
from tb_houston_service.DeploymentStatus import DeploymentStatus


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/folder/"

# Additional headers.
headers = {"Content-Type": "application/json"}
id = "0"

rootfolderid = "rootfolderid"
testFolder = "test_folder"
testFolderId = "test_folder_id"
testTaskId = "test_task_id"


def test_folder():
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
    payload = {
        "id": 0,
        "parentFolderId": rootfolderid,
        "folderId": None,
        "folderName": testFolder,
        "status": DeploymentStatus.PENDING,
        "taskId": None,
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)
    id = resp_json["id"]
    assert resp.status_code == 201

    # Get Request to check Post has created item as expected
    resp = requests.get(url + str(id), headers=headers)
    resp_json = resp.json()
    print(resp_json)
    resp_headers = resp.headers
    # Validate GET response
    assert resp.status_code == 200
    assert resp_json["parentFolderId"] == rootfolderid
    assert resp_json["folderId"] == None
    assert resp_json["folderName"] == testFolder
    assert resp_json["status"] == DeploymentStatus.PENDING
    assert resp_json["taskId"] == None
    assert resp_headers["content-type"] == "application/json"
    return resp_json


def put(id):

    # Test Update Then get updated value
    newpayload = {
        "folderId": testFolderId,
        "status": DeploymentStatus.SUCCESS,
        "taskId": testTaskId,
    }

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
    assert resp_json["folderId"] == testFolderId
    assert resp_json["status"] == DeploymentStatus.SUCCESS
    assert resp_json["taskId"] == testTaskId


def delete(id):

    # Delete Request
    resp = requests.delete(url + id, headers=headers)
    # Validate Delete response
    assert resp.status_code == 200

    # Then Get request to check the item has been actully deleted
    resp = requests.get(url + id, headers=headers)
    # Validate Get response
    assert resp.status_code == 404


def delete_error(id):

    # Delete Request for a non existing item
    resp = requests.delete(url + id, headers=headers)
    # resp_json = resp.json()
    # Validate response ; expect Not found
    assert resp.status_code == 404


def get_all():

    url = f"http://{HOUSTON_SERVICE_URL}/api/folders/"
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
