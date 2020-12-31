"""
folder_deployment module.
"""
import json
import logging
import os
import re
from pprint import pformat

import requests

from config import app

logger = logging.getLogger("gcp_dac_folder_deployment")

gcp_dac_url = f"http://{os.environ['GCP_DAC_URL']}"
headers = {"Content-Type": "application/json"}
folder_url = f"{gcp_dac_url}/dac/folder_async"
create_folder_result_url = f"{gcp_dac_url}/dac/folder_async/result/create/"
delete_folder_result_url = f"{gcp_dac_url}/dac/folder_async/result/delete/"

folderid_regex = re.compile(r"folders/(?P<folder>\w+)")

# Send the payload to the DAC


def create(details):
    response = requests.post(folder_url, data=json.dumps(details), headers=headers)
    resp_json = response.json()
    logger.debug("create::Response from DAC")
    logger.debug("create::%s", pformat(resp_json))
    return resp_json, 200


def get_create_results(task_id):
    """
    Get the deployment results from the DAC.
    params: task_id
    """
    response = requests.get(create_folder_result_url + task_id, headers=headers)
    resp_json = response.json()
    return resp_json, 200


def get_delete_results(task_id):
    """
    Get the deployment results from the DAC.
    params: task_id
    """
    response = requests.get(delete_folder_result_url + task_id, headers=headers)
    resp_json = response.json()
    return resp_json, 200


def get_folder_id_from_payload(payload):
    """
    Get the folder id from the payload.

    Arguments:
        payload {string} -- The payload returned from the DAC.

    Returns:
        string -- The folder id.
    """
    app.logger.debug(f"payload: {payload}")
    dac_folder_id = payload.get("folder").get("value").get("id")
    if dac_folder_id:
        match = folderid_regex.search(dac_folder_id)
        if match:
            return match.group("folder")
    return dac_folder_id
