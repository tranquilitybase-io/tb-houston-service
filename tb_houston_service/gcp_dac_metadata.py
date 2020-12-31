"""
gcpdac metadata module.
"""
import logging
import os

import requests

logger = logging.getLogger("gcp_dac_metadata")

gcp_dac_url = f"http://{os.environ['GCP_DAC_URL']}"
headers = {"Content-Type": "application/json"}
metadata_url = f"{gcp_dac_url}/dac/metadata"


def read():
    response = requests.get(metadata_url, headers=headers)
    data = response.json()
    logger.debug("metadata: %s", data)
    return data
