"""
This is the landig zone meta data module and supports all the ReST actions for the
landig zone meta data 
"""

# 3rd party modules
from pprint import pformat
import json
from flask import make_response, abort

from config import db, app
from tb_houston_service.models import LZMetadata, LZMetadataSchema
from tb_houston_service.extendedSchemas import ExtendedLZMetadataSchema
from tb_houston_service.extendedSchemas import ExtendedLZMetadataFSApplicationSchema

folder_structure_group = "folder_structure"
folder_structure_name = "folder_structure"

def read_all():
    """
    This function responds to a request for /api/lzmetadata
    with the all the landing zone metadata

    :return:        json string of list of Landing zone metadata
    """

    # Create the list of lzmetadata from our data
    lzmetadata = (
        db.session.query(LZMetadata).filter(LZMetadata.active == True)
        .order_by(LZMetadata.group, LZMetadata.name)
        .all()
    )
    app.logger.debug(pformat(lzmetadata))

    # Check id returned metadata list is empty
    if lzmetadata:
        # Serialize the data for the response
        for metadata_row in lzmetadata:
            metadata_row.value = json.loads(metadata_row.value or '[]')

        schema = ExtendedLZMetadataSchema(many=True)
        data = schema.dump(lzmetadata)
        return data, 200
    else:
        abort(404, f"Landing zone metadata not found")


def read_one(group, name):
    """
    This function responds to a request for /api/lzmetadata/{group}/{name}
    with one matching landing zone metadata 

    :param group, name:   group and name of landing zone metadata to find
    :return:              landing zone metadata matching group and name
    """

    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.name == name, LZMetadata.group == group, LZMetadata.active == True
    ).one_or_none()

    if lzmetadata is not None:
        # Serialize the data for the response
        schema = ExtendedLZMetadataSchema(many=False)
        lzmetadata.value = json.loads(lzmetadata.value or "[]")
        return schema.dump(lzmetadata), 200
    else:
        abort(404, f"Landing zone metadata for group {group}, name {name} not found")


def read_one_group(group):
    """
    This function responds to a request for /api/lzmetadata_group/{group}
    with one matching group

    :param group:   group of landing zone metadata to find
    :return:        landing zone metadata matching group and name
    """

    lzmetadata = db.session.query(LZMetadata).filter(
            LZMetadata.group == group, LZMetadata.active == True
    ).all()

    if lzmetadata:
        # Serialize the data for the response
        for metadata_row in lzmetadata:
            metadata_row.value = json.loads(metadata_row.value or '[]')

        schema = ExtendedLZMetadataSchema(many=True)
        data = schema.dump(lzmetadata)
        return data, 200
    else:
        abort(404, f"Landing zone metadata for group {group} not found")


def create(lzMetadataDetails):
    """
    This function updates an existing or creates a lzmetadata 

    :param lzmetadata:   lzmetadata to create or update
    :return:       updated landing zone metadata
    """

    app.logger.debug(pformat(lzMetadataDetails))

    group = lzMetadataDetails["group"]
    name = lzMetadataDetails["name"]
    # Always set active to True while creating
    lzMetadataDetails["active"] = True
    lzMetadataDetails["value"] = json.dumps(lzMetadataDetails.get("value", []))

    app.logger.debug("lzmetadata:create")
    app.logger.debug(pformat(lzMetadataDetails))

    app.logger.debug(f"group: {group} name: {name}")

    # Does the landing zone metadata exist already?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == group, LZMetadata.name == name
    ).one_or_none()

    schema = LZMetadataSchema()
    # Does the landig zone meta data for the given group and name exist?
    if lzmetadata is not None:
        db.session.query(LZMetadata).filter(
            LZMetadata.group == group, LZMetadata.name == name
        ).update(lzMetadataDetails)
        db.session.commit()
    else:
        lzmetadata = schema.load(lzMetadataDetails, session=db.session)
        db.session.add(lzmetadata)
        db.session.commit()

    # return the updated/created object in the response
    # TODO: Already serialized above?
    #lzmetadata.value = json.loads(lzmetadata.value or "[]")
    app.logger.debug("lzmetadata")
    app.logger.debug(pformat(lzmetadata))
    return schema.dump(lzmetadata), 201


def delete(group, name):
    """
    Deletes a landing zone metadata.

    :param group, name: composite name of the landing zone metadata to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the landing zone metadata to delete exist?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == group, LZMetadata.name == name, LZMetadata.active == True
    ).one_or_none()
    schema = LZMetadataSchema()

    # if found?
    if lzmetadata is not None:
        # Deactivate the metadata instead of deleting it
        lzmetadataDetails = schema.dump(lzmetadata)
        lzmetadataDetails["active"] = False
        db.session.query(LZMetadata).filter(
            LZMetadata.name == name, LZMetadata.group == group
        ).update(lzmetadataDetails)
        db.session.commit()

        return make_response(
            f"Landing zone metadata for group: {group} name: {name} successfully deactivated",
            200,
        )

    # Otherwise, nope, landing zone metadata to delete not found
    else:
        abort(404, f"Landing zone metadata for group: {group} name: {name} not found")


def read_folder_structure():
    """
    This function responds to a request for /api/lztablestructure
    with one matching landing zone table structure

    :return:              Landing Zone table structure metadata
    """

    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == folder_structure_group, 
        LZMetadata.name == folder_structure_name, 
        LZMetadata.active == True
    ).one_or_none()

    if lzmetadata is not None:
        # Serialize the data for the response
        schema = ExtendedLZMetadataFSApplicationSchema(many=True)
        lzmetadataFolderStructure = json.loads(f"[{lzmetadata.value}]")
        return schema.dump(lzmetadataFolderStructure), 200
    else:
        abort(404, f"Landing zone folder_structure not found")


def create_folder_structure(lzMetadataFolderStructureDetails):
    """
    This function updates an existing or creates a 
    lzmetadata folder structure.

    :param lzFolderStructureDetails:   lzmetadata to create or update
    :return:       updated landing zone metadata folder structure metadata
    """

    app.logger.debug(pformat(lzMetadataFolderStructureDetails))

    # Always set active to True while creating
    lzMetadataDetails = {}
    lzMetadataDetails["active"] = True
    lzMetadataDetails["group"] = folder_structure_group
    lzMetadataDetails["name"] = folder_structure_name
    lzMetadataDetails["value"] = json.dumps(lzMetadataFolderStructureDetails)

    app.logger.debug("lzmetadata:create")
    app.logger.debug(pformat(lzMetadataFolderStructureDetails))

    # Does the landing zone metadata exist already?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == folder_structure_group,
        LZMetadata.name == folder_structure_name
    ).one_or_none()

    schema = ExtendedLZMetadataFSApplicationSchema(many=True)
    # Does the landing zone meta data for the given group and name exist?
    if lzmetadata is not None:
        db.session.query(LZMetadata).filter(
            LZMetadata.group == folder_structure_group,
            LZMetadata.name == folder_structure_name
        ).update(lzMetadataDetails)
        db.session.commit()
    else:
        lzmetadata = schema.load(lzMetadataDetails, session=db.session)
        db.session.add(lzmetadata)
        db.session.commit()

    # return the updated/created object in the response
    # TODO: Already serialized above?
    lzmetadata_value = json.loads(f"[{lzmetadata.value}]")
    app.logger.debug("lzmetadata")
    app.logger.debug(pformat(lzmetadata_value))
    return schema.dump(lzmetadata_value), 201

