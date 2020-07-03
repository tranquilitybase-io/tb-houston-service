"""
This is the deployments module and supports all the ReST actions for the
sourceControl collection
"""

# System modules
from pprint import pformat
from flask import make_response, abort

# 3rd party modules
from config import db, app
from tb_houston_service.models import SourceControl, SourceControlSchema


def read_all():
    """
    This function responds to a request for /api/sourceControl
    with the complete lists of sourceControls

    :return:        json string of list of sourceControls
    """

    # Create the list of sourceControls from our data
    sourceControl = db.session.query(SourceControl).order_by(SourceControl.id).all()
    app.logger.debug(pformat(sourceControl))
    # Serialize the data for the response
    sourceControl_schema = SourceControlSchema(many=True)
    data = sourceControl_schema.dump(sourceControl)
    return data


def read_one(id):
    """
    This function responds to a request for /api/sourceControl/{id}
    with one matching sourceControl from sourceControls

    :param application:   id of sourceControl to find
    :return:              sourceControl matching id
    """

    sourceControl = (
        db.session.query(SourceControl).filter(SourceControl.id == id).one_or_none()
    )

    if sourceControl is not None:
        # Serialize the data for the response
        sourceControl_schema = SourceControlSchema()
        data = sourceControl_schema.dump(sourceControl)
        return data
    else:
        abort(404, "SourceControl with id {id} not found".format(id=id))


def create(sourceControlDetails):
    """
    This function creates a new sourceControl in the sourceControl list
    based on the passed in sourceControl data

    :param sourceControl:  sourceControl to create in sourceControl structure
    :return:        201 on success, 406 on sourceControl exists
    """
    id = sourceControlDetails.get("id", None)
    # value = sourceControlDetails.get("value", None)

    # Does the sourceControl exist already?
    existing_sourceControl = (
        db.session.query(SourceControl).filter(SourceControl.id == id).one_or_none()
    )

    if existing_sourceControl is None:
        schema = SourceControlSchema()
        new_sourceControl = schema.load(sourceControlDetails, session=db.session)
        db.session.add(new_sourceControl)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_sourceControl)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, "SourceControl already exists")


def update(id, sourceControlDetails):
    """
    This function updates an existing sourceControl in the sourceControl list

    :param id:    id of the sourceControl to update in the sourceControl list
    :param sourceControl:   sourceControl to update
    :return:       updated sourceControl
    """

    app.logger.debug(pformat(sourceControlDetails))

    if sourceControlDetails["id"] != id:
        abort(400, "Key mismatch in path and body")

    # Does the sourceControl exist in sourceControl list?
    existing_sourceControl = (
        db.session.query(SourceControl).filter(SourceControl.id == id).one_or_none()
    )

    # Does sourceControl exist?

    if existing_sourceControl is not None:
        schema = SourceControlSchema()
        update_sourceControl = schema.load(sourceControlDetails, session=db.session)
        update_sourceControl.id = sourceControlDetails["id"]

        db.session.merge(update_sourceControl)
        db.session.commit()

        # return the updted sourceControl in the response
        data = schema.dump(update_sourceControl)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, "SourceControl not found")


def delete(id):
    """
    This function deletes a sourceControl from the sourceControls list

    :param id: id of the sourceControl to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the sourceControl to delete exist?
    existing_sourceControl = (
        db.session.query(SourceControl).filter(SourceControl.id == id).one_or_none()
    )

    # if found?
    if existing_sourceControl is not None:
        db.session.delete(existing_sourceControl)
        db.session.commit()

        return make_response(f"SourceControl {id} successfully deleted", 200)

    # Otherwise, nope, sourceControl to delete not found
    else:
        abort(404, f"SourceControl {id} not found")
