import logging
from tb_houston_service.models import User, SourceControl
from tb_houston_service import activator_ci, activator_cd, activator_environment
from config import db
from copy import deepcopy


logger = logging.getLogger("tb_houston_service.activator_extension")


def expand_activator(act, dbsession):
    """
    Expand accessRequestedBy from an integer to an object. 
    Do not use, fails with:
    '_mysql_connector.MySQLInterfaceError: Python type User cannot be converted'
    Need to fix the data model later. 
    """
    logger.debug("expand_activator: %s", act)
    act.accessRequestedBy = (
        dbsession.query(User).filter(User.id == act.accessRequestedById).one_or_none()
    )
    expand_activator_fields(act)
    return act


def expand_activator_fields(act):
    """
    Expand ci from an integer  list to an object list. 
    Do not use, fails with:
    '_mysql_connector.MySQLInterfaceError: Python type User cannot be converted'
    Need to fix the data model later. 
    """
    logger.debug("expand_activator_full: %s", act)
    act = activator_ci.expand_ci(act)
    act = activator_cd.expand_cd(act)
    act = activator_environment.expand_environment(act)
    act = expand_sourceControl(act)

    return act


def expand_sourceControl(act):

    sc_object = (
        db.session.query(SourceControl)
        .filter(SourceControl.id == act.sourceControlId)
        .one_or_none()
    )
    act.sourceControl = sc_object
    return act


def refine_activator_details(activatorDetails):

    newActivatorDetails = deepcopy(activatorDetails)

    if "ci" in newActivatorDetails:
        del newActivatorDetails["ci"]

    if "cd" in newActivatorDetails:
        del newActivatorDetails["cd"]

    if "envs" in newActivatorDetails:
        del newActivatorDetails["envs"]

    return newActivatorDetails


def create_activator_associations(activatorDetails, new_activator, dbs):

    if "ci" in activatorDetails:
        act_ci_list = activatorDetails["ci"]

    if "cd" in activatorDetails:
        act_cd_list = activatorDetails["cd"]

    if "envs" in activatorDetails:
        act_env_list = activatorDetails["envs"]

    if act_ci_list:
        activator_ci.create_activator_ci(new_activator.id, act_ci_list, dbs)
    else:
        logger.error(
            "ci details in activator are missing, the transaction will be rolled back for this activator!"
        )
        dbs.rollback()

    if act_cd_list:
        activator_cd.create_activator_cd(new_activator.id, act_cd_list, dbs)
    else:
        logger.error(
            "cd details in activator are missing, the transaction will be rolled back for this activator!"
        )
        dbs.rollback()

    if act_env_list:
        activator_environment.create_activator_environment(
            new_activator.id, act_env_list, dbs
        )
    else:
        logger.error(
            "env details in activator are missing, the transaction will be rolled back for this activator!"
        )
        dbs.rollback()


def delete_activator_associations(id, dbs):

    activator_ci.delete_activator_ci(id, dbs)
    activator_cd.delete_activator_cd(id, dbs)
    activator_environment.delete_activator_environment(id, dbs)
