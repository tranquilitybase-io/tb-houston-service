import logging
from tb_houston_service import activator_ci, activator_cd, activator_environment, activatorByURL
from tb_houston_service.models import User
from tb_houston_service.models import SourceControl
from tb_houston_service.models import BusinessUnit
from tb_houston_service.models import ActivatorMetadata
from tb_houston_service.models import ActivatorMetadataVariable
from tb_houston_service.models import ActivatorMetadataPlatform
from tb_houston_service.tools import ModelTools


logger = logging.getLogger("tb_houston_service.activator_extension")

def expand_activator(act, dbsession):
    """
    Expand ci, cd, envs, accessRequestedBy to objects. 
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

    #expand businessUnit
    act.businessUnit = (
        dbsession.query(BusinessUnit).filter(BusinessUnit.id == act.businessUnitId).one_or_none()
    )
    # expand activator metadata
    act_metadata= (
        dbsession.query(ActivatorMetadata).filter(ActivatorMetadata.activatorId == act.id).one_or_none()
    )
    if act_metadata is not None:
        act.activatorMetadata = activatorByURL.expand_activator_metadata(act_metadata, dbsession)

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
    
    if "activatorMetadata" in activatorDetails:
        extraFields["activatorMetadata"] = activatorDetails["activatorMetadata"]
        del activatorDetails["activatorMetadata"]

    if "accessRequestedBy" in activatorDetails:
        extraFields["accessRequestedBy"] = activatorDetails["accessRequestedBy"]
        del activatorDetails["accessRequestedBy"]

    if "sourceControl" in activatorDetails:
        extraFields["sourceControl"] = activatorDetails["sourceControl"]
        del activatorDetails["sourceControl"]

    if "businessUnit" in activatorDetails:
        extraFields["businessUnit"] = activatorDetails["businessUnit"]
        del activatorDetails["businessUnit"]

    return extraFields


def update_activator_metadata(activator_id, act_metadata, dbsession):
    actMetaDetails = dbsession.query(ActivatorMetadata).filter(ActivatorMetadata.activatorId == activator_id).one_or_none() 
    if actMetaDetails:
        actMetaDetails.name = act_metadata.get("name")
        actMetaDetails.description = act_metadata.get("description")
        actMetaDetails.category = act_metadata.get("category")
        actMetaDetails.activatorLink = act_metadata.get("activatorLink")
        actMetaDetails.typeId = act_metadata.get("typeId")
        actMetaDetails.lastUpdated = ModelTools.get_utc_timestamp()
        actMetaDetails.latestVersion = act_metadata.get("latestVersion")
        dbsession.merge(actMetaDetails)
        dbsession.flush()
    return actMetaDetails


def update_activator_metadata_platforms(platforms, activator_metadata_id, dbsession):
    for platform in platforms:
        platform = dbsession.query(ActivatorMetadataPlatform).filter(
            ActivatorMetadataPlatform.activatorMetadataId == activator_metadata_id,
            ActivatorMetadataPlatform.platformId == platform.get("id")
            ).one_or_none()
        platform.lastUpdated = ModelTools.get_utc_timestamp()
        platform.isActive = True
        dbsession.add(platform)
        dbsession.flush()


def update_activator_metadata_variables(variables, dbsession):
    for variable in variables:
        variableDetails = dbsession.query(ActivatorMetadataVariable).filter(ActivatorMetadataVariable.id == variable.get("id")).one_or_none()
        if variableDetails:
            variableDetails.name = variable.get("name")
            variableDetails.type = variable.get("type")
            variableDetails.value = variable.get("value")
            variableDetails.defaultValue = variable.get("defaultValue")
            variableDetails.isOptional = variable.get('isOptional')
            dbsession.merge(variableDetails)
            dbsession.flush()


def create_activator_associations(extraFields, activator, dbsession):

    if "ci" in extraFields:
        act_ci_list = extraFields["ci"]
    
    if "cd" in extraFields:
        act_cd_list = extraFields["cd"]
    
    if "envs" in extraFields:
        act_env_list = extraFields["envs"]

    if "activatorMetadata" in extraFields:
        activator_metadata = extraFields['activatorMetadata']
        update_activator_metadata(activator.id, activator_metadata, dbsession)
        platforms = activator_metadata['platforms']
        update_activator_metadata_platforms(platforms, activator_metadata["id"], dbsession)
        activator_metadata_variables = activator_metadata['variables']
        update_activator_metadata_variables(activator_metadata_variables, dbsession)
    else:
        logger.error(
            "activatorMetadata missing, the transaction will be rolled back for this activator!"
        )
        dbsession.rollback()
        return {
            "code": 400, 
            "message": "activatorMetadata missing, the transaction will be rolled back for this activator!"
        } 

    activator_ci.create_activator_ci(activator.id, act_ci_list, dbsession)
    activator_cd.create_activator_cd(activator.id, act_cd_list, dbsession)
    activator_environment.create_activator_environment(activator.id, act_env_list, dbsession)
    dbsession.commit()


def delete_activator_associations(id, dbsession):

    activator_ci.delete_activator_ci(id , dbsession)
    activator_cd.delete_activator_cd(id , dbsession)
    activator_environment.delete_activator_environment(id , dbsession)


