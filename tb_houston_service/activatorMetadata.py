import logging
import yaml

from config.db_lib import db_session
from tb_houston_service.tools import ModelTools
from tb_houston_service.models import ActivatorSchema, ActivatorMetadataSchema


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
        create_activator(dbs, parsed_yaml_file)
        
        # Task # 4
        create_activator_metadata(dbs, parsed_yaml_file)



    


def create_activator(dbs, parsed_yaml_file):

    schema = ActivatorSchema()
    activatorDetails = {}
    activatorDetails["name"] = parsed_yaml_file["name"]
    activatorDetails["gitRepoUrl"] = parsed_yaml_file["url"]
    print(activatorDetails)
    new_activator = schema.load(activatorDetails, session=dbs)
    print(new_activator)
    dbs.add(new_activator)
    dbs.flush()

def create_activator_metadata(dbs, parsed_yaml_file):

    schema = ActivatorMetadataSchema()
    actMetaDetails = {}
    actMetaDetails["name"] = parsed_yaml_file["name"]
    actMetaDetails["description"] = parsed_yaml_file["description"]
    actMetaDetails["category"] = parsed_yaml_file["category"]
    actMetaDetails["typeId"] = 1
    print(actMetaDetails)
    new_activator_meta_data = schema.load(actMetaDetails, session=dbs)
    print(new_activator_meta_data)
    dbs.add(new_activator_meta_data)
    dbs.flush()


