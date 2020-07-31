import logging

from tb_houston_service.tools import ModelTools
from tb_houston_service.models import ActivatorEnvironment, Environment


logger = logging.getLogger("tb_houston_service.activator_environment")


def create_activator_environment(activatorId, list_of_environment, dbsession):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_environment ([list]): [A list of Environment ids]

        1. Logically delete all active Environment ids for this activator
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
    act_environment_list = (
        dbsession.query(ActivatorEnvironment)
        .filter(
            ActivatorEnvironment.activatorId == act.id, ActivatorEnvironment.isActive
        )
        .all()
    )
    newList = []
    for act_environment in act_environment_list:
        environment_object = (
            dbsession.query(Environment)
            .filter(Environment.id == act_environment.envId)
            .one_or_none()
        )
        newList.append(environment_object)
    act.envs = newList
    return act
