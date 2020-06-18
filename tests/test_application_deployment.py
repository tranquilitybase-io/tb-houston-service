import requests
import time
import os
import json
from pprint import pformat
from pprint import pprint
import unittest
from tests.Spinner import Spinner

from tb_houston_service.DeploymentStatus import DeploymentStatus


class TestApplicationDeployment(unittest.TestCase):
    HOUSTON_SERVICE_URL = os.environ["HOUSTON_SERVICE_URL"]
    application_url = f"http://{HOUSTON_SERVICE_URL}/api/application/"
    url = f"http://{HOUSTON_SERVICE_URL}/api/applicationDeployment/"
    urls = f"http://{HOUSTON_SERVICE_URL}/api/applicationDeployments/"

    # Additional headers.
    headers = {"Content-Type": "application/json"}
    oid = None
    taskId = None


    # Main tests are prefix with test_
    def test_application_deployment(self):
        # Testing POST request
        self.oid = self.post_application()

        self.post_deployment()

        # Testing get deployment results
        self.get_deployment_results()

        # Testing PUT request
        #self.put_deployment()


    def typestest_application_deployment(self, resp):
        self.assertTrue(isinstance(resp["id"], int))
        self.assertTrue(isinstance(resp["deployed"], bool))
        self.assertTrue(isinstance(resp["deploymentState"], str))
        self.assertTrue(isinstance(resp["statusCode"], str))
        self.assertTrue(isinstance(resp["statusMessage"], str))
        self.assertTrue(isinstance(resp["statusId"], int))
        self.assertTrue(isinstance(resp["taskId"], str) or resp["taskId"] is None)
        pprint(resp)


    def post_deployment(self):
        print("Post Application Deployment Tests")
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


    def put_deployment(self):
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
            self.url + self.oid,
            headers=self.headers,
            data=newpayload.format(int(self.oid)),
        )
        resp_json = resp.json()
        print(f"put resp_json: {resp_json}")
        self.typestest_application_deployment(resp_json)
        self.assertEqual(resp_json["id"], int(self.oid))
        self.assertEqual(resp_json["deploymentState"], "PENDING")
        self.assertEqual(resp_json["taskId"], None)

        # Validate update/Put response
        self.assertEqual(resp.status_code, 200)


    def post_application(self):
        print("Create an Application Test")
        # Test POST Then GET
        # Body
        payload = {
            "activatorId": 1,
            "description": "New Application",
            "env": "Development",
            "isActive": True,
            "isFavourite": True,
            "lastUpdated": "",
            "name": "New Application",
            "resources": [
                {
                    "ipaddress": "100.100.023.001",
                    "name": "DevServer"
                }
            ],
            "solutionId": 1,
            "status": "Available"
        }
    
        # convert dict to json by json.dumps() for body data.
        resp = requests.post(self.application_url, headers=self.headers, data=json.dumps(payload, indent=4))
    
        # Validate response headers and body contents, e.g. status code.
        resp_json = resp.json()
        id = str(resp_json["id"])
        assert resp.status_code == 201
    
        # Get Request to check Post has created item as expected
        resp = requests.get(self.application_url + id, headers=self.headers)
        resp_json = resp.json()
        resp_headers = resp.headers
        # Validate response
        assert resp.status_code == 200
        assert resp_json["name"] == "New Application"
        assert resp_json["description"] == "New Application"
        assert resp_headers["content-type"] == "application/json"
        print(f"id: {id}")
        return id


    def find_deployment(self):
        resps = requests.get(self.urls, headers=self.headers)
        resps_json = resps.json()
        for j in resps_json:
            if j['id'] == self.oid:
                return j
        time.sleep(1)
        return j


    def get_deployment_results(self):
        print("Get Test Results")
        with Spinner():
            foundTaskId = False
            while foundTaskId == False:
                j = self.find_deployment()
                print(f"Found deployment: {j}")
                taskId = j['taskId']
                if taskId:
                    foundTaskId = True

            done = False
            while done == False:
                k = self.find_deployment()
                if k['deploymentState'] == DeploymentStatus.SUCCESS or k['deploymentState'] == DeploymentStatus.FAILURE:
                    done = True  
                    print(f"Finish deployment: {k}")
            self.assertTrue(done)


if __name__ == '__main__':
    unittest.main(verbosity=2)
