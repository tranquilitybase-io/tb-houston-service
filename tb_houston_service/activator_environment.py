import logging

from models import Activator, ActivatorEnvironment, LZEnvironment
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.activator_environment")


def create_activator_environment(activatorId, list_of_environment, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_environment ([list]): [A list of Environment ids]

        1. Logically delete all active LZEnvironment ids for this activator
        2. Reactivate the activator environment relaionship that are in this list: list_of_environment
        3. Create the activator-environment rows that are not in this list.

    """
    # Inactivates the active activator-environment for this activator (activatorId)
    environment_list = (
        dbsession.query(ActivatorEnvironment)
        .filter(
            ActivatorEnvironment.activatorId == activatorId,
            ActivatorEnvironment.isActive,
        )
        .all()
    )
    for environment in environment_list:
        environment.isActive = False
    dbsession.flush()

    for environment in list_of_environment:
        existing_act_environment = (
            dbsession.query(ActivatorEnvironment)
            .filter(
                ActivatorEnvironment.activatorId == activatorId,
                ActivatorEnvironment.envId == environment,
            )
            .one_or_none()
        )

        if existing_act_environment:
            existing_act_environment.isActive = True
            dbsession.merge(existing_act_environment)
        else:
            new_act_environment = ActivatorEnvironment(
                activatorId=activatorId,
                envId=environment,
                lastUpdated=ModelTools.get_utc_timestamp(),
                isActive=True,
            )
            dbsession.add(new_act_environment)
        logger.debug(
            "Added Activator Environment: {new_act_environment} to transaction."
        )

    return dbsession


def delete_activator_environment(activatorId, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_environment ([list]): [A list of Environment ids]

        1. Logically delete all active Environment ids for this activator
    """
    # Inactivates the active activator-environment for this activator (activatorId)
    environment_list = (
        dbsession.query(ActivatorEnvironment)
        .filter(
            ActivatorEnvironment.activatorId == activatorId,
            ActivatorEnvironment.isActive,
        )
        .all()
    )
    for environment in environment_list:
        environment.isActive = False
    dbsession.flush()

    return dbsession


def expand_environment(act, dbsession):
    act.envs = (
        dbsession.query(LZEnvironment)
        .filter(
            LZEnvironment.id == ActivatorEnvironment.envId,
            Activator.id == ActivatorEnvironment.activatorId,
            Activator.id == act.id,
            ActivatorEnvironment.isActive,
            Activator.isActive,
            LZEnvironment.isActive,
        )
        .all()
    )

    return act
