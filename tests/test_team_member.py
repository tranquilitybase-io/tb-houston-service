import json
import logging
import os
from pprint import pprint

import requests

from tests import pytest_lib, test_team, test_user

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
user_url = f"http://{HOUSTON_SERVICE_URL}/api/user/"
team_member_url = f"http://{HOUSTON_SERVICE_URL}/api/teamMember/"
team_members_url = f"http://{HOUSTON_SERVICE_URL}/api/teamMembers/"


# Additional headers.
headers = {"Content-Type": "application/json"}
test_email_account = "new_team@test.com"


def typestest(resp):
    assert isinstance(resp["userId"], int)
    assert isinstance(resp["teamId"], int)
    assert isinstance(resp["isTeamAdmin"], bool)
    assert isinstance(resp["isActive"], bool)
    pprint(resp)


def test_teammember():

    # Testing POST request
    user_id = test_user.post()
    test_user.put(user_id)
    team_id = test_team.post()

    team_member_id = post_team_member(userId=user_id, teamId=team_id)
    # Testing PUT request
    put_team_member(teamMemberId=team_member_id, userId=user_id, teamId=team_id)
    # Test GET all teammbers with parameters
    get_all_params(userId=user_id, teamId=team_id)
    # Testing DELETE request
    pytest_lib.logical_delete(team_member_url, str(team_member_id))
    # Testing DELETE Request Error
    pytest_lib.delete_error(team_member_url, "-1")
    # Testing GETALL request
    pytest_lib.get_all(team_members_url)


def post_team_member(userId, teamId):
    print("Post Tests")
    # Test POST Then GET
    # Body
    payload = {
        "id": 0,
        "userId": userId,
        "teamId": teamId,
        "isTeamAdmin": True,
        "isActive": True,
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(
        team_member_url, headers=headers, data=json.dumps(payload, indent=4)
    )

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    oid = resp_json["id"]

    # Get Request to check Post has created item as expected
    resp = requests.get(team_member_url + str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    # Validate response
    assert resp.status_code == 200
    assert resp_json["userId"] == userId
    assert resp_json["teamId"] == teamId
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return oid


def put_team_member(teamMemberId, userId, teamId):
    print("Put Tests")

    # Test Update Then get new value
    newpayload = {
        "id": teamMemberId,
        "userId": userId,
        "teamId": teamId,
        "isTeamAdmin": True,
        "isActive": False,
    }

    resp = requests.put(
        team_member_url + str(teamMemberId),
        headers=headers,
        data=json.dumps(newpayload, indent=4),
    )

    # Validate update/Put response
    assert resp.status_code == 200

    # Get Request to get updated values
    resp = requests.get(team_member_url + str(teamMemberId), headers=headers)
    resp_json = resp.json()
    # id = resp_json["id"]

    # Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["userId"] == userId
    assert resp_json["teamId"] == teamId
    assert resp_json["isActive"] is False

    typestest(resp_json)


def get_all_params(userId, teamId):
    print("get_all Tests with parameters")

    # defining a params dict for the parameters to be sent to the API
    params = {"userId": userId, "teamId": teamId}

    resp = requests.get(team_members_url, headers=headers, params=params)

    # Validate Get All response
    assert resp.status_code == 200


if __name__ == "__main__":
    test_teammember()
