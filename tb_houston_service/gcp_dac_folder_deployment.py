"""
folder_deployment module.
"""
from pprint import pformat
import re
import logging

from tb_common.remote.standard_request import Dac
from config import app

logger = logging.getLogger("gcp_dac_folder_deployment")


def create(details):
    response = Dac().post("/folder_async", details)
    resp_json = response.json()
    logger.debug("create::Response from DAC")
    logger.debug("create::%s", pformat(resp_json))
    return resp_json, 200


def get_create_results(task_id):
    """
    Get the deployment results from the DAC.
    params: task_id
    """

    response = Dac().get("/folder_async/result/create/" + task_id)
    resp_json = response.json()
    return resp_json, 200


def get_delete_results(task_id):
    """
    Get the deployment results from the DAC.
    params: task_id
    """

    response = Dac().get("/folder_async/result/delete/" + task_id)
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
        folderid_regex = re.compile(r"folders/(?P<folder>\w+)")
        match = folderid_regex.search(dac_folder_id)
        if match:
            return match.group("folder")
    return dac_folder_id
