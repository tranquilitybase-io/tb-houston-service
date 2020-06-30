import logging
from tb_houston_service.models import Activator
from config import db
from tb_houston_service import activator_extension

logger = logging.getLogger("tb_houston_service.application_extension")


def expand_application(app):
    app.activator = (
        db.session.query(Activator).filter(
            Activator.id == app.activatorId,
            Activator.isActive
        ).one_or_none()
    )
    if app.activator:
        activator_extension.expand_activator(app.activator)
    return app
