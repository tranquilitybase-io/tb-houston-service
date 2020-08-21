import logging
import yaml

from config.db_lib import db_session
from tb_houston_service.tools import ModelTools
from tb_houston_service.models import ActivatorSchema, ActivatorMetadataSchema
from tb_houston_service.models import ActivatorMetadataPlatformSchema, ActivatorMetadataVariableSchema
from tb_houston_service.models import ActivatorMetadata, ActivatorMetadataPlatform, ActivatorMetadataVariable
from tb_houston_service.models import Type ,Platform, ActivatorMetadataPlatform
from tb_houston_service.extendedSchemas import ExtendedActivatorMetadataSchema


logger = logging.getLogger("tb_houston_service.activator_metadata")


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
    #Task # 2
    a_yaml_file = open("docs/activator_metadata.yml")
    parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    print(parsed_yaml_file)

    with db_session() as dbs:
        
        # Task # 3
        activator_id=create_activator(dbs, parsed_yaml_file)
        
        # Task # 4
        activator_metadata=create_activator_metadata(dbs, parsed_yaml_file, activator_id)
        
        # Task # 5
        create_activator_metadata_platforms(dbs, parsed_yaml_file, activator_metadata.id)
        
        # Task # 6 
        mandatoryVariables = parsed_yaml_file["mandatoryVariables"]
        create_activator_metadata_variables(dbs,activator_metadata.id, mandatoryVariables, False)
        
        # Task # 7 
        optionalVariables = parsed_yaml_file["optionalVariables"]
        create_activator_metadata_variables(dbs,activator_metadata.id, optionalVariables, True)
       
        # Expand activator metadata object to return
        schema = ExtendedActivatorMetadataSchema()
        expand_activator_metadata(activator_metadata, dbs)
        data = schema.dump(activator_metadata)
        return data, 201
    return "a"

    


def create_activator(dbs, parsed_yaml_file):

    schema = ActivatorSchema()
    activatorDetails = {}
    activatorDetails["name"] = parsed_yaml_file["name"]
    activatorDetails["gitRepoUrl"] = parsed_yaml_file["url"]
    print(activatorDetails)
    activator = schema.load(activatorDetails, session=dbs)
    print(activator)
    dbs.add(activator)
    dbs.flush()
    return activator.id

def create_activator_metadata(dbs, parsed_yaml_file, activator_id):

    schema = ActivatorMetadataSchema()
    actMetaDetails = {}
    actMetaDetails["activatorId"] = activator_id
    actMetaDetails["name"] = parsed_yaml_file["name"]
    actMetaDetails["description"] = parsed_yaml_file["description"]
    actMetaDetails["category"] = parsed_yaml_file["category"]
    actMetaDetails["activatorLink"] = parsed_yaml_file["url"]
    actMetaDetails["typeId"] = (dbs.query(Type).filter(Type.value == parsed_yaml_file["type"]).one_or_none()).id
    actMetaDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
    print(actMetaDetails)
    activator_metadata = schema.load(actMetaDetails, session=dbs)
    print(activator_metadata)
    dbs.add(activator_metadata)
    dbs.flush()
    return activator_metadata

def create_activator_metadata_platforms(dbs, parsed_yaml_file, activator_metadata_id):

    schema = ActivatorMetadataPlatformSchema()
    platforms = parsed_yaml_file["platforms"]
    
    for p in platforms:
        actPlatformDetails = {}
        actPlatformDetails["activatorMetadataId"] = activator_metadata_id
        actPlatformDetails["platformId"] = (dbs.query(Platform).filter(Platform.value == p ).one_or_none()).id
        actPlatformDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
        actPlatformDetails["isActive"] = True
        print(actPlatformDetails)
        activator_metadata_platform = schema.load(actPlatformDetails, session=dbs)
        print(activator_metadata_platform)
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
            variableDetails["value"] = value
        else:
            variableDetails["value"] = ""

        variableDetails["isOptional"] = isOptional
        print(variableDetails)
        activator_metadata_variable = schema.load(variableDetails, session=dbs)
        print(activator_metadata_variable)
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






