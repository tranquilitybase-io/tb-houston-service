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
    assert resp_json['googleSession']['primaryRegion'] == 'test-post'
    assert resp_json['googleSession']['primarySubnetName'] == 'test-post'
    assert resp_json['googleSession']['secondaryGcpVpcSubnet'] == 'test-post'
    assert resp_json['googleSession']['secondaryRegion'] == 'test-post'
    assert resp_json['googleSession']['secondarySubnetName'] == 'test-post'
    assert resp_json['onPremiseSession']['primaryBgpPeer'] == 'test-post'
    assert resp_json['onPremiseSession']['primaryPeerIp'] == 'test-post'
    assert resp_json['onPremiseSession']['primaryPeerIpSubnet'] == 'test-post'
    assert resp_json['onPremiseSession']['primarySharedSecret'] == 'test-post'
    assert resp_json['onPremiseSession']['primaryVpnTunnel'] == 'test-post'
    assert resp_json['onPremiseSession']['secondaryBgpPeer'] == 'test-post'
    assert resp_json['onPremiseSession']['secondaryPeerIpSubnet'] == 'test-post'
    assert resp_json['onPremiseSession']['secondarySharedSecret'] == 'test-post'
    assert resp_json['onPremiseSession']['secondaryVpnTunnel'] == 'test-post'
    assert resp_json['onPremiseSession']['vendor'] == 'test-post'
    assert resp_json['vpn']['bgpInterfaceNetLength'] == 'test-post'
    assert resp_json['vpn']['bgpRoutingMode'] == 'test-post'
    assert resp_json['vpn']['cloudRouterName'] == 'test-post'
    assert resp_json['vpn']['description'] == 'test-post'
    assert resp_json['vpn']['externalVpnGateway'] == 'test-post'
    assert resp_json['vpn']['googleASN'] == 0
    assert resp_json['vpn']['haVpnGateway'] == 'test-post'
    assert resp_json['vpn']['peerASN'] == 0
    assert resp_json['vpn']['projectName'] == 'test-post'
    assert resp_json['vpn']['subnetMode'] == 'test-post'
    assert resp_json['vpn']['vpcName'] == 'test-post'
    assert resp_headers['content-type'] == 'application/json'

    return resp_json


def put(oid):

    # Test Update Then get updated value
    newpayload = {
    'googleSession':
        {
        'primaryGcpVpcSubnet': 'new-test-put',
        'primaryRegion': 'new-test-put',
        'primarySubnetName': 'new-test-put',
        'secondaryGcpVpcSubnet': 'new-test-put',
        'secondaryRegion': 'new-test-put',
        'secondarySubnetName': 'new-test-put'
        },
    'id': int(oid),
    'onPremiseSession':
        {
        'primaryBgpPeer': 'new-test-put',
        'primaryPeerIp': 'new-test-put',
        'primaryPeerIpSubnet': 'new-test-put',
        'primarySharedSecret': 'new-test-put',
        'primaryVpnTunnel': 'new-test-put',
        'secondaryBgpPeer': 'new-test-put',
        'secondaryPeerIp': 'new-test-put',
        'secondaryPeerIpSubnet': 'new-test-put',
        'secondarySharedSecret': 'new-test-put',
        'secondaryVpnTunnel': 'new-test-put',
        'vendor': 'new-test-put'
        },
    'vpn':
        {
        'bgpInterfaceNetLength': 'new-test-put',
        'bgpRoutingMode': 'new-test-put',
        'cloudRouterName': 'new-test-put',
        'description': 'new-test-put',
        'externalVpnGateway': 'new-test-put',
        'googleASN': 0,
        'haVpnGateway': 'new-test-put',
        'peerASN': 0,
        'projectName': 'new-test-put',
        'subnetMode': 'new-test-put',
        'vpcName': 'new-test-put'
        }
    }
  
    resp = requests.put(url+oid, headers=headers, data=json.dumps(newpayload,indent=4))
   
    #Validate update/Put response
    assert resp.status_code == 200

    #Get Request to get updated values
    resp = requests.get(url+oid, headers=headers)
    resp_json = resp.json()
    resp_headers = resp.headers
    oid = resp_json['id']
    #Validate response body for updated values
    assert resp.status_code == 200
    assert resp_json['googleSession']['primaryGcpVpcSubnet'] == 'new-test-put'
    assert resp_json['googleSession']['primaryRegion'] == 'new-test-put'
    assert resp_json['googleSession']['primarySubnetName'] == 'new-test-put'
    assert resp_json['googleSession']['secondaryGcpVpcSubnet'] == 'new-test-put'
    assert resp_json['googleSession']['secondaryRegion'] == 'new-test-put'
    assert resp_json['googleSession']['secondarySubnetName'] == 'new-test-put'
    assert resp_json['onPremiseSession']['primaryBgpPeer'] == 'new-test-put'
    assert resp_json['onPremiseSession']['primaryPeerIp'] == 'new-test-put'
    assert resp_json['onPremiseSession']['primaryPeerIpSubnet'] == 'new-test-put'
    assert resp_json['onPremiseSession']['primarySharedSecret'] == 'new-test-put'
    assert resp_json['onPremiseSession']['primaryVpnTunnel'] == 'new-test-put'
    assert resp_json['onPremiseSession']['secondaryBgpPeer'] == 'new-test-put'
    assert resp_json['onPremiseSession']['secondaryPeerIpSubnet'] == 'new-test-put'
    assert resp_json['onPremiseSession']['secondarySharedSecret'] == 'new-test-put'
    assert resp_json['onPremiseSession']['secondaryVpnTunnel'] == 'new-test-put'
    assert resp_json['onPremiseSession']['vendor'] == 'new-test-put'
    assert resp_json['vpn']['bgpInterfaceNetLength'] == 'new-test-put'
    assert resp_json['vpn']['bgpRoutingMode'] == 'new-test-put'
    assert resp_json['vpn']['cloudRouterName'] == 'new-test-put'
    assert resp_json['vpn']['description'] == 'new-test-put'
    assert resp_json['vpn']['externalVpnGateway'] == 'new-test-put'
    assert resp_json['vpn']['googleASN'] == 0
    assert resp_json['vpn']['haVpnGateway'] == 'new-test-put'
    assert resp_json['vpn']['peerASN'] == 0
    assert resp_json['vpn']['projectName'] == 'new-test-put'
    assert resp_json['vpn']['subnetMode'] == 'new-test-put'
    assert resp_json['vpn']['vpcName'] == 'new-test-put'
    assert resp_headers['content-type'] == 'application/json'
    

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
