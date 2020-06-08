import requests
import json
import os


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/landingzoneaction/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

def test_landingzoneaction():
    
    #Testing POST request
    resp_json = post()
    id = str(resp_json['id'])
    #Testing PUT request
    put(id)
    #Testing DELETE request
    delete(id)
    #Testing DELETE Request Error
    delete_error(id)
    #Testing GETALL request
    get_all()
    

def post():

    #Test POST Then GET
    # Body
    payload  =    {
    'categoryClass': 'test-folder-structure',
    'categoryName': 'testCategory',
    'completionRate': 100,
    'id': 0,
    'locked': False,
    'routerLink': 'testLink',
    'title': 'Test Landing Zone'
  }
  
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = resp_json['id']
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ str(id), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate GET response
    assert resp.status_code == 200
    assert resp_json['categoryClass'] == 'test-folder-structure'
    assert resp_json['categoryName'] == 'testCategory'
    assert resp_json['completionRate'] == 100
    assert resp_json['locked'] == False
    assert resp_json['routerLink'] == 'testLink'
    assert resp_json['title'] == 'Test Landing Zone'
    assert resp_headers['content-type'] == 'application/json'

    return resp_json


def put(id):

    # Test Update Then get updated value
    newpayload = {
    'categoryClass': 'test-folder-structure',
    'categoryName': 'testCategory',
    'completionRate': 100,
    'id': int(id),
    'locked': True,
    'routerLink': 'testLink',
    'title': 'Test Landing Zone'
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
    assert resp_json['locked'] == True


def delete(id):

    # Delete Request
    resp = requests.delete(url+id, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200
    
    #Then Get request to check the item has been actully deleted
    resp = requests.get(url+id, headers=headers)
    #Validate Get response
    #resp_json = resp.json()
    assert resp.status_code == 404


def delete_error(id):

    # Delete Request for a non existing item
    resp = requests.delete(url+id, headers=headers)
    #resp_json = resp.json()
    #resp_headers = resp.headers
    #Validate response ; expect Not found
    assert resp.status_code == 404


def get_all():
    local_url = f"http://{HOUSTON_SERVICE_URL}/api/landingzoneactions/"
    resp = requests.get(local_url, headers=headers)
    assert resp.status_code == 200
