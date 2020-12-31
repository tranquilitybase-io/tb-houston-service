import logging
import os
import shutil
import tempfile
from pprint import pformat

# import pycurl
import git
import yaml
from flask import abort

from config.db_lib import db_session
from models import (
    Activator,
    ActivatorMetadata,
    ActivatorMetadataPlatform,
    ActivatorMetadataPlatformSchema,
    ActivatorMetadataSchema,
    ActivatorMetadataVariable,
    ActivatorMetadataVariableSchema,
    ActivatorSchema,
    Platform,
    Type,
)
from tb_houston_service import activator_extension, security, systemsettings
from tb_houston_service.extendedSchemas import ExtendedActivatorSchema
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.activatorMetadata")
blank = ""


def create(activatorByURLDetails):
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
    try:
        with db_session() as dbs:
            user = security.get_valid_user_from_token(dbsession=dbs)
            if not (user and user.isAdmin):
                return abort(401, "JWT not valid or user is not an Admin")

            github_credentials = systemsettings.get_github_credentials(user.id)

            # get Yaml from gitgub and read the contents of the yaml file
            act_metadata_yml_dict = get_file_from_repo(
                activatorByURLDetails["url"], github_credentials
            )

            activator_id = create_activator(
                dbs, act_metadata_yml_dict, activatorByURLDetails["url"]
            )

            activator_metadata = create_activator_metadata(
                dbs, act_metadata_yml_dict, activator_id, activatorByURLDetails["url"]
            )

            create_activator_metadata_platforms(
                dbs, act_metadata_yml_dict, activator_metadata.id
            )

            mandatoryVariables = act_metadata_yml_dict["mandatoryVariables"]
            create_activator_metadata_variables(
                dbs, activator_metadata.id, mandatoryVariables, False
            )

            optionalVariables = act_metadata_yml_dict["optionalVariables"]
            create_activator_metadata_variables(
                dbs, activator_metadata.id, optionalVariables, True
            )

            # return the activator
            # filter activators by logged in user
            business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
            act = (
                dbs.query(Activator)
                .filter(
                    Activator.id == activator_id,
                    (
                        business_unit_ids == None
                        or Activator.businessUnitId.in_(business_unit_ids)
                    ),
                )
                .one_or_none()
            )

            if act is not None:
                # Expand Activator
                act = activator_extension.expand_activator(act, dbs)
                schema = ExtendedActivatorSchema(many=False)
                data = schema.dump(act)
                return data, 200

    except Exception as ex:
        logger.exception(ex)
        abort(500, "Internal Server Error")


def get_file_from_repo(url, github_credentials):
    # Create temporary dir
    t = tempfile.mkdtemp()
    # user/token
    logger.debug(f"GitHub Credentials {github_credentials}")
    if github_credentials.username and github_credentials.token:
        # Update url to clone private repo
        url = f"https://{github_credentials.username}:{github_credentials.token}@{url.split('https://')[1]}"
    logger.debug(f"Cloning {url} into temporary dir")
    repo = git.Repo.clone_from(url, t, depth=1)
    tag = repo.tags.pop()
    act_metadata_yaml_file = open(os.path.join(t, ".tb/activator_metadata.yml"))
    act_metadata_yml_dict = yaml.load(act_metadata_yaml_file, Loader=yaml.FullLoader)
    act_metadata_yml_dict["latestVersion"] = tag.name
    logger.debug("activator_metadata.yml file :::: %s", pformat(act_metadata_yml_dict))
    # Remove temporary dir
    shutil.rmtree(t)
    return act_metadata_yml_dict


def create_activator(dbs, act_metadata_yml, url):
    schema = ActivatorSchema()
    activatorDetails = {}
    activatorDetails["name"] = act_metadata_yml["name"]
    activatorDetails["gitRepoUrl"] = url
    activatorDetails["status"] = "Draft"
    activator = schema.load(activatorDetails, session=dbs)
    dbs.add(activator)
    dbs.flush()
    return activator.id


def create_activator_metadata(dbs, act_metadata_yml, activator_id, url):
    schema = ActivatorMetadataSchema()
    actMetaDetails = {}
    actMetaDetails["activatorId"] = activator_id
    actMetaDetails["name"] = act_metadata_yml["name"]
    actMetaDetails["description"] = act_metadata_yml["description"]
    actMetaDetails["category"] = act_metadata_yml["category"]
    actMetaDetails["activatorLink"] = url
    actMetaDetails["typeId"] = (
        dbs.query(Type).filter(Type.value == act_metadata_yml["type"]).one_or_none()
    ).id
    actMetaDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
    actMetaDetails["latestVersion"] = act_metadata_yml["latestVersion"]
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
        actPlatformDetails["platformId"] = (
            dbs.query(Platform).filter(Platform.value == p).one_or_none()
        ).id
        actPlatformDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
        actPlatformDetails["isActive"] = True
        activator_metadata_platform = schema.load(actPlatformDetails, session=dbs)
        dbs.add(activator_metadata_platform)
        dbs.flush()


def create_activator_metadata_variables(
    dbs, activator_metadata_id, variables, isOptional
):
    schema = ActivatorMetadataVariableSchema()

    for variable in variables or ():
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
    act_metadata.type = (
        dbs.query(Type).filter(Type.id == act_metadata.typeId).one_or_none()
    )

    act_metadata.platforms = (
        dbs.query(Platform)
        .filter(
            Platform.id == ActivatorMetadataPlatform.platformId,
            ActivatorMetadata.id == ActivatorMetadataPlatform.activatorMetadataId,
            ActivatorMetadata.id == act_metadata.id,
            ActivatorMetadataPlatform.isActive,
        )
        .all()
    )

    act_metadata.variables = (
        dbs.query(ActivatorMetadataVariable)
        .filter(
            ActivatorMetadata.id == ActivatorMetadataVariable.activatorMetadataId,
            ActivatorMetadata.id == act_metadata.id,
        )
        .all()
    )

    return act_metadata
