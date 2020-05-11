"""
This is the deployments module and supports all the ReST actions for the
solutions collection
"""

# 3rd party modules
from flask import make_response, jsonify, abort
from config import db, app
from models import Solution, SolutionSchema
from models import ModelTools
from extendedSchemas import ExtendedSolutionSchema
from extendedSchemas import SolutionDeploymentSchema
from extendedSchemas import SolutionNamesOnlySchema
import solution_extension
from pprint import pformat
import requests
import os
import json
from sqlalchemy import literal_column
import solutionresourcejson


deployment_create_url = f"http://{os.environ['GCP_DAC_URL']}/api/solution_async/"
deployment_create_result_url = f"http://{os.environ['GCP_DAC_URL']}/api/solution_async/result/create/"
headers = { 'Content-Type': "application/json" }
DEPLOYMENT_STATE = {
    "PENDING": "PENDING",
    "STARTED": "STARTED",
    "SUCCESS": "SUCCESS",
    "RETRY": "RETRY",
    "FAILURE": "FAILURE",
    "REVOKED": "REVOKED"
}

def read_all(active=None, namesonly=None, page=None, page_size=None, sort=None):
    """
    This function responds to a request for /api/solutions
    with the complete lists of solutions

    :return:        json string of list of solutions
    """

    app.logger.debug("solution.read_all")
    app.logger.debug(f"Active: {active}, namesonly: {namesonly}")

    # pre-process sort instructions
    if (sort==None):
        solution_query = Solution.query.order_by(Solution.id)
    else:
        try:
            sort_inst = [ si.split(":") for si in sort ]
            orderby_arr = []
            for si in sort_inst:
                si1 = si[0]
                if len(si) > 1:
                    si2 = si[1]
                else:
                    si2 = "asc"
                orderby_arr.append(f"{si1} {si2}")
            #print("orderby: {}".format(orderby_arr))
            solution_query = Solution.query.order_by(literal_column(", ".join(orderby_arr)))
        except Exception as e:
            print("Exception: {}".format(pformat(e)))
            solution_query = Solution.query.order_by(Solution.id)

    # Create the list of solutions from our data
    if active != None:
      solution_query = solution_query.filter(Solution.active == active)

    # do limit and offset last
    if (page==None or page_size==None):
      solutions = solution_query.all()
    else:
      solutions = solution_query.limit(page_size).offset(page * page_size)

    if namesonly == True:
      # Serialize the data for the response
      schema = SolutionNamesOnlySchema(many=True)
      data = schema.dump(solutions)
    else:
      solutions_arr = []
      for sol in solutions:
        solutions_arr.append(solution_extension.build_solution(sol))
      app.logger.debug("solutions array:")
      app.logger.debug(pformat(solutions_arr))
      # Serialize the data for the response
      schema = ExtendedSolutionSchema(many=True)
      data = schema.dump(solutions_arr)

    app.logger.debug("solutions data:")
    app.logger.debug(data)
    return data, 200


def read_one(oid):
    """
    This function responds to a request for /api/solution/{oid}
    with one matching solution from solutions

    :param application:   id of solution to find
    :return:              solution matching id
    """

    sol = (Solution.query.filter(Solution.id == oid).one_or_none())

    if sol is not None:
        solution = solution_extension.build_solution(sol)
        # Serialize the data for the response
        solution_schema = ExtendedSolutionSchema()
        data = solution_schema.dump(solution)
        return data, 200
    else:
        abort(
            404, f"Solution with id {oid} not found".format(id=oid)
        )


def create(solutionDetails):
    """
    This function creates a new solution in the solutions list
    based on the passed in solutions data

    :param solution:  solution to create in solutions list
    :return:        201 on success, 406 on solutions exists
    """

    # Defaults
    if (solutionDetails.get('active') == None):
      solutionDetails['active'] = True

    if (solutionDetails.get('favourite') == None):
      solutionDetails['favourite'] = True

    if (solutionDetails.get('teams') == None):
      solutionDetails['teams'] = 0

    if (solutionDetails.get('deployed') == None):
      solutionDetails['deployed'] = False

    if (solutionDetails.get('deploymentState') == None):
      solutionDetails['deploymentState'] = ""

    if (solutionDetails.get('statusId') == None):
      solutionDetails['statusId'] = 0

    if (solutionDetails.get('statusCode') == None):
      solutionDetails['statusCode'] = ""

    if (solutionDetails.get('statusMessage') == None):
      solutionDetails['statusMessage'] = ""

    # Remove applications because Solutions don't have
    # any applications when they are first created
    if ('applications' in solutionDetails):
      del solutionDetails['applications']

    # we don't need the id, the is generated automatically on the database
    if ('id' in solutionDetails):
      del solutionDetails["id"]

    solutionDetails['lastUpdated'] = ModelTools.get_utc_timestamp()
    solutionDetails['environments'] = json.dumps(solutionDetails.get('environments') or [])

    schema = SolutionSchema(many=False)
    new_solution = schema.load(solutionDetails, session=db.session)
    db.session.add(new_solution)
    db.session.commit()

    # Serialize and return the newly created solution
    # in the response

    schema = SolutionSchema()
    data = schema.dump(new_solution)
    data['environments'] = json.loads(data['environments'])
    return data, 201


def update(oid, solutionDetails):
    """
    Updates an existing solutions in the solutions list.

    :param key:    key of the solutions to update in the solutions list
    :param solutions:   solutions to update
    :return:       updated solutions
    """

    app.logger.debug(solutionDetails)

    # Does the solutions exist in solutions list?
    existing_solution = Solution.query.filter(
            Solution.id == oid
    ).one_or_none()

    # Does solutions exist?

    if existing_solution is not None:
        solutionDetails['environments'] = json.dumps(solutionDetails.get('environments') or existing_solution.environments)
        schema = SolutionSchema()
        update_solution = schema.load(solutionDetails, session=db.session)
        update_solution.key = solutionDetails.get('id', oid)
        update_solution.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(update_solution)
        db.session.commit()

        # return the updted solutions in the response
        schema = ExtendedSolutionSchema(many=False)
        solutionDetails['environments'] = json.loads(solutionDetails['environments'])
        data = schema.dump(solutionDetails)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Solution not found")


def delete(oid):
    """
    This function deletes a solution from the solutions list

    :param key: id of the solutions to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solution to delete exist?
    existing_solution = Solution.query.filter(Solution.id == oid).one_or_none()

    # if found?
    if existing_solution is not None:
        db.session.delete(existing_solution)
        db.session.commit()

        return make_response(f"Solution {oid} successfully deleted", 200)

    # Otherwise, nope, solution to delete not found
    else:
        abort(404, f"Solution {oid} not found")


def deployment_read_all():
    """
    This function responds to a request for /api/solutiondeployments
    with the complete lists of deployed solutions

    :return:        json string of list of deployed solutions
                    id and deployed fields
    """

    app.logger.debug("solution.deployment_read_all")

    solutions = Solution.query.filter(Solution.deploymentState != "").all()
    # Loop through solutions, if not a SUCCESS requery from DAC
    for sol in solutions:
        app.logger.debug(f"deployment_read_all::sol.deploymentState: {sol.deploymentState}")
        if sol.deploymentState != DEPLOYMENT_STATE['SUCCESS']:
            oid = sol.id
            task_id = sol.taskId
            app.logger.debug(f"oid: {oid} {task_id}")
            response = get_solution_results_from_the_dac(oid, task_id)
            app.logger.debug(pformat(response))
            print("response: " + pformat(response))

    schema = SolutionDeploymentSchema(many=True)
    data = schema.dump(solutions)

    app.logger.debug("solutions data:")
    app.logger.debug(data)
    return data, 200


def deployment_read_one(oid):
    """
    This function responds to a request for /api/solutiondeployment/{oid}
    with one matching solution deployment from solutions

    :param application:   id of solution to find
    :return:              solution matching id
    """

    sol = (Solution.query.filter(Solution.id == oid).one_or_none())

    if sol is not None:
        # Serialize the data for the response
        solution_schema = SolutionDeploymentSchema(many=False)
        data = solution_schema.dump(sol)
        return data, 200
    else:
        abort(
            404, f"Solution with id {oid} not found".format(id=oid)
        )


def deployment_create(solutionDeploymentDetails):
    """
    This function queries a solution forwards the request to the DaC

    :param solution:  id
    :return:        201 on success
    :               404 if solution not found
    :               500 if other failure
    """

    app.logger.debug(pformat(solutionDeploymentDetails))
    oid = solutionDeploymentDetails['id'];
    sol = (Solution.query.filter(Solution.id == oid).one_or_none())

    if sol == None:
        abort(
            404, f"Solution with id {oid} not found".format(id=oid)
        )

    if sol.deploymentState == DEPLOYMENT_STATE['SUCCESS']:
        resp_json = {
            "id": oid,
            "deploymentState": sol.deploymentState
        }
        return resp_json, 200

    if sol is not None:
        # Serialize the data for forwarding to the DaC
        url = "http://" + os.environ['GCP_DAC_URL'] + "/api/solution/"
        solution = solution_extension.build_solution(sol)
        app.logger.debug("deployment_create: solution start")
        app.logger.debug(pformat(solution))
        app.logger.debug("deployment_create: solution end")

        solution_schema = ExtendedSolutionSchema(many=False)
        data_to_dac = solution_schema.dump(solution)

        response_json = send_solution_deployment_to_the_dac(data_to_dac)
        app.logger.debug(pformat(response_json))
        print(f"response_json: {pformat(response_json)}")
        statusId = response_json.get('statusId')
        return response_json, statusId


def deployment_update(oid, solutionDeploymentDetails):
    """
    Updates an existing solutions in the solutions list with the deployed status.

    :param key:    id of the solution
    :param solutionDetails:   solution details to update
    :return:       updated solution
    """

    app.logger.debug(solutionDeploymentDetails)

    # Does the solutions exist in solutions list?
    existing_solution = Solution.query.filter(
            Solution.id == oid
    ).one_or_none()

    # Does solutions exist?

    if existing_solution is not None:
        schema = SolutionSchema(many=False)
        update_solution = schema.load(solutionDeploymentDetails, session=db.session)
        update_solution.id = oid
        update_solution.lastUpdated = ModelTools.get_utc_timestamp()
        update_solution.deployed = solutionDeploymentDetails.get('deployed', existing_solution.deployed)
        update_solution.deploymentState = solutionDeploymentDetails.get('deploymentState', existing_solution.deploymentState)
        update_solution.statusId = solutionDeploymentDetails.get('statusId', existing_solution.statusId)
        update_solution.statusCode = solutionDeploymentDetails.get('statusCode', existing_solution.statusCode)
        update_solution.statusMessage = solutionDeploymentDetails.get('statusMessage', existing_solution.statusMessage)
        update_solution.taskId = solutionDeploymentDetails.get('taskId', existing_solution.taskId)

        db.session.merge(update_solution)
        db.session.commit()

        # return the updted solutions in the response
        schema = SolutionDeploymentSchema(many=False)
        data = schema.dump(update_solution)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Solution {oid} not found")


# Send the solution to the DAC
def send_solution_deployment_to_the_dac(solution_deployment):
    oid = solution_deployment.get('id')
    resp_json = None
    try:
        response = requests.post(deployment_create_url, data=json.dumps(solution_deployment), headers=headers)
        resp_json = response.json()
        app.logger.debug("Response from Dac")
        app.logger.debug(pformat(resp_json))
    except Exception:
        app.logger.debug("send_solution_deployment_to_the_dac::Failed during request to DAC")
        resp_json_error = {
            "id": oid,
            "statusId": 500,
            "errorCode": "ERROR",
            "statusMessage": "Failed communicating with the DAC"
        }
        return resp_json_error

    try:
        taskid = resp_json.get('taskid', '')
        # update with taskId
        deployment_json = {
            "id": oid,
            "taskId": f"{taskid}",
            "deployed": False,
            "deploymentState": DEPLOYMENT_STATE['PENDING'],
            "statusId": 200,
            "statusCode": "200",
            "statusMessage": "Solution deployment sent."
        }

        app.logger.debug(f"send_solution_deployment_to_the_dac::deployment_json: {pformat(deployment_json)}")
        app.logger.debug(pformat(deployment_json))
        deployment_update(oid, deployment_json)
        return deployment_json
    except Exception:
        app.logger.debug("send_solution_deployment_to_the_dac::Failed updating the database with the response from the DAC.")
        resp_json_error = {
            "id": oid,
            "statusId": 500,
            "statusCode": "ERROR",
            "statusMessage": "Failed updating the database with the response from the DAC"
        }
        return resp_json_error


def validate_json(some_json):
    try:
        json.loads(some_json)
        return True
    except ValueError:
        return False


def get_solution_results_from_the_dac(oid, task_id):
    """
    Get the solution deployment results from the DAC.
    params: task_id
    """
    resp_json = None
    try:
        response = requests.get(deployment_create_result_url+task_id, headers=headers)
        resp_json = response.json()
        app.logger.debug("Response from Dac")
        app.logger.debug(pformat(resp_json))
        print(pformat(resp_json))
    except Exception:
        app.logger.debug("get_solution_results_from_the_dac::Failed during request to DAC")
        resp_json_error = {
            "id": oid,
            "statusId": 30,
            "statusCode": "ERROR",
            "statusMessage": "get_solution_results_from_the_dac::failed communicating with the DAC"
        }

    json = resp_json.get('tf_state', '')
    is_valid_json = validate_json(json)
    app.logger.debug(f"is_valid_json: {is_valid_json}")
    print(f"is_valid_json: {is_valid_json}")

    # update SolutionDeployment with results
    deployed = False
    if resp_json.get('status', 'ERROR') == DEPLOYMENT_STATE['SUCCESS']:
        deployed = True
    deployment_json = {
        "statusId": 200,
        "deployed": deployed,
        "deploymentState": resp_json.get('status', 'ERROR'),
        "statusCode": "200",
        "statusMessage": "Solution deployment updated."
    }
    app.logger.debug(f"get_solution_results_from_the_dac::deployment_json: {pformat(deployment_json)}")
    try:
        deployment_update(oid, deployment_json)
    except Exception:
        app.logger.debug("get_solution_results_from_the_dac::Failed updating the SolutionDeployment with the response from the DAC.")
        resp_json_error = {
            "id": oid,
            "statusId": 500,
            "statusCode": "500",
            "statusMessage": "get_solution_results_from_the_dac::Failed updating the SolutionDeployment with the response from the DAC."
        }
        return resp_json_error

    if is_valid_json and resp_json.get('status', '') == DEPLOYMENT_STATE['SUCCESS'] and len(json) > 0:
        tf_json = {
            "solutionId": oid,
            "json": json
        }
        print("tf_json: " + pformat(tf_json))
        solutionresourcejson.create(tf_json)
        
    try:
        # Update Solution Resource JSON
        app.logger.debug(f"is_valid_json: {is_valid_json}")
        if is_valid_json and resp_json.get('status', '') == DEPLOYMENT_STATE['SUCCESS'] and len(json) > 0:
            tf_json = {
                "solutionId": oid,
                "json": json
            }
            print("tf_json: " + pformat(tf_json))
            solutionresourcejson.create(tf_json)
        return deployment_json
    except Exception:
        app.logger.debug("get_solution_results_from_the_dac::Failed updating the SolutionResourceJSON with the response from the DAC.")
        resp_json = {
            "id": oid,
            "statusId": 500,
            "errorCode": "ERROR",
            "statusMessage": "get_solution_results_from_the_dac::Failed updating the SolutionResourceJSON with the response from the DAC."
        }
        return resp_json
