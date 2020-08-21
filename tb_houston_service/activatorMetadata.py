import logging
import yaml
import os
import git
import shutil
import tempfile

from config.db_lib import db_session
from pprint import pformat
from tb_houston_service.tools import ModelTools
from tb_houston_service.models import ActivatorSchema, ActivatorMetadataSchema
from tb_houston_service.models import ActivatorMetadataPlatformSchema, ActivatorMetadataVariableSchema
from tb_houston_service.models import ActivatorMetadata, ActivatorMetadataPlatform, ActivatorMetadataVariable
from tb_houston_service.models import Type ,Platform
from tb_houston_service.extendedSchemas import ExtendedActivatorMetadataSchema


logger = logging.getLogger("tb_houston_service.activatorMetadata")


def create(activatorMetadataDetails):
    """
    Args:
        url ([url]): [URL of the githib repo to get activator_metadata.yml]

        1. Connect to GitHIB repo using Github API and download yaml file
        2. Read  the contents of activator_metadata.yml file
        3. Create activator object to insert an entry into 'activator' table
        4. Create activatorMetadata object to insert an entry into 'activatorMetadata' table
        5. Read 'Platforms' field from yaml file and create 'activatorPlatform' object and insert into 'activatorPlatform' table
        6. Read 'mandatoryVariables'from yaml and insert into 'activatorVariables' table with 'isOptional'=False
        7. Read 'optionalVariables' from yaml and insert into 'activatorVariables' table with 'isOptional'=True

    """
    #get Yaml from gitgub and read the contents of the yaml file
    act_metadata_yml_dict = get_file_from_repo(activatorMetadataDetails["uri"])

    with db_session() as dbs:
        
        activator_id=create_activator(dbs, act_metadata_yml_dict)
        
        activator_metadata=create_activator_metadata(dbs, act_metadata_yml_dict, activator_id)
        
        create_activator_metadata_platforms(dbs, act_metadata_yml_dict, activator_metadata.id)
        
        mandatoryVariables = act_metadata_yml_dict["mandatoryVariables"]
        create_activator_metadata_variables(dbs,activator_metadata.id, mandatoryVariables, False)
        
        optionalVariables = act_metadata_yml_dict["optionalVariables"]
        create_activator_metadata_variables(dbs,activator_metadata.id, optionalVariables, True)
       
        # Expand activator metadata object to return
        schema = ExtendedActivatorMetadataSchema()
        expand_activator_metadata(activator_metadata, dbs)
        data = schema.dump(activator_metadata)
        logger.debug(pformat(data))
        return data, 201

    
def get_file_from_repo(url):
    # Create temporary dir
    t = tempfile.mkdtemp()
    # Clone into temporary dir
    git.Repo.clone_from(url, t, branch='master', depth=1)
    # Copy desired file from temporary dir
    shutil.move(os.path.join(t, '.tb/activator_metadata.yml'), '.')
    # Remove temporary dir
    shutil.rmtree(t)
    act_metadata_yaml_file = open("activator_metadata.yml")
    act_metadata_yml_dict = yaml.load(act_metadata_yaml_file, Loader=yaml.FullLoader)
    logger.debug("activator_metadata.yml file :::: %s", pformat(act_metadata_yml_dict))
    # Remove yaml file 
    os.remove("activator_metadata.yml")
    return act_metadata_yml_dict



def create_activator(dbs, act_metadata_yml):

    schema = ActivatorSchema()
    activatorDetails = {}
    activatorDetails["name"] = act_metadata_yml["name"]
    activatorDetails["gitRepoUrl"] = act_metadata_yml["url"]
    activator = schema.load(activatorDetails, session=dbs)
    dbs.add(activator)
    dbs.flush()
    return activator.id

def create_activator_metadata(dbs, act_metadata_yml, activator_id):

    schema = ActivatorMetadataSchema()
    actMetaDetails = {}
    actMetaDetails["activatorId"] = activator_id
    actMetaDetails["name"] = act_metadata_yml["name"]
    actMetaDetails["description"] = act_metadata_yml["description"]
    actMetaDetails["category"] = act_metadata_yml["category"]
    actMetaDetails["activatorLink"] = act_metadata_yml["url"]
    actMetaDetails["typeId"] = (dbs.query(Type).filter(Type.value == act_metadata_yml["type"]).one_or_none()).id
    actMetaDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
    activator_metadata = schema.load(actMetaDetails, session=dbs)
    dbs.add(activator_metadata)
    dbs.flush()
    return activator_metadata

def create_activator_metadata_platforms(dbs, act_metadata_yml, activator_metadata_id):

    schema = ActivatorMetadataPlatformSchema()
    platforms = act_metadata_yml["platforms"]
    
    for p in platforms:
        actPlatformDetails = {}
        actPlatformDetails["activatorMetadataId"] = activator_metadata_id
        actPlatformDetails["platformId"] = (dbs.query(Platform).filter(Platform.value == p ).one_or_none()).id
        actPlatformDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
        actPlatformDetails["isActive"] = True
        activator_metadata_platform = schema.load(actPlatformDetails, session=dbs)
        dbs.add(activator_metadata_platform)
        dbs.flush()

def create_activator_metadata_variables(dbs, activator_metadata_id, variables,isOptional):

    schema = ActivatorMetadataVariableSchema()
    
    for variable in variables:
        variableDetails = {}
        variableDetails["activatorMetadataId"] = activator_metadata_id
        variableDetails["name"] = variable["name"]
        variableDetails["type"] = variable["type"]
        if "value" in variable:
            variableDetails["value"] = variable["value"]
        else:
            variableDetails["value"] = ""

        variableDetails["isOptional"] = isOptional
        activator_metadata_variable = schema.load(variableDetails, session=dbs)
        dbs.add(activator_metadata_variable)
        dbs.flush()

def expand_activator_metadata(act_metadata, dbs):
    
    act_metadata.type = dbs.query(Type).filter(
        Type.id == act_metadata.typeId).one_or_none()
    
    act_metadata.platforms = dbs.query(ActivatorMetadataPlatform).filter(
        Platform.id == ActivatorMetadataPlatform.platformId, 
        ActivatorMetadata.id == ActivatorMetadataPlatform.activatorMetadataId, 
        ActivatorMetadata.id == act_metadata.id).all()

    act_metadata.variables = dbs.query(ActivatorMetadataVariable).filter(
        ActivatorMetadata.id == ActivatorMetadataVariable.activatorMetadataId, 
        ActivatorMetadata.id == act_metadata.id).all()

    return act_metadata






