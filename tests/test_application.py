import requests
import json
import os
from pprint import pprint
from pprint import pformat


HOUSTON_SERVICE_URL=os.environ["HOUSTON_SERVICE_URL"]
url = f"http://{HOUSTON_SERVICE_URL}/api/application/"
    
# Additional headers.
headers = {"Content-Type": "application/json" }

def typestest(resp):
    assert isinstance(resp["activatorId"], int)
    assert isinstance(resp["description"], str)
    assert isinstance(resp["env"], str)
    assert isinstance(resp["id"], int)
    assert isinstance(resp["name"], str)
    assert isinstance(resp["resources"], list)
    assert isinstance(resp["solutionId"], int)
    assert isinstance(resp["status"], str)
    pprint(resp)


def test_application():

    #Testing POST request
    oid = post()
    #Testing PUT request
    put(oid)
    #Testing DELETE request
    delete(oid)
    #Testing GETALL request
    get_all()
    # Test post with no resources
    oid = post1()
    delete(oid)

    

def post():

    #Test POST Then GET
    # Body
    payload  =  {
        "solutionId": 0,
        "activatorId": 0,
        "name": "test",
        "env": "DEV",
        "status": "Active",
        "description": "test",
        "resources": [
            { "ipaddress": "address1", "name": "value1" },
            { "ipaddress": "address2", "name": "value2" },
            { "ipaddress": "address3", "name": "value3" }
        ]
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print("post resp_json: " + pformat(resp_json))

    oid = str(resp_json["id"])
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ oid, headers=headers) 
    resp_json = resp.json()
    print("post resp_json: " + pformat(resp_json))

    resp_headers = resp.headers
    #Validate response
    assert resp.status_code == 200
    assert resp_json["name"] == "test"
    assert resp_json["env"] == "DEV"
    assert resp_json["status"] == "Active"
    assert resp_json["description"] == "test"
    assert resp_json["resources"][0]["ipaddress"] == "address1"
    assert resp_json["resources"][0]["name"] == "value1"
    assert resp_json["resources"][1]["ipaddress"] == "address2"
    assert resp_json["resources"][1]["name"] == "value2"
    assert resp_json["resources"][2]["ipaddress"] == "address3"
    assert resp_json["resources"][2]["name"] == "value3"

    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return oid

# test null resources
def post1():
    #Test POST Then GET
    # Body
    payload  =  {
        "solutionId": 0,
        "activatorId": 0,
        "name": "test",
        "env": "DEV",
        "status": "Active",
        "description": "test"
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    oid = str(resp_json["id"])
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url + oid, headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response
    assert resp.status_code == 200
    assert resp_json["name"] == "test"
    assert resp_json["env"] == "DEV"
    assert resp_json["status"] == "Active"
    assert resp_json["description"] == "test"
    assert resp_headers["content-type"] == "application/json"
    typestest(resp_json)
    return oid


def put(oid):

    # Test Update Then get new value
    newpayload  =  { "id": int(oid), "description": "test put", "status": "Inactive" }
    resp = requests.put(url+oid, headers=headers, data=json.dumps(newpayload,indent=4))

    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+oid, headers=headers)
    resp_json = resp.json()
    oid = resp_json["id"]

    
    print("resources: " + pformat(resp_json["resources"]))

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json["description"] == "test put"
    assert resp_json["status"] == "Inactive"



def delete(oid):

    #Test Delete Then GET
    resp = requests.delete(url+oid, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200

    #Then GET request to check the item has been actully deleted
    resp = requests.get(url+oid, headers=headers)
    #Validate Get response
    #resp_json = resp.json()
    assert resp.status_code == 404


def get_all():

    url = f"http://{HOUSTON_SERVICE_URL}/api/applications/"
    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200





