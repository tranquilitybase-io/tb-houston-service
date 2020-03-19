"""
This is the landingZoneAction module and supports all the ReST actions for the
landingZoneAction collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import LandingZoneAction, LandingZoneActionSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/landingZoneActions
    with the complete lists of landingZoneActions

    :return:        json string of list of landingZoneActions
    """

    # Create the list of people from our data
    landingZoneActions = LandingZoneAction.query.all()

    # Serialize the data for the response
    landingZoneAction_schema = LandingZoneActionSchema(many=True)
    data = landingZoneAction_schema.dump(landingZoneActions)
    app.logger.debug("landingZoneAction data:")
    app.logger.debug(pformat(data))
    return data


def read_one(id):
    """
    This function responds to a request for /api/landingzoneaction/{id}
    with one matching landingZoneAction from landingZoneActions

    :param landingZoneAction:   id of the landingZoneAction to find
    :return:              landingZoneAction matching the id
    """

    landingZoneAction = (LandingZoneAction.query.filter(LandingZoneAction.id == id).one_or_none())

    if landingZoneAction is not None:
        # Serialize the data for the response
        landingZoneAction_schema = LandingZoneActionSchema()
        data = landingZoneAction_schema.dump(landingZoneAction)
        app.logger.debug("landingZoneAction data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(
            404, "LandingZoneAction with id {id} not found".format(id=id)
        )


def create(landingZoneAction):
    """
    This function creates a new landingZoneAction in the landingZoneAction structure
    based on the passed in landingZoneAction data

    :param landingZoneAction:  landingZoneAction to create in landingZoneAction list
    :return:             201 on success, 406 on landingZoneAction exists
    """

    # we don't need the id, the is generated automatically on the database
    if ('id' in landingZoneAction):
      del landingZoneAction["id"]

    schema = LandingZoneActionSchema()
    new_landingZoneAction = schema.load(landingZoneAction, session=db.session)
    db.session.add(new_landingZoneAction)
    db.session.commit()

    # Serialize and return the newly created landingZoneAction
    # in the response
    data = schema.dump(new_landingZoneAction)
    app.logger.debug("landingZoneAction data:")
    app.logger.debug(pformat(data))

    return data, 201


def update(id, landingZoneAction):
    """
    This function updates an existing landingZoneAction in the landingZoneAction list

    :param id: id of the landingZoneAction to update in the landingZoneAction list
    :param landingZoneAction:   landingZoneAction to update
    :return: updated landingZoneAction
    """

    app.logger.debug("landingZoneAction: ")
    app.logger.debug(pformat(landingZoneAction))

    if landingZoneAction["id"] != id:
      abort(400, f"Key mismatch in path and body")

    # Does the landingZoneAction exist in landingZoneActions?
    existing_landingZoneAction = LandingZoneAction.query.filter(LandingZoneAction.id == id).one_or_none()

    # Does landingZoneAction exist?
    if existing_landingZoneAction is not None:
        schema = LandingZoneActionSchema()
        update_landingZoneAction = schema.load(landingZoneAction, session=db.session)
        update_landingZoneAction.id = id

        db.session.merge(update_landingZoneAction)
        db.session.commit()

        # return the updated landingZoneAction in the response
        data = schema.dump(update_landingZoneAction)
        app.logger.debug("landingZoneAction data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, landingZoneAction doesn't exist, so that's an error
    else:
        abort(404, f"LandingZoneAction not found")


def delete(id):
    """
    This function deletes an landingZoneAction from the landingZoneAction list

    :param id: id of the landingZoneAction to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the landingZoneAction to delete exist?
    existing_landingZoneAction = LandingZoneAction.query.filter(LandingZoneAction.id == id).one_or_none()

    # if found?
    if existing_landingZoneAction is not None:
        db.session.delete(existing_landingZoneAction)
        db.session.commit()

        return make_response(f"LandingZoneAction id {id} successfully deleted", 200)

    # Otherwise, nope, landingZoneAction to delete not found
    else:
        abort(404, f"LandingZoneAction id {id} not found")


