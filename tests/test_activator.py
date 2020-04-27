import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/activator/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }

def typestest(resp):
    assert isinstance(resp['activator'], str)
    assert isinstance(resp['activatorLink'], str)
    assert isinstance(resp['apiManagement'], list)
    assert isinstance(resp['available'], bool)
    assert isinstance(resp['billing'], str)
    assert isinstance(resp['category'], str)
    assert isinstance(resp['ci'], list)
    assert isinstance(resp['cd'], list)
    assert isinstance(resp['description'], str)
    assert isinstance(resp['envs'], list)
    assert isinstance(resp['platforms'], list)
    assert isinstance(resp['regions'], list)
    assert isinstance(resp['sensitivity'], str)
    assert isinstance(resp['serverCapacity'], int)
    assert isinstance(resp['source'], str)
    assert isinstance(resp['sourceControl'], list)
    assert isinstance(resp['status'], str)
    assert isinstance(resp['technologyOwner'], str)
    assert isinstance(resp['technologyOwnerEmail'], str)
    assert isinstance(resp['type'], str)
    assert isinstance(resp['userCapacity'], int)
    pprint(resp)


def test_activators():
    #Testing POST request
    resp_json = post()
    oid = str(resp_json['id'])
    #Testing Set Activator Status
    set_activator_status(resp_json['id'])
    #Testing PUT request
    put(oid)
    #Testing DELETE request
    delete(oid)
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
        'activatorLink': 'test-post-',
        'apiManagement': [ 'test-post-', 'test-post-1', 'test-post-2', 'test-post-3', 'test-post-4', 'test-post-5' ],
        'available': True,
        'billing': 'test-post-',
        'businessUnit': 'test-post-',
        'category': 'test-post-',
        'cd': [ 'test-post-1', 'test-post-2', 'test-post-3' ],
        'ci': [ 'test-post-1', 'test-post-2' ],
        'description': 'test-post-test-post-test-post-test-post-test-post-test-post-test-post-test-post-',
        'envs': [ 'dev', 'prd', 'poc' ],
        'hosting': [ 'test-post-1', 'test-post-2', 'test-post-3', 'test-post-4', 'test-post-5' ],
        'id': 0,
        'lastUpdated': 'test-post-',
        'name': 'test-post-',
        'platforms': [ 'test-post-1', 'test-post-2', 'test-post-3', 'test-post-4', 'test-post-5', 'test-post-6' ],
        'regions': [ 'test-post-1', 'test-post-2', 'test-post-3', 'test-post-4', 'test-post-5' ],
        'sensitivity': 'test-post-',
        'serverCapacity': 999999999,
        'source': 'test-post-',
        'sourceControl': [ 'test-post-', 'test-post-1' ],
        'status': 'Available',
        'technologyOwner': 'test-post-',
        'technologyOwnerEmail': 'test-post-',
        'type': 'test-post-',
        'userCapacity': 999999999
        }
        
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    assert resp_json['activator'] == 'test-activator'
    oid = resp_json['id']
    print(oid)
    

    resp = requests.get(url+ str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    
    #Validate response
    assert resp.status_code == 200
    assert resp_json['activator'] == 'test-activator'
    assert resp_headers['content-type'] == 'application/json'
    assert isinstance(resp_json['accessRequestedBy'], type(None))
    typestest(resp_json)
    return resp_json


def set_activator_status(oid):

    url = url = f"http://{HOUSTON_SERVICE_URL}/api/setactivatorstatus/"
    payload= {'accessRequestedBy': 0, 'id': oid, 'status': 'Locked' }
    resp = requests.post(url, headers=headers , data= json.dumps(payload,indent=4))
    resp_json = resp.json()
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['id'] == oid
    assert resp_json['status'] == 'Locked'


def put(oid):

    # Test Update Then get new value
    newpayload = {
        'activator': 'new-test-activator',
        'accessRequestedBy': 0,
        'activatorLink': 'test-put-',
        'apiManagement': [ 'test-put-6', 'test-put-7', 'test-put-8' ],
        'available': False,
        'billing': 'billing',
        'businessUnit': 'businessUnit',
        'category': 'category',
        'cd': [ 'test-put-4', 'test-put-5', 'test-put-6' ],
        'ci': [ 'test-put-7', 'test-put-8' ],
        'description': 'TheQuickBrownFoxJumpedOverTheLazyDogs',
        'envs': [ 'dev', 'Prd', 'Poc' ],
        'hosting': [ 'test-put-11', 'test-put-22', 'test-put-33', 'test-put-44', 'test-put-55' ],
        'lastUpdated': 'fredbloggs',
        'name': 'mynewactivatortest',
        'platforms': [ 'test-put-101', 'test-put-102', 'test-put-103', 'test-put-104', 'test-put-105', 'test-put-106' ],
        'regions': [ 'test-put-101', 'test-put-210', 'test-put-310', 'test-put-410', 'test-put-510' ],
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
    resp = requests.put(url+oid, headers=headers, data=json.dumps(newpayload,indent=4))

    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+oid, headers=headers)
    resp_json = resp.json()
    oid = resp_json['id']

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['activator'] == 'new-test-activator'
    typestest(resp_json)


def delete(oid):

    #Test Delete Then GET
    resp = requests.delete(url+oid, headers=headers)
    assert resp.status_code == 200

    resp = requests.get(url+oid, headers=headers)
    #resp_json = resp.json()
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
