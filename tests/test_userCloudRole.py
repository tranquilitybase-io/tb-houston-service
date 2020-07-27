  
import requests
import json
import logging
import os
from pprint import pprint
from tests import pytest_lib
from tests import test_user
from tests import test_cloudRole


LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
user_url = f"http://{HOUSTON_SERVICE_URL}/api/user/"
user_cloud_role_url = f"http://{HOUSTON_SERVICE_URL}/api/userCloudRole/"
user_roles_url = f"http://{HOUSTON_SERVICE_URL}/api/userCloudRoles/"


# Additional headers.
headers = {"Content-Type": "application/json"}

def typestest(resp):
    assert isinstance(resp["userId"], int)
    assert isinstance(resp["cloudRoleId"], int)
    assert isinstance(resp["isActive"], bool)
    pprint(resp)


def test_userCloudRole():

    # Testing POST request
    user_id = test_user.post()
    test_user.put(user_id)
    cloud_role_id = test_cloudRole.post()    

    user_cloud_role_id = post_user_role(userId = user_id, cloudRoleId = cloud_role_id)
    # Testing PUT request
    put_user_role(userCloudRoleId = user_cloud_role_id, userId = user_id, cloudRoleId = cloud_role_id)
    # Test GET all user-roles with parameters
    get_all_params(userId = user_id)
    # Testing DELETE request
    pytest_lib.logical_delete(user_cloud_role_url, str(user_cloud_role_id))
    # Testing DELETE Request Error
    pytest_lib.delete_error(user_cloud_role_url, "-1")
    # Testing GETALL request
    pytest_lib.get_all(user_roles_url)


def post_user_role(userId, cloudRoleId):
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "id": 0,
        "userId": userId,
        "cloudRoleId": cloudRoleId,
        "isActive": True,
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(user_cloud_role_url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    oid = resp_json["id"]

    # Get Request to check Post has created item as expected
    resp = requests.get(user_cloud_role_url + str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200
    assert resp_json["userId"] == userId
    assert resp_json["cloudRoleId"] == cloudRoleId
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return oid


def put_user_role(userCloudRoleId, userId, cloudRoleId):
    print("Put Tests")

    # Test Update Then get new value
    newpayload = {
        "id": userCloudRoleId,
        "userId": userId,
        "cloudRoleId": cloudRoleId,
        "isActive": False,
    }

    resp = requests.put(
        user_cloud_role_url + str(userCloudRoleId), headers=headers, data=json.dumps(newpayload, indent=4)
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(user_cloud_role_url + str(userCloudRoleId), headers=headers)
    resp_json = resp.json()
    #id = resp_json["id"]

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["userId"] == userId
    assert resp_json["cloudRoleId"] == cloudRoleId    
    assert resp_json["isActive"] == False

    typestest(resp_json)


def get_all_params(userId):
    print("get_all Tests with parameters")

    # defining a params dict for the parameters to be sent to the API
    params = {"userId": userId}

    resp = requests.get(user_roles_url, headers=headers, params=params)

    # Validate Get All response
    assert resp.status_code == 200


if __name__ == "__main__":
    test_user_role()
