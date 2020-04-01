"""
This is the deployments module and supports all the ReST actions for the
subnetMode collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import SubnetMode, SubnetModeSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/subnetMode
    with the complete lists of SubnetModes 

    :return:        json string of list of SubnetModes 
    """

    # Create the list of SubnetModes from our data
    subnetMode = SubnetMode.query.order_by(SubnetMode.key).all()
    app.logger.debug(pformat(subnetMode))
    # Serialize the data for the response
    subnetMode_schema = SubnetModeSchema(many=True)
    data = subnetMode_schema.dump(subnetMode)
    return data


def read_one(key):
    """
    This function responds to a request for /api/subnetMode/{key}
    with one matching subnetMode from SubnetModes 

    :param application:   key of subnetMode to find
    :return:              subnetMode matching key
    """

    subnetMode = (SubnetMode.query.filter(SubnetMode.key == key).one_or_none())

    if subnetMode is not None:
        # Serialize the data for the response
        subnetMode_schema = SubnetModeSchema()
        data = subnetMode_schema.dump(subnetMode)
        return data
    else:
        abort(
            404, "SubnetMode with key {key} not found".format(key=key)
        )


def create(subnetMode):
    """
    This function creates a new subnetMode in the subnetMode list
    based on the passed in subnetMode data

    :param subnetMode: subnetMode to create in subnetMode structure
    :return:        201 on success, 406 on subnetMode exists
    """
    key = subnetMode.get("key", None)
    value = subnetMode.get("value", None)

    # Does the subnetMode exist already?
    existing_subnetMode = (
        SubnetMode.query.filter(SubnetMode.key == key).one_or_none()
    )

    if existing_subnetMode is None:
        schema = SubnetModeSchema()
        new_subnetMode = schema.load(subnetMode, session=db.session)
        db.session.add(new_subnetMode)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_subnetMode)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"SubnetMode already exists")


def update(key, subnetMode):
    """
    This function updates an existing subnetMode in the subnetMode list

    :param key:    key of the subnetMode to update in the subnetMode list
    :param subnetMode:   subnetMode to update
    :return:       updated subnetMode
    """

    app.logger.debug(pformat(subnetMode))

    if subnetMode["key"] != key:
           abort(400, f"Key mismatch in path and body")

    # Does the subnetMode exist in subnetMode list?
    existing_subnetMode = SubnetMode.query.filter(
            SubnetMode.key == key
    ).one_or_none()

    # Does subnetMode exist?

    if existing_subnetMode is not None:
        schema = SubnetModeSchema()
        update_subnetMode = schema.load(subnetMode, session=db.session)
        update_subnetMode.key = subnetMode['key']

        db.session.merge(update_subnetMode)
        db.session.commit()

        # return the updted subnetMode in the response
        data = schema.dump(update_subnetMode)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"SubnetMode not found")


def delete(key):
    """
    This function deletes a SubnetMode from the SubnetMode list

    :param key: key of the SubnetMode to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the subnetMode to delete exist?
    existing_subnetMode = SubnetMode.query.filter(SubnetMode.key == key).one_or_none()

    # if found?
    if existing_subnetMode is not None:
        db.session.delete(existing_subnetMode)
        db.session.commit()

        return make_response(f"SubnetMode {key} successfully deleted", 200)

    # Otherwise, nope, subnetMode to delete not found
    else:
        abort(404, f"SubnetMode {key} not found")


