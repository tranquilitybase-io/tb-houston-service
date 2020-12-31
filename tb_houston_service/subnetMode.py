"""
Deployments module, supports all the ReST actions for the
subnetMode collection
"""
from pprint import pformat

from flask import abort, make_response

from config import app, db
from models import SubnetMode, SubnetModeSchema


def read_all():
    """
    Responds to a request for /api/subnetMode
    with the complete lists of subnetModes

    :return:        json string of list of subnetModes
    """
    # Create the list of subnetModes from our data
    subnetMode = db.session.query(SubnetMode).order_by(SubnetMode.key).all()
    app.logger.debug(pformat(subnetMode))
    # Serialize the data for the response
    subnetMode_schema = SubnetModeSchema(many=True)
    data = subnetMode_schema.dump(subnetMode)
    return data


def read_one(oid):
    """
    Responds to a request for /api/subnetmode/{oid}
    with one matching subnetMode from subnetModes

    :param application:   id of subnetMode to find
    :return:              subnetMode matching key
    """
    subnetMode = db.session.query(SubnetMode).filter(SubnetMode.id == oid).one_or_none()

    if subnetMode is not None:
        # Serialize the data for the response
        subnetMode_schema = SubnetModeSchema()
        data = subnetMode_schema.dump(subnetMode)
        return data
    else:
        abort(404, f"SubnetMode with id {oid} not found")


def create(subnetModeDetails):
    """
    Creates a new subnetMode in the subnetMode list
    based on the passed in subnetMode data

    :param subnetMode:  subnetMode to create in subnetMode structure
    :return:        201 on success, 406 on subnetMode exists
    """
    # Remove id as it's created automatically
    if "id" in subnetModeDetails:
        del subnetModeDetails["id"]

    schema = SubnetModeSchema()
    new_subnetMode = schema.load(subnetModeDetails, session=db.session)
    db.session.add(new_subnetMode)
    db.session.commit()

    # Serialize and return the newly created deployment
    # in the response
    data = schema.dump(new_subnetMode)
    return data, 201


def update(oid, subnetModeDetails):
    """
    Updates an existing subnetMode in the subnetMode list

    :param key:    key of the subnetMode to update in the subnetMode list
    :param subnetMode:   subnetMode to update
    :return:       updated subnetMode
    """
    app.logger.debug(pformat(subnetModeDetails))

    if "id" in subnetModeDetails and subnetModeDetails["id"] != oid:
        abort(400, f"Key mismatch in path and body")

    existing_subnetMode = (
        db.session.query(SubnetMode).filter(SubnetMode.id == oid).one_or_none()
    )

    if existing_subnetMode is not None:
        db.session.query(SubnetMode).filter(SubnetMode.id == oid).update(
            subnetModeDetails
        )
        db.session.commit()
        schema = SubnetModeSchema()
        data = schema.dump(existing_subnetMode)
        return data, 200
    else:
        abort(404, f"SubnetMode {oid} not found")


def delete(oid):
    """
    Deletes a subnetMode from the subnetModes list

    :param key: key of the subnetMode to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the subnetMode to delete exist?
    existing_subnetMode = (
        db.session.query(SubnetMode).filter(SubnetMode.id == oid).one_or_none()
    )

    # if found?
    if existing_subnetMode is not None:
        db.session.delete(existing_subnetMode)
        db.session.commit()

        return make_response(f"SubnetMode {oid} successfully deleted", 200)

    # Otherwise, nope, subnetMode to delete not found
    else:
        abort(404, f"SubnetMode {oid} not found")
