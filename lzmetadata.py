"""
This is the landig zone meta data module and supports all the ReST actions for the
landig zone meta data 
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import LZMetadata, LZMetadataSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/lzmetadata
    with the all the landing zone metadata

    :return:        json string of list of Landing zone metadata
    """

    # Create the list of lzmetadata from our data
    lzmetadata = LZMetadata.query.filter(LZMetadata.active == True).order_by(LZMetadata.group).all()
    app.logger.debug(pformat(lzmetadata))
    # Serialize the data for the response
    lzmetadata_schema = LZMetadataSchema(many=True)
    data = lzmetadata_schema.dump(lzmetadata)
    return data, 200


def read_one(group, name):
    """
    This function responds to a request for /api/lzmetadata/{group}/{name}
    with one matching landing zone metadata 

    :param group, name:   group and name of landing zone metadata to find
    :return:              landing zone metadata matching group and name
    """

    lzmetadata = LZMetadata.query.filter(LZMetadata.name == name, LZMetadata.group == group , LZMetadata.active == True).one_or_none()

    if lzmetadata is not None:
        # Serialize the data for the response
        lzmetadata_schema = LZMetadataSchema()
        data = lzmetadata_schema.dump(lzmetadata)
        return data, 200
    else:
        abort(404, f"Landing zone metadata for group {group}, name {name} not found")


def create(lzMetadataDetails):
    """
    This function updates an existing or creates a lzmetadata 

    :param lzmetadata:   lzmetadata to create or update
    :return:       updated landing zone metadata
    """

    app.logger.debug(pformat(lzMetadataDetails))

    group = lzMetadataDetails['group']
    name = lzMetadataDetails['name']
    # Always set active to True while creating 
    lzMetadataDetails['active'] = True

    app.logger.debug("lzmetadata:create")
    app.logger.debug(pformat(lzMetadataDetails))

    app.logger.debug(f"group: {group} name: {name}")
    
    # Does the landing zone metadata exist already?
    lzmetadata = LZMetadata.query.filter(LZMetadata.group == group, LZMetadata.name == name).one_or_none()

    schema = LZMetadataSchema()
    # Does the landig zone meta data for the given group and name exist?
    if lzmetadata is not None:
        LZMetadata.query.filter(LZMetadata.name == name, LZMetadata.group == group).update(lzMetadataDetails)
        db.session.commit()
    else:
        lzmetadata = schema.load(lzMetadataDetails, session=db.session)
        db.session.add(lzmetadata)
        db.session.commit()

    # return the updated/created object in the response
    data = schema.dump(lzmetadata)
    app.logger.debug("lzmetadata")
    app.logger.debug(pformat(data))
    return data, 201


def delete(group, name):
    """
    Deletes a landing zone metadata.

    :param group, name: composite name of the landing zone metadata to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the landing zone metadata to delete exist?
    lzmetadata = LZMetadata.query.filter(LZMetadata.group == group, LZMetadata.name == name, LZMetadata.active == True).one_or_none()
    schema = LZMetadataSchema()

    # if found?
    if lzmetadata is not None:
        # Always set active to True while creating 
        lzmetadataDetails = schema.dump(lzmetadata)
        lzmetadataDetails['active'] = False
        LZMetadata.query.filter(LZMetadata.name == name, LZMetadata.group == group).update(lzmetadataDetails)
        db.session.commit()

        return make_response(f"Landing zone metadata for group: {group} name: {name} successfully deactivated", 200)

    # Otherwise, nope, landing zone metadata to delete not found
    else:
        abort(404, f"Landing zone metadata for group: {group} name: {name} not found")
