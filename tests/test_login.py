import requests
import json
import os

def test_login():
    HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
    url = f"http://{HOUSTON_SERVICE_URL}/api/login"

    headers = {'Content-Type': 'application/json' } 

    false = 1 == 0
    payload = {
    'email': 'test@testmail.com',
    'username': 'string',
    'firstName': 'string',
    'id': 0,
    'isAdmin': false,
    'lastName': 'string',
    'password': 'string'
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    resp_json = resp.json()
    # Validate Response
    assert resp.status_code == 401
