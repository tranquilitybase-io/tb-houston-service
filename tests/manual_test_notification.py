import json
import os
from pprint import pprint

import requests

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/notifications/"

# Additional headers.
headers = {"Content-Type": "application/json"}

if os.environ.get("TOKEN"):
    headers["Authorization"] = f"Bearer {os.environ['TOKEN']}"

print(f"headers: {headers}")

# *** make sure toUserId is set to the user in the Token ***


def typestest(resp):
    assert isinstance(resp["id"], int)
    assert isinstance(resp["isActive"], bool)
    assert isinstance(resp["lastUpdated"], str)
    assert isinstance(resp["toUserId"], int)
    assert isinstance(resp["fromUserId"], int) or resp["fromUserId"] is None
    assert isinstance(resp["importance"], int) or resp["importance"] is None
    assert isinstance(resp["message"], str)
    assert isinstance(resp["isRead"], bool)
    assert isinstance(resp["typeId"], int)
    assert isinstance(resp["details"], dict)
    pprint(resp)


def test_notifications():
    # Testing POST request
    oid = create_notification_activators()
    # disabled for now, the automated filter from the token makes the update difficult to test
    # update_notification_activator(oid)
    oid = create_notification_teams()
    # update_notification_team(oid)
    read_all()


def create_notification_activators():
    # Test POST Then GET
    # Body
    payload = [
        {
            "isActive": True,
            "toUserId": 4,
            "importance": 1,
            "message": "User Jon Snow requested access to Activator 2",
            "isRead": False,
            "activatorId": 2,
        },
        {
            "isActive": True,
            "toUserId": 4,
            "importance": 2,
            "message": "User Cersei Lannister requested access to an Activator 3",
            "isRead": False,
            "activatorId": 3,
        },
    ]

    resp = requests.post(
        url + "?typeId=1&isActive=true&isRead=false",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(f"resp_json: {resp_json}")
    oid = 0
    for rj in resp_json:
        print(rj)
        oid = rj["id"]
    assert resp.status_code == 201
    print(f"oid: {oid}")
    return oid


def update_notification_activator(oid):
    # Test POST Then GET
    # Body
    payload = [{"id": oid, "isActive": False, "importance": 1, "isRead": True}]
    print(f"payload: {payload}")

    resp = requests.post(
        url + "?typeId=1&isActive=true&isRead=false&sort=importance:asc",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )
    # Validate response headers and body contents, e.g. status code.
    # resp_json = resp.json()
    assert resp.status_code == 201


def create_notification_teams():
    # Test POST Then GET
    # Body
    payload = [
        {
            "isActive": True,
            "toUserId": 4,
            "importance": 1,
            "message": "User Jon Snow requested access to Team 1",
            "isRead": False,
            "teamId": 1,
        },
        {
            "isActive": True,
            "toUserId": 4,
            "importance": 2,
            "message": "User Cersei Lannister requested access to an Team 1",
            "isRead": False,
            "teamId": 1,
        },
    ]

    resp = requests.post(
        url + "?typeId=2&isActive=true&isRead=false",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)
    oid = 0
    for rj in resp_json:
        print(rj)
        oid = rj["id"]
    assert resp.status_code == 201
    print(f"oid: {oid}")
    return oid


def update_notification_team(oid):
    # Test POST Then GET
    # Body
    payload = [{"id": oid, "isActive": False, "importance": 1, "isRead": True}]

    resp = requests.post(
        url + "?typeId=2&isActive=true&isRead=false&sort=importance:asc",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )
    # Validate response headers and body contents, e.g. status code.
    # resp_json = resp.json()
    assert resp.status_code == 201


def create_notification_application_deployment():
    # Test POST Then GET
    # Body
    payload = [
        {
            "isActive": True,
            "toUserId": 1,
            "importance": 1,
            "message": "User Jon Snow has deployed application 1 successfully",
            "isRead": False,
            "applicationId": 1,
        },
        {
            "isActive": True,
            "toUserId": 3,
            "importance": 2,
            "message": "User Cersei Lannister has deployed application 2 successfully",
            "isRead": False,
            "applicationId": 2,
        },
    ]

    resp = requests.post(
        url + "?typeId=3&isActive=true&isRead=false",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)
    oid = 0
    for rj in resp_json:
        print(rj)
        oid = rj["id"]
    assert resp.status_code == 201
    print(f"oid: {oid}")
    return oid


def update_notification_application_deployment(oid):
    # Test POST Then GET
    # Body
    payload = [{"id": oid, "isActive": False, "importance": 1, "isRead": True}]

    resp = requests.post(
        url + "?typeId=3&isActive=true&isRead=false&sort=importance:asc",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )
    # Validate response headers and body contents, e.g. status code.
    # resp_json = resp.json()
    assert resp.status_code == 201


def create_notification_solution_deployment():
    # Test POST Then GET
    # Body
    payload = [
        {
            "isActive": True,
            "toUserId": 1,
            "importance": 1,
            "message": "User Jon Snow has deployed solution 1 successfully",
            "isRead": False,
            "applicationId": 1,
        },
        {
            "isActive": True,
            "toUserId": 3,
            "importance": 2,
            "message": "User Cersei Lannister has deployed solution 2 successfully",
            "isRead": False,
            "applicationId": 2,
        },
    ]

    resp = requests.post(
        url + "?typeId=4&isActive=true&isRead=false",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)
    oid = 0
    for rj in resp_json:
        print(rj)
        oid = rj["id"]
    assert resp.status_code == 201
    print(f"oid: {oid}")
    return oid


def update_notification_solution_deployment(oid):
    # Test POST Then GET
    # Body
    payload = [{"id": oid, "isActive": False, "importance": 1, "isRead": True}]

    resp = requests.post(
        url + "?typeId=4&isActive=true&isRead=false&sort=importance:asc",
        headers=headers,
        data=json.dumps(payload, indent=4),
    )
    # Validate response headers and body contents, e.g. status code.
    # resp_json = resp.json()
    assert resp.status_code == 201


def read_all():
    resp = requests.get(
        url + "?typeId=1&isActive=true&isRead=false&sort=importance:asc",
        headers=headers,
    )
    resp_json = resp.json()
    print(resp_json)
    assert resp.status_code == 200
    for j in resp_json:
        typestest(j)


if __name__ == "__main__":
    test_notifications()
