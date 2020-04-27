import requests
import json
import os


HOUSTON_SERVICE_URL=os.environ['HOUSTON_SERVICE_URL']
url = f"http://{HOUSTON_SERVICE_URL}/api/landingzonewan/"
    
# Additional headers.
headers = {'Content-Type': 'application/json' }

def test_landingzonewan():
    
    #Testing POST request
    resp_json = post()
    oid = str(resp_json['id'])
    #Testing PUT request
    put(oid)
    #Testing DELETE request
    delete(oid)
    #Testing DELETE Request Error
    delete_error(oid)
    #Testing GETALL request
    get_all()
    

def post():

    #Test POST Then GET
    # Body
    payload  =   {
        'googleSession':
            {
            'primaryGcpVpcSubnet': 'test-post',
            'primaryRegion': 'test-post',
            'primarySubnetName': 'test-post',
            'secondaryGcpVpcSubnet': 'test-post',
            'secondaryRegion': 'test-post',
            'secondarySubnetName': 'test-post'
            },
        'id': 0,
        'onPremiseSession':
            {
            'primaryBgpPeer': 'test-post',
            'primaryPeerIp': 'test-post',
            'primaryPeerIpSubnet': 'test-post',
            'primarySharedSecret': 'test-post',
            'primaryVpnTunnel': 'test-post',
            'secondaryBgpPeer': 'test-post',
            'secondaryPeerIp': 'test-post',
            'secondaryPeerIpSubnet': 'test-post',
            'secondarySharedSecret': 'test-post',
            'secondaryVpnTunnel': 'test-post',
            'vendor': 'test-post'
            },
        'vpn': 
            {
            'bgpInterfaceNetLength': 'test-post',
            'bgpRoutingMode': 'test-post',
            'cloudRouterName': 'test-post',
            'description': 'test-post',
            'externalVpnGateway': 'test-post',
            'googleASN': 0,
            'haVpnGateway': 'test-post',
            'peerASN': 0,
            'projectName': 'test-post',
            'subnetMode': 'test-post',
            'vpcName': 'test-post'
            }
    }
  
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    
    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    oid = resp_json['id']
    assert resp.status_code == 201
    
    #Get Request to check Post has created item as expected
    resp = requests.get(url+ str(oid), headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    #Validate GET response
    assert resp.status_code == 200
    assert resp_json['googleSession']['primaryGcpVpcSubnet'] == 'test-post'
    assert resp_json['onPremiseSession']['primaryBgpPeer'] == 'test-post'
    assert resp_json['vpn']['bgpInterfaceNetLength'] == 'test-post'
    assert resp_headers['content-type'] == 'application/json'

    return resp_json


def put(oid):

    # Test Update Then get updated value
    newpayload = {
    'googleSession':
        {
        'primaryGcpVpcSubnet': 'new-test-put',
        'primaryRegion': 'test-put',
        'primarySubnetName': 'test-put',
        'secondaryGcpVpcSubnet': 'test-put',
        'secondaryRegion': 'test-put',
        'secondarySubnetName': 'test-put'
        },
    'id': int(oid),
    'onPremiseSession':
        {
        'primaryBgpPeer': 'new-test-put',
        'primaryPeerIp': 'test-put',
        'primaryPeerIpSubnet': 'test-put',
        'primarySharedSecret': 'test-put',
        'primaryVpnTunnel': 'test-put',
        'secondaryBgpPeer': 'test-put',
        'secondaryPeerIp': 'test-put',
        'secondaryPeerIpSubnet': 'test-put',
        'secondarySharedSecret': 'test-put',
        'secondaryVpnTunnel': 'test-put',
        'vendor': 'test-put'
        },
    'vpn':
        {
        'bgpInterfaceNetLength': 'new-test-put',
        'bgpRoutingMode': 'test-put',
        'cloudRouterName': 'test-put',
        'description': 'test-put',
        'externalVpnGateway': 'test-put',
        'googleASN': 0,
        'haVpnGateway': 'test-put',
        'peerASN': 0,
        'projectName': 'test-put',
        'subnetMode': 'test-put',
        'vpcName': 'test-put'
        }
    }
  
    resp = requests.put(url+oid, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+oid, headers=headers)
    resp_json = resp.json()
    oid = resp_json['id']
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['googleSession']['primaryGcpVpcSubnet'] == 'new-test-put'
    assert resp_json['onPremiseSession']['primaryBgpPeer'] == 'new-test-put'
    assert resp_json['vpn']['bgpInterfaceNetLength'] == 'new-test-put'
    

def delete(oid):

    # Delete Request
    resp = requests.delete(url+oid, headers=headers)
    #Validate Delete response
    assert resp.status_code == 200
    
    #Then Get request to check the item has been actully deleted
    resp = requests.get(url+oid, headers=headers)
    #Validate Get response
    resp_json = resp.json()
    assert resp.status_code == 404


def delete_error(oid):

    # Delete Request for a non existing item
    resp = requests.delete(url+oid, headers=headers)
    #resp_json = resp.json()
    #resp_headers = resp.headers
    #Validate response ; expect Not found
    assert resp.status_code == 404


def get_all():

    url = f"http://{HOUSTON_SERVICE_URL}/api/landingzonewans/"
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
