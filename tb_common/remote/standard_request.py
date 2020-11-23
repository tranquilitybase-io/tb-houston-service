import os
import logging
import requests
import json

logger = logging.getLogger(os.path.basename(__file__))
headers = {"Content-Type": "application/json"}


def validate_endpoint(endpoint: str):
    if endpoint[0] == "/":
        pass
    else:
        raise Exception("check the endpoint value '{0}', missing leading '/'".format(endpoint))


class Dac:

    dac_url = f"http://{os.environ['GCP_DAC_URL']}/dac"

    def __init__(self):
        pass

    def post(self, endpoint: str, payload):
        validate_endpoint(endpoint)
        url = self.dac_url + endpoint
        return requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    def get(self, endpoint: str):
        validate_endpoint(endpoint)
        url = self.dac_url + endpoint
        return requests.get(url, headers=headers)


class Houston:

    houston_url = f"http://{os.environ['HOUSTON_SERVICE_URL']}/api"

    def __init__(self):
        pass

    def post(self, endpoint: str, payload):
        validate_endpoint(endpoint)
        url = self.houston_url + endpoint
        return requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    def get(self, endpoint: str):
        validate_endpoint(endpoint)
        url = self.houston_url + endpoint
        return requests.get(url, headers=headers)
