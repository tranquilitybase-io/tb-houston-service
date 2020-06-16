import json
import time
import logging
import requests
import os
from pprint import pformat
from flask import make_response, abort
from config import db, executor
from tb_houston_service.DeploymentStatus import DeploymentStatus
from tb_houston_service.models import Application
from tb_houston_service.models import ApplicationDeployment, ApplicationDeploymentSchema
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedApplicationDeploymentSchema
from tb_houston_service.extendedSchemas import ExtendedApplicationForDACSchema


logger = logging.getLogger("tb_houston_service.application_deployment")

deployment_create_url = f"http://{os.environ['GCP_DAC_URL']}/dac/application_async/"
deployment_create_result_url = (
    f"http://{os.environ['GCP_DAC_URL']}/dac/application_async/result/create/"
)
headers = {"Content-Type": "application/json"}


def start_deployment(applicationId):
    print("start_deployment")
    deployment_complete = False 
    while deployment_complete == False:
        app_dep = db.session.query(ApplicationDeployment).filter(ApplicationDeployment.applicationId == applicationId).one_or_none()
        if app_dep:
            if app_dep.deploymentState == DeploymentStatus.SUCCESS:
                deployment_complete = True
                logger.debug("start_deployment::deployment complete for Application: %s", app_dep.applicationId)                
            else:
                oid = app_dep.applicationId
                task_id = app_dep.taskId
                logger.debug("start_deployment: deploymentState: %s, oid: %s, task_id %s", app_dep.deploymentState, oid, task_id)
                if task_id is None or task_id == "":
                    response = deploy_application(app_dep)
                    logger.debug("start_deployment::deploy_application: oid: %s", oid)
                    logger.debug(pformat(response))
                else:
                    logger.debug("start_deployment::polling_results_from_the_DaC: oid: %s task_id: %s", oid, task_id)
                    response = get_application_results_from_the_dac(oid, task_id)
                    logger.debug(pformat(response))
                print("Sleep 5")
                time.sleep(5)
        else:
            logger.debug("start_deployment::deployment Solution not found: %s", app_dep.applicationId)            
    db.session.close()
    return True


def deployment_create(applicationDeploymentDetails):
    """
    This function queries a application forwards the request to the DaC

    :param solution:  id
    :return:        201 on success
    :               404 if application not found
    :               500 if other failure
    """

    logger.debug("deployment_create: %s", pformat(applicationDeploymentDetails))
    oid = applicationDeploymentDetails["id"]
    app = db.session.query(Application).filter(Application.id == oid).one_or_none()
    app_deployment = db.session.query(ApplicationDeployment).filter(ApplicationDeployment.applicationId == oid).one_or_none()

    if not app:
      abort("This application doesn't exist.", 404)

    resp_json = {}
    if app_deployment:
        resp_json = {"id": oid, "deploymentState": app_deployment.deploymentState}
    else:
      schema = ApplicationDeploymentSchema(many=False)
      app_deployment_dict = {}
      app_deployment_dict["applicationId"] = oid
      app_deployment_dict["lastUpdated"] = ModelTools.get_utc_timestamp()
      app_deployment_dict["deploymentState"] = DeploymentStatus.PENDING
      app_deployment_dict["taskId"] = None
      app_deployment_dict["solutionId"] = app.solutionId
      app_deployment = schema.load(app_deployment_dict, session=db.session)      
  
      db.session.add(app_deployment)
      db.session.commit()
      resp_json = {"id": oid, "deploymentState": app_deployment.deploymentState}

    db.session.close()
    executor.submit(start_deployment, app_deployment.applicationId)
    return make_response(resp_json, 200)


def deployment_read_all():
    app_deployments = (
        db.session.query(ApplicationDeployment).filter(ApplicationDeployment.deploymentState != "").all()
    )
    schema = ExtendedApplicationDeploymentSchema(many=True)
    data = schema.dump(app_deployments)

    db.session.close()
    logger.debug("applications data: %s", data)
    return data, 200


def deployment_update(oid, applicationDeploymentDetails):
    """
    Updates an existing applications in the application list with the deployed status.

    :param key:    id of the application
    :param solutionDetails:   application details to update
    :return:       updated application
    """

    logger.debug(applicationDeploymentDetails)

    # Does the application exist in application list?
    existing_application_deployment = (
        db.session.query(ApplicationDeployment).filter(ApplicationDeployment.applicationId == oid).one_or_none()
    )

    # Does the application deployment exist?
    if existing_application_deployment is not None:
        schema = ApplicationDeploymentSchema(many=False)       
        applicationDeploymentDetails['applicationId'] = oid
        if "id" in applicationDeploymentDetails:
            del applicationDeploymentDetails["id"]
        app = db.session.query(Application).filter(Application.id == oid).one_or_none()
        if app:
          applicationDeploymentDetails['solutionId'] = app.solutionId      
        update_application_deployment = schema.load(
            applicationDeploymentDetails, session=db.session
        )
        update_application_deployment.applicationId = oid
        update_application_deployment.lastUpdated = ModelTools.get_utc_timestamp()
        db.session.merge(update_application_deployment)
        db.session.commit()

        # return the updted solutions in the response
        schema = ApplicationDeploymentSchema(many=False)
        data = schema.dump(update_application_deployment)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Solution {oid} not found")


def deploy_application(app_deployment):
    return send_application_deployment_to_the_dac(app_deployment)


# Send the application to the DAC
def send_application_deployment_to_the_dac(app_deployment):
    oid = app_deployment.applicationId
    schema = ExtendedApplicationForDACSchema(many=False)
    application_deployment_data = schema.dump(app_deployment)
    application_deployment_data = json.dumps(application_deployment_data, indent=4)
    logger.debug(
        "send_application_deployment_to_the_dac::application_deployment: %s",
        application_deployment_data,
    )
    resp_json = None
    try:
        response = requests.post(
            deployment_create_url, data=application_deployment_data, headers=headers
        )
        resp_json = response.json()
        logger.debug(
            "send_application_deployment_to_the_dac::ResponseFromDAC: %s",
            pformat(resp_json),
        )
    except requests.exceptions.RequestException as e:
        logger.debug(
            "send_application_deployment_to_the_dac::Failed during request to DAC %s", e
        )
        abort("Failed communicating with the DAC", 500)

    try:
        taskid = resp_json.get("taskid", None)
        # update with taskId
        deployment_json = {
            "id": oid,
            "taskId": taskid,
            "deploymentState": DeploymentStatus.PENDING,
        }

        logger.debug(
            "send_application_deployment_to_the_dac::deployment_json: %s",
            pformat(deployment_json),
        )
        logger.debug(pformat(deployment_json))
        deployment_update(oid, deployment_json)
        return deployment_json
    except requests.exceptions.RequestException as e:
        logger.debug(
            "send_application_deployment_to_the_dac::Failed updating the database with the response from the DAC, %s.",
            e,
        )
        abort(
            "send_application_deployment_to_the_dac::Failed updating the database with the response from the DAC.",
            500,
        )


def validate_json(some_json):
    try:
        json.loads(some_json)
        return True
    except ValueError:
        return False


def get_application_results_from_the_dac(oid, task_id):
    """
    Get the application deployment results from the DAC.
    params: task_id
    """
    logger.debug(
        "get_application_results_from_the_dac: oid: %s taskId: %s", oid, task_id
    )
    resp_json = None
    try:
        response = requests.get(deployment_create_result_url + task_id, headers=headers)
        resp_json = response.json()
        logger.debug("Response from Dac: %s", resp_json)
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_application_results_from_the_dac::Failed during request to DAC, %s", e
        )
        abort(
            "get_application_results_from_the_dac::failed communicating with the DAC",
            500,
        )

    # update ApplicationDeployment with results
    deployment_json = {
      "applicationId": oid,
      "deploymentState": resp_json.get("status", "ERROR")
    }
    logger.debug(
        "get_application_results_from_the_dac::deployment_json: %s",
        pformat(deployment_json),
    )
    try:
        deployment_update(oid, deployment_json)
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_application_results_from_the_dac::Failed updating the ApplicationDeployment with the response from the DAC, %s",
            e,
        )
        abort(
            "get_application_results_from_the_dac::Failed updating the ApplicationDeployment with the response from the DAC.",
            500,
        )

    if resp_json.get("status", "ERROR") != DeploymentStatus.SUCCESS:
        return make_response(deployment_json, 200)

    my_json = resp_json.get("payload", "")
    is_valid_json = validate_json(my_json)
    logger.debug("is_valid_json: %s", is_valid_json)


    # TODO
    # try:
    #     # Update Solution Resource JSON
    #     if (
    #         is_valid_json
    #         and resp_json.get("status", "") == DeploymentStatus.SUCCESS
    #         and len(my_json) > 0
    #     ):
    #         tf_json = {"solutionId": oid, "json": my_json}
    #         # print("tf_json: " + pformat(tf_json))
    #         # TODO: Need to uncomment and test
    #         # applicationresourcejson.create(tf_json)
    #     return deployment_json
    # except requests.exceptions.RequestException as e:
    #     logger.debug(
    #         "get_application_results_from_the_dac::Failed updating the ApplicationResourceJSON with the response from the DAC, %s",
    #         e,
    #     )
    #     abort(
    #         "get_application_results_from_the_dac::Failed updating the ApplicationResourceJSON with the response from the DAC.",
    #         500,
    #     )
