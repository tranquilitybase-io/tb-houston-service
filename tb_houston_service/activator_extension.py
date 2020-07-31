import logging
from tb_houston_service.models import User, SourceControl
from tb_houston_service import activator_ci, activator_cd, activator_environment


logger = logging.getLogger("tb_houston_service.activator_extension")

def expand_activator(act, dbsession):
    """
    Expand ci, cd, envs, accessRequestedBy to objects. 
    Do not use, fails with:
    '_mysql_connector.MySQLInterfaceError: Python type User cannot be converted'
    Need to fix the data model later. 
    """
    logger.debug("expand_activator: %s", act)
    #expand accessRequestedBy
    act.accessRequestedBy = (
        dbsession.query(User).filter(User.id == act.accessRequestedById).one_or_none()
    )  
    #expand source control
    act.sourceControl = (
        dbsession.query(SourceControl).filter(SourceControl.id == act.sourceControlId).one_or_none()
    )
    #expand CI
    act = activator_ci.expand_ci(act , dbsession)
    #expand CD
    act = activator_cd.expand_cd(act, dbsession)
    #expand environments
    act = activator_environment.expand_environment(act, dbsession)

    return act

def refine_activator_details(activatorDetails):
    
    extraFields = {}
    if "ci" in activatorDetails:
        extraFields["ci"] = activatorDetails["ci"]
        del activatorDetails["ci"]
    
    if "cd" in activatorDetails:
        extraFields["cd"] = activatorDetails["cd"]
        del activatorDetails["cd"]
    
    if "envs" in activatorDetails:
        extraFields["envs"] = activatorDetails["envs"]
        del activatorDetails["envs"]
    
    return extraFields
     

def create_activator_associations(extraFields, activator, dbsession):

    if "ci" in extraFields:
        act_ci_list = extraFields["ci"]
    
    if "cd" in extraFields:
        act_cd_list = extraFields["cd"]
    
    if "envs" in extraFields:
        act_env_list = extraFields["envs"]
 
    if act_ci_list:
            activator_ci.create_activator_ci(activator.id, act_ci_list, dbsession)
    else:
        logger.error(
            "ci details in activator are missing, the transaction will be rolled back for this activator!"
        )
        dbsession.rollback()

    if act_cd_list:
        activator_cd.create_activator_cd(activator.id, act_cd_list, dbsession)
    else:
        logger.error(
            "cd details in activator are missing, the transaction will be rolled back for this activator!"
        )
        dbs.rollback()

    if act_env_list:
        activator_environment.create_activator_environment(activator.id, act_env_list, dbsession)
    else:
        logger.error(
            "env details in activator are missing, the transaction will be rolled back for this activator!"
        )
        dbs.rollback()

def delete_activator_associations(id, dbsession):

    activator_ci.delete_activator_ci(id , dbsession)
    activator_cd.delete_activator_cd(id , dbsession)
    activator_environment.delete_activator_environment(id , dbsession)








