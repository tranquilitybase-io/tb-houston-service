"""
This is the deployments module and supports all the ReST actions for the
environment collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response
from config import db, app
from tb_houston_service.models import LZEnvironment, LZEnvironmentSchema
from tb_houston_service.extendedSchemas import KeyValueSchema

def read_all():
    """
    This function responds to a request for /api/environment
    with the complete lists of environments

    :return:        json string of list of environments
    """

    # Create the list of environments from our data
    lzenvironment = db.session.query(LZEnvironment).order_by(LZEnvironment.name).all()
    app.logger.debug(pformat(lzenvironment))
    # Serialize the data for the response
    environment_schema = LZEnvironmentSchema(many=True)
    data = environment_schema.dump(lzenvironment)
    return data, 200


def read_all_key_values():
    """
    This function responds to a request for /api/environment
    with the complete lists of environments

    :return:        json string of list of environments
    """

    # Create the list of environments from our data
    lzenvironment = db.session.query(LZEnvironment).order_by(LZEnvironment.name).all()
    keyvalues = []
    for lze in lzenvironment:
        kv = {}
        kv['key'] = lze.id
        kv['value'] = lze.name
        keyvalues.append(kv)
        
    app.logger.debug(pformat(lzenvironment))
    schema = KeyValueSchema(many=True)
    data = schema.dump(keyvalues)
    return data, 200


def create(lzenvDetails):
    app.logger.debug(f"lzmetadata_env::create: {lzenvDetails}")
    # Remove the id
    lzenvDetails.pop('id', None)
    # Does the environment exist in environment list?
    existing_environment = db.session.query(LZEnvironment).filter(LZEnvironment.name == lzenvDetails['name']).one_or_none()
    schema = LZEnvironmentSchema()


    # Does environment exist?
    if existing_environment is not None:
        app.logger.debug(f"lzmetadata_env::update: {lzenvDetails} {existing_environment}")        
        existing_environment.isActive = lzenvDetails.get('isActive')
        db.session.merge(existing_environment)
        db.session.commit()
        data = schema.dump(existing_environment)
        return data, 201        
    else:
        app.logger.debug(f"lzmetadata_env::create: {lzenvDetails}")          
        env_change = schema.load(lzenvDetails, session=db.session)
        db.session.add(env_change)
        db.session.commit()
        data = schema.dump(env_change)
        return data, 201


def create_all(lzMetadataEnvListDetails):
    """
    This function updates lzenvironments from a list of  lz environment

    :param key:    key of the environment to update in the environment list
    :param environment:   environment to update
    :return:       updated environment
    """

    app.logger.debug(pformat(lzMetadataEnvListDetails))

    for lze in lzMetadataEnvListDetails:
        create(lze)
    return make_response(f"Environments successfully created/updated", 201)


def delete_all(lzMetadataEnvListDetails):
    """
    Deletes an lzenvironment from the lzenvironments list.

    :param key: oid of the environment to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the environment to delete exist?
    for lze in lzMetadataEnvListDetails:
        lzenv = db.session.query(LZEnvironment).filter(LZEnvironment.name == lze.name).one_or_none()
        db.session.close()
        # if found?
        if lzenv is not None:
            lzenv.isActive = False
            db.session.merge(lzenv)
            db.session.commit()

    return make_response(f"Environments successfully deleted", 200)
