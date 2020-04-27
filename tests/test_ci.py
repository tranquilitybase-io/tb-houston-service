import requests
import json
import logging
import os
LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/keyValues/ci/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }

#key = 'test/'
           
def test_post():

    #Test POST Then GET
    # Body
    payload = {'key': 'test', 'value': 'test-post-value'}
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    assert resp_json['key'] == 'test'
    assert resp_json['value'] == 'test-post-value'
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+'test', headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response
    assert resp.status_code == 200
    assert resp_json['key'] == 'test'
    assert resp_json['value'] == 'test-post-value'
    assert resp_headers['content-type'] == 'application/json'


def test_put():

    # Test Update Then get new value
    newpayload = {'key': 'test', 'value': 'new-test-value'}
    resp = requests.put(url+'test', headers=headers, data=json.dumps(newpayload,indent=4))

    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+'test', headers=headers)
    resp_json = resp.json()

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['key'] == 'test'
    assert resp_json['value'] == 'new-test-value'


def test_delete():

    #Test Delete Then GET
    resp = requests.delete(url+'test', headers=headers)
    assert resp.status_code == 200

def test_delete_error():

    #Test Delete for an non existing item
    resp = requests.delete(url+'test', headers=headers)
    assert resp.status_code == 404

def test_get_error():

    resp = requests.get(url+'test', headers=headers)
    #resp_json = resp.json()
    assert resp.status_code == 404

def test_get_all():

    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
