import requests
import json
import os


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/landingzoneprogressitem/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }

def test_vpnonpremisevendor():
    
    #Testing POST request
    resp_json = post()
    oid = str(resp_json['id'])
    #Testing PUT request
    put(oid)
    #Testing DELETE request
    delete(oid)
    #Testing DELETE Request Error
    delete_error(oid)
    #Testing GETALL request
    get_all()
    

def post():

    #Test POST Then GET
    # Body
    payload  =    { 'completed': True, 'id': 0, 'label': 'Testing-post' }
  
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    oid = resp_json['id']
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate GET response
    assert resp.status_code == 200
    assert resp_json['completed'] == True
    assert resp_json['label'] == 'Testing-post'
    assert resp_headers['content-type'] == 'application/json'

    return resp_json


def put(oid):

    # Test Update Then get updated value
    newpayload = { 'completed': False, 'id': int(oid), 'label': 'Testing-post' }
  
    resp = requests.put(url+oid, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+oid, headers=headers)
    resp_json = resp.json()
    oid = resp_json['id']
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['completed'] == False


def delete(oid):

    # Delete Request
    resp = requests.delete(url+oid, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200
    
    #Then Get request to check the item has been actully deleted
    resp = requests.get(url+oid, headers=headers)
    #Validate Get response
    #resp_json = resp.json()
    assert resp.status_code == 404


def delete_error(oid):

    # Delete Request for a non existing item
    resp = requests.delete(url+oid, headers=headers)
    #resp_json = resp.json()
    #resp_headers = resp.headers
    #Validate response ; expect Not found
    assert resp.status_code == 404


def get_all():

    url = f"http://{HOUSTON_SERVICE_URL}/api/landingzoneprogressitems/"
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
