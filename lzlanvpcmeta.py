"""
The lzLANVPCMeta module and supports all the ReST actions for the
lzLANVPCMeta collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import LZLANVPCMeta, LZLANVPCMetaSchema
from pprint import pformat


def read_all():
    """
    Responds to a request for /api/lzLANVPCMetas
    with the complete lists of lzLANVPCMetas

    :return:        json string of list of lzLANVPCMetas
    """

    # Create the list of lzLANVPCMetas from our data
    lzLANVPCMetas = LZLANVPCMeta.query.all()

    # Serialize the data for the response
    LZLANVPCMeta_schema = LZLANVPCMetaSchema(many=True)
    data = LZLANVPCMeta_schema.dump(LZLANVPCMetas)
    app.logger.debug("LZLANVPCMeta data:")
    app.logger.debug(pformat(data))
    return data


def read_one(oid):
    """
    Responds to a request for /api/lzlanvpcmeta/{oid}
    with one matching lzLANVPCMeta from lzLANVPCMetas

    :param lzLANVPCMeta:   id of the lzLANVPCMeta to find
    :return:              lzLANVPCMeta matching the id
    """

    lzLANVPCMeta = (lzLANVPCMeta.query.filter(lzLANVPCMeta.id == oid).one_or_none())

    if lzLANVPCMeta is not None:
        # Serialize the data for the response
        lzLANVPCMeta_schema = lzLANVPCMetaSchema()
        data = lzLANVPCMeta_schema.dump(lzLANVPCMeta)
        app.logger.debug("lzLANVPCMeta data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(404, f"lzLANVPCMeta with id {oid} not found")


def create(lzLANVPCMetaDetails):
    """
    Creates a new lzLANVPCMeta in the lzLANVPCMeta structure
    based on the passed in lzLANVPCMeta data

    :param lzLANVPCMeta:  lzLANVPCMeta to create in lzLANVPCMeta list
    :return:             201 on success, 406 on lzLANVPCMeta exists
    """

    # we don't need the id, the is generated automatically on the database
    if ('id' in lzLANVPCMetaDetails):
      del lzLANVPCMetaDetails["id"]

    schema = lzLANVPCMetaSchema()
    new_lzLANVPCMeta = schema.load(lzLANVPCMetaDetails, session=db.session)
    db.session.add(new_lzLANVPCMeta)
    db.session.commit()

    # Serialize and return the newly created lzLANVPCMeta
    # in the response
    data = schema.dump(new_lzLANVPCMeta)
    app.logger.debug("lzLANVPCMeta data:")
    app.logger.debug(pformat(data))

    return data, 201


def update(oid, lzLANVPCMetaDetails):
    """
    Updates an existing lzLANVPCMeta in the lzLANVPCMeta list

    :param id: id of the lzLANVPCMeta to update in the lzLANVPCMeta list
    :param lzLANVPCMeta:   lzLANVPCMeta to update
    :return: updated lzLANVPCMeta
    """

    app.logger.debug("lzLANVPCMeta: ")
    app.logger.debug(pformat(lzLANVPCMetaDetails))

    if lzLANVPCMetaDetails["id"] != oid:
      abort(400, f"Key mismatch in path and body")

    # Does the lzLANVPCMeta exist in lzLANVPCMetas?
    existing_LZLANVPCMeta = LZLANVPCMeta.query.filter(LZLANVPCMeta.id == oid).one_or_none()

    # Does lzLANVPCMeta exist?
    if existing_LZLANVPCMeta is not None:
        schema = LZLANVPCMetaSchema()
        update_lzLANVPCMeta = schema.load(lzLANVPCMetaDetails, session=db.session)
        update_lzLANVPCMeta.id = oid

        db.session.merge(update_lzLANVPCMeta)
        db.session.commit()

        # return the updated lzLANVPCMeta in the response
        data = schema.dump(update_lzLANVPCMeta)
        app.logger.debug("lzLANVPCMeta data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, LZLANVPCMeta doesn't exist, so that's an error
    else:
        abort(404, f"LZLANVPCMeta not found")


def delete(oid):
    """
    Deletes an LZLANVPCMeta from the LZLANVPCMeta list.

    :param id: id of the LZLANVPCMeta to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the lzLANVPCMeta to delete exist?
    existing_LZLANVPCMeta = LZLANVPCMeta.query.filter(LZLANVPCMeta.id == oid).one_or_none()

    # if found?
    if existing_LZLANVPCMeta is not None:
        db.session.delete(existing_LZLANVPCMeta)
        db.session.commit()

        return make_response(f"lzLANVPCMeta id {oid} successfully deleted", 200)

    # Otherwise, nope, LZLANVPCMeta to delete not found
    else:
        abort(404, f"LZLANVPCMeta id {oid} not found")


