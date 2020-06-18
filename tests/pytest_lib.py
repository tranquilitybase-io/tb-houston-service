import os
import requests
from pprint import pformat

HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]

# Additional headers.
headers = {"Content-Type": "application/json"}


def get_all(url):

    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200


def delete(url, oid):

    # Delete Request
    resp = requests.delete(url + oid, headers=headers)
    # Validate Delete response
    assert resp.status_code == 200

    # Then Get request to check the item has been actully deleted
    resp = requests.get(url + oid, headers=headers)
    # Validate Get response
    # resp_json = resp.json()
    assert resp.status_code == 404


def logical_delete(url, oid):

    # Delete Request
    resp = requests.delete(url + oid, headers=headers)
    # Validate Delete response
    assert resp.status_code == 200

    # Then Get request to check the item has been logically deleted
    resp = requests.get(url + oid, headers=headers)
    # Validate Get response
    assert resp.status_code == 200
    resp_json = resp.json()
    print("resp_json: {resp_json}")
    assert resp_json.get("isActive") == False


def delete_error(url, oid):

    # Delete Request for a non existing item
    resp = requests.delete(url + oid, headers=headers)
    # resp_json = resp.json()
    # resp_headers = resp.headers
    # Validate response ; expect Not found
    assert resp.status_code == 404


def typestest_activator(obj):
    assert isinstance(obj["accessRequestedBy"], dict) or obj["accessRequestedBy"] is None
    assert isinstance(obj["id"], int)
    assert isinstance(obj["isActive"], bool)
    assert isinstance(obj["lastUpdated"], str)
    assert isinstance(obj["isFavourite"], bool)
    assert isinstance(obj["activator"], str)
    assert isinstance(obj["activatorLink"], str)
    assert isinstance(obj["apiManagement"], list)
    assert isinstance(obj["available"], bool)
    assert isinstance(obj["billing"], str)
    assert isinstance(obj["businessUnit"], str)
    assert isinstance(obj["category"], str)
    assert isinstance(obj["cd"], list)
    assert isinstance(obj["ci"], list)
    assert isinstance(obj["description"], str)
    assert isinstance(obj["hosting"], list)
    assert isinstance(obj["name"], str)
    assert isinstance(obj["platforms"], list)
    assert isinstance(obj["regions"], list)
    assert isinstance(obj["sensitivity"], str)
    assert isinstance(obj["serverCapacity"], int)
    assert isinstance(obj["source"], str)
    assert isinstance(obj["sourceControl"], list)
    assert isinstance(obj["status"], str)
    assert isinstance(obj["technologyOwner"], str)
    assert isinstance(obj["technologyOwnerEmail"], str)
    assert isinstance(obj["type"], str)
    assert isinstance(obj["userCapacity"], int)


def typestest_application(obj):
    assert isinstance(obj["id"], int)
    assert isinstance(obj["isActive"], bool)
    assert isinstance(obj["lastUpdated"], str)
    assert isinstance(obj["isFavourite"], bool)
    assert isinstance(obj["activatorId"], int)
    assert isinstance(obj["description"], str)
    assert isinstance(obj["env"], str)
    assert isinstance(obj["name"], str)
    assert isinstance(obj["resources"], list)
    assert isinstance(obj["solutionId"], int)
    assert isinstance(obj["status"], str)
    assert isinstance(obj["activator"], dict)
    typestest_activator(obj["activator"])


def typestest_business_unit(obj):
    assert isinstance(obj["id"], id)
    assert isinstance(obj["description"], str)
    assert isinstance(obj["name"], str)
    assert isinstance(obj["isActive"], bool)


def typestest_team(obj):
    assert isinstance(obj["businessUnitId"], int)
    typestest_business_unit(obj["businessUnit"])


def typestest_solution(obj):
    assert isinstance(obj["isActive"], bool)
    assert isinstance(obj["lastUpdated"], str)
    assert isinstance(obj["isFavourite"], bool)
    assert isinstance(obj["businessUnitId"], int)
    assert isinstance(obj["ci"], str)
    assert isinstance(obj["cd"], str)
    assert isinstance(obj["costCentre"], str)
    assert isinstance(obj["description"], str)
    assert isinstance(obj["id"], int)
    assert isinstance(obj["name"], str)
    assert isinstance(obj["sourceControl"], str)
    assert isinstance(obj["teamId"], int)
    assert isinstance(obj["team"], dict)
    assert isinstance(obj["applications"], list)
    for app in obj["applications"]:
        typestest_application(app)
    print(f"obj: {pformat(obj)}")
