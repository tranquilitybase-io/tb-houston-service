
import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/solutionresourcejson/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

my_json = """
{"version": 4,"terraform_version": "0.12.24","serial": 1,"lineage": "7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c","outputs": {},"resources": [{"module": "module.solution_folder","mode": "managed","type": "google_folder","name": "solution_folder","provider": "provider.google","instances": [{"schema_version": 0,"attributes": {"create_time": "2020-04-30T13:51:27.390Z","display_name": "sol22 - ksjs726s","id": "folders/615899412414","lifecycle_state": "ACTIVE","name": "folders/615899412414","parent": "folders/943956663445","timeouts": null},"private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0="}]},{"module": "module.dev_environment","mode": "managed","type": "google_project","name": "environment_project","provider": "provider.google","instances": [{"schema_version": 1,"attributes": {"auto_create_network": true,"billing_account": null,"folder_id": "615899412414","id": "projects/sol22-dev-env-ksjs726s","labels": null,"name": "sol22-dev-env","number": "6570889872","org_id": "","project_id": "sol22-dev-env-ksjs726s","skip_delete": null,"timeouts": null},"private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=","dependencies": ["module.solution_folder.google_folder.solution_folder"]}]},{"module": "module.prod_environment","mode": "managed","type": "google_project","name": "environment_project","provider": "provider.google","instances": [{"schema_version": 1,"attributes": {"auto_create_network": true,"billing_account": null,"folder_id": "615899412414","id": "projects/sol22-prod-env-ksjs726s","labels": null,"name": "sol22-prod-env","number": "1072288444773","org_id": "","project_id": "sol22-prod-env-ksjs726s","skip_delete": null,"timeouts": null},"private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=","dependencies": ["module.solution_folder.google_folder.solution_folder"]}]},{"module": "module.staging_environment","mode": "managed","type": "google_project","name": "environment_project","provider": "provider.google","instances": [{"schema_version": 1,"attributes": {"auto_create_network": true,"billing_account": null,"folder_id": "615899412414","id": "projects/sol22-staging-env-ksjs726s","labels": null,"name": "sol22-staging-env","number": "292492613552","org_id": "","project_id": "sol22-staging-env-ksjs726s","skip_delete": null,"timeouts": null},"private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=","dependencies": ["module.solution_folder.google_folder.solution_folder"]}]},{"module": "module.workspace_project","mode": "managed","type": "google_project","name": "workspace_project","provider": "provider.google","instances": [{"schema_version": 1,"attributes": {"auto_create_network": true,"billing_account": null,"folder_id": "615899412414","id": "projects/sol22-workspace-ksjs726s","labels": null,"name": "sol22-workspace","number": "555918489693","org_id": "","project_id": "sol22-workspace-ksjs726s","skip_delete": null,"timeouts": null},"private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=","dependencies": ["module.solution_folder.google_folder.solution_folder"]}]}]}
"""

my_json_s = json.dumps(my_json)
print(my_json_s)

def typestest_solution_resource_json(resp):
    assert isinstance(resp['id'], int)
    assert isinstance(resp['solutionId'], int)
    assert isinstance(resp['json'], str)
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
      "json": my_json_s,
    }

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    print(pprint(resp))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()

    assert resp_json['solutionId'] == 1
    assert resp_json['json'] == my_json_s

    assert resp.status_code == 201
    assert resp.headers['content-type'] == 'application/json'
    pprint(resp.json())
    typestest_solution_resource_json(resp_json)

    #Get Request to get updated values
    id = str(resp_json['id'])
    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    print("solution_response_json_post")
    pprint(resp_json)

    return id


def put(id):
    print("Put Tests")

    true = 1 == 1
    # Test Update Then get new value
    newpayload  =  {
      "solutionId": 2,
      "json": my_json_s
    }

    print("url: " + url)
    resp = requests.put(url+id, headers=headers, data=json.dumps(newpayload,indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json['solutionId'] == 2
    assert resp_json['json'] == my_json_s

    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+id, headers=headers)
    resp_json = resp.json()

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['solutionId'] == 2
    assert resp_json['json'] == my_json_s
    typestest_solution_resource_json(resp_json)


def get_all():
    print("get_all Tests")

    url = 'http://localhost:3000/api/solutionresourcejsons/'
    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200
