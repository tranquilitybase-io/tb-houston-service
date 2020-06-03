"""
This is the deployments module and supports all the ReST actions for the
folderstructures collection
"""

# 3rd party modules
from pprint import pformat
import json
import os
import requests
from config import app


class GCP_DAC_Deployment:
    def __init__(self, deployment_type):
        self.create_url = f"{os.environ['GCP_DAC_URL']}/api/{deployment_type}_async/"
        self.create_result_url = f"http://{os.environ['GCP_DAC_URL']}/api/{deployment_type}_async/result/create/"
        self.headers = {"Content-Type": "application/json"}

    # Send the payload to the DAC
    def send_payload(self, json_payload):
        resp_json = None
        try:
            response = requests.post(
                self.create_url, data=json.dumps(json_payload), headers=self.headers
            )
            resp_json = response.json()
            app.logger.debug("Response from DAC")
            app.logger.debug(pformat(resp_json))
        except requests.exceptions.RequestException as e:
            app.logger.debug("GCP_DAC_Deployment::Failed sending request to DAC")
            resp_json = {
                "statusId": e.errno,
                "statusCode": e.strerror,
                "statusMessage": e.message,
            }
        return resp_json

    def get_results(self, task_id):
        """
        Get the deployment results from the DAC.
        params: task_id
        """
        resp_json = None
        try:
            response = requests.get(
                self.create_result_url + task_id, headers=self.headers
            )
            resp_json = response.json()
            app.logger.debug("Response from Dac")
            app.logger.debug(pformat(resp_json))
            print(pformat(resp_json))
        except requests.exceptions.RequestException as e:
            app.logger.debug("GCP_DAC_Deployment::Failed getting results from the DAC")
            resp_json = {
                "taskId": task_id,
                "statusId": e.errno,
                "statusCode": e.strerror,
                "statusMessage": e.message,
            }
        return resp_json
