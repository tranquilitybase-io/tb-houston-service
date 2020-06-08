import requests
import os

def test_health():

    HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
    url = f"http://{HOUSTON_SERVICE_URL}/api/health"

    resp = requests.get(url) 
    resp_json = resp.json()
    # Validate Response
    assert resp.status_code == 200
    assert resp_json['status'] == 'Healthy'
