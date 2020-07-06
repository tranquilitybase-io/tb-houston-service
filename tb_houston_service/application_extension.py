import logging
from tb_houston_service.models import Application, Activator, ApplicationDeployment
from tb_houston_service import activator_extension
from config import db


logger = logging.getLogger("tb_houston_service.application_extension")


def expand_application(app):
    app.activator = (
        db.session.query(Activator).filter(
            Activator.id == app.activatorId
        ).one_or_none()
    )
    if app.activator:
        activator_extension.expand_activator(app.activator)

    app_dep = db.session.query(ApplicationDeployment).filter(
        ApplicationDeployment.applicationId == app.id,
        ApplicationDeployment.solutionId == app.solutionId
    ).one_or_none()

    if app_dep:
        app.deploymentState = app_dep.deploymentState
    else:
        app.deploymentState = None
    return app
