import requests
import json
import logging
import os
from pprint import pprint


LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/team/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

def typestest(resp):
    assert isinstance(resp['businessUnitId'], int)
    assert isinstance(resp['description'], str)
    assert isinstance(resp['id'], int)
    assert isinstance(resp['isActive'], bool)
    assert isinstance(resp['name'], str)
    pprint(resp)


def test_team():

    #Testing POST request
    id = post()
    #Testing PUT request
    put(id)
    #Testing DELETE request
    delete(id)
    #Testing GETALL request
    get_all()
    # Test GET Activator Meta

    

def post():
    print("Post Tests")
    #Test POST Then GET
    # Body
    true = 1 == 1
    payload = { 
    "businessUnitId": 0,
    "description": "Test Team",
    "id": 0,
    "isActive": True,
    "name": "Team-Test"
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    id = str(resp_json['id'])
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ id, headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response
    assert resp.status_code == 200
    assert resp_json['name'] == 'Team-Test'
    assert resp_json['businessUnitId'] == 0
    assert resp_json['description'] == 'Test Team'
    assert resp_headers['content-type'] == 'application/json'
    typestest(resp_json)
    return id


def put(id):
    print("Put Tests")

    true = 1 == 1
    # Test Update Then get new value
    newpayload  =  { 
    "businessUnitId": 0,
    "description": "Test Team",
    "id": int(id),
    "isActive": False,
    "name": "Team-Test-Updated"
    }

    resp = requests.put(url+id, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    id = resp_json['id']

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['name'] == 'Team-Test-Updated'
    assert resp_json['description'] == 'Test Team'
    assert resp_json['isActive'] == False

    typestest(resp_json)



def delete(id):
    print("Delete Tests")

    #Test Delete Then GET
    resp = requests.delete(url+id, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200
    
    #Then GET request to check the item has been actully deleted
    resp = requests.get(url+id, headers=headers)
    #Validate Get response
    #resp_json = resp.json()
    assert resp.status_code == 404


def get_all():
    print("get_all Tests")

    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200

