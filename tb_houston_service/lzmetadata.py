"""
This is the lzmetadata module and supports all the ReST actions for the
LZMetadata collection
"""

# 3rd party modules
import logging
from flask import abort
from config import db, app
from config.db_lib import db_session
from tb_houston_service.models import LZMetadata, LZMetadataSchema


logger = logging.getLogger("lzmetadata")


def read(key):
    """
    Responds to a request for /api/lzmetadata/{key}
    with one matching lzmetadata from LZMetadatas

    :param application:   key of lzmetadata to find
    :return:              LZMetadata matching key
    """

    with db_session() as dbs:
        lzmetadata = (
            dbs.query(LZMetadata).filter(LZMetadata.key == key).one_or_none()
        )

        if lzmetadata is not None:
            # Serialize the data for the response
            schema = LZMetadataSchema()
            data = schema.dump(lzmetadata)
            app.logger.debug(data)
            return data, 200
        else:
            abort(404, f"LZMetadata with key {key} not found")


def create(keyValueDetails):
    """
    Creates a new lzmetadata in the lzmetadata list
    based on the passed in lzmetadata data

    :param lzmetadata: lzmetadata to create in lzmetadata structure
    :return:        201 on success, 406 on lzmetadata exists
    """
    # Remove id as it's created automatically
    if "id" in keyValueDetails:
        del keyValueDetails["id"]

    with db_session() as dbs:
        schema = LZMetadataSchema()
        new_lzmetadata = schema.load(keyValueDetails, session=dbs)
        db.session.add(new_lzmetadata)
        db.session.commit()

        # Serialize and return the newly created lzmetadata
        # in the response
        data = schema.dump(new_lzmetadata)
        app.logger.debug(data)
        return data, 201
    abort("500", "Problem encountered creating an LZMetadata.")


def update(key, keyValueDetails):
    """
    Updates an existing lzmetadata in the lzmetadata list

    :param key:    id of the lzmetadata to update in the lzmetadata list
    :param lzmetadata:   lzmetadata to update
    :return:       updated lzmetadata.
    """

    if "key" in keyValueDetails and keyValueDetails["key"] != key:
        abort(400, "Key mismatch in path and body")
    else:
        keyValueDetails["key"] = key

    # Does the lzmetadata exist in lzmetadata list?
    with db_session() as dbs:
        existing_lzmetadata = (
            dbs.query(LZMetadata).filter(LZMetadata.key == key).one_or_none()
        )

        # Does lzmetadata exist?
        if existing_lzmetadata is not None:
            schema = LZMetadataSchema(many=False)
            update_lzmetadata = schema.load(keyValueDetails, session=db.session)
            dbs.merge(update_lzmetadata)
            dbs.commit()

            # return the updated obj in the response
            data = schema.dump(update_lzmetadata)
            app.logger.debug(data)
            return data, 200
        else:
            # otherwise, nope, it doesn't exist, so that's an error
            abort(404, f"LZMetadata with key {key} not found")
    abort(500, "Problem encountered updating lzmetadata.")


def get_gcp_project_id(projectId):
    local_key = "GCP_PROJECT_URL"
    logger.debug("get_gcp_project_id: projectId=%s", local_key)
    with db_session() as dbs:
        lzmetadata = dbs.query(LZMetadata).filter(LZMetadata.key == local_key).one_or_none()
        logger.debug("lzmetadata: %s", lzmetadata)
        if lzmetadata:
            val = {}
            val["key"] = lzmetadata.key
            val["value"] = lzmetadata.value
            val["value"] = val["value"].replace("{{project_id}}", projectId)
            schema = LZMetadataSchema(many=False)
            data = schema.dump(val)
            return data, 200
    abort(500, "Problem encountered getting the GCP Project URL.")

