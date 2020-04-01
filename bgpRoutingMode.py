"""
This is the deployments module and supports all the ReST actions for the
bgpRoutingMode collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import BGPRoutingMode, BGPRoutingModeSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/bgpRoutingMode
    with the complete lists of BGPRoutingModes 

    :return:        json string of list of BGPRoutingModes 
    """

    # Create the list of BGPRoutingModes from our data
    bgpRoutingMode = BGPRoutingMode.query.order_by(BGPRoutingMode.key).all()
    app.logger.debug(pformat(bgpRoutingMode))
    # Serialize the data for the response
    bgpRoutingMode_schema = BGPRoutingModeSchema(many=True)
    data = bgpRoutingMode_schema.dump(bgpRoutingMode)
    return data


def read_one(key):
    """
    This function responds to a request for /api/bgpRoutingMode/{key}
    with one matching bgpRoutingMode from BGPRoutingModes 

    :param application:   key of bgpRoutingMode to find
    :return:              bgpRoutingMode matching key
    """

    bgpRoutingMode = (BGPRoutingMode.query.filter(BGPRoutingMode.key == key).one_or_none())

    if bgpRoutingMode is not None:
        # Serialize the data for the response
        bgpRoutingMode_schema = BGPRoutingModeSchema()
        data = bgpRoutingMode_schema.dump(bgpRoutingMode)
        return data
    else:
        abort(
            404, "BGPRoutingMode with key {key} not found".format(key=key)
        )


def create(bgpRoutingMode):
    """
    This function creates a new bgpRoutingMode in the bgpRoutingMode list
    based on the passed in bgpRoutingMode data

    :param bgpRoutingMode: bgpRoutingMode to create in bgpRoutingMode structure
    :return:        201 on success, 406 on bgpRoutingMode exists
    """
    key = bgpRoutingMode.get("key", None)
    value = bgpRoutingMode.get("value", None)

    # Does the bgpRoutingMode exist already?
    existing_bgpRoutingMode = (
        BGPRoutingMode.query.filter(BGPRoutingMode.key == key).one_or_none()
    )

    if existing_bgpRoutingMode is None:
        schema = BGPRoutingModeSchema()
        new_bgpRoutingMode = schema.load(bgpRoutingMode, session=db.session)
        db.session.add(new_bgpRoutingMode)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_bgpRoutingMode)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"BGPRoutingMode already exists")


def update(key, bgpRoutingMode):
    """
    This function updates an existing bgpRoutingMode in the bgpRoutingMode list

    :param key:    key of the bgpRoutingMode to update in the bgpRoutingMode list
    :param bgpRoutingMode:   bgpRoutingMode to update
    :return:       updated bgpRoutingMode
    """

    app.logger.debug(pformat(bgpRoutingMode))

    if bgpRoutingMode["key"] != key:
           abort(400, f"Key mismatch in path and body")

    # Does the bgpRoutingMode exist in bgpRoutingMode list?
    existing_bgpRoutingMode = BGPRoutingMode.query.filter(
            BGPRoutingMode.key == key
    ).one_or_none()

    # Does bgpRoutingMode exist?

    if existing_bgpRoutingMode is not None:
        schema = BGPRoutingModeSchema()
        update_bgpRoutingMode = schema.load(bgpRoutingMode, session=db.session)
        update_bgpRoutingMode.key = bgpRoutingMode['key']

        db.session.merge(update_bgpRoutingMode)
        db.session.commit()

        # return the updted bgpRoutingMode in the response
        data = schema.dump(update_bgpRoutingMode)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"BGPRoutingMode not found")


def delete(key):
    """
    This function deletes a BGPRoutingMode from the BGPRoutingMode list

    :param key: key of the BGPRoutingMode to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the bgpRoutingMode to delete exist?
    existing_bgpRoutingMode = BGPRoutingMode.query.filter(BGPRoutingMode.key == key).one_or_none()

    # if found?
    if existing_bgpRoutingMode is not None:
        db.session.delete(existing_bgpRoutingMode)
        db.session.commit()

        return make_response(f"BGPRoutingMode {key} successfully deleted", 200)

    # Otherwise, nope, bgpRoutingMode to delete not found
    else:
        abort(404, f"BGPRoutingMode {key} not found")


