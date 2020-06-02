import requests
import os

HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']

# Additional headers.
headers = {'Content-Type': 'application/json' }


def get_all(url):

    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200


def delete(url, oid):

    # Delete Request
    resp = requests.delete(url + oid, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200

    #Then Get request to check the item has been actully deleted
    resp = requests.get(url + oid, headers=headers)
    #Validate Get response
    #resp_json = resp.json()
    assert resp.status_code == 404


def delete_isActive(url, oid):

    # Delete Request
    resp = requests.delete(url + oid, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200

    #Then Get request to check the item has been actully deleted
    resp = requests.get(url + oid, headers=headers)
    #Validate Get response
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json.get('isActive') == False


def delete_error(url, oid):

    # Delete Request for a non existing item
    resp = requests.delete(url + oid, headers=headers)
    #resp_json = resp.json()
    #resp_headers = resp.headers
    #Validate response ; expect Not found
    assert resp.status_code == 404
