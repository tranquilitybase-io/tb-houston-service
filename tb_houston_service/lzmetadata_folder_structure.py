import json
from http import HTTPStatus
from pprint import pformat
from flask import make_response, abort

from config import db, app
from models import LZMetadata, LZMetadataSchema
from tb_houston_service.extendedSchemas import ExtendedLZMetadataFSSchema

folder_structure_group = "folder_structure"
folder_structure_name = "folder_structure"

def read():
    """
    This function responds to a request for /api/lzmetadata_folder_structure
    with one matching landing zone table structure

    :return:              Landing Zone table structure metadata
    """
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == folder_structure_group,
        LZMetadata.name == folder_structure_name
    ).one_or_none()
    db.session.close()
    app.logger.info(f"lzmetadata_folder_structure::read_one: {pformat(lzmetadata)}")

    if lzmetadata is not None:
        # Serialize the data for the response
        lzmetadata.value = json.loads(lzmetadata.value or "[]")
        schema = ExtendedLZMetadataFSSchema(many=False)
        data = schema.dump(lzmetadata)
        print(data)
        return data, 200
    else:
        abort(404, "Landing zone folder_structure not found")

def create(lzMetadataFolderStructureDetails):
    """
    This function updates an existing or creates a 
    lzmetadata folder structure.

    :param lzFolderStructureDetails:   lzmetadata to create or update
    :return:       updated landing zone metadata folder structure metadata
    """
    app.logger.debug(pformat(lzMetadataFolderStructureDetails))

    # Always set active to True while creating
    lzMetadataDetails = {}
    lzMetadataDetails["isActive"] = True
    lzMetadataDetails["group"] = folder_structure_group
    lzMetadataDetails["name"] = folder_structure_name
    lzMetadataDetails["value"] = json.dumps(lzMetadataFolderStructureDetails.get('value'))

    app.logger.debug("lzmetadata:create")
    app.logger.debug(pformat(lzMetadataFolderStructureDetails))

    # Does the landing zone metadata exist already?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == folder_structure_group,
        LZMetadata.name == folder_structure_name,
    ).one_or_none()
    db.session.close()
    schema = ExtendedLZMetadataFSSchema(many=False)
    # Does the landing zone meta data for the given group and name exist?
    if lzmetadata is not None:
        db.session.query(LZMetadata).filter(
            LZMetadata.group == folder_structure_group,
            LZMetadata.name == folder_structure_name,
        ).update(lzMetadataDetails)
        db.session.commit()
    else:
        lzmetadata = schema.load(lzMetadataDetails, session=db.session)
        db.session.add(lzmetadata)
        db.session.commit()
    db.session.close()
    # return the updated/created object in the response
    app.logger.debug("lzmetadata")
    app.logger.debug(pformat(lzmetadata))
    lzmetadata.name = folder_structure_name
    lzmetadata.value = json.loads(lzmetadata.value)
    return schema.dump(lzmetadata), 201

def delete():
    """
    This function responds to a request for /api/lzmetadata_folder_structure/
    with one matching landing zone table structure

    :return:              Landing Zone LAN VPC metadata for a given name
    """
    # Does the landing zone folder structure metadata row to delete exist?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == folder_structure_group, 
        LZMetadata.name == folder_structure_name
    ).one_or_none()

    schema = LZMetadataSchema(many=False)

    # if found?
    if lzmetadata is not None:
        # Deactivate the metadata instead of deleting it
        lzmetadataDetails = schema.dump(lzmetadata)
        lzmetadataDetails["isActive"] = False
        db.session.query(LZMetadata).filter(
            LZMetadata.group == folder_structure_group,
            LZMetadata.name == folder_structure_name
        ).update(lzmetadataDetails)
        db.session.commit()
        db.session.close()

        return make_response(
            f"Landing zone metadata for group: {folder_structure_group} name: {folder_structure_name} successfully deactivated",
            200,
        )

    # Otherwise, nope, landing zone metadata to delete not found
    else:
        abort(404, f"Landing zone metadata for group: {folder_structure_group} name: {folder_structure_name} not found")

def read_value():
    resp = read()
    print(f"lzmetadata_folder_structure::read_value: {resp}")
    if resp[1] == HTTPStatus.OK:
        return resp[0]['value']
    else:
        return abort(500, "Unable to read folder structure metadata.")
