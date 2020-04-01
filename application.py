"""
This is the application module and supports all the ReST actions for the
application collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import Application, ApplicationSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/applications
    with the complete lists of applications

    :return:        json string of list of applications
    """

    # Create the list of people from our data
    applications = Application.query.all()
    # Serialize the data for the response
    application_schema = ApplicationSchema(many=True)
    data = application_schema.dump(applications)
    app.logger.debug("application data:")
    app.logger.debug(pformat(data))
    return data


def read_one(id):
    """
    This function responds to a request for /api/application/{id}
    with one matching application from applications

    :param application:   id of the application to find
    :return:              application matching the id
    """

    application = (Application.query.filter(Application.id == id).one_or_none())

    app.logger.debug("application data:")
    app.logger.debug(pformat(application))

    if application is not None:
        # Serialize the data for the response
        application_schema = ApplicationSchema()
        data = application_schema.dump(application)
        app.logger.debug("application data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(
            404, "Application with id {id} not found".format(id=id)
        )


def create(application):
    """
    This function creates a new application in the application structure
    based on the passed in application data

    :param application:  application to create in application list
    :return:             201 on success, 406 on application exists
    """

    schema = ApplicationSchema()
    new_application = schema.load(application, session=db.session)
    db.session.add(new_application)
    db.session.commit()

    # Serialize and return the newly created application
    # in the response
    data = schema.dump(new_application)
    app.logger.debug("application data:")
    app.logger.debug(pformat(data))

    return data, 201


def update(id, application):
    """
    This function updates an existing application in the application list

    :param id: id of the application to update in the application list
    :param application:   application to update
    :return: updated application
    """

    app.logger.debug("application: ")
    app.logger.debug(pformat(application))

    # Does the application exist in applications?
    existing_application = Application.query.filter(Application.id == id).one_or_none()

    # Does application exist?
    if existing_application is not None:
        schema = ApplicationSchema()
        update_application = schema.load(application, session=db.session)
        update_application.id = id

        db.session.merge(update_application)
        db.session.commit()

        # return the updated application in the response
        data = schema.dump(update_application)
        app.logger.debug("application data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, application doesn't exist, so that's an error
    else:
        abort(404, f"Application not found")


def delete(id):
    """
    This function deletes an application from the application list

    :param id: id of the application to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the application to delete exist?
    existing_application = Application.query.filter(Application.id == id).one_or_none()

    # if found?
    if existing_application is not None:
        db.session.delete(existing_application)
        db.session.commit()

        return make_response(f"Application id {id} successfully deleted", 200)

    # Otherwise, nope, application to delete not found
    else:
        abort(404, f"Application id {id} not found")


