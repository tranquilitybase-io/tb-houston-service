import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/application/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' } 
id = 0

def typestest(resp):
    assert type(resp['activatorId']) is int
    assert type(resp['description']) is str
    assert type(resp['env']) is str
    assert type(resp['id']) is int
    assert type(resp['name']) is str
    assert type(resp['resources']) is list
    assert type(resp['solutionId']) is int
    assert type(resp['status']) is str
    pprint(resp)


def test_application():

    #Testing POST request
    id = post()
    #Testing PUT request
    put(id)
    #Testing DELETE request
    delete(id)
    #Testing GETALL request
    get_all()
    # Test post with no resources
    id = post1()

    

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
            { "ipaddress": "string", "name": "string" },
            { "ipaddress": "string", "name": "string" },
            { "ipaddress": "string", "name": "string" }
        ]
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
    assert resp_json['env'] == 'DEV'
    assert resp_json['status'] == 'Active'
    assert resp_json['description'] == 'test'
    assert resp_headers['content-type'] == 'application/json'
    typestest(resp_json)
    return id

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
    id = str(resp_json['id'])
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ id, headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response 
    assert resp.status_code == 200
    assert resp_json['name'] == 'test'
    assert resp_json['env'] == 'DEV'
    assert resp_json['status'] == 'Active'
    assert resp_json['description'] == 'test'
    assert resp_headers['content-type'] == 'application/json'
    typestest(resp_json)
    return id


def put(id):

    # Test Update Then get new value
    newpayload  =  { 'id': int(id), 'description': 'test put', 'status': 'Inactive' }
    resp = requests.put(url+id, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response 
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    id = resp_json['id']

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['description'] == 'test put'
    assert resp_json['status'] == 'Inactive'



def delete(id):

    #Test Delete Then GET
    resp = requests.delete(url+id, headers=headers) 
    #Validate Delete response
    assert resp.status_code == 200
    
    #Then GET request to check the item has been actully deleted
    resp = requests.get(url+id, headers=headers) 
    #Validate Get response
    resp_json = resp.json()
    assert resp.status_code == 404


def get_all():

    url = 'http://localhost:3000/api/applications/'
    resp = requests.get(url, headers=headers)  
    #Validate Get All response
    assert resp.status_code == 200





