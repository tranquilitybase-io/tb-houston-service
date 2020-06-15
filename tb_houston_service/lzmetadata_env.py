"""
This is the deployments module and supports all the ReST actions for the
environment collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import LZEnvironment, LZEnvironmentSchema
from tb_houston_service.extendedSchemas import KeyValueSchema

def read_all(readActiveOnly=False):
    """
    This function responds to a request for /api/environment
    with the complete lists of environments

    :return:        json string of list of environments
    """

    # Create the list of environments from our data
    lzenvironment_query = db.session.query(LZEnvironment)
    if readActiveOnly:
        lzenvironment_query = lzenvironment_query.filter(LZEnvironment.isActive)

    lzenvironment = lzenvironment_query.order_by(LZEnvironment.name).all()

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
        kv["key"] = lze.id
        kv["value"] = lze.name
        keyvalues.append(kv)

    app.logger.debug(pformat(lzenvironment))
    schema = KeyValueSchema(many=True)
    data = schema.dump(keyvalues)
    return data, 200


def create(lzenvDetails):
    app.logger.debug(f"lzmetadata_env::create: {lzenvDetails}")

    # Does the environment exist in environment list?

    schema = LZEnvironmentSchema()

    # Does environment exist?
    if lzenvDetails.get("id"):
        existing_environment = (
            db.session.query(LZEnvironment)
            .filter(LZEnvironment.id == lzenvDetails["id"])
            .one_or_none()
        )

        if existing_environment is not None:
            app.logger.debug(
                f"lzmetadata_env::update: {lzenvDetails} {existing_environment}"
            )
            updated_env = schema.load(lzenvDetails, session=db.session)
            db.session.merge(updated_env)
            db.session.commit()
            data = schema.dump(updated_env)
            return data, 201
    
    # Can't find without the id, so search using the name 
    if lzenvDetails.get("name"):
        existing_environment = (
            db.session.query(LZEnvironment)
            .filter(LZEnvironment.name == lzenvDetails["name"])
            .one_or_none()
        )
        if existing_environment is not None:
            app.logger.debug(
                f"lzmetadata_env::update: {lzenvDetails} {existing_environment}"
            )
            updated_env = schema.load(lzenvDetails, session=db.session)
            updated_env.id = existing_environment.id
            db.session.merge(updated_env)
            db.session.commit()
            data = schema.dump(updated_env)
            return data, 201
        else:
            # Just create a new object from the details
            app.logger.debug(f"lzmetadata_env::create: {lzenvDetails}")
            env_change = schema.load(lzenvDetails, session=db.session)
            db.session.add(env_change)
            db.session.commit()
            data = schema.dump(env_change)
            return data, 201
    abort("Create: Unable to create without the id or name!", 500)
 

def logical_delete_all_active():
    objs = db.session.query(LZEnvironment).filter(LZEnvironment.isActive == True).all()
    for o in objs:
        o.isActive = False
        db.session.add(o)


def create_all(lzMetadataEnvListDetails, readActiveOnly=False, bulkDelete=False):
    """
    This function updates lzenvironments from a list of  lz environment

    :param key:    key of the environment to update in the environment list
    :param environment:   environment to update
    :return:       updated environment
    """

    app.logger.debug(pformat(lzMetadataEnvListDetails))

    try:
        if bulkDelete:
            logical_delete_all_active()
            db.session.flush()
        for lze in lzMetadataEnvListDetails:
            create(lze)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    resp = read_all(readActiveOnly=readActiveOnly)
    return resp[0], 201
