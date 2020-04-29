import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployment/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

def typestest_solution_deployment(resp):
    assert isinstance(resp['id'], int)
    assert isinstance(resp['deployed'], bool)
    assert isinstance(resp['deploymentState'], str)
    assert isinstance(resp['statusCode'], str)
    assert isinstance(resp['statusMessage'], str)
    assert isinstance(resp['statusId'], int)
    pprint(resp)


def test_solutiondeployment():

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
      "id": 1
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    print(pprint(resp))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = str(resp_json['id'])
    assert resp.status_code == 201
    assert resp.headers['content-type'] == 'application/json'
    pprint(resp.json())
    typestest_solution_deployment(resp_json)

    #Get Request to get updated values
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
      "id": int(id),
      "deployed": true,
      "deploymentState": "Deployed",
      "statusCode": "12",
      "statusId": 1,
      "statusMessage": "I just deployed again"
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
    assert resp_json['deployed'] == true
    assert resp_json['deploymentState'] == 'Deployed'
    assert resp_json['statusCode'] == '12'
    assert resp_json['statusId'] == 1
    assert resp_json['statusMessage'] == 'I just deployed again'
    typestest_solution_deployment(resp_json)


def get_all():
    print("get_all Tests")

    url = 'http://localhost:3000/api/solutiondeployments/'
    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200





