import json
import os
import time
import unittest
from pprint import pformat, pprint

import requests

from tb_houston_service.DeploymentStatus import DeploymentStatus
from tests.Spinner import Spinner


class TestDeployment(unittest.TestCase):
    HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
    lzenvironment_deployment_url = (
        f"http://{HOUSTON_SERVICE_URL}/api/lzEnvironmentDeployment/"
    )
    solution_url = f"http://{HOUSTON_SERVICE_URL}/api/solution/"
    solution_deployment_url = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployment/"
    solution_deployments_url = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployments/"

    application_url = f"http://{HOUSTON_SERVICE_URL}/api/application/"
    application_deployment_url = (
        f"http://{HOUSTON_SERVICE_URL}/api/applicationDeployment/"
    )
    application_deployments_url = (
        f"http://{HOUSTON_SERVICE_URL}/api/applicationDeployments/"
    )

    # Additional headers.
    headers = {"Content-Type": "application/json"}
    solution_oid = None
    application_oid = None

    # Main tests are prefix with test_
    def lzenvironment_deployment(self):
        resp = requests.post(self.lzenvironment_deployment_url, headers=self.headers)
        print(f"resp: {resp}")
        self.assertEqual(resp.status_code, 200)

    def solution_deployment(self):
        # Testing POST request
        self.solution_oid = self.post_solution()

        taskid = self.post_solution_deployment()
        print(f"taskid: {taskid}")

        # Testing PUT request
        self.put_solution_deployment()

        # Testing get deployment results
        self.get_solution_deployment_results()

    def typestest_solution_deployment(self, resp):
        self.assertTrue(isinstance(resp["id"], int))
        self.assertTrue(isinstance(resp["deployed"], bool))
        self.assertTrue(isinstance(resp["deploymentState"], str))
        self.assertTrue(isinstance(resp["statusCode"], str))
        self.assertTrue(isinstance(resp["statusMessage"], str))
        self.assertTrue(isinstance(resp["statusId"], int))
        self.assertTrue(isinstance(resp["taskId"], str) or resp["taskId"] is None)
        pprint(resp)

    def post_solution_deployment(self):
        print("Post Solution Deployment Tests")
        # Test POST Then GET
        # Body
        payload = """
        {{
            "id": {0}
        }}
        """

        # convert dict to json by json.dumps() for body data.
        resp = requests.post(
            self.solution_deployment_url,
            headers=self.headers,
            data=payload.format(self.solution_oid),
        )

        # Validate response headers and body contents, e.g. status code.
        resp_json = resp.json()
        print(pformat(resp.json()))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")

        # Get Request to get updated values
        resp = requests.get(
            self.solution_deployment_url + self.solution_oid, headers=self.headers
        )
        resp_json = resp.json()
        print("solution_post")
        pprint(resp_json)
        return resp_json.get("taskId")

    def put_solution_deployment(self):
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
            self.solution_deployment_url + self.solution_oid,
            headers=self.headers,
            data=newpayload.format(self.solution_oid),
        )
        resp_json = resp.json()
        print(f"put resp_json: {resp_json}")
        self.typestest_solution_deployment(resp_json)
        self.assertEqual(resp_json["id"], int(self.solution_oid))
        self.assertEqual(resp_json["deployed"], True)
        self.assertEqual(resp_json["deploymentState"], "PENDING")
        self.assertEqual(resp_json["statusCode"], "200")
        self.assertEqual(resp_json["statusId"], 1)
        self.assertEqual(resp_json["statusMessage"], "Deployment test.")
        self.assertEqual(resp_json["taskId"], None)

        # Validate update/Put response
        self.assertEqual(resp.status_code, 200)

        # Get Request to get updated values
        resp = requests.get(
            self.solution_deployment_url + self.solution_oid, headers=self.headers
        )
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

    def post_solution(self):
        print("Post Solution Tests")
        # Test POST Then GET
        # Body
        payload = {
            "isActive": True,
            "businessUnitId": 1,
            "cdId": 1,
            "ciId": 1,
            "costCentre": "test",
            "description": "test",
            "isFavourite": True,
            "name": "test solution",
            "sourceControlId": 1,
            "teamId": 1,
            "environments": [1, 2],
        }

        # convert dict to json by json.dumps() for body data.
        resp = requests.post(
            self.solution_url, headers=self.headers, data=json.dumps(payload, indent=4)
        )

        # Validate response headers and body contents, e.g. status code.
        resp_json = resp.json()
        id = str(resp_json["id"])
        assert resp.status_code == 201

        # Get Request to check Post has created item as expected
        resp = requests.get(self.solution_url + id, headers=self.headers)
        resp_json = resp.json()
        resp_headers = resp.headers
        # Validate response
        assert resp.status_code == 200
        assert resp_json["name"] == "test solution"
        assert resp_json["businessUnitId"] == 1
        assert resp_json["description"] == "test"
        assert len(resp_json["environments"]) == 2
        assert resp_headers["content-type"] == "application/json"
        return id

    def get_solution_deployment_results(self):
        print("Get Solution Test Results")
        with Spinner():
            resp = requests.get(
                self.solution_deployment_url + str(self.solution_oid),
                headers=self.headers,
            )
            resp_json = resp.json()
            while (
                resp_json["deploymentState"] != DeploymentStatus.SUCCESS
                and resp_json["deploymentState"] != DeploymentStatus.FAILURE
            ):
                time.sleep(1)
                resp = requests.get(
                    self.solution_deployment_url + str(self.solution_oid),
                    headers=self.headers,
                )
                resp_json = resp.json()
                print(f" Solution Deployment {resp_json['deploymentState']}")
            # Validate Get All response
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(
                resp_json["deploymentState"] == DeploymentStatus.SUCCESS
                or resp_json["deploymentState"] == DeploymentStatus.FAILURE
            )

    # Main tests are prefix with test_
    def application_deployment(self):
        # Testing POST request
        self.post_application()
        self.post_application_deployment()
        # Testing get deployment results
        self.get_application_deployment_results()

        # Testing PUT request
        # self.put_deployment()

    def typestest_application_deployment(self, resp):
        self.assertTrue(isinstance(resp["id"], int))
        self.assertTrue(isinstance(resp["deployed"], bool))
        self.assertTrue(isinstance(resp["deploymentState"], str))
        self.assertTrue(isinstance(resp["statusCode"], str))
        self.assertTrue(isinstance(resp["statusMessage"], str))
        self.assertTrue(isinstance(resp["statusId"], int))
        self.assertTrue(isinstance(resp["taskId"], str) or resp["taskId"] is None)
        pprint(resp)

    def post_application_deployment(self):
        print("Post Application Deployment Tests")
        # Test POST Then GET
        # Body
        payload = """
        {{
            "id": {0}
        }}
        """

        new_payload = payload.format(int(self.application_oid))
        print(f"application deployment payload: {new_payload}")
        # convert dict to json by json.dumps() for body data.
        resp = requests.post(
            self.application_deployment_url, headers=self.headers, data=new_payload
        )

        # Validate response headers and body contents, e.g. status code.
        print(resp)
        self.assertEqual(resp.status_code, 200)

    def put_application_deployment(self):
        print("Put Tests, example of redeploying an application.")

        # Test Update Then get new value
        newpayload = """
        {{
            "id": {0},
            "deploymentState": "PENDING",
            "statusMessage": "Deployment test.",
            "taskId": null
        }}
        """

        resp = requests.put(
            self.application_deployment_url + self.application_oid,
            headers=self.headers,
            data=newpayload.format(int(self.application_oid)),
        )
        resp_json = resp.json()
        print(f"put resp_json: {resp_json}")
        self.typestest_application_deployment(resp_json)
        self.assertEqual(resp_json["id"], int(self.application_oid))
        self.assertEqual(resp_json["deploymentState"], "PENDING")
        self.assertEqual(resp_json["taskId"], None)

        # Validate update/Put response
        self.assertEqual(resp.status_code, 200)

    def post_application(self):
        print("Create an Application Test")
        # Test POST Then GET
        # Body
        payload = """
        {{
            "activatorId": 1,
            "description": "New Application",
            "env": "development",
            "isActive": true,
            "isFavourite": true,
            "lastUpdated": "",
            "name": "New Application",
            "resources": [
                {{
                    "ipaddress": "100.100.023.001",
                    "name": "DevServer"
                }}
            ],
            "solutionId": {0},
            "status": "Available"
        }}
        """

        new_payload = payload.format(int(self.solution_oid))
        print("post_application payload: %s", new_payload)
        resp = requests.post(
            self.application_url, headers=self.headers, data=new_payload
        )

        # Validate response headers and body contents, e.g. status code.
        resp_json = resp.json()
        self.application_oid = str(resp_json["id"])
        assert resp.status_code == 201

        # Get Request to check Post has created item as expected
        resp = requests.get(
            self.application_url + self.application_oid, headers=self.headers
        )
        resp_json = resp.json()
        resp_headers = resp.headers
        # Validate response
        assert resp.status_code == 200
        assert resp_json["name"] == "New Application"
        assert resp_json["description"] == "New Application"
        assert resp_headers["content-type"] == "application/json"

    def find_application_deployment(self):
        resps = requests.get(self.application_deployments_url, headers=self.headers)
        resps_json = resps.json()
        for j in resps_json:
            if j["id"] == self.application_oid:
                return j
        time.sleep(1)
        return j

    def get_application_deployment_results(self):
        print("Get Test Results")
        with Spinner():
            foundTaskId = False
            while foundTaskId == False:
                j = self.find_application_deployment()
                print(f"Found application deployment: {j}")
                taskId = j["taskId"]
                if taskId:
                    foundTaskId = True

            done = False
            while done == False:
                k = self.find_application_deployment()
                if (
                    k["deploymentState"] == DeploymentStatus.SUCCESS
                    or k["deploymentState"] == DeploymentStatus.FAILURE
                ):
                    done = True
                    print(f"Finish application deployment: {k}")
            self.assertTrue(done)

    def test_deployment(self):
        self.lzenvironment_deployment()
        self.solution_deployment()
        self.application_deployment()


if __name__ == "__main__":
    unittest.main(verbosity=2)
