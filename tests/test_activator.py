import requests
import json


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/activator/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' } 
id = 0

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
        'apiManagement': [
        {
        'api': 'string'
        }
        ],
        'available': True,
        'billing': 'string',
        'businessUnit': 'string',
        'category': 'string',
        'cd': [
            {
            'acd': 'string'
            }
        ],
        'ci': [
            {
            'aci': 'string'
            }
        ],
        'description': 'string',
        'envs': [
            {
            'env': 'string'
            }
        ],
        'hosting': [
            {
            'host': 'string'
            }
        ],
        'id': 0,
        'lastUpdated': 'string',
        'name': 'string',
        'platforms': [
            {
            'platform': 'string'
            }
        ],
        'regions': [
            {
            'region': 'string'
            }
        ],
        'resources': [
            {
            'ipaddress': 'string',
            'name': 'string'
            }
        ],
        'sensitivity': 'string',
        'serverCapacity': 0,
        'source': 'string',
        'sourceControl': [
            {
            'sc': 'string'
            }
        ],
        'status': 'Available',
        'technologyOwner': 'string',
        'technologyOwnerEmail': 'string',
        'type': 'string',
        'userCapacity': 0
        }

    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = resp_json['id']
    assert resp.status_code == 201
    assert resp_json['activator'] == 'test-activator'

    resp = requests.get(url+ str(id), headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    
    #Validate response 
    assert resp.status_code == 200
    assert resp_json['activator'] == 'test-activator'
    assert resp_headers['content-type'] == 'application/json'
    return resp_json


def set_activator_status(id):

    url = 'http://localhost:3000/api/setactivatorstatus/'
    payload= {'accessRequestedBy': 0, 'id': id, 'status': 'Locked' }
    resp = requests.post(url, headers=headers , data= json.dumps(payload,indent=4))
    resp_json = resp.json()
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['id'] == id
    assert resp_json['status'] == 'Locked'


def put(id):

    # Test Update Then get new value
    newpayload = {'activator': 'new-test-activator'}
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


def delete(id):

    #Test Delete Then GET
    resp = requests.delete(url+id, headers=headers) 
    assert resp.status_code == 200

    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    #Todo Ideally we should get 404 Need to check with Karwoo
    assert resp.status_code == 500


def get_all():
    
    geturl = 'http://localhost:3000/api/activators/'
    resp = requests.get(geturl, headers=headers)  
    assert resp.status_code == 200


def get_meta():

    url = 'http://localhost:3000/api/activator_meta/'
    resp = requests.get(url, headers=headers)  
    resp_json = resp.json()
    count = resp_json['count']
    #Validate response
    assert resp.status_code == 200
    assert count >=0


def get_categories():

    url = 'http://localhost:3000/api/activatorcategories/'
    resp = requests.get(url, headers=headers)  
    #Validate response
    assert resp.status_code == 200







