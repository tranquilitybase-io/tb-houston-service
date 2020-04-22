import requests
import json
import os


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/keyValues/vpnonpremisevendor/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' } 
id = 0

def test_vpnonpremisevendor():

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
    payload  =  {'key': 'test' , 'value': 'test-value'}
  
    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = resp_json['id']
    assert resp.status_code == 201
    assert resp_json['key'] == 'test'   
    assert resp_json['value'] == 'test-value'

    resp = requests.get(url+ str(id), headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    
    #Validate response 
    assert resp.status_code == 200
    assert resp_json['key'] == 'test'
    assert resp_headers['content-type'] == 'application/json'
    return resp_json


def put(id):

    # Test Update Then get updated value
    newpayload = {'key': 'test', 'value': 'new-test-value'}
    resp = requests.put(url+id, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response 
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    id = resp_json['id']

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['value'] == 'new-test-value'


def delete(id):

    # Delete Request
    resp = requests.delete(url+id, headers=headers) 
    #Validate Delete response
    assert resp.status_code == 200
    #Then Get request to check the item has been actully deleted
    resp = requests.get(url+id, headers=headers) 
    #Validate Get response
    resp_json = resp.json()
    assert resp.status_code == 404



def delete_error(id):

    # Delete Request for a non existing item
    resp = requests.delete(url+id, headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response ; expect Not found
    assert resp.status_code == 404
    assert resp_json['detail'] == 'VPNOnPremiseVendor '+str(id)+' not found'
    assert resp_headers['content-type'] == 'application/problem+json'


def get_all():

    resp = requests.get(url, headers=headers)  
    assert resp.status_code == 200