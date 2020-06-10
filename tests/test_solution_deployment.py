import requests
import os
from pprint import pformat
from pprint import pprint
import unittest

from tb_houston_service.DeploymentStatus import DeploymentStatus


class TestSolutionDeployment(unittest.TestCase):
    HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
    url = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployment/"
    urls = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployments/"

    # Additional headers.
    headers = {"Content-Type": "application/json"}
    oid = "1"

    def typestest_solution_deployment(self, resp):
        self.assertTrue(isinstance(resp["id"], int))
        self.assertTrue(isinstance(resp["deployed"], bool))
        self.assertTrue(isinstance(resp["deploymentState"], str))
        self.assertTrue(isinstance(resp["statusCode"], str))
        self.assertTrue(isinstance(resp["statusMessage"], str))
        self.assertTrue(isinstance(resp["statusId"], int))
        self.assertTrue(isinstance(resp["taskId"], str) or resp["taskId"] is None)
        pprint(resp)

    def test_solutiondeployment(self):
        # Testing POST request
        taskid = self.post()
        print(f"taskid: {taskid}")
        # Testing PUT request
        self.put(self.oid)
        # Testing get deployment results
        self.get_deployment_results()

    def post(self):
        print("Post Tests")
        # Test POST Then GET
        # Body
        payload = """
        {{
            "id": {0}
        }}
        """

        # convert dict to json by json.dumps() for body data.
        resp = requests.post(
            self.url, headers=self.headers, data=payload.format(self.oid)
        )

        # Validate response headers and body contents, e.g. status code.
        resp_json = resp.json()
        print(pformat(resp.json()))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")

        # Get Request to get updated values
        resp = requests.get(self.url + self.oid, headers=self.headers)
        resp_json = resp.json()
        print("solution_post")
        pprint(resp_json)
        return resp_json.get("taskId")

    def put(self, oid):
        print("Put Tests")

        # Test Update Then get new value
        newpayload = """
        {{
            "id": {0},
            "deployed": true,
            "deploymentState": "PENDING",
            "statusCode": "200",
            "statusId": 1,
            "statusMessage": "Deployment test.",
            "taskId": null
        }}
        """

        resp = requests.put(
            self.url + self.oid,
            headers=self.headers,
            data=newpayload.format(int(self.oid)),
        )
        resp_json = resp.json()
        print(f"put resp_json: {resp_json}")
        self.typestest_solution_deployment(resp_json)
        self.assertEqual(resp_json["id"], int(oid))
        self.assertEqual(resp_json["deployed"], True)
        self.assertEqual(resp_json["deploymentState"], "PENDING")
        self.assertEqual(resp_json["statusCode"], "200")
        self.assertEqual(resp_json["statusId"], 1)
        self.assertEqual(resp_json["statusMessage"], "Deployment test.")
        self.assertEqual(resp_json["taskId"], None)

        # Validate update/Put response
        self.assertEqual(resp.status_code, 200)

        # Get Request to get updated values
        resp = requests.get(self.url + self.oid, headers=self.headers)
        resp_json = resp.json()

        # Validate response body for updated values
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json["deployed"], True)
        self.assertEqual(resp_json["deploymentState"], "PENDING")

        self.assertEqual(resp_json["statusCode"], "200")
        self.assertEqual(resp_json["statusId"], 1)
        self.assertEqual(resp_json["statusMessage"], "Deployment test.")
        self.assertEqual(resp_json["taskId"], None)
        self.typestest_solution_deployment(resp_json)

    def get_deployment_results(self):
        print("get_all Tests")
        resp = requests.get(self.urls, headers=self.headers)
        resp_json = resp.json()
        print(f"resp_json: {resp_json}")
        for x in range(0, 50):
            resp = requests.get(self.urls, headers=self.headers)
            resp_json = resp.json()
            print(f"{resp_json}")
            # time.sleep(1)
        # Validate Get All response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json[0]["deploymentState"], DeploymentStatus.SUCCESS)
