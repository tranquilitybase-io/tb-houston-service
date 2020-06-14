"""
This is the application module and supports all the ReST actions for the
application collection
"""

# 3rd party modules
from flask import make_response, abort
import logging
import json
from pprint import pformat
from sqlalchemy import literal_column
from sqlalchemy.exc import SQLAlchemyError

from config import db
from tb_houston_service.models import Application, ApplicationSchema
from tb_houston_service.extendedSchemas import ExtendedApplicationSchema
from tb_houston_service.tools import ModelTools
from tb_houston_service import application_extension


logger = logging.getLogger("tb_houston_service.application")


def read_all(
    isActive=None,
    isFavourite=None,
    status=None,
    activatorId=None,
    environment=None,
    page=None,
    page_size=None,
    sort=None,
):
    """
    This function responds to a request for /api/applications
    with the complete lists of applications

    :return:        json string of list of applications
    """

    logger.debug("Parameters: isActive: %s, isFavourite: %s, status: %s, activatorId: %s, environment: %s, page: %s, page_size: %s, sort: %s",
     isActive, isFavourite, status, activatorId, environment, page, page_size, sort)
    # Create the list of applications from our data
    # pre-process sort instructions
    if sort == None:
        application_query = db.session.query(Application).order_by(Application.id)
    else:
        try:
            sort_inst = [si.split(":") for si in sort]
            orderby_arr = []
            for si in sort_inst:
                si1 = si[0]
                if len(si) > 1:
                    si2 = si[1]
                else:
                    si2 = "asc"
                orderby_arr.append(f"{si1} {si2}")
            # print("orderby: {}".format(orderby_arr))
            application_query = db.session.query(Application).order_by(
                literal_column(", ".join(orderby_arr))
            )

        except SQLAlchemyError as e:
            logger.warning(e)
            application_query = db.session.query(Application).order_by(Application.id)

    application_query = application_query.filter(
        (status == None or Application.status == status),
        (activatorId == None or Application.activatorId == activatorId),
        (environment == None or Application.env == environment),
        (isActive == None or Application.isActive == isActive),
        (isFavourite == None or Application.isFavourite == isFavourite), 
    )

    if page == None or page_size == None:
        applications = application_query.all()
    else:
        applications = application_query.limit(page_size).offset(page * page_size).all()


    for app in applications:
        application_extension.expand_application(app)

    # Serialize the data for the response
    application_schema = ExtendedApplicationSchema(many=True)
    data = application_schema.dump(applications)
    logger.debug("application data:")
    logger.debug(pformat(data))
    return data


def read_one(oid):
    """
    This function responds to a request for /api/application/{oid}
    with one matching application from applications

    :param application:   id of the application to find
    :return:              application matching the id
    """

    application = (
        db.session.query(Application).filter(Application.id == oid).one_or_none()
    )

    db.session.close()

    logger.debug("application data:")
    logger.debug(pformat(application))

    if application is not None:
        application = application_extension.expand_application(application)
        # Serialize the data for the response
        application_schema = ExtendedApplicationSchema()
        data = application_schema.dump(application)
        logger.debug("application data:")
        logger.debug(pformat(data))
        return data
    else:
        abort(404, f"Application with id {oid} not found".format(id=oid))


def create(applicationDetails):
    """
    This function creates a new application in the application structure
    based on the passed in application data

    :param application:  application to create in application list
    :return:             201 on success, 406 on application exists
    """

    # Remove id as it's created automatically
    if "id" in applicationDetails:
        del applicationDetails["id"]

    schema = ApplicationSchema()
    new_application = schema.load(applicationDetails, session=db.session)
    new_application.lastUpdated = ModelTools.get_utc_timestamp()
    db.session.add(new_application)
    db.session.commit()

    schema = ExtendedApplicationSchema()
    data = schema.dump(new_application)
    logger.debug("application data:")
    logger.debug(pformat(data))
    return data, 201


def update(oid, applicationDetails):
    """
    This function updates an existing application in the application list

    :param id: id of the application to update in the application list
    :param application:   application to update
    :return: updated application
    """

    logger.debug("application: ")
    logger.debug(pformat(applicationDetails))

    # Does the application exist in applications?
    existing_application = (
        db.session.query(Application).filter(Application.id == oid).one_or_none()
    )

    # Does application exist?
    if existing_application is not None:
        schema = ApplicationSchema()
        applicationDetails['id'] = oid
        schema.load(applicationDetails, session=db.session)
        db.session.merge(existing_application)
        db.session.commit()

        # return the updated application in the response
        schema = ExtendedApplicationSchema()
        data = schema.dump(existing_application)
        return data, 200

    # otherwise, nope, application doesn't exist, so that's an error
    else:
        db.session.close()
        abort(404, f"Application {oid} not found")


def delete(oid):
    """
    Deletes an application from the application list.

    :param id: id of the application to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the application to delete exist?
    existing_application = (
        db.session.query(Application).filter(Application.id == oid).one_or_none()
    )

    # if found?
    if existing_application is not None:
        existing_application.isActive = False
        db.session.merge(existing_application)
        db.session.commit()

        return make_response(f"Application id {oid} successfully deleted", 200)

    # Otherwise, nope, application to delete not found
    else:
        db.session.close()
        abort(404, f"Application id {oid} not found")
