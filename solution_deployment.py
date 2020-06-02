"""
This is the deployments module and supports all the ReST actions for the
solutions collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import Solution, SolutionSchema
from models import ModelTools
from extendedSchemas import ExtendedSolutionSchema
from extendedSchemas import SolutionDeploymentSchema
import solution_extension
from pprint import pformat
import requests
import os
import json
import solutionresourcejson
from DeploymentStatus import DeploymentStatus
import folder
import gcp_dac_folder_deployment
from tb_houston_service import team
from http import HTTPStatus


deployment_create_url = f"http://{os.environ['GCP_DAC_URL']}/api/solution_async/"
deployment_create_result_url = f"http://{os.environ['GCP_DAC_URL']}/api/solution_async/result/create/"
headers = { 'Content-Type': "application/json" }


def deployment_read_all():
    """
    This function responds to a request for /api/solutiondeployments
    with the complete lists of deployed pending/started/complete solutions.
    1. Solutions in a pending state and without a task_id are deployed.
    2. The status of Solutions in a pending state and with a task_id are updated from the DAC.

    :return:        json string of list of deployed solutions
                    id and deployed fields
    """

    app.logger.debug("solution.deployment_read_all")

    solutions = Solution.query.filter(Solution.deploymentState != "").all()
    # Loop through solutions, if not a SUCCESS
    #   - send folders
    #   - once folders are sent send solution deployment
    for sol in solutions:
        app.logger.debug(f"deployment_read_all::sol.deploymentState: {sol.deploymentState}")
        if sol.deploymentState != DeploymentStatus.SUCCESS:
            oid = sol.id
            task_id = sol.taskId
            if task_id is None or task_id == "":
                response = deploy_folders_and_solution(sol)
                app.logger.debug(pformat(response))                
            else:
                app.logger.debug(f"oid: {oid} {task_id}")
                response = get_solution_results_from_the_dac(oid, task_id)
                app.logger.debug(pformat(response))

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
    oid = solutionDeploymentDetails['id']
    sol = (Solution.query.filter(Solution.id == oid).one_or_none())

    if sol is None:
        abort(
            404, f"Solution with id {oid} not found".format(id=oid)
        )

    if sol.deploymentState == DeploymentStatus.SUCCESS:
        resp_json = {
            "id": oid,
            "deploymentState": sol.deploymentState
        }
    else:
        schema = SolutionSchema(many=False)
        update_solution = schema.load(solutionDeploymentDetails, session=db.session)
        update_solution.id = oid
        update_solution.lastUpdated = ModelTools.get_utc_timestamp()
        update_solution.deployed = False
        update_solution.deploymentState = DeploymentStatus.PENDING
        update_solution.taskId = None
        db.session.merge(update_solution)
        db.session.commit()        
        resp_json = {
            "id": oid,
            "deploymentState": update_solution.deploymentState
        }
    return make_response(resp_json, 200)


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
        update_solution.deploymentFolderId = solutionDeploymentDetails.get('deploymentFolderId', existing_solution.deploymentFolderId)

        db.session.merge(update_solution)
        db.session.commit()

        # return the updted solutions in the response
        schema = SolutionDeploymentSchema(many=False)
        data = schema.dump(update_solution)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Solution {oid} not found")



def create_folder(folderId, folderName):
    # retrieve+create folder from folder table
    # Returns folderId and Deployment Status
    # folderId is used as the parentFolderId for new folders
    resp = folder.read_or_create_by_parent_folder_id_and_folder_name(folderId, folderName)
    next_folder_id = None 
    status = DeploymentStatus.PENDING
    if resp[1] == HTTPStatus.OK:
        resp_dict = resp[0]
        app.logger.debug(f"create_folder_resp: {resp_dict}")
        # send folder to GCP DAC
        task_id = resp_dict['taskId']
        status = resp_dict['status']
        db_folder_id = resp_dict['id']        
        next_folder_id = resp_dict['folderId']
        if status != DeploymentStatus.SUCCESS:
            # The folder creation is not complete
            if task_id == None:
                # Request for folder to be created on the DAC
                # Obtain a taskId, which is updated on the folder table
                dac_create_payload = {
                    "folder": { "parentFolderId": folderId, "folderName": folderName }
                }
                dac_resp = gcp_dac_folder_deployment.create(dac_create_payload)
                dac_resp_json = dac_resp[0]
                app.logger.debug(f"create_folder::create_results::dac_folder_resp: {dac_resp_json}")
                if dac_resp_json.get('taskid'):
                    app.logger.debug(f"create_folder::update_db::taskId: {dac_resp_json.get('taskid')}")
                    resp_dict['taskId'] = dac_resp_json.get('taskid')
                    folder.update(db_folder_id, resp_dict)
            else:
                # We have a task_id, query for results
                # Obtain the folder id (means the folder has been created by the DAC)
                # folder_id updated on the database along with the status
                dac_resp = gcp_dac_folder_deployment.get_create_results(task_id)
                dac_resp_json = dac_resp[0]
                app.logger.debug(f"create_folder::create_dac_folder_resp: {dac_resp_json}")
                if dac_resp_json.get('status') == DeploymentStatus.SUCCESS:
                    payload = json.loads(dac_resp_json.get("payload"))
                    dac_folder_id = gcp_dac_folder_deployment.get_folder_id_from_payload(payload)
                    if dac_folder_id:
                        resp_dict['folderId'] = dac_folder_id
                        resp_dict['status'] = DeploymentStatus.SUCCESS                        
                        folder.update(db_folder_id, resp_dict)
                        next_folder_id = dac_folder_id
                    else:
                        app.logger.error(f"Unable to get folder_id for folder {folderName} from the DAC payload, skipping.")


    # return current status and next_folder_id if avaiable, 
    # if not available may be available in the next iteration.
    return (next_folder_id, status)


# Return SUCCESS if all folders have been created on the DB and DAC
def create_folders(solution):
    app.logger.debug(f"solution: {pformat(solution)}")
    folder_meta = folder.get_folder_meta()
    resp = gcp_dac_folder_deployment.metadata()
    app.logger.debug(f"resp_json: {resp.json()}")
    dac_metadata = resp.json()
    app.logger.debug(f"dac_metadata: {dac_metadata}")
    root_folder_id = dac_metadata['root_folder_id']
    folder_id = None    
    status = None
    if folder.APPLICATIONS in folder_meta:
        (folder_id, status) = create_folder(root_folder_id, folder.APPLICATIONS)
    if status == DeploymentStatus.SUCCESS and folder.BUSINESS_UNIT in folder_meta:
        (folder_id, status) = create_folder(folder_id, solution.businessUnit)
    if status == DeploymentStatus.SUCCESS and folder.TEAM in folder_meta:
        oteam = team.read_one(solution.teamId)
        app.logger.debug(f"team: {oteam}")
        team_name = oteam.get("name")
        app.logger.debug(f"team_name: {team_name}")
        (folder_id, status) = create_folder(folder_id, team_name)        

    data = {}
    data['deploymentFolderId'] = folder_id
    data['status'] = status
    app.logger.debug(f"create_folders::return {data}")
    return data
    

# 
def deploy_folders_and_solution(sol_deployment):
    create_folders_resp = create_folders(sol_deployment)
    deploymentFolderId = create_folders_resp.get("deploymentFolderId")
    status = create_folders_resp.get("status")    
    app.logger.debug(f"deploy_folders_and_solution::deploymentFolderId: {deploymentFolderId} status: {status}")
    if deploymentFolderId and status == DeploymentStatus.SUCCESS:
        sol_deployment.deploymentFolderId = deploymentFolderId
        status = send_solution_deployment_to_the_dac(sol_deployment)
    return status, 200


# Send the solution to the DAC
def send_solution_deployment_to_the_dac(sol_deployment):
    oid = sol_deployment.id
    solution = solution_extension.build_solution(sol_deployment)
    schema = ExtendedSolutionSchema(many=False)
    solution_data = json.dumps(schema.dump(solution))
    app.logger.debug(f"send_solution_deployment_to_the_dac::solution_deployment: {solution_data}")    
    resp_json = None
    try:
        response = requests.post(deployment_create_url, data=solution_data, headers=headers)
        resp_json = response.json()
        app.logger.debug(f"send_solution_deployment_to_the_dac::ResponseFromDAC: {pformat(resp_json)}")
    except Exception:
        app.logger.debug("send_solution_deployment_to_the_dac::Failed during request to DAC")
        abort("Failed communicating with the DAC", 500)

    try:
        taskid = resp_json.get('taskid', None)
        # update with taskId
        deployment_json = {
            "id": oid,
            "taskId": taskid,
            "deployed": False,
            "deploymentState": DeploymentStatus.PENDING,
            "statusId": 200,
            "statusCode": "200",
            "statusMessage": "Solution deployment sent.",
            "deploymentFolderId": sol_deployment.deploymentFolderId
        }

        app.logger.debug(f"send_solution_deployment_to_the_dac::deployment_json: {pformat(deployment_json)}")
        app.logger.debug(pformat(deployment_json))
        deployment_update(oid, deployment_json)
        return deployment_json
    except Exception:
        app.logger.debug("send_solution_deployment_to_the_dac::Failed updating the database with the response from the DAC.")
        abort("send_solution_deployment_to_the_dac::Failed updating the database with the response from the DAC.", 500)


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
    app.logger.debug(f"get_solution_results_from_the_dac: oid: {oid} taskId: {task_id}")
    resp_json = None
    try:
        response = requests.get(deployment_create_result_url+task_id, headers=headers)
        resp_json = response.json()
        app.logger.debug("Response from Dac")
        app.logger.debug(pformat(resp_json))
        print(pformat(resp_json))
    except Exception:
        app.logger.debug("get_solution_results_from_the_dac::Failed during request to DAC")
        abort("get_solution_results_from_the_dac::failed communicating with the DAC", 500)

    # update SolutionDeployment with results
    deployed = False
    if resp_json.get('status', 'ERROR') == DeploymentStatus.SUCCESS:
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
        abort("get_solution_results_from_the_dac::Failed updating the SolutionDeployment with the response from the DAC.", 500)


    if resp_json.get('status', 'ERROR') != DeploymentStatus.SUCCESS:
        return make_response(deployment_json, 200)

    json = resp_json.get('tf_state', '')
    is_valid_json = validate_json(json)
    app.logger.debug(f"is_valid_json: {is_valid_json}")
    print(f"is_valid_json: {is_valid_json}")

    if is_valid_json and resp_json.get('status', '') == DeploymentStatus.SUCCESS and len(json) > 0:
        tf_json = {
            "solutionId": oid,
            "json": json
        }
        print("tf_json: " + pformat(tf_json))
        solutionresourcejson.create(tf_json)
        
    try:
        # Update Solution Resource JSON
        app.logger.debug(f"is_valid_json: {is_valid_json}")
        if is_valid_json and resp_json.get('status', '') == DeploymentStatus.SUCCESS and len(json) > 0:
            tf_json = {
                "solutionId": oid,
                "json": json
            }
            print("tf_json: " + pformat(tf_json))
            solutionresourcejson.create(tf_json)
        return deployment_json
    except Exception:
        app.logger.debug("get_solution_results_from_the_dac::Failed updating the SolutionResourceJSON with the response from the DAC.")
        abort("get_solution_results_from_the_dac::Failed updating the SolutionResourceJSON with the response from the DAC.", 500)
