import requests
import json


url = 'http://localhost:3000/api/keyValues/bgproutingmode/'
    
# Additional headers.
headers = {'Content-Type': 'application/json' } 
id = 0

def test_bpgroutingmode():
    #Testing POST request
    id = post()
    #Testing PUT request
    put(id)
    #Testing DELETE request
    delete(id)
    #Testing GETALL request
    get_all()
    # Test GET Activator Meta

    

def post():
    #Test POST Then GET
    # Body
    payload  =  { 'id': 0, 'key': 'Local', 'value': 'Local' }

    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    id = str(resp_json['id'])
    assert resp.status_code == 201

    resp = requests.get(url+ id, headers=headers) 
    resp_json = resp.json()
    resp_headers = resp.headers
    
    #Validate response 
    assert resp.status_code == 200
    assert resp_json['key'] == 'Local'
    assert resp_json['value'] == 'Local'
    assert resp_headers['content-type'] == 'application/json'
    return id


def put(id):
    # Test Update Then get new value
    newpayload  =  { 'id': int(id), 'key': 'new-key', 'value': 'new-value' }
    resp = requests.put(url+id, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response 
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+id, headers=headers) 
    resp_json = resp.json()
    id = resp_json['id']

    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['key'] == 'new-key'
    assert resp_json['value'] == 'new-value'



def delete(id):
    #Test Delete Then GET
    resp = requests.delete(url+id, headers=headers) 
    #Validate Delete response
    assert resp.status_code == 200
    
    #Then GET request to check the item has been actully deleted
    resp = requests.get(url+id, headers=headers) 
    #Validate Get response
    resp_json = resp.json()
    assert resp.status_code == 404


def get_all():
    url = 'http://localhost:3000/api/keyValues/bgproutingmode/'
    resp = requests.get(url, headers=headers)  
    #Validate Get All response
    assert resp.status_code == 200





