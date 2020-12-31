import logging

from models import Activator, ApplicationDeployment
from tb_houston_service import activator_extension
from tb_houston_service.DeploymentStatus import DeploymentStatus

logger = logging.getLogger("tb_houston_service.application_extension")


def expand_application(app, dbsession):
    app.activator = (
        dbsession.query(Activator).filter(Activator.id == app.activatorId).one_or_none()
    )
    if app.activator:
        activator_extension.expand_activator(app.activator, dbsession)

    # TODO?: Expand app deployments if required
    # app.deployments = dbs.query(ApplicationDeployment).filter(
    #   ApplicationDeployment.applicationId == app.id
    # ).all()

    app_deps = (
        dbsession.query(ApplicationDeployment)
        .filter(ApplicationDeployment.applicationId == app.id)
        .all()
    )
    logger.debug("expand_application: %s", app_deps)
    if len(app_deps) > 0:
        if all(elem.deploymentState == DeploymentStatus.SUCCESS for elem in app_deps):
            app.deploymentState = DeploymentStatus.SUCCESS
        elif any(elem.deploymentState == DeploymentStatus.PENDING for elem in app_deps):
            app.deploymentState = DeploymentStatus.PENDING
        elif any(elem.deploymentState == DeploymentStatus.FAILURE for elem in app_deps):
            app.deploymentState = DeploymentStatus.FAILURE
        elif any(elem.deploymentState == DeploymentStatus.STARTED for elem in app_deps):
            app.deploymentState = DeploymentStatus.STARTED
    else:
        app.deploymentState = None
    logger.debug("expand_application::deploymentState: %s", app.deploymentState)
    return app
