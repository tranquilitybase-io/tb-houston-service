from flask import make_response, jsonify, abort
import os
import requests
import json
from pprint import pformat
from extendedSchemas import ResponseSchema

def create(solutionDetails):
    print(pformat(solutionDetails))

    # mkdir Folders/Projects

    # skeleton code 
    success = True

    if success == True:
        id = solutionDetails['id']
        resp = { "id": id, "deployed": False, "deploymentState": "In progress", "statusId": 0, "statusCode": "SS", "statusMessage": "Successful" }
        schema = ResponseSchema()
        data = schema.dump(resp)
        print(pformat(data))
        return data, 200
    else:
        abort(500, "Failed to receive solution")


def successful_deployment_update(id):

    url = "http://" + os.environ['HOUSTON_SERVICE_URL'] + "/api/solutiondeployment/"

    payload = { 'id': id, 'deployed': True }
    print(f"url: {url}")
    print(f"data: {payload}")
    headers = { 'Content-Type': "application/json" }
    response = requests.put(url + f"/{id}", data=json.dumps(payload), headers=headers)
    print(pformat(response))
    return response

