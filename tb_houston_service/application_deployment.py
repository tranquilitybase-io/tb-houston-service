import json
import time
import logging
import os
from pprint import pformat
import requests
from flask import make_response, abort

from config import db, executor
from config.db_lib import db_session
from models import  Application, Activator, ActivatorMetadata, \
                    ApplicationDeployment, ApplicationDeploymentSchema, \
                    LZLanVpc, LZEnvironment, LZLanVpcEnvironment, \
                    Solution, SolutionEnvironment, SolutionResource
from tb_houston_service import security
from tb_houston_service import notification
from tb_houston_service.DeploymentStatus import DeploymentStatus
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedApplicationDeploymentSchema
from tb_houston_service.extendedSchemas import ExtendedApplicationForDACSchema

logger = logging.getLogger("tb_houston_service.application_deployment")

deployment_create_url = f"http://{os.environ['GCP_DAC_URL']}/dac/application_async/"
deployment_create_result_url = (
    f"http://{os.environ['GCP_DAC_URL']}/dac/application_async/result/create/"
)
headers = {"Content-Type": "application/json"}

def notify_user(applicationId):
    """
    Notify the user the application deployment has completed.

    Args:
        applicationId ([int]): [The application id]
    """
    with db_session() as dbs:
        user = security.get_valid_user_from_token(dbsession=dbs)
        logger.debug("user: %s", user)        
        if user:
            (app, app_deploy) = dbs.query(Application, ApplicationDeployment).filter(
                ApplicationDeployment.applicationId == applicationId,
                ApplicationDeployment.applicationId == Application.id
                ).one_or_none()
            if app:
                deploymentState = app_deploy.deploymentState
                if deploymentState == DeploymentStatus.SUCCESS:
                    message = f"Your Application {applicationId} ({app.name}) deployment has completed successfully"
                else:
                    message = f"Your Application {applicationId} ({app.name}) deployment has failed."                    
                payload = {
                    "isActive": True,
                    "toUserId": user.id,
                    "importance": 1,
                    "message": message,
                    "isRead": False,
                    "applicationId": app.id
                }
                notification.create(notification = payload, typeId = 3, dbsession = dbs)
            else:
                logger.warning("Cannot send notification, unable to find the application (%s).", app.id)
        else:
            logger.warning("Cannot send notification, unable to validate the token.")

def start_deployment(applicationId):
    logger.info("start_deployment::applicationId: %s", applicationId)
    # can only deploy an application if the solution it belong's to has already been
    # deployed successfully.
    with db_session() as dbs:
        deployment_complete = False 
        while deployment_complete == False:
            app_dep = dbs.query(ApplicationDeployment).filter(
                ApplicationDeployment.applicationId == applicationId,
                ApplicationDeployment.deploymentState.notin_((
                    DeploymentStatus.SUCCESS, 
                    DeploymentStatus.FAILURE
                ))
            ).first()
            logger.debug("start_deployment::app_dep *** %s", app_dep)
            if app_dep:
                app_id = app_dep.applicationId
                task_id = app_dep.taskId
                logger.debug("start_deployment: deploymentState: %s, app_id: %s, workspaceProjectId %s, task_id %s", app_dep.deploymentState, app_id, app_dep.workspaceProjectId, task_id)
                if task_id is None or task_id == "":
                    response = deploy_application(app_dep, dbsession = dbs)
                    dbs.flush()
                    logger.debug("start_deployment::deploy_application: app_id: %s", app_id)
                    logger.debug(pformat(response))
                else:
                    logger.debug("start_deployment::polling_results_from_the_DaC: app_id: %s task_id: %s", app_id, task_id)
                    get_application_results_from_the_dac(app_id = app_id, lzEnvId = app_dep.lzEnvironmentId, task_id = task_id, dbsession = dbs)
                    dbs.flush()
                print("Sleep 2")
                time.sleep(2)
            else:
                deployment_complete = True   
        logger.debug("start_deployment::deployment complete for Application: %s", applicationId)                       
    notify_user(applicationId = applicationId)     
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
    app_id = applicationDeploymentDetails["id"]

    with db_session() as dbs:
        app = dbs.query(Application).filter(Application.id == app_id).one_or_none()

        if not app:
            abort("This application doesn't exist.", 404)

        sol = dbs.query(Solution).filter(
            Application.id == app_id, 
            Application.solutionId == Solution.id
            ).one_or_none()
        if sol and sol.deploymentState != DeploymentStatus.SUCCESS:
            logger.warning("Cannot deploy an application if the solution deployment has not completed successfully.")
            abort(400, "Cannot deploy an application if the solution deployment has not completed successfully.")


        sol_envs = dbs.query(LZEnvironment).filter(
            SolutionEnvironment.environmentId == LZEnvironment.id,
            SolutionEnvironment.solutionId == sol.id,
            SolutionEnvironment.isActive,
            LZEnvironment.isActive
        ).all()
    
        for lzenv in sol_envs:
            workspace_resource_key = "project-id-workspace"
            workspace_resource = dbs.query(SolutionResource).filter(
                SolutionResource.solutionId == sol.id,
                SolutionResource.key == workspace_resource_key
            ).one_or_none()

            if workspace_resource:            
                workspaceProjectId = workspace_resource.value
            else:
                logger.error("deployment_create: This application deployment %s is missing the workspaceProjectId, resourceKey: %s, skipping...", app_id, workspace_resource_key)
                continue

            resource_key = f"project-id-{lzenv.name.lower()}"
            solution_resource = dbs.query(SolutionResource).filter(
                SolutionResource.solutionId == sol.id,
                SolutionResource.key == resource_key
            ).one_or_none()

            if solution_resource:            
                projectId = solution_resource.value
            else:
                logger.error("deployment_create: This application deployment %s is missing the projectId, resourceKey: %s, skipping...", app_id, resource_key)
                continue

            app_deployment = dbs.query(ApplicationDeployment).filter(
                ApplicationDeployment.solutionId == sol.id,
                ApplicationDeployment.applicationId == app_id,
                ApplicationDeployment.lzEnvironmentId == lzenv.id
            ).one_or_none()
            if not app_deployment:
                schema = ApplicationDeploymentSchema(many=False)
                app_deployment_dict = {}
                app_deployment_dict["applicationId"] = app_id
                app_deployment_dict["lastUpdated"] = ModelTools.get_utc_timestamp()
                app_deployment_dict["deploymentState"] = DeploymentStatus.PENDING
                app_deployment_dict["taskId"] = None
                app_deployment_dict["solutionId"] = app.solutionId
                app_deployment_dict["deploymentProjectId"] = projectId
                app_deployment_dict["lzEnvironmentId"] = lzenv.id                
                app_deployment_dict["workspaceProjectId"] = workspaceProjectId 

                app_deployment = schema.load(app_deployment_dict, session=db.session)      
                dbs.add(app_deployment)
            else:
                # Allow re-deployment of a previously unsuccessful deployment
                if app_deployment.deploymentState != DeploymentStatus.SUCCESS:
                    app_deployment.deploymentState = DeploymentStatus.PENDING
                    app_deployment.taskId = None

    # above db transaction should be complete before the next steps
    executor.submit(start_deployment, app_id)

    return make_response("Application deployment is complete.", 200)

def deployment_read_all():
    with db_session() as dbs:
        app_deployments = (
            dbs.query(ApplicationDeployment).filter(ApplicationDeployment.deploymentState != "").all()
        )
        for ad in app_deployments:
            ad.lzEnvironment=dbs.query(LZEnvironment).filter(LZEnvironment.id == ad.lzEnvironmentId).one_or_none()

        schema = ExtendedApplicationDeploymentSchema(many=True)
        data = schema.dump(app_deployments)
        #logger.debug("deployment_read_all::applications data: %s", data)
        return data, 200

def deployment_update(app_id, lzEnvId, applicationDeploymentDetails, dbsession):
    """
    Updates an existing applications in the application list with the deployed status.

    :param key:    id of the application
    :param solutionDetails:   application details to update
    :return:       updated application
    """
    logger.debug("deployment_update::applicationDeploymentDetails: %s", applicationDeploymentDetails)

    # Does the application exist in application list?
    existing_application_deployment = (
        dbsession.query(ApplicationDeployment).filter(
            ApplicationDeployment.applicationId == app_id,
            ApplicationDeployment.lzEnvironmentId == lzEnvId
        ).one_or_none()
    )

    # Does the application deployment exist?
    if existing_application_deployment:   
        existing_application_deployment.lastUpdated = ModelTools.get_utc_timestamp()
        if "deploymentState" in applicationDeploymentDetails:
            existing_application_deployment.deploymentState = applicationDeploymentDetails["deploymentState"]
        if "taskId" in applicationDeploymentDetails:
            existing_application_deployment.taskId = applicationDeploymentDetails["taskId"]            
        dbsession.merge(existing_application_deployment)
    else:
        logger.debug("deployment_update::existing application deployment not found, %s, %s", app_id, lzEnvId)

def deploy_application(app_deployment, dbsession):
    logger.debug("deploy_application:: %s", app_deployment)
    # expand fields for DaC application deployment
    app, act, actMetadata, lzenv = dbsession.query(Application, Activator, ActivatorMetadata, LZEnvironment).filter(
        Activator.id == Application.activatorId,
        ActivatorMetadata.activatorId == Application.activatorId,
        Application.id == app_deployment.applicationId,
        ApplicationDeployment.applicationId == Application.id,
        ApplicationDeployment.lzEnvironmentId == LZEnvironment.id,
        LZEnvironment.id == app_deployment.lzEnvironmentId            
    ).one_or_none()
    if act:
        gitSnapshot = json.loads(act.gitSnapshotJson)
        app_deployment.activatorGitUrl = gitSnapshot["git_clone_url"]
        #app_deployment.deploymentEnvironment = lzenv.name.lower()
        app_deployment.workspaceProjectId = app_deployment.workspaceProjectId
        app_deployment.deploymentProjectId = app_deployment.deploymentProjectId
        app_deployment.mandatoryVariables = []

        if actMetadata:
            app_deployment.optionalVariables = actMetadata
        else:
            app_deployment.optionalVariables = []

        app_deployment.id = app.id
        app_deployment.name = app.name
        app_deployment.description = app.description
        # app_deployment.actMetadata = actMetadata

        environment, lzlanvpc = dbsession.query(LZEnvironment, LZLanVpc).filter(
            LZLanVpcEnvironment.lzlanvpcId == LZLanVpc.id, 
            LZLanVpcEnvironment.environmentId == lzenv.id,
            LZLanVpcEnvironment.environmentId == LZEnvironment.id,
            LZLanVpcEnvironment.isActive,
            LZEnvironment.isActive,
        ).one_or_none()
        if lzlanvpc:
            environment.sharedVPCProjectId = lzlanvpc.sharedVPCProjectId
        else:
            environment.sharedVPCProjectId = ""
        app_deployment.deploymentEnvironment = environment

        return send_application_deployment_to_the_dac(app_deployment, dbsession = dbsession)
    else:
        logger.error("deploy_application::activator not found, %s!", app.activatorId)

# Send the application to the DAC
def send_application_deployment_to_the_dac(app_deployment, dbsession):
    app_id = app_deployment.applicationId
    lzEnvId = app_deployment.lzEnvironmentId
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
        logger.error(
            "send_application_deployment_to_the_dac::Failed during request to DAC %s", e
        )
        abort(500, "Failed communicating with the DAC")

    try:
        taskid = resp_json.get("taskid", None)
        # update with taskId
        deployment_json = {
            "id": app_id,
            "taskId": taskid,
            "deploymentState": DeploymentStatus.PENDING,
        }

        logger.debug(
            "send_application_deployment_to_the_dac::deployment_json: %s",
            pformat(deployment_json),
        )
        logger.debug(pformat(deployment_json))
        deployment_update(app_id, lzEnvId, deployment_json, dbsession)
        return deployment_json
    except requests.exceptions.RequestException as e:
        logger.error(
            "send_application_deployment_to_the_dac::Failed updating the database with the response from the DAC, %s.",
            e,
        )
        abort(500,
            "send_application_deployment_to_the_dac::Failed updating the database with the response from the DAC."
        )

def validate_json(some_json):
    try:
        json.loads(some_json)
        return True
    except ValueError:
        return False

def get_application_results_from_the_dac(app_id, lzEnvId, task_id, dbsession):
    """
    Get the application deployment results from the DAC.
    params: task_id
    """
    logger.debug(
        "get_application_results_from_the_dac: oid: %s taskId: %s", app_id, task_id
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
            500,
            "get_application_results_from_the_dac::failed communicating with the DAC"
        )

    # update ApplicationDeployment with results
    deployment_json = {
      "applicationId": app_id,
      "deploymentState": resp_json.get("status", "ERROR")
    }
    logger.debug(
        "get_application_results_from_the_dac::deployment_json: %s",
        pformat(deployment_json),
    )
    try:
        deployment_update(app_id, lzEnvId, deployment_json, dbsession = dbsession)
    except requests.exceptions.RequestException as e:
        logger.debug(
            "get_application_results_from_the_dac::Failed updating the ApplicationDeployment with the response from the DAC, %s",
            e,
        )
        abort(
            500, 
            "get_application_results_from_the_dac::Failed updating the ApplicationDeployment with the response from the DAC."
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
