"""
This is the solution rollback module and supports all the solution rollback ReST actions for the
solutions collection
"""

# 3rd party modules
from pprint import pformat
import time
import os
import json
import logging
import requests
from flask import make_response, abort

from config import db, executor
from tb_houston_service.models import Solution, SolutionSchema
from tb_houston_service.DeploymentStatus import DeploymentStatus
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import SolutionRollbackSchema
from tb_houston_service import solutionresourcejson
from tb_houston_service import security
from tb_houston_service import notification
from config.db_lib import db_session


logger = logging.getLogger("tb_houston_service.solution_rollback")

rollback_delete_url = f"http://{os.environ['GCP_DAC_URL']}/dac/solution_async/"
rollback_delete_result_url = (
    f"http://{os.environ['GCP_DAC_URL']}/dac/solution_async/result/delete/"
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
                rollbackState = sol.rollbackState
                if rollbackState == DeploymentStatus.SUCCESS:
                    message = f"Your Solution {sol.id} ({sol.name}) rollback has completed successfully"
                else:
                    message = f"Your Solution {sol.id} ({sol.name}) rollback has failed."
                payload = {
                    "isActive": True,
                    "toUserId": user.id,
                    "importance": 1,
                    "message": message,
                    "isRead": False,
                    "solutionId": sol.id
                }
                notification.create(notification = payload, typeId = 5, dbsession = dbs)
            else:
                logger.warning("notify_user::Cannot send notification, unable to find the solution (%s).", sol.id)
        else:
            logger.warning("notify_user::Cannot send notification, unable to validate the token.")


def rollback_read_all():
    """
    This function responds to a request for /api/solutionrollbacks
    with the complete lists of pending/started/complete solution rollbacks.
    1. Solutions in a pending state and without a task_id are rolled-back.
    2. The status of Solutions in a pending state and with a task_id are updated from the DAC.

    :return:        json string of list of rolled-back solutions
                    id and rolled-back fields
    """

    logger.debug("rollback_read_all")

    solutions = db.session.query(Solution).filter(Solution.rollbackState != "").all()
    schema = SolutionRollbackSchema(many=True)
    data = schema.dump(solutions)

    db.session.close()
    logger.debug("solutions data: %s", data)
    return data, 200


def rollback_read_one(oid):
    """
    This function responds to a request for /api/solutionrollback/{oid}
    with one matching solution-rollback from solutions

    :param application:   id of solution to find
    :return:              solution matching id
    """

    sol = db.session.query(Solution).filter(Solution.id == oid).one_or_none()
    db.session.close()

    if sol is not None:
        # Serialize the data for the response
        solution_schema = SolutionRollbackSchema(many=False)
        data = solution_schema.dump(sol)
        return data, 200
    else:
        abort(404, f"Solution with id {oid} not found".format(id=oid))


def start_rollback(solutionId):
    logger.debug("start_rollback")

    deployment_complete = False 
    with db_session() as dbs:
        while deployment_complete == False:
            sol = dbs.query(Solution).filter(Solution.id == solutionId).one_or_none()
            if sol:
                if sol.rollbackState == DeploymentStatus.SUCCESS or sol.rollbackState == DeploymentStatus.FAILURE:
                    deployment_complete = True
                    logger.debug("start_rollback::rollback complete for Solution: %s", sol.id)                
                else:
                    oid = sol.id
                    rollback_task_id = sol.rollbackTaskId
                    logger.debug("start_rollback: rollbackState: %s, oid: %s, rollback_task_id %s", sol.rollbackState, oid, rollback_task_id)
                    if rollback_task_id is None or rollback_task_id == "":
                        response = rollback_solution(sol, dbsession = dbs)
                        logger.debug("start_rollback::rollback_solution: oid: %s", oid)
                        logger.debug(pformat(response))
                    else:
                        logger.debug("start_rollback::polling_results_from_the_DaC: oid: %s rollback_task_id: %s", oid, rollback_task_id)
                        response = get_solution_results_from_the_dac(oid, rollback_task_id, dbsession = dbs)
                        logger.debug(pformat(response))
                    logger.debug("Sleep 2")
                    time.sleep(2)
            else:
                logger.debug("start_rollback::rollback Solution not found: %s", sol.id)                       
    notify_user(solutionId = solutionId)     
    return True


def rollback_create(solutionRollbackDetails):
    """
    This function sends a solution deployment rollback request to the DaC

    :param solution:  id
    :return:        201 on success
    :               404 if solution not found
    :               500 if other failure
    """

    logger.debug(pformat(solutionRollbackDetails))

    oid = solutionRollbackDetails["id"]
    sol = db.session.query(Solution).filter(Solution.id == oid).one_or_none()

    if sol is None:
        abort(404, f"Solution with id {oid} not found".format(id=oid))

    with db_session() as dbs:
        if sol.rollbackState == DeploymentStatus.SUCCESS:
            resp_json = {"id": oid, "rollbackState": sol.rollbackState}
        else:
            schema = SolutionSchema(many=False)
            update_solution = schema.load(solutionRollbackDetails, session=db.session)
            update_solution.id = oid
            update_solution.lastUpdated = ModelTools.get_utc_timestamp()
            update_solution.rollbackState = DeploymentStatus.PENDING
            update_solution.rollbackTaskId = None
            dbs.merge(update_solution)
            resp_json = {"id": oid, "rollbackState": update_solution.rollbackState}
            # This step is in a separate thread.       
    executor.submit(start_rollback, oid)
    return make_response(resp_json, 200)


def rollback_update(oid, solutionRollbackDetails, dbsession):
    """
    Updates an existing solutions in the solutions list with the rollback status.

    :param key:    id of the solution
    :param solutionDetails:   solution details to update
    :return:       updated solution
    """

    logger.debug(solutionRollbackDetails)

    # Does the solutions exist in solutions list?
    existing_solution = (
        dbsession.query(Solution).filter(Solution.id == oid).one_or_none()
    )

    # Does solutions exist?

    if existing_solution is not None:
        schema = SolutionSchema(many=False)
        update_solution = schema.load(solutionRollbackDetails, session=db.session)
        update_solution.id = oid
        update_solution.lastUpdated = ModelTools.get_utc_timestamp()
        update_solution.deploymentState = solutionRollbackDetails.get(
            "rollbackState", existing_solution.rollbackState
        )
        update_solution.rollbackTaskId = solutionRollbackDetails.get(
            "rollbackTaskId", existing_solution.rollbackTaskId
        )

        dbsession.merge(update_solution)
        dbsession.flush()

        # return the updted solutions in the response
        schema = SolutionRollbackSchema(many=False)
        data = schema.dump(update_solution)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Solution {oid} not found")

#
def rollback_solution(sol_rollback, dbsession):
    logger.debug("rollback_solution")
    status = send_solution_rollback_to_the_dac(sol_rollback, dbsession = dbsession)
    return status, 200


# Send the solution to the DAC
def send_solution_rollback_to_the_dac(sol_rollback, dbsession):
    oid = sol_rollback.id
    try:
        response = requests.delete(
            rollback_delete_url + str(sol_rollback.id), headers=headers
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
        rollbackTaskId = resp_json.get("taskid", None)
        # update with taskId
        rollback_json = {
            "id": oid,
            "rollbackTaskId": rollbackTaskId,
            "rollbackState": DeploymentStatus.PENDING,
            "statusMessage": "Solution rollback sent.",
        }

        logger.debug(
            "send_solution_rollback_to_the_dac::rollback_json: %s",
            pformat(rollback_json),
        )
        logger.debug(pformat(rollback_json))
        rollback_update(oid, rollback_json, dbsession = dbsession)
        return rollback_json
    except requests.exceptions.RequestException as e:
        logger.debug(
            "send_solution_rollback_to_the_dac::Failed updating the database with the response from the DAC, %s.",
            e,
        )
        abort(
            "send_solution_rollback_to_the_dac::Failed updating the database with the response from the DAC.",
            500,
        )


def validate_json(some_json):
    try:
        json.loads(some_json)
        return True
    except ValueError:
        return False


def get_solution_results_from_the_dac(oid, rollback_task_id, dbsession):
    """
    Get the solution rollback results from the DAC.
    params: task_id
    """
    logger.debug(f"get_solution_results_from_the_dac: oid: %s taskId: %s", oid, rollback_task_id)
    resp_json = None
    try:
        response = requests.get(rollback_delete_result_url + rollback_task_id, headers=headers)
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
        deployed = False
    rollback_json = {
        "statusId": 200,
        "deployed": deployed,
        "rollbackState": resp_json.get("status", "ERROR"),
        "statusMessage": "Solution rollback updated.",
    }
    logger.debug(
        "get_solution_results_from_the_dac::rollback_json: %s",
        pformat(rollback_json),
    )
    try:
        rollback_update(oid, rollback_json, dbsession)
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
        return make_response(rollback_json, 200)

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
            logger.debug("tf_json: " + pformat(tf_json))
            solutionresourcejson.delete(oid)
        return rollback_json
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_solution_results_from_the_dac::Failed deleting the SolutionResourceJSON with the response from the DAC, %s",
            e,
        )
        abort(
            "get_solution_results_from_the_dac::Failed deleting the SolutionResourceJSON with the response from the DAC.",
            500
        )
