from pprint import pformat
import json
from config import db, app
from flask import abort, make_response
from tb_houston_service.models import LZMetadata, LZMetadataSchema
from tb_houston_service.extendedSchemas import (
    ExtendedLZMetadataListSchema
)

lan_vpc_group = "lan_vpc"

def read_group():
    """
    This function responds to a request for /api/lzmetadata_lan_vpc/{name}
    with one matching landing zone table structure

    :return:              Landing Zone LAN VPC metadata
    """

    lzmetadata = db.session.query(LZMetadata).filter(
            LZMetadata.group == lan_vpc_group
    ).all()

    if lzmetadata:
        # Serialize the data for the response
        for metadata_row in lzmetadata:
            metadata_row.value = json.loads(metadata_row.value or '[]')

        schema = ExtendedLZMetadataListSchema(many=True)
        data = schema.dump(lzmetadata)
        return data, 200
    else:
        abort(404, f"Landing zone metadata for group {lan_vpc_group} not found")


def read(name):
    """
    This function responds to a request for /api/lzmetadata_lan_vpc/
    with one matching landing zone table structure

    :return:              Landing Zone LAN VPC metadata for a given name
    """
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == lan_vpc_group,
        LZMetadata.name == name
    ).one_or_none()

    if lzmetadata is not None:
        # Serialize the data for the response
        schema = ExtendedLZMetadataListSchema(many=False)
        lzmetadata.value = json.loads(lzmetadata.value or "[]")
        return schema.dump(lzmetadata), 200
    else:
        abort(404, f"Landing zone metadata for group {lan_vpc_group}, name {name} not found")



def create(name, lzMetadataListDetails):
    """
    This function responds to a request for /api/lzmetadata_lan_vpc/
    with one matching landing zone table structure

    :return:              Landing Zone LAN VPC metadata for a given name
    """
    app.logger.debug(pformat(lzMetadataListDetails))
    if lzMetadataListDetails.get("name") and lzMetadataListDetails.get("name") != name:
        return abort(404, "Mismatch between name in path and body!")

    app.logger.debug("lzmetadata:create")
    app.logger.debug(pformat(lzMetadataListDetails))
    app.logger.debug(f"group: {lan_vpc_group}")

    # Does the landing zone metadata exist already?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == lan_vpc_group, 
        LZMetadata.name == name
    ).one_or_none()

    lzMetadataListDetails["value"] = json.dumps(lzMetadataListDetails.get("value", []))
    lzMetadataListDetails["group"] = lan_vpc_group
    lzMetadataListDetails["name"] = name

    # Does the landig zone meta data for the given group and name exist?
    if lzmetadata is not None:        
        lzmetadata.description = lzMetadataListDetails.get('description')
        lzmetadata.value = lzMetadataListDetails.get('value')
        lzmetadata.isActive = lzMetadataListDetails.get('isActive')
        lzmetadata.group = lan_vpc_group
        lzmetadata.name = name
        db.session.merge(lzmetadata)
        db.session.commit()
    else:
        schema = LZMetadataSchema(many=False, session=db.session)
        lzmetadata = schema.load(lzMetadataListDetails)
        db.session.add(lzmetadata)
        db.session.commit()

    # return the updated/created object in the response
    lzmetadata.value = json.loads(lzmetadata.value or "[]")
    app.logger.debug("lzmetadata")
    app.logger.debug(pformat(lzmetadata))
    schema = ExtendedLZMetadataListSchema(many=False)
    return schema.dump(lzmetadata), 201


def delete(name):
    """
    This function responds to a request for /api/lzmetadata_lan_vpc/
    with one matching landing zone lan vpc

    :return:              Landing Zone LAN VPC metadata for a given name
    """
    # Does the landing zone metadata to delete exist?
    lzmetadata = db.session.query(LZMetadata).filter(
        LZMetadata.group == lan_vpc_group, 
        LZMetadata.name == name
    ).one_or_none()
    schema = LZMetadataSchema()

    # if found?
    if lzmetadata is not None:
        # Deactivate the metadata instead of deleting it
        lzmetadataDetails = schema.dump(lzmetadata)
        lzmetadataDetails["isActive"] = False
        db.session.query(LZMetadata).filter(
            LZMetadata.group == lan_vpc_group,
            LZMetadata.name == name
        ).update(lzmetadataDetails)
        db.session.commit()

        return make_response(
            f"Landing zone metadata for group: {lan_vpc_group} name: {name} successfully deactivated",
            200,
        )

    # Otherwise, nope, landing zone metadata to delete not found
    else:
        abort(404, f"Landing zone metadata for group: {lan_vpc_group} name: {name} not found")