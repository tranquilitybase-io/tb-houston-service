"""
This is the deployments module and supports all the ReST actions for the
solutions collection
"""

# 3rd party modules
from pprint import pformat
import time
import os
import json
import logging
from http import HTTPStatus
import requests
from flask import make_response, abort

from config import db, executor
from tb_houston_service.models import Solution, SolutionSchema
from tb_houston_service.DeploymentStatus import DeploymentStatus
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedSolutionForDACSchema
from tb_houston_service.extendedSchemas import SolutionDeploymentSchema
from tb_houston_service import folder
from tb_houston_service import team
from tb_houston_service import gcp_dac_folder_deployment
from tb_houston_service import solution_extension
from tb_houston_service import solutionresourcejson
from tb_houston_service import security
from tb_houston_service import notification
from config.db_lib import db_session


logger = logging.getLogger("tb_houston_service.solution_deployment")

deployment_create_url = f"http://{os.environ['GCP_DAC_URL']}/dac/solution_async/"
deployment_create_result_url = (
    f"http://{os.environ['GCP_DAC_URL']}/dac/solution_async/result/create/"
)
headers = {"Content-Type": "application/json"}

authorization_token = None

def notify_user(solutionId):
    """
    Notify the user the solution deployment has completed.

    Args:
        solutionId ([int]): [The solution id]
    """

    with db_session() as dbs:
        user = security.get_valid_user_from_token(dbsession = dbs)
        logger.debug("user: %s", user)
        if user:
            sol = dbs.query(Solution).filter(Solution.id == solutionId).one_or_none()
            if sol:
                deploymentState = sol.deploymentState
                if deploymentState == DeploymentStatus.SUCCESS:
                    message = f"Your Solution {sol.id} ({sol.name}) deployment has completed successfully"
                else:
                    message = f"Your Solution {sol.id} ({sol.name}) deployment has failed."
                payload = {
                    "isActive": True,
                    "toUserId": user.id,
                    "importance": 1,
                    "message": message,
                    "isRead": False,
                    "solutionId": sol.id
                }
                notification.create(notification = payload, typeId = 4, dbsession = dbs)
            else:
                logger.warning("notify_user::Cannot send notification, unable to find the solution (%s).", sol.id)
        else:
            logger.warning("notify_user::Cannot send notification, unable to validate the token.")


def deployment_read_all():
    """
    This function responds to a request for /api/solutiondeployments
    with the complete lists of deployed pending/started/complete solutions.
    1. Solutions in a pending state and without a task_id are deployed.
    2. The status of Solutions in a pending state and with a task_id are updated from the DAC.

    :return:        json string of list of deployed solutions
                    id and deployed fields
    """

    logger.debug("deployment_read_all")

    solutions = db.session.query(Solution).filter(Solution.deploymentState != "").all()
    schema = SolutionDeploymentSchema(many=True)
    data = schema.dump(solutions)

    db.session.close()
    logger.debug("solutions data: %s", data)
    return data, 200


def deployment_read_one(oid):
    """
    This function responds to a request for /api/solutiondeployment/{oid}
    with one matching solution deployment from solutions

    :param application:   id of solution to find
    :return:              solution matching id
    """

    sol = db.session.query(Solution).filter(Solution.id == oid).one_or_none()
    db.session.close()

    if sol is not None:
        # Serialize the data for the response
        solution_schema = SolutionDeploymentSchema(many=False)
        data = solution_schema.dump(sol)
        return data, 200
    else:
        abort(404, f"Solution with id {oid} not found".format(id=oid))


def start_deployment(solutionId):
    logger.debug("start_deployment")

    with db_session() as dbs:
        deployment_complete = False 
        while deployment_complete == False:
            sol = db.session.query(Solution).filter(Solution.id == solutionId).one_or_none()
            if sol:
                if sol.deploymentState == DeploymentStatus.SUCCESS or sol.deploymentState == DeploymentStatus.FAILURE:
                    deployment_complete = True
                    logger.debug("start_deployment::deployment complete for Solution: %s", sol.id)                
                else:
                    oid = sol.id
                    task_id = sol.taskId
                    logger.debug("start_deployment: deploymentState: %s, oid: %s, task_id %s", sol.deploymentState, oid, task_id)
                    if task_id is None or task_id == "":
                        response = deploy_folders_and_solution(sol)
                        logger.debug("start_deployment::deploy_folders_and_solution: oid: %s", oid)
                        logger.debug(pformat(response))
                    else:
                        logger.debug("start_deployment::polling_results_from_the_DaC: oid: %s task_id: %s", oid, task_id)
                        response = get_solution_results_from_the_dac(oid, task_id)
                        logger.debug(pformat(response))
                    logger.debug("Sleep 2")
                    time.sleep(2)
            else:
                logger.debug("start_deployment::deployment Solution not found: %s", sol.id)                       
    notify_user(solutionId = solutionId)     
    return True


def deployment_create(solutionDeploymentDetails):
    """
    This function queries a solution forwards the request to the DaC

    :param solution:  id
    :return:        201 on success
    :               404 if solution not found
    :               500 if other failure
    """

    logger.debug(pformat(solutionDeploymentDetails))

    oid = solutionDeploymentDetails["id"]
    sol = db.session.query(Solution).filter(Solution.id == oid).one_or_none()

    if sol is None:
        abort(404, f"Solution with id {oid} not found".format(id=oid))

    if sol.deploymentState == DeploymentStatus.SUCCESS:
        resp_json = {"id": oid, "deploymentState": sol.deploymentState}
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
        resp_json = {"id": oid, "deploymentState": update_solution.deploymentState}
        # This step is in a separate thread.
        db.session.close()        
        executor.submit(start_deployment, sol.id)

    return make_response(resp_json, 200)


def deployment_update(oid, solutionDeploymentDetails):
    """
    Updates an existing solutions in the solutions list with the deployed status.

    :param key:    id of the solution
    :param solutionDetails:   solution details to update
    :return:       updated solution
    """

    logger.debug(solutionDeploymentDetails)

    # Does the solutions exist in solutions list?
    existing_solution = (
        db.session.query(Solution).filter(Solution.id == oid).one_or_none()
    )

    # Does solutions exist?

    if existing_solution is not None:
        schema = SolutionSchema(many=False)
        update_solution = schema.load(solutionDeploymentDetails, session=db.session)
        update_solution.id = oid
        update_solution.lastUpdated = ModelTools.get_utc_timestamp()
        update_solution.deployed = solutionDeploymentDetails.get(
            "deployed", existing_solution.deployed
        )
        update_solution.deploymentState = solutionDeploymentDetails.get(
            "deploymentState", existing_solution.deploymentState
        )
        update_solution.statusId = solutionDeploymentDetails.get(
            "statusId", existing_solution.statusId
        )
        update_solution.statusCode = solutionDeploymentDetails.get(
            "statusCode", existing_solution.statusCode
        )
        update_solution.statusMessage = solutionDeploymentDetails.get(
            "statusMessage", existing_solution.statusMessage
        )
        update_solution.taskId = solutionDeploymentDetails.get(
            "taskId", existing_solution.taskId
        )
        update_solution.deploymentFolderId = solutionDeploymentDetails.get(
            "deploymentFolderId", existing_solution.deploymentFolderId
        )

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
    logger.debug("create_folder: %s, %s", folderId, folderName)
    resp = folder.read_or_create_by_parent_folder_id_and_folder_name(
        folderId, folderName
    )
    next_folder_id = None
    status = DeploymentStatus.PENDING
    if resp[1] == HTTPStatus.OK:
        resp_dict = resp[0]
        logger.debug("create_folder_resp: %s", resp_dict)
        # send folder to GCP DAC
        task_id = resp_dict["taskId"]
        status = resp_dict["status"]
        db_folder_id = resp_dict["id"]
        next_folder_id = resp_dict["folderId"]
        if status != DeploymentStatus.SUCCESS:
            # The folder creation is not complete
            if task_id == None:
                # Request for folder to be created on the DAC
                # Obtain a taskId, which is updated on the folder table
                dac_create_payload = {
                    "folder": {"parentFolderId": folderId, "folderName": folderName}
                }
                dac_resp = gcp_dac_folder_deployment.create(dac_create_payload)
                dac_resp_json = dac_resp[0]
                logger.debug(
                    "create_folder::create_results::dac_folder_resp: %s", dac_resp_json
                )
                if dac_resp_json.get("taskid"):
                    logger.debug(
                        "create_folder::update_db::taskId: %s",
                        dac_resp_json.get("taskid"),
                    )
                    resp_dict["taskId"] = dac_resp_json.get("taskid")
                    folder.update(db_folder_id, resp_dict)
            else:
                # We have a task_id, query for results
                # Obtain the folder id (means the folder has been created by the DAC)
                # folder_id updated on the database along with the status
                dac_resp = gcp_dac_folder_deployment.get_create_results(task_id)
                dac_resp_json = dac_resp[0]
                logger.debug("create_folder::create_dac_folder_resp: %s", dac_resp_json)
                if dac_resp_json.get("status") == DeploymentStatus.SUCCESS:
                    payload = json.loads(dac_resp_json.get("payload"))
                    dac_folder_id = gcp_dac_folder_deployment.get_folder_id_from_payload(
                        payload
                    )
                    if dac_folder_id:
                        resp_dict["folderId"] = dac_folder_id
                        resp_dict["status"] = DeploymentStatus.SUCCESS
                        folder.update(db_folder_id, resp_dict)
                        next_folder_id = dac_folder_id
                    else:
                        logger.error(
                            "Unable to get folder_id for folder %sfrom the DAC payload, skipping.",
                            folderName,
                        )

    # return current status and next_folder_id if avaiable,
    # if not available may be available in the next iteration.
    return (next_folder_id, status)


# Return SUCCESS if all folders have been created on the DB and DAC
def create_folders(solution):
    logger.debug("create_folders::solution: %s", pformat(solution))
    resp = gcp_dac_folder_deployment.metadata()
    logger.debug("resp_json: {resp.json()}")
    dac_metadata = resp.json()
    logger.debug("dac_metadata: %s", dac_metadata)
    root_folder_id = dac_metadata["root_folder_id"]
    folder_id = root_folder_id
    status = DeploymentStatus.SUCCESS

    folder_meta = folder.get_folder_meta()
    logger.debug("solution_deployment::folder_meta: %s", folder_meta)

    if status == DeploymentStatus.SUCCESS and folder.APPLICATIONS in folder_meta:
        (folder_id, status) = create_folder(folder_id, folder.APPLICATIONS)
    if status == DeploymentStatus.SUCCESS and folder.BUSINESS_UNIT in folder_meta:
        (folder_id, status) = create_folder(folder_id, solution.businessUnit.name)
    if status == DeploymentStatus.SUCCESS and folder.TEAM in folder_meta:
        oteam = team.read_one(solution.teamId)
        logger.debug("team: %s", oteam)
        team_name = oteam.get("name")
        logger.debug("team_name: %s", team_name)
        (folder_id, status) = create_folder(folder_id, team_name)

    data = {}
    data["deploymentFolderId"] = folder_id
    data["status"] = status
    logger.debug("create_folders::return %s", data)
    return data


#
def deploy_folders_and_solution(sol_deployment):
    logger.debug("deploy_folders_and_solution")
    with db_session() as dbs:
        solution = solution_extension.expand_solution(sol_deployment, dbsession = dbs)
        create_folders_resp = create_folders(solution)
        deploymentFolderId = create_folders_resp.get("deploymentFolderId")
        status = create_folders_resp.get("status")
        logger.debug(
            "deploy_folders_and_solution::deploymentFolderId: %s status: %s",
            deploymentFolderId,
            status,
        )
        if deploymentFolderId and status == DeploymentStatus.SUCCESS:
            solution.deploymentFolderId = deploymentFolderId
            status = send_solution_deployment_to_the_dac(solution, dbsession = dbs)
        return status, 200


# Send the solution to the DAC
def send_solution_deployment_to_the_dac(sol_deployment, dbsession):
    oid = sol_deployment.id
    solution = solution_extension.expand_solution_for_dac(sol_deployment, dbsession = dbsession)
    schema = ExtendedSolutionForDACSchema(many=False)
    solution_data = schema.dump(solution)
    solution_data = json.dumps(solution_data, indent=4)
    logger.debug(
        "send_solution_deployment_to_the_dac::solution_deployment: %s", solution_data
    )
    resp_json = None
    try:
        response = requests.post(
            deployment_create_url, data=solution_data, headers=headers
        )
        resp_json = response.json()
        logger.debug(
            "send_solution_deployment_to_the_dac::ResponseFromDAC: %s",
            pformat(resp_json),
        )
    except requests.exceptions.RequestException as e:
        logger.debug(
            "send_solution_deployment_to_the_dac::Failed during request to DAC %s", e
        )
        abort("Failed communicating with the DAC", 500)

    try:
        taskid = resp_json.get("taskid", None)
        # update with taskId
        deployment_json = {
            "id": oid,
            "taskId": taskid,
            "deployed": False,
            "deploymentState": DeploymentStatus.PENDING,
            "statusId": 200,
            "statusCode": "200",
            "statusMessage": "Solution deployment sent.",
            "deploymentFolderId": sol_deployment.deploymentFolderId,
        }

        logger.debug(
            "send_solution_deployment_to_the_dac::deployment_json: %s",
            pformat(deployment_json),
        )
        logger.debug(pformat(deployment_json))
        deployment_update(oid, deployment_json)
        return deployment_json
    except requests.exceptions.RequestException as e:
        logger.debug(
            "send_solution_deployment_to_the_dac::Failed updating the database with the response from the DAC, %s.",
            e,
        )
        abort(
            "send_solution_deployment_to_the_dac::Failed updating the database with the response from the DAC.",
            500,
        )


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
    logger.debug(f"get_solution_results_from_the_dac: oid: %s taskId: %s", oid, task_id)
    resp_json = None
    try:
        response = requests.get(deployment_create_result_url + task_id, headers=headers)
        resp_json = response.json()
        logger.debug("Response from Dac: %s", resp_json)
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_solution_results_from_the_dac::Failed during request to DAC, %s", e
        )
        abort(
            "get_solution_results_from_the_dac::failed communicating with the DAC", 500
        )

    # update SolutionDeployment with results
    deployed = False
    if resp_json.get("status", "ERROR") == DeploymentStatus.SUCCESS:
        deployed = True
    deployment_json = {
        "statusId": 200,
        "deployed": deployed,
        "deploymentState": resp_json.get("status", "ERROR"),
        "statusCode": "200",
        "statusMessage": "Solution deployment updated.",
    }
    logger.debug(
        "get_solution_results_from_the_dac::deployment_json: %s",
        pformat(deployment_json),
    )
    try:
        deployment_update(oid, deployment_json)
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_solution_results_from_the_dac::Failed updating the SolutionDeployment with the response from the DAC, %s",
            e,
        )
        abort(
            "get_solution_results_from_the_dac::Failed updating the SolutionDeployment with the response from the DAC.",
            500,
        )

    if resp_json.get("status", "ERROR") != DeploymentStatus.SUCCESS:
        return make_response(deployment_json, 200)

    my_json = resp_json.get("payload", "")
    is_valid_json = validate_json(my_json)
    logger.debug("is_valid_json: %s", is_valid_json)

    try:
        # Update Solution Resource JSON
        if (
            is_valid_json
            and resp_json.get("status", "") == DeploymentStatus.SUCCESS
            and len(my_json) > 0
        ):
            tf_json = {"solutionId": oid, "json": my_json}
            # print("tf_json: " + pformat(tf_json))
            solutionresourcejson.create(tf_json)
        return deployment_json
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_solution_results_from_the_dac::Failed updating the SolutionResourceJSON with the response from the DAC, %s",
            e,
        )
        abort(
            "get_solution_results_from_the_dac::Failed updating the SolutionResourceJSON with the response from the DAC.",
            500
        )
