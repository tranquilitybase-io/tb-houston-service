import requests
import json
import logging
import os

LOG_LEVEL = logging.DEBUG # DEBUG, INFO, WARNING, ERROR, CRITICAL

HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/solutionEnvironment/"
# Additional headers.
headers = {'Content-Type': 'application/json' }

def typestest(resp):
    assert isinstance(resp['id'], int)
    assert isinstance(resp['lastUpdated'], str)
    assert isinstance(resp['solutionId'], int)
    assert isinstance(resp['environmentId'], int)
    assert isinstance(resp['isActive'], bool)


def test_post():
    #Test POST Then GET
    # Body
    payload = [ { "environmentId": 1, "isActive": True, "solutionId": 1 }, { "environmentId": 2, "isActive": True, "solutionId": 1 }, { "environmentId": 2, "isActive": True, "solutionId": 2 }  ]
    # convert obj to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 201

    #Get Request to check Post has created item as expected
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate response
    assert resp.status_code == 200
    assert resp_headers['content-type'] == 'application/json'

    print(json.dumps(resp_json, indent=4))
    for i in resp_json:
        typestest(i)


def test_get_all():
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    assert resp.status_code == 200
    for i in resp_json:
        typestest(i)


if __name__ == "__main__":
    test_post()
    test_get_all()
