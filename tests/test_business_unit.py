import requests
import json

def testBusinessUnitEndPoint():

    url = 'http://localhost:3000/api/keyValues/businessUnit/'
    
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 
    
    resp = requests.get(url, headers=headers)  
    resp_json = resp.json()
     
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    
    assert resp_json[0]['key'] == 'Data'
    assert resp_json[1]['key'] == 'FICC'
    assert resp_json[2]['key'] == 'Hello'
    assert resp_json[3]['key'] == 'Modern Apps'

    assert resp_json[0]['value'] == 'Data'
    assert resp_json[1]['value'] == 'FICC'
    assert resp_json[2]['value'] == 'Mario'
    assert resp_json[3]['value'] == 'Modern Apps'
    
    # print response full body as text
    print('\n')
    print(':::: GET ALL SUCCESSFUL ::::')
   
    #########################################################################################
    
    url = 'http://localhost:3000/api/keyValues/businessUnit/'
    
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    #########################################################################################

    # test GET for non existant key 404 expected
    getUrl = url+'test/'
    resp = requests.get(getUrl, headers=headers) 
    
    #Validate response 
    assert resp.status_code == 404
    
    print(':::: GET SUCCESSFUL ::::')

   #########################################################################################

    #Test POST Then GET
    # Body
    payload = {'key': 'test', 'value': 'test-value'}
    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    assert resp.status_code == 201
    assert resp_json['key'] == 'test'
    assert resp_json['value'] == 'test-value'
    
    print(':::: POST SUCCESSFUL ::::')

    resp = requests.get(url+'/test', headers=headers) 
    resp_json = resp.json()
    
    #Validate response 
    assert resp.status_code == 200
    assert resp_json['key'] == 'test'
    assert resp_json['value'] == 'test-value'

    # Test Update Then get new value
    newpayload = {'key': 'test', 'value': 'new-test-value'}
    resp = requests.put(url+'/test', headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response 
    assert resp.status_code == 200
  
   #########################################################################################

    #Get Request to get updated values
    resp = requests.get(url+'/test', headers=headers) 
    resp_json = resp.json()
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['key'] == 'test'
    assert resp_json['value'] == 'new-test-value'
    print(':::: PUT SUCCESSFUL ::::')
  
   #########################################################################################

    #Test Delete Then GET
    resp = requests.delete(url+'/test', headers=headers) 
    assert resp.status_code == 200
    resp = requests.get(url+'/test', headers=headers) 
    resp_json = resp.json()
    assert resp.status_code == 404
    print(':::: DELETE SUCCESSFUL ::::')

    #########################################################################################