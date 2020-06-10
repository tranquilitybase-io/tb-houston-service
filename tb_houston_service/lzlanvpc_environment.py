"""
This is the deployments module and supports all the ReST actions for the
lzlanvpc environment relationship collection
"""

# 3rd party modules
import logging
from pprint import pformat
from flask import make_response
from config import db
from tb_houston_service.models import LZLanVpcEnvironment, LZLanVpcEnvironmentSchema
from tb_houston_service.models import LZEnvironment, LZLanVpc
from tb_houston_service.extendedSchemas import ExtendedLZLanVpcEnvironmentSchema

logger = logging.getLogger("tb_houston_service.lzlanvpc_environment")


def read_all():
    """
    This function responds to a request for /api/lzmetadata_lan_vpc_environment
    with the complete lists of lzmetadata lan vpc environment relationships

    :return:        json string of list of lzmetadata lan vpc environment relationships
    """

    # Return a list of lzmetadata lan vpc environment relationships
    sol_env = (
        db.session.query(LZLanVpcEnvironment).order_by(LZLanVpcEnvironment.id).all()
    )
    logger.debug(pformat(sol_env))
    # Serialize the data for the response

    for se in sol_env:
        se.lzlanvpc = (
            db.session.query(LZLanVpc)
            .filter(LZLanVpc.id == se.lzlanvpcId)
            .one_or_none()
        )
        se.environment = (
            db.session.query(LZEnvironment)
            .filter(LZEnvironment.id == se.environmentId)
            .one_or_none()
        )
    schema = ExtendedLZLanVpcEnvironmentSchema(many=True)
    data = schema.dump(sol_env)
    return data, 200


def create(lzLanVpcEnvironmentListDetail):
    logger.debug("create: %s", lzLanVpcEnvironmentListDetail)
    # Remove the id
    lzLanVpcEnvironmentListDetail.pop("id", None)
    # Does the LZ Lanvpc environment exist?
    existing_lzlanvpc_env = (
        db.session.query(LZLanVpcEnvironment)
        .filter(
            LZLanVpcEnvironment.lzlanvpcId
            == lzLanVpcEnvironmentListDetail["lzlanvpcId"],
            LZLanVpcEnvironment.environmentId
            == lzLanVpcEnvironmentListDetail["environmentId"],
        )
        .one_or_none()
    )
    schema = LZLanVpcEnvironmentSchema()

    # Does sol_env exist?
    if existing_lzlanvpc_env is not None:
        logger.debug("update: %s", existing_lzlanvpc_env)
        existing_lzlanvpc_env.isActive = lzLanVpcEnvironmentListDetail.get(
            "isActive", True
        )
        db.session.merge(existing_lzlanvpc_env)
        db.session.commit()
        data = schema.dump(existing_lzlanvpc_env)
        return data, 201
    else:
        logger.debug("create: %s", lzLanVpcEnvironmentListDetail)
        lzlanvpc_env_change = schema.load(
            lzLanVpcEnvironmentListDetail, session=db.session
        )
        lzlanvpc_env_change.isActive = lzLanVpcEnvironmentListDetail.get(
            "isActive", True
        )
        db.session.add(lzlanvpc_env_change)
        db.session.commit()
        data = schema.dump(lzlanvpc_env_change)
        return data, 201


def create_all(lzLanVpcEnvironmentListDetails):
    """
    This function updates lzlanvpc environments relationships.

    :param lzlanvpc environment:  lzlanvpc environment to update
    :return:       updated lzlanvpc environment
    """

    logger.debug("create_all: %s", pformat(lzLanVpcEnvironmentListDetails))

    for lze in lzLanVpcEnvironmentListDetails:
        create(lze)
    return make_response("LZ LAN VPC environments successfully created/updated", 201)
