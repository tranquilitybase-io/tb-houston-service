"""
This is the deployments module and supports all the ReST actions for the
lzlanvpc collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response
from config import db, app
from tb_houston_service.models import LZLanVpc, LZLanVpcSchema


def read():
    """
    This function responds to a request for /api/lzmetadata_lan_vpc
    with the complete lists of lzlanvpcs

    :return:        json string of list of lzlanvpc
    """

    # Create the list of lzlanvpc from our data
    lzlanvpc = db.session.query(LZLanVpc).order_by(LZLanVpc.name).all()
    app.logger.debug(pformat(lzlanvpc))
    # Serialize the data for the response
    schema = LZLanVpcSchema(many=True)
    data = schema.dump(lzlanvpc)
    return data, 200


def create(lzLanVpcDetails):
    app.logger.debug(f"lzmetadata_env::create: {lzLanVpcDetails}")
    # Remove the id
    lzLanVpcDetails.pop("id", None)
    # Does the environment exist in environment list?
    existing_lanvpc = (
        db.session.query(LZLanVpc)
        .filter(LZLanVpc.name == lzLanVpcDetails["name"])
        .one_or_none()
    )
    schema = LZLanVpcSchema()

    # Does environment exist?
    if existing_lanvpc is not None:
        app.logger.debug(f"lzmetadata_env::update: {lzLanVpcDetails} {existing_lanvpc}")
        existing_lanvpc.isActive = lzLanVpcDetails.get("isActive")
        db.session.merge(existing_lanvpc)
        db.session.commit()
        data = schema.dump(existing_lanvpc)
        return data, 201
    else:
        app.logger.debug(f"lzmetadata_env::create: {lzLanVpcDetails}")
        env_change = schema.load(lzLanVpcDetails, session=db.session)
        db.session.add(env_change)
        db.session.commit()
        data = schema.dump(env_change)
        return data, 201


def create_all(lzLanVpcListDetails):
    """
    This function updates lzlanvpcs from a list of  lzlanvpcs

    :param key:    key of the lzlanvpc to update in the lzlanvpc list
    :param lzlanvpc:   lzlanvpc to update
    :return:       updated lzlanvpc
    """

    app.logger.debug(pformat(lzLanVpcListDetails))

    for lze in lzLanVpcListDetails:
        create(lze)
    return make_response(f"LAN VPC successfully created/updated", 201)
