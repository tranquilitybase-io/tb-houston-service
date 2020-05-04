
import requests
import json
import os
from pprint import pprint


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/solutionresourcejson/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }
id = 0

my_json = {'lineage': '7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c',
 'outputs': {},
 'resources': [{'instances': [{'attributes': {'create_time': '2020-04-30T13:51:27.390Z',
                                              'display_name': 'sol22 - '
                                                              'ksjs726s',
                                              'id': 'folders/615899412414',
                                              'lifecycle_state': 'ACTIVE',
                                              'name': 'folders/615899412414',
                                              'parent': 'folders/943956663445',
                                              'timeouts': None},
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0=',
                               'schema_version': 0}],
                'mode': 'managed',
                'module': 'module.solution_folder',
                'name': 'solution_folder',
                'provider': 'provider.google',
                'type': 'google_folder'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-dev-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-dev-env',
                                              'number': '6570889872',
                                              'org_id': '',
                                              'project_id': 'sol22-dev-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.dev_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-prod-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-prod-env',
                                              'number': '1072288444773',
                                              'org_id': '',
                                              'project_id': 'sol22-prod-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.prod_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-staging-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-staging-env',
                                              'number': '292492613552',
                                              'org_id': '',
                                              'project_id': 'sol22-staging-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.staging_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-workspace-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-workspace',
                                              'number': '555918489693',
                                              'org_id': '',
                                              'project_id': 'sol22-workspace-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.workspace_project',
                'name': 'workspace_project',
                'provider': 'provider.google',
                'type': 'google_project'}],
 'serial': 1,
 'terraform_version': '0.12.24',
 'version': 4}

my_json2 = {'lineage': '7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c',
 'outputs': {},
 'resources': [{'instances': [{'attributes': {'create_time': '2020-04-30T13:51:27.390Z',
                                              'display_name': 'sol22 - '
                                                              'ksjs726s',
                                              'id': 'folders/615899412414',
                                              'lifecycle_state': 'ACTIVE',
                                              'name': 'folders/615899412414',
                                              'parent': 'folders/943956663445',
                                              'timeouts': None},
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0=',
                               'schema_version': 0}],
                'mode': 'managed',
                'module': 'module.solution_folder',
                'name': 'solution_folder',
                'provider': 'provider.google',
                'type': 'google_folder'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-dev-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-dev-env',
                                              'number': '6570889872',
                                              'org_id': '',
                                              'project_id': 'sol23-dev-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.dev_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-prod-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-prod-env',
                                              'number': '1072288444773',
                                              'org_id': '',
                                              'project_id': 'sol23-prod-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.prod_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-staging-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-staging-env',
                                              'number': '292492613552',
                                              'org_id': '',
                                              'project_id': 'sol23-staging-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.staging_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-workspace-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-workspace',
                                              'number': '555918489693',
                                              'org_id': '',
                                              'project_id': 'sol23-workspace-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.workspace_project',
                'name': 'workspace_project',
                'provider': 'provider.google',
                'type': 'google_project'}],
 'serial': 1,
 'terraform_version': '0.12.24',
 'version': 4}

my_json_s = str(json.dumps(my_json, separators=(',', ':')))
my_json_s2 = str(json.dumps(my_json2, separators=(',', ':')))

print(my_json_s)

def typestest_solution_resource_json(resp):
    assert isinstance(resp['solutionId'], int)
    assert isinstance(resp['json'], str)
    pprint(resp)


def test_solutionresourcejson():

    #Testing POST request - create + update existing row
    id1 = post()
    #Testing GET ALL request
    get_all()
    #Testing DELETE request
    delete(id1)
    post2()
    post3()
    post4()
    

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
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    print(pprint(resp_json))

    assert resp_json['solutionId'] == 1
    assert resp_json['json'] == my_json_s

    assert resp.status_code == 201
    assert resp.headers['content-type'] == 'application/json'
    pprint(resp.json())
    typestest_solution_resource_json(resp_json)

    #Get Request to get updated values
    solutionId = str(resp_json['solutionId'])
    resp = requests.get(url+solutionId, headers=headers) 
    resp_json = resp.json()
    assert resp_json['solutionId'] == 1
    assert resp_json['json'] == my_json_s
    print("solution_response_json_post")
    pprint(resp_json)

    return solutionId


def post2():
    print("Post 2 Test")

    # Test Update 
    payload  =  {
      "solutionId": 2,
      "json": my_json_s
    }

    print("url: " + url)
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json['solutionId'] == 2
    assert resp_json['json'] == my_json_s

    #Validate update/Put response
    assert resp.status_code == 201

    #Get Request to get updated values
    solutionId = str(resp_json['solutionId'])
    resp = requests.get(url+solutionId, headers=headers)
    resp_json = resp.json()

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['solutionId'] == 2
    assert resp_json['json'] == my_json_s
    typestest_solution_resource_json(resp_json)


def post3():
    print("Post 3 Test")

    # Test Update 
    payload  =  {
      "solutionId": 3,
      "json": my_json_s
    }

    print("url: " + url)
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json['solutionId'] == 3
    assert resp_json['json'] == my_json_s

    #Validate update/Put response
    assert resp.status_code == 201

    #Get Request to get updated values
    solutionId = str(resp_json['solutionId'])
    resp = requests.get(url+solutionId, headers=headers)
    resp_json = resp.json()

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['solutionId'] == 3
    assert resp_json['json'] == my_json_s
    typestest_solution_resource_json(resp_json)


def post4():
    print("Post 4 Test")

    # Test Update 
    payload  =  {
      "solutionId": 4,
      "json": my_json_s2
    }

    print("url: " + url)
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    resp_json = resp.json()
    typestest_solution_resource_json(resp_json)
    assert resp_json['solutionId'] == 4
    assert resp_json['json'] == my_json_s2

    #Validate update/Put response
    assert resp.status_code == 201

    #Get Request to get updated values
    solutionId= str(resp_json['solutionId'])
    resp = requests.get(url+solutionId, headers=headers)
    resp_json = resp.json()

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['solutionId'] == 4
    assert resp_json['json'] == my_json_s2
    typestest_solution_resource_json(resp_json)
    

def delete(solutionId):
    print("Delete Tests")

    #Test Delete Then GET
    resp = requests.delete(url+solutionId, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200

    #Then GET request to check the item has been actully deleted
    resp = requests.get(url+solutionId, headers=headers)
    #Validate Get response
    #resp_json = resp.json()
    assert resp.status_code == 404


def get_all():
    print("get_all Tests")

    url = 'http://localhost:3000/api/solutionresourcejsons/'
    resp = requests.get(url, headers=headers)
    #Validate Get All response
    assert resp.status_code == 200
