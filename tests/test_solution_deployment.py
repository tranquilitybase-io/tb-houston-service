import requests
import time
import os
import json
from pprint import pformat
from pprint import pprint
import unittest
from tests.Spinner import Spinner

from tb_houston_service.DeploymentStatus import DeploymentStatus


class TestSolutionDeployment(unittest.TestCase):
    HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
    solution_url = f"http://{HOUSTON_SERVICE_URL}/api/solution/"
    url = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployment/"
    urls = f"http://{HOUSTON_SERVICE_URL}/api/solutiondeployments/"

    # Additional headers.
    headers = {"Content-Type": "application/json"}
    oid = None


    # Main tests are prefix with test_
    def test_solution_deployment(self):
        # Testing POST request
        self.oid = self.post_solution()

        taskid = self.post_deployment()
        print(f"taskid: {taskid}")

        # Testing PUT request
        self.put_deployment()

        # Testing get deployment results
        self.get_deployment_results()



    def typestest_solution_deployment(self, resp):
        self.assertTrue(isinstance(resp["id"], int))
        self.assertTrue(isinstance(resp["deployed"], bool))
        self.assertTrue(isinstance(resp["deploymentState"], str))
        self.assertTrue(isinstance(resp["statusCode"], str))
        self.assertTrue(isinstance(resp["statusMessage"], str))
        self.assertTrue(isinstance(resp["statusId"], int))
        self.assertTrue(isinstance(resp["taskId"], str) or resp["taskId"] is None)
        pprint(resp)


    def post_deployment(self):
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

    def put_deployment(self):
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
        self.assertEqual(resp_json["id"], int(self.oid))
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

    def post_solution(self):
        print("Post Solution Tests")
        # Test POST Then GET
        # Body
        payload = {
            "isActive": True,
            "businessUnitId": 1,
            "cd": "test",
            "ci": "test",
            "costCentre": "test",
            "description": "test",
            "isFavourite": True,
            "name": "test solution",
            "sourceControl": "test",
            "teamId": 1,
            "environments": [1, 2]
        }
    
        # convert dict to json by json.dumps() for body data.
        resp = requests.post(self.solution_url, headers=self.headers, data=json.dumps(payload, indent=4))
    
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


    def get_deployment_results(self):
        print("Get Test Results")
        with Spinner():
            resp = requests.get(self.url+str(self.oid), headers=self.headers)
            resp_json = resp.json()
            while resp_json["deploymentState"] != DeploymentStatus.SUCCESS and resp_json["deploymentState"] != DeploymentStatus.FAILURE:
                time.sleep(1)
                resp = requests.get(self.url+str(self.oid), headers=self.headers)
                resp_json = resp.json()
                print(f" Deployment {resp_json['deploymentState']}")
            # Validate Get All response
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(resp_json["deploymentState"] == DeploymentStatus.SUCCESS or resp_json["deploymentState"] == DeploymentStatus.FAILURE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
