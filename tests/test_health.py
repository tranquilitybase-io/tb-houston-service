import requests
import json

def test_health():

    url = 'http://localhost:3000/api/health'

    resp = requests.get(url) 
    resp_json = resp.json()
    # Validate Response
    assert resp.status_code == 200
    assert resp_json['status'] == 'Healthy'



