import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/solutionresource/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

def typestest_solution_resource(resp):
    assert isinstance(resp['id'], int)
    assert isinstance(resp['solutionId'], int)
    assert isinstance(resp['key'], str)
    assert isinstance(resp['value'], str)
    pprint(resp)


def test_solutionresource():

    #Testing POST request
    id = post()
    #Testing PUT request
    put(id)
    #Testing GETALL request
    get_all()
    

def post():
    print("Post Tests")
    #Test POST Then GET
    # Body
    payload  =  {
      "solutionId": 1,
      "key": "key 1",
      "value": "value 1"
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    print(pprint(resp))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()

    assert resp_json['solutionId'] == 1
    assert resp_json['key'] == "key 1"
    assert resp_json['value'] == "value 1"

    assert resp.status_code == 201
    assert resp.headers['content-type'] == 'application/json'
    pprint(resp.json())
    typestest_solution_resource(resp_json)

    #Get Request to get updated values
    id = str(resp_json['id'])
    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    print("solution_post")
    pprint(resp_json)

    return id


def put(id):
    print("Put Tests")

    true = 1 == 1
    # Test Update Then get new value
    newpayload  =  {
      "solutionId": 2,
      "key": "key put 1",
      "value": "value put 1"
    }

    print("url: " + url)
    resp = requests.put(url+id, headers=headers, data=json.dumps(newpayload,indent=4))
    resp_json = resp.json()
    typestest_solution_resource(resp_json)
    assert resp_json['solutionId'] == 2
    assert resp_json['key'] == "key put 1"
    assert resp_json['value'] == "value put 1"

    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+id, headers=headers)
    resp_json = resp.json()

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['solutionId'] == 2
    assert resp_json['key'] == 'key put 1'
    assert resp_json['value'] == 'value put 1'
    typestest_solution_resource(resp_json)


def get_all():
    print("get_all Tests")

    url = 'http://localhost:3000/api/solutionresources/'
    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200
