import requests
import json

def testBusinessUnit():
    url = 'http://localhost:3000/api/keyValues/businessUnit/'
    
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    payload = {'key1': 1, 'key2': 'value2'}
    
    # convert dict to json by json.dumps() for body data. 
    #resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    #resp = requests.post(url, headers=headers)       
    resp = requests.get(url, headers=headers)       
    
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    #assert resp_body['key'] == url
    
    # print response full body as text
    print(resp.text)
