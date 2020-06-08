import requests
import json
from tests import pytest_lib 
    
url = f"http://{pytest_lib.HOUSTON_SERVICE_URL}/api/lzmetadata_lan_vpc/"
test_name = "testing_999999999"

def test_main():
    
    pytest_lib.get_all(url)
    #Testing POST request
    post()
    #Testing PUT request
    put()
    #Testing DELETE request
    pytest_lib.logical_delete(url, test_name)
    #Testing DELETE Request Error
    pytest_lib.delete_error(url, "-1")
    #Testing GETALL request
    pytest_lib.get_all(url)
    

def post():

    #Test POST Then GET
    # Body
    payload = { "isActive": True, "description": "Landing Zone metadata for LAN VPC of TEST environment", "name": test_name, "value": [ "Test", "Unit Testing" ] }
  
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url+test_name, headers=pytest_lib.headers, data=json.dumps(payload))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(f"resp_json: {resp_json}")
    print(f"url: {url}")
    print(f"payload: {json.dumps(payload)}")
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url + test_name, headers=pytest_lib.headers)
    resp_json = resp.json()
    #resp_headers = resp.headers
    #Validate GET response
    assert resp.status_code == 200
    assert resp_json['name'] == test_name
    assert resp_json['description'] == 'Landing Zone metadata for LAN VPC of TEST environment'
    assert resp_json['isActive'] == True
    assert resp_json['value'] == ['Test', 'Unit Testing']


def put():

    # Test Update Then get updated value
    payload = { "isActive": False, "description": "Landing Zone metadata for LAN VPC of Staging environment", "name": test_name, "value": [ "StagingTest", "Staging Unit Testing" ] }

    #Put Request to update values
    resp = requests.post(url + test_name, data=json.dumps(payload), headers=pytest_lib.headers)
    resp_json = resp.json()
    #Validate response body for updated values
    assert resp.status_code == 201
    assert resp_json['name'] == test_name
    assert resp_json['description'] == 'Landing Zone metadata for LAN VPC of Staging environment'
    assert resp_json['isActive'] == False
    assert resp_json['value'] == ['StagingTest', 'Staging Unit Testing']
