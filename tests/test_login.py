import requests
import json

def test_login():

    url = 'http://localhost:3000/api/login'

    headers = {'Content-Type': 'application/json' } 

    payload = {
    'email': 'test@testmail.com',
    'firstName': 'string',
    'id': '0',
    'isAdmin': False,
    'lastName': 'string',
    'password': 'string'
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    # Validate Response
    assert resp.status_code == 500



