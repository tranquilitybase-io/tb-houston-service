import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/solution/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

def typestest(resp):
    assert isinstance(resp['active'], bool)
    assert isinstance(resp['businessUnit'], str)
    assert isinstance(resp['ci'], str)
    assert isinstance(resp['cd'], str)
    assert isinstance(resp['costCentre'], str)
    assert isinstance(resp['description'], str)
    assert isinstance(resp['environments'], list)
    assert isinstance(resp['favourite'], bool)
    assert isinstance(resp['id'], int)
    assert isinstance(resp['lastUpdated'], str)
    assert isinstance(resp['name'], str)
    assert isinstance(resp['sourceControl'], str)
    assert isinstance(resp['teamId'], int)
    pprint(resp)


def test_solution():

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
    payload  =  {
      "active": true,
      "businessUnit": "test",
      "cd": "test",
      "ci": "test",
      "costCentre": "test",
      "description": "test",
      "environments": [ "test" ],
      "favourite": true,
      "id": 0,
      "lastUpdated": "test",
      "name": "test",
      "sourceControl": "test",
      "teamId": 1
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = str(resp_json['id'])
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ id, headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response
    assert resp.status_code == 200
    assert resp_json['name'] == 'test'
    assert resp_json['businessUnit'] == 'test'
    assert resp_json['description'] == 'test'
    assert resp_headers['content-type'] == 'application/json'
    typestest(resp_json)
    return id


def put(id):
    print("Put Tests")

    true = 1 == 1
    # Test Update Then get new value
    newpayload  =  {
      "id": int(id),
      "active": true,
      "businessUnit": "test put",
      "cd": "test put",
      "ci": "test put",
      "costCentre": "test put",
      "description": "test put",
      "environments": [ "test put 1", "test put 2", "test put 3" ],
      "favourite": true,
      "lastUpdated": "test put",
      "name": "test put",
      "sourceControl": "test put"
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
    assert resp_json['name'] == 'test put'
    assert resp_json['description'] == 'test put'
    assert resp_json['businessUnit'] == 'test put'
    assert resp_json['ci'] == 'test put'
    assert resp_json['cd'] == 'test put'
    assert resp_json['sourceControl'] == 'test put'
    assert resp_json['environments'][0] == 'test put 1'
    assert resp_json['environments'][1] == 'test put 2'
    assert resp_json['environments'][2] == 'test put 3'
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

    url = f"http://{HOUSTON_SERVICE_URL}/api/solutions/"
    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200





