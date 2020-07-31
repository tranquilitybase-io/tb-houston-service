import logging

from config import db
from tb_houston_service.tools import ModelTools
from tb_houston_service.models import ActivatorCI, CI


logger = logging.getLogger("tb_houston_service.activator_ci")


def create_activator_ci(activatorId, list_of_ci, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_ci ([list]): [A list of CI ids]

        1. Logically delete all active CI ids for this activator
        2. Reactivate the activator ci relaionship that are in this list: list_of_ci
        3. Create the activator-ci rows that are not in this list.

    """

    # Inactivates the active activator-ci for this activator (activatorId)
    ci_list = (
        dbsession.query(ActivatorCI)
        .filter(ActivatorCI.activatorId == activatorId, ActivatorCI.isActive)
        .all()
    )
    for ci in ci_list:
        ci.isActive = False
    dbsession.flush()

    for ci in list_of_ci:
        existing_act_ci = (
            dbsession.query(ActivatorCI)
            .filter(ActivatorCI.activatorId == activatorId, ActivatorCI.ciId == ci)
            .one_or_none()
        )

        if existing_act_ci:
            existing_act_ci.isActive = True
            dbsession.merge(existing_act_ci)
        else:
            new_act_ci = ActivatorCI(
                activatorId=activatorId,
                ciId=ci,
                lastUpdated=ModelTools.get_utc_timestamp(),
                isActive=True,
            )
            dbsession.add(new_act_ci)
        logger.debug("Added Activator CI: {new_act_ci} to transaction.")

    return dbsession


def delete_activator_ci(activatorId, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_ci ([list]): [A list of CI ids]

        1. Logically delete all active CI ids for this activator
    """

    # Inactivates the active activator-ci for this activator (activatorId)
    ci_list = (
        dbsession.query(ActivatorCI)
        .filter(ActivatorCI.activatorId == activatorId, ActivatorCI.isActive)
        .all()
    )
    for ci in ci_list:
        ci.isActive = False
    dbsession.flush()

    return dbsession


def expand_ci(act,  dbsession):
    act_ci_list = (
        dbsession.query(ActivatorCI)
        .filter(ActivatorCI.activatorId == act.id, ActivatorCI.isActive)
        .all()
    )
    newList = []
    for act_ci in act_ci_list:
        ci_object = dbsession.query(CI).filter(CI.id == act_ci.ciId).one_or_none()
        newList.append(ci_object)
    act.ci = newList
    return act
