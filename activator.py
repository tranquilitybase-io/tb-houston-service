"""
This is the activator module and supports all the ReST actions for the
activators collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import User
from models import Activator
from models import ModelTools
from extendedSchemas import ExtendedActivatorSchema
from extendedSchemas import ExtendedUserSchema
import user_extension
import activator_extension
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/activators
    with the complete lists of activators

    :return:        json string of list of activators
    """

    # Create the list of activators from our data
    activators = Activator.query.order_by(Activator.id).all()
    activators_arr = []
    for act in activators:
        activators_arr.append(activator_extension.build_activator(act))

    # Serialize the data for the response
    activator_schema = ExtendedActivatorSchema(many=True)
    data = activator_schema.dump(activators_arr)
    app.logger.debug("read_all")
    app.logger.debug(pformat(data))
    return data


def read_one(id):
    """
    This function responds to a request for /api/activator/{key}
    with one matching activator from activatorss

    :param application:   key of activator to find
    :return:              activator matching key
    """

    activator = (Activator.query.filter(Activator.id == id).one_or_none())

    if activator is not None:
        # Serialize the data for the response
        activator_schema = ActivatorSchema()
        data = activator_schema.dump(activator)
        return data
    else:
        abort(
            404, "Activator with id {id} not found".format(id=id)
        )


def create(activator):
    """
    This function creates a new activator in the activator list
    based on the passed in activator data

    :param activator:  activator to create in activator list
    :return:        201 on success, 406 on activator exists
    """
    id = activator.get("id", None)

    # Does the activators exist already?
    existing_activator = (
        Activator.query.filter(Activator.id == id).one_or_none()
    )


    if existing_activator is None:
        schema = ActivatorSchema()
        new_activator = schema.load(activator, session=db.session)
        new_activator.lastUpdated = ModelTools.get_utc_timestamp()
        db.session.add(new_activator)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_activator)
        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"Activator id {id} already exists")


def update(id, activator):
    """
    This function updates an existing activator in the activators list

    :param key:    key of the activator to update in the activators list
    :param activator:   activator to update
    :return:       updated activator
    """

    app.logger.debug("update")
    app.logger.debug("id")
    app.logger.debug(id)
    app.logger.debug("activator")
    app.logger.debug(pformat(activator))

    # Does the activators exist in activators list?
    existing_activator = Activator.query.filter(Activator.id == id).one_or_none()

    # Does activator exist?

    if existing_activator is not None:
        schema = ActivatorSchema()
        update_activator = schema.load(activator, session=db.session)
        update_activator.id = activator['id']
        update_activator.name = activator.get('name', '')
        update_activator.envs = activator.get('envs', '')
        new_activator.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(update_activator)
        db.session.commit()

        # return the updated activator in the response
        data = schema.dump(update_activator)
        app.logger.debug("activator data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Activator id {id} not found")


def delete(id):
    """
    This function deletes an activator from the activators list

    :param key: key of the activator to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the activator to delete exist?
    existing_activator = Activator.query.filter(Activator.id == id).one_or_none()

    # if found?
    if existing_activator is not None:
        db.session.delete(existing_activator)
        db.session.commit()

        return make_response(f"Activator id {id} successfully deleted", 200)

    # Otherwise, nope, activator to delete not found
    else:
        abort(404, f"Activator id {id} not found")


def setActivatorStatus(activator):
    " update the activator status"

    print(pformat(activator))
    app.logger.info(activator)
    # Does the activator to delete exist?
    existing_activator = Activator.query.filter(Activator.id == activator['id']).one_or_none()

    # if found?
    if existing_activator is not None:
        existing_activator.status = activator.get('status', existing_activator.status)
        existing_activator.accessRequestedBy = activator.get('accessRequestedBy', existing_activator.accessRequestedBy)
        existing_activator.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(existing_activator)
        db.session.commit()

        id = activator['id']
        return make_response(f"Activator {id} successfully updated", 200)

    # Otherwise, nope, activator to update was not found
    else:
        id = activator['id']
        abort(404, f"Activator id {id} not found")
