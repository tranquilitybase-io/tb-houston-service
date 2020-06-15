"""
This is the deployments module and supports all the ReST actions for the
lzlanvpc collection
"""

# 3rd party modules
from pprint import pformat
import logging
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import LZLanVpc, LZLanVpcSchema
from tb_houston_service.models import LZLanVpcEnvironment
from tb_houston_service import lzlanvpc_extension
from tb_houston_service.extendedSchemas import ExtendedLZLanVpcSchema


logger = logging.getLogger("tb_houston_service.lzlanvpc")

def read(readActiveOnly=None):
    """
    This function responds to a request for /api/lzmetadata_lan_vpc
    with the complete lists of lzlanvpcs

    :return:        json string of list of lzlanvpc
    """

    logger.debug("readActiveOnly: %s", readActiveOnly)

    # Create the list of lzlanvpc from our data
    lzlanvpcs_query = db.session.query(LZLanVpc)
    if readActiveOnly:
        lzlanvpcs_query = lzlanvpcs_query.filter(LZLanVpc.isActive)
    
    lzlanvpcs = lzlanvpcs_query.order_by(LZLanVpc.name).all()
    app.logger.debug(pformat(lzlanvpcs))
    for lzlanvpc in lzlanvpcs:
        lzlanvpc_extension.expand_lzlanvpc(lzlanvpc)    

    # Serialize the data for the response
    schema = ExtendedLZLanVpcSchema(many=True)
    data = schema.dump(lzlanvpcs)
    return data, 200


def create(lzLanVpcDetails):
    app.logger.debug(f"lzmetadata_env::create: {lzLanVpcDetails}")
    # Does the environment exist in environment list?

    schema = LZLanVpcSchema()

    # Store for use later
    envs = lzLanVpcDetails['environments']
    # Removing this as the below schema is not expecting this field.
    if "environments" in lzLanVpcDetails:
        del lzLanVpcDetails["environments"]

    oid = lzLanVpcDetails.get("id")
    logger.debug("Create: obj is %s", lzLanVpcDetails)    
    logger.debug("Create: oid is %s", oid)

    # Does lanvpc exist?
    if lzLanVpcDetails.get("id"):
        logger.debug("create::Existing id is: %s", lzLanVpcDetails.get("id"))
        existing_lanvpc = (
            db.session.query(LZLanVpc)
            .filter(LZLanVpc.id == lzLanVpcDetails["id"])
            .one_or_none()
        )
        app.logger.debug("lzlanvpc::create: %s, %s.", lzLanVpcDetails, existing_lanvpc)        
        if existing_lanvpc is not None:
            updated_lanvpc = schema.load(lzLanVpcDetails, session=db.session)
            db.session.merge(updated_lanvpc)
            lzlanvpc_extension.create_lzlanvpc_environments(updated_lanvpc.id, envs)
            return
    
    # id (if populated) doesn't exist, so remove it and create a new object
    if "id" in lzLanVpcDetails:
        del lzLanVpcDetails["id"] 
    else:
        logger.debug("Create: id was missing so creating a new object instead.")
            
    if "name" in lzLanVpcDetails:
        existing_lanvpc = (
            db.session.query(LZLanVpc)
            .filter(LZLanVpc.name == lzLanVpcDetails.get("name"))
            .first()
        )
        if existing_lanvpc:
            app.logger.debug(f"lzlanvpc::create: {lzLanVpcDetails}")
            lzLanVpcDetails["id"] = existing_lanvpc.id
            lzlanvpc_change = schema.load(lzLanVpcDetails, session=db.session)
            db.session.merge(lzlanvpc_change)
            db.session.flush()
            lzlanvpc_extension.create_lzlanvpc_environments(lzlanvpc_change.id, envs)
        else:
            app.logger.debug(f"lzlanvpc::create: {lzLanVpcDetails}")
            lzlanvpc_new = schema.load(lzLanVpcDetails, session=db.session)
            db.session.add(lzlanvpc_new)
            db.session.flush()
            lzlanvpc_extension.create_lzlanvpc_environments(lzlanvpc_new.id, envs)
    else:
        abort("Cannot create without the id or name.", 500)


def logical_delete_all_active():
    objs = db.session.query(LZLanVpc).filter(LZLanVpc.isActive == True).all()
    for o in objs:
        o.isActive = False
        db.session.add(o)
    objs = db.session.query(LZLanVpcEnvironment).filter(LZLanVpcEnvironment.isActive == True).all()
    for o in objs:
        o.isActive = False
        db.session.add(o)    


def create_all(lzLanVpcListDetails, readActiveOnly=False, bulkDelete=False):
    """
    This function updates lzlanvpcs from a list of  lzlanvpcs

    :param key:    key of the lzlanvpc to update in the lzlanvpc list
    :param lzlanvpc:   lzlanvpc to update
    :return:       updated lzlanvpc
    """

    app.logger.debug("create_all: %s", pformat(lzLanVpcListDetails))

    try:
        if bulkDelete:
            logical_delete_all_active()
            db.session.flush()
        for lze in lzLanVpcListDetails:
            create(lze)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    resp = read(readActiveOnly=readActiveOnly)
    return resp[0], 201
