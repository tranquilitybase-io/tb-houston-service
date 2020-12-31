import json
import os
import unittest
from pprint import pformat

import requests


class TestLZMetadata(unittest.TestCase):
    HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
    url = f"http://{HOUSTON_SERVICE_URL}/api/lzmetadata/"

    # Additional headers.
    headers = {"Content-Type": "application/json"}

    # Main tests are prefix with test_
    def test_main(self):
        key = "new_test_metadata"
        # Testing POST request
        self.post(key)

        # Testing get results
        self.get(key)

        # Testing PUT request
        self.put(key)

    def post(self, key):
        print("Post Tests")
        # Test POST Then GET
        # Body
        payload = {"key": key, "value": "new lzmetadata"}

        # convert dict to json by json.dumps() for body data.
        resp = requests.post(self.url, headers=self.headers, data=json.dumps(payload))

        # Validate response headers and body contents, e.g. status code.
        print(pformat(resp.json()))
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.headers["content-type"], "application/json")

    def put(self, key):
        # Test Update Then get new value
        newpayload = {"value": "updated value"}

        resp = requests.put(
            self.url + key,
            headers=self.headers,
            data=json.dumps(newpayload),
        )
        resp_json = resp.json()
        print(f"put resp_json: {resp_json}")
        self.assertEqual(resp_json["key"], key)
        self.assertEqual(resp_json["value"], "updated value")

        # Validate update/Put response
        self.assertEqual(resp.status_code, 200)

    def get(self, key):
        resp = requests.get(self.url + key, headers=self.headers)
        resp_json = resp.json()
        print(f"get resp_json: {resp_json}")
        self.assertEqual(resp_json["key"], key)


if __name__ == "__main__":
    unittest.main(verbosity=2)
