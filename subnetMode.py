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
    with the complete lists of subnetModes

    :return:        json string of list of subnetModes
    """

    # Create the list of subnetModes from our data
    subnetMode = SubnetMode.query.order_by(SubnetMode.key).all()
    app.logger.debug(pformat(subnetMode))
    # Serialize the data for the response
    subnetMode_schema = SubnetModeSchema(many=True)
    data = subnetMode_schema.dump(subnetMode)
    return data


def read_one(id):
    """
    This function responds to a request for /api/subnetmode/{id}
    with one matching subnetMode from subnetModes

    :param application:   id of subnetMode to find
    :return:              subnetMode matching key
    """

    subnetMode = SubnetMode.query.filter(SubnetMode.id == id).one_or_none()

    if subnetMode is not None:
        # Serialize the data for the response
        subnetMode_schema = SubnetModeSchema()
        data = subnetMode_schema.dump(subnetMode)
        return data
    else:
        abort(404, f"SubnetMode with id {id} not found")


def create(subnetMode):
    """
    This function creates a new subnetMode in the subnetMode list
    based on the passed in subnetMode data

    :param subnetMode:  subnetMode to create in subnetMode structure
    :return:        201 on success, 406 on subnetMode exists
    """

    # Remove id as it's created automatically
    if 'id' in subnetMode:
        del subnetMode['id']

    schema = SubnetModeSchema()
    new_subnetMode = schema.load(subnetMode, session=db.session)
    db.session.add(new_subnetMode)
    db.session.commit()

    # Serialize and return the newly created deployment
    # in the response
    data = schema.dump(new_subnetMode)
    return data, 201


def update(id, subnetMode):
    """
    This function updates an existing subnetMode in the subnetMode list

    :param key:    key of the subnetMode to update in the subnetMode list
    :param subnetMode:   subnetMode to update
    :return:       updated subnetMode
    """

    app.logger.debug(pformat(subnetMode))

    if 'id' in subnetMode and subnetMode['id'] != id:
           abort(400, f"Key mismatch in path and body")

    existing_subnetMode = SubnetMode.query.filter(SubnetMode.id == id).one_or_none()

    if existing_subnetMode is not None:
      SubnetMode.query.filter(SubnetMode.id == id).update(subnetMode)
      db.session.commit()
      schema = SubnetModeSchema()
      data = schema.dump(existing_subnetMode)
      return data, 200
    else:
      abort(404, f"SubnetMode {id} not found")
      

def delete(id):
    """
    This function deletes a subnetMode from the subnetModes list

    :param key: key of the subnetMode to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the subnetMode to delete exist?
    existing_subnetMode = SubnetMode.query.filter(SubnetMode.id == id).one_or_none()

    # if found?
    if existing_subnetMode is not None:
        db.session.delete(existing_subnetMode)
        db.session.commit()

        return make_response(f"SubnetMode {id} successfully deleted", 200)

    # Otherwise, nope, subnetMode to delete not found
    else:
        abort(404, f"SubnetMode {id} not found")


