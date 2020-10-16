"""
The landingZoneAction module and supports all the ReST actions for the
landingZoneAction collection
"""
from pprint import pformat
from flask import make_response, abort

from config import db, app
from models import LandingZoneAction, LandingZoneActionSchema

def read_all():
    """
    Responds to a request for /api/landingZoneActions
    with the complete lists of landingZoneActions

    :return:        json string of list of landingZoneActions
    """
    # Create the list of people from our data
    landingZoneActions = db.session.query(LandingZoneAction).all()

    # Serialize the data for the response
    landingZoneAction_schema = LandingZoneActionSchema(many=True)
    data = landingZoneAction_schema.dump(landingZoneActions)
    app.logger.debug("landingZoneAction data:")
    app.logger.debug(pformat(data))
    return data

def read_one(oid):
    """
    Responds to a request for /api/landingzoneaction/{oid}
    with one matching landingZoneAction from landingZoneActions

    :param landingZoneAction:   id of the landingZoneAction to find
    :return:              landingZoneAction matching the id
    """
    landingZoneAction = (
        db.session.query(LandingZoneAction)
        .filter(LandingZoneAction.id == oid)
        .one_or_none()
    )

    if landingZoneAction is not None:
        # Serialize the data for the response
        landingZoneAction_schema = LandingZoneActionSchema()
        data = landingZoneAction_schema.dump(landingZoneAction)
        app.logger.debug("landingZoneAction data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(404, f"LandingZoneAction with id {oid} not found")

def create(landingZoneActionDetails):
    """
    Creates a new landingZoneAction in the landingZoneAction structure
    based on the passed in landingZoneAction data

    :param landingZoneAction:  landingZoneAction to create in landingZoneAction list
    :return:             201 on success, 406 on landingZoneAction exists
    """
    # we don't need the id, the is generated automatically on the database
    if "id" in landingZoneActionDetails:
        del landingZoneActionDetails["id"]

    schema = LandingZoneActionSchema()
    new_landingZoneAction = schema.load(landingZoneActionDetails, session=db.session)
    db.session.add(new_landingZoneAction)
    db.session.commit()

    # Serialize and return the newly created landingZoneAction
    # in the response
    data = schema.dump(new_landingZoneAction)
    app.logger.debug("landingZoneAction data:")
    app.logger.debug(pformat(data))

    return data, 201

def update(oid, landingZoneActionDetails):
    """
    Updates an existing landingZoneAction in the landingZoneAction list

    :param id: id of the landingZoneAction to update in the landingZoneAction list
    :param landingZoneAction:   landingZoneAction to update
    :return: updated landingZoneAction
    """
    app.logger.debug("landingZoneAction: ")
    app.logger.debug(pformat(landingZoneActionDetails))

    if landingZoneActionDetails["id"] != oid:
        abort(400, f"Key mismatch in path and body")

    # Does the landingZoneAction exist in landingZoneActions?
    existing_landingZoneAction = (
        db.session.query(LandingZoneAction)
        .filter(LandingZoneAction.id == oid)
        .one_or_none()
    )

    # Does landingZoneAction exist?
    if existing_landingZoneAction is not None:
        schema = LandingZoneActionSchema()
        update_landingZoneAction = schema.load(
            landingZoneActionDetails, session=db.session
        )
        update_landingZoneAction.id = oid

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

def delete(oid):
    """
    Deletes an landingZoneAction from the landingZoneAction list.

    :param id: id of the landingZoneAction to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the landingZoneAction to delete exist?
    existing_landingZoneAction = (
        db.session.query(LandingZoneAction)
        .filter(LandingZoneAction.id == oid)
        .one_or_none()
    )

    # if found?
    if existing_landingZoneAction is not None:
        db.session.delete(existing_landingZoneAction)
        db.session.commit()

        return make_response(f"LandingZoneAction id {oid} successfully deleted", 200)

    # Otherwise, nope, landingZoneAction to delete not found
    else:
        abort(404, f"LandingZoneAction id {oid} not found")
