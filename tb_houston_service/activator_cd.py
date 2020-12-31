import logging

from models import CD, Activator, ActivatorCD
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.activator_cd")


def create_activator_cd(activatorId, list_of_cd, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_cd ([list]): [A list of CD ids]

        1. Logically delete all active CD ids for this activator
        2. Reactivate the activator cd relaionship that are in this list: list_of_cd
        3. Create the activator-cd rows that are not in this list.

    """
    # Inactivates the active activator-cd for this activator (activatorId)
    cd_list = (
        dbsession.query(ActivatorCD)
        .filter(ActivatorCD.activatorId == activatorId, ActivatorCD.isActive)
        .all()
    )
    for cd in cd_list:
        cd.isActive = False
    dbsession.flush()

    for cd in list_of_cd:
        existing_act_cd = (
            dbsession.query(ActivatorCD)
            .filter(ActivatorCD.activatorId == activatorId, ActivatorCD.cdId == cd)
            .one_or_none()
        )

        if existing_act_cd:
            existing_act_cd.isActive = True
            dbsession.merge(existing_act_cd)
        else:
            new_act_cd = ActivatorCD(
                activatorId=activatorId,
                cdId=cd,
                lastUpdated=ModelTools.get_utc_timestamp(),
                isActive=True,
            )
            dbsession.add(new_act_cd)
        logger.debug("Added Activator CD: {new_act_cd} to transaction.")

    return dbsession


def delete_activator_cd(activatorId, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_cd ([list]): [A list of CD ids]

        1. Logically delete all active CD ids for this activator
    """
    # Inactivates the active activator-cd for this activator (activatorId)
    cd_list = (
        dbsession.query(ActivatorCD)
        .filter(ActivatorCD.activatorId == activatorId, ActivatorCD.isActive)
        .all()
    )
    for cd in cd_list:
        cd.isActive = False
    dbsession.flush()

    return dbsession


def expand_cd(act, dbsession):
    act.cd = (
        dbsession.query(CD)
        .filter(
            CD.id == ActivatorCD.cdId,
            Activator.id == ActivatorCD.activatorId,
            Activator.id == act.id,
            ActivatorCD.isActive,
            Activator.isActive,
        )
        .all()
    )

    return act
