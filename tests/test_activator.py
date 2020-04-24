import requests
import json
import os
import pytest_lib
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/activator/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' } 
id = 0

def typestest(resp):
    assert type(resp['activator']) is str
    assert type(resp['activatorLink']) is str
    assert type(resp['apiManagement']) is list
    assert type(resp['available']) is bool
    assert type(resp['billing']) is str
    assert type(resp['category']) is str
    assert type(resp['ci']) is list
    assert type(resp['cd']) is list
    assert type(resp['description']) is str
    assert type(resp['envs']) is list
    assert type(resp['platforms']) is list
    assert type(resp['regions']) is list
    assert type(resp['sensitivity']) is str
    assert type(resp['serverCapacity']) is int
    assert type(resp['source']) is str
    assert type(resp['sourceControl']) is list
    assert type(resp['status']) is str
    assert type(resp['technologyOwner']) is str
    assert type(resp['technologyOwnerEmail']) is str
    assert type(resp['type']) is str
    assert type(resp['userCapacity']) is int
    pprint(resp)


def test_activators():
    #Testing POST request
    resp_json = post()
    id = str(resp_json['id'])
    #Testing Set Activator Status
    set_activator_status(resp_json['id'])
    #Testing PUT request
    put(id)
    #Testing DELETE request
    delete(id)
    #Testing GETALL request
    get_all()
    # Test GET Activator Meta
    get_meta()
    # Test Get Activator Categories
    get_categories()
    

def post():
    #Test POST Then GET
    # Body
    payload  =  {
        'accessRequestedBy': 0,
        'activator': 'test-activator',
        'activatorLink': 'string',
        'apiManagement': [ 'string', 'string1', 'string2', 'string3', 'string4', 'string5' ],
        'available': True,
        'billing': 'string',
        'businessUnit': 'string',
        'category': 'string',
        'cd': [ 'string1', 'string2', 'string3' ],
        'ci': [ 'string1', 'string2' ],
        'description': 'stringstringstringstringstringstringstringstring',
        'envs': [ 'dev', 'prd', 'poc' ],
        'hosting': [ 'string1', 'string2', 'string3', 'string4', 'string5' ],
        'id': 0,
        'lastUpdated': 'string',
        'name': 'string',
        'platforms': [ 'string1', 'string2', 'string3', 'string4', 'string5', 'string6' ],
        'regions': [ 'string1', 'string2', 'string3', 'string4', 'string5' ],
        'sensitivity': 'string',
        'serverCapacity': 999999999,
        'source': 'string',
        'sourceControl': [ 'string', 'string1' ],
        'status': 'Available',
        'technologyOwner': 'string',
        'technologyOwnerEmail': 'string',
        'type': 'string',
        'userCapacity': 999999999
        }
        
    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    assert resp_json['activator'] == 'test-activator'
    id = resp_json['id']
    print(id)
    

    resp = requests.get(url+ str(id), headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    
    #Validate response 
    assert resp.status_code == 200
    assert resp_json['activator'] == 'test-activator'
    assert resp_headers['content-type'] == 'application/json'
    assert type(resp_json['accessRequestedBy']) is type(None)
    typestest(resp_json)
    return resp_json


def set_activator_status(id):

    url = url = f"http://{HOUSTON_SERVICE_URL}/api/setactivatorstatus/"
    payload= {'accessRequestedBy': 0, 'id': id, 'status': 'Locked' }
    resp = requests.post(url, headers=headers , data= json.dumps(payload,indent=4))
    resp_json = resp.json()
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['id'] == id
    assert resp_json['status'] == 'Locked'


def put(id):

    # Test Update Then get new value
    newpayload = {
        'activator': 'new-test-activator',
        'accessRequestedBy': 0,
        'activatorLink': 'string',
        'apiManagement': [ 'string6', 'string7', 'string8' ],
        'available': False,
        'billing': 'billing',
        'businessUnit': 'businessUnit',
        'category': 'category',
        'cd': [ 'string4', 'string5', 'string6' ],
        'ci': [ 'string7', 'string8' ],
        'description': 'TheQuickBrownFoxJumpedOverTheLazyDogs',
        'envs': [ 'dev', 'Prd', 'Poc' ],
        'hosting': [ 'string11', 'string22', 'string33', 'string44', 'string55' ],
        'lastUpdated': 'fredbloggs',
        'name': 'mynewactivatortest',
        'platforms': [ 'string101', 'string102', 'string103', 'string104', 'string105', 'string106' ],
        'regions': [ 'string101', 'string210', 'string310', 'string410', 'string510' ],
        'sensitivity': 'confidential',
        'serverCapacity': 5,
        'source': 'original',
        'sourceControl': [ 'dotmatrix', 'tape' ],
        'status': 'NotAvailable',
        'technologyOwner': 'me',
        'technologyOwnerEmail': 'me@me.com',
        'type': 'best',
        'userCapacity': 10
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
    assert resp_json['activator'] == 'new-test-activator'
    typestest(resp_json)


def delete(id):

    #Test Delete Then GET
    resp = requests.delete(url+id, headers=headers) 
    assert resp.status_code == 200

    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    #Todo Ideally we should get 404 Need to check with Karwoo
    assert resp.status_code == 404


def get_all():
    
    geturl = f"http://{HOUSTON_SERVICE_URL}/api/activators/"
    resp = requests.get(geturl, headers=headers)  
    assert resp.status_code == 200


def get_meta():

    url = f"http://{HOUSTON_SERVICE_URL}/api/activator_meta/"
    resp = requests.get(url, headers=headers)  
    resp_json = resp.json()
    count = resp_json['count']
    #Validate response
    assert resp.status_code == 200
    assert count >=0


def get_categories():

    url = f"http://{HOUSTON_SERVICE_URL}/api/activatorcategories/"
    resp = requests.get(url, headers=headers)  
    pprint(resp.json())
    #Validate response
    assert resp.status_code == 200

