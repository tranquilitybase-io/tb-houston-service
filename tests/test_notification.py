import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/notifications/"

# Additional headers.
headers = {"Content-Type": "application/json"}


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
    assert isinstance(resp["activatorId"], int)
    pprint(resp)


def test_notifications():
    # Testing POST request
    oid = create()
    update(oid)
    read_all()


def create():
    # Test POST Then GET
    # Body
    payload = [
        {
            "isActive": True,
            "toUserId": 1,
            "importance": 1,
            "message": "User Jon Snow requested access to Activator 2",
            "isRead": False,
            "activatorId": 2
        },
        {
            "isActive": True,
            "toUserId": 2,
            "importance": 2,
            "message": "User Cersei Lannister requested access to an Activator 3",
            "isRead": False,
            "activatorId": 3
        }
    ]

    resp = requests.post(url + "?typeId=1&toUserId=1&isActive=true&isRead=false", headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(resp_json)
    oid = 0
    for rj in resp_json:
        print(rj)
        oid = rj['id']
    assert resp.status_code == 201
    print(f"oid: {oid}")
    return oid


def update(oid):
    # Test POST Then GET
    # Body
    payload = [
        {
            "id": oid,
            "isActive": False,
            "importance": 1,
            "isRead": True
        }
    ]

    resp = requests.post(url + "?typeId=1&isActive=true&isRead=false&sort=importance:asc", headers=headers, data=json.dumps(payload, indent=4))
    # Validate response headers and body contents, e.g. status code.
    #resp_json = resp.json()
    assert resp.status_code == 201


def read_all():
    resp = requests.get(url + "?typeId=1&isActive=true&isRead=false&sort=importance:asc", headers=headers)
    resp_json = resp.json()
    print(resp_json)
    assert resp.status_code == 200
    for j in resp_json:
        typestest(j)


if __name__ == "__main__":
    test_notifications()
