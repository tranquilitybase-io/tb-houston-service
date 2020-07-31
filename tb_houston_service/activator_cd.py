import logging

from config import db
from tb_houston_service.tools import ModelTools
from tb_houston_service.models import ActivatorCD, CD


logger = logging.getLogger("tb_houston_service.activator_cd")


def create_activator_cd(activatorId, list_of_cd, dbs):
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
        dbs.query(ActivatorCD)
        .filter(ActivatorCD.activatorId == activatorId, ActivatorCD.isActive)
        .all()
    )
    for cd in cd_list:
        cd.isActive = False
    dbs.flush()

    for cd in list_of_cd:
        existing_act_cd = (
            dbs.query(ActivatorCD)
            .filter(ActivatorCD.activatorId == activatorId, ActivatorCD.cdId == cd)
            .one_or_none()
        )

        if existing_act_cd:
            existing_act_cd.isActive = True
            dbs.merge(existing_act_cd)
        else:
            new_act_cd = ActivatorCD(
                activatorId=activatorId,
                cdId=cd,
                lastUpdated=ModelTools.get_utc_timestamp(),
                isActive=True,
            )
            dbs.add(new_act_cd)
        logger.debug("Added Activator CD: {new_act_cd} to transaction.")

    return dbs


def delete_activator_cd(activatorId, dbs):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_cd ([list]): [A list of CD ids]

        1. Logically delete all active CD ids for this activator
    """

    # Inactivates the active activator-cd for this activator (activatorId)
    cd_list = (
        dbs.query(ActivatorCD)
        .filter(ActivatorCD.activatorId == activatorId, ActivatorCD.isActive)
        .all()
    )
    for cd in cd_list:
        cd.isActive = False
    dbs.flush()

    return dbs


def expand_cd(act):
    act_cd_list = (
        db.session.query(ActivatorCD)
        .filter(ActivatorCD.activatorId == act.id, ActivatorCD.isActive)
        .all()
    )
    newList = []
    for act_cd in act_cd_list:
        cd_object = db.session.query(CD).filter(CD.id == act_cd.cdId).one_or_none()
        newList.append(cd_object)
    act.cd = newList
    return act
