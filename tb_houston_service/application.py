"""
This is the application module and supports all the ReST actions for the
application collection
"""
import logging
from pprint import pformat

from flask import abort, make_response
from sqlalchemy import literal_column
from sqlalchemy.exc import SQLAlchemyError

from config import db
from config.db_lib import db_session
from models import Activator, Application, ApplicationSchema, ActivatorMetadataVariable
from tb_houston_service import application_extension, security, application_settings
from tb_houston_service.extendedSchemas import ExtendedApplicationSchema
from tb_houston_service.tools import ModelTools

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
    logger.debug(
        "read_all::Parameters: isActive: %s, isFavourite: %s, status: %s, activatorId: %s, environment: %s, page: %s, page_size: %s, sort: %s",
        isActive,
        isFavourite,
        status,
        activatorId,
        environment,
        page,
        page_size,
        sort,
    )
    # Create the list of applications from our data
    # pre-process sort instructions

    with db_session() as dbs:
        if sort is None:
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
                application_query = dbs.query(Application).order_by(Application.id)

        # filter activators by logged in user
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)

        application_query = application_query.filter(
            Activator.id == Application.activatorId,
            (status is None or Application.status == status),
            (activatorId is None or Application.activatorId == activatorId),
            (environment is None or Application.env == environment),
            (isActive is None or Application.isActive == isActive),
            (isFavourite is None or Application.isFavourite == isFavourite),
            (
                    business_unit_ids is None
                    or Activator.businessUnitId.in_(business_unit_ids)
            ),
        )

        if page is None or page_size is None:
            applications = application_query.all()
        else:
            applications = (
                application_query.limit(page_size).offset(page * page_size).all()
            )

        for app in applications:
            application_extension.expand_application(app, dbsession=dbs)

        # Serialize the data for the response
        application_schema = ExtendedApplicationSchema(many=True)
        data = application_schema.dump(applications)
        logger.debug("read_all::application data:")
        logger.debug(pformat(data))
        return data


def read_one(oid):
    """
    This function responds to a request for /api/application/{oid}
    with one matching application from applications

    :param application:   id of the application to find
    :return:              application matching the id
    """
    with db_session() as dbs:
        # filter activators by logged in user
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
        application = (
            dbs.query(Application)
                .filter(
                Application.id == oid,
                Activator.id == Application.activatorId,
                (
                        business_unit_ids is None
                        or Activator.businessUnitId.in_(business_unit_ids)
                ),
            )
                .one_or_none()
        )

        logger.debug("application data:")
        logger.debug(pformat(application))

        if application is not None:
            application = application_extension.expand_application(
                application, dbsession=dbs
            )
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
    logger.debug("create: %s", applicationDetails)
    with db_session() as dbs:
        # Remove id as it's created automatically
        if "id" in applicationDetails:
            del applicationDetails["id"]

        # Validate the business unit
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
        if business_unit_ids:
            activator = (
                dbs.query(Activator)
                    .filter(Activator.id == applicationDetails.get("activatorId"))
                    .one_or_none()
            )
            business_unit = activator.businessUnitId
            if business_unit not in business_unit_ids:
                abort(
                    400,
                    f"Unauthorized to create applications for business unit {business_unit}",
                )
        else:
            # initially will let this pass, but in future we could abort if user is
            # not a member of any business units
            pass

        schema = ApplicationSchema()
        new_application = schema.load(applicationDetails, session=dbs)
        new_application.lastUpdated = ModelTools.get_utc_timestamp()
        dbs.add(new_application)
        dbs.commit()
        # Call create default application settings
        activator_variables = (dbs.query(ActivatorMetadataVariable)
                               .filter(Activator.id == activator.id)
                               .one_or_none())
        application_settings.create_default_settings(dbs, new_application.id, activator_variables, False)

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
    logger.debug("update: %s", applicationDetails)

    with db_session() as dbs:
        logger.debug("application: ")
        logger.debug(pformat(applicationDetails))

        # Does the application exist in applications?
        existing_application = (
            dbs.query(Application).filter(Application.id == oid).one_or_none()
        )

        # Does application exist?
        if existing_application is not None:
            # Validate the business unit
            business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
            if business_unit_ids:
                activator = (
                    dbs.query(Activator)
                        .filter(Activator.id == applicationDetails.get("activatorId"))
                        .one_or_none()
                )
                business_unit = activator.businessUnitId
                if business_unit and business_unit not in business_unit_ids:
                    abort(
                        400,
                        f"Unauthorized to update solutions for business unit {business_unit}",
                    )
            else:
                # initially will let this pass, but in future we could abort if user is
                # not a member of any business units
                pass

            schema = ApplicationSchema()
            applicationDetails["id"] = oid
            schema.load(applicationDetails, session=db.session)
            dbs.merge(existing_application)
            dbs.commit()

            # return the updated application in the response
            schema = ExtendedApplicationSchema()
            data = schema.dump(existing_application)
            return data, 200

        # otherwise, nope, application doesn't exist, so that's an error
        else:
            abort(404, f"Application {oid} not found")


def delete(oid):
    """
    Deletes an application from the application list.

    :param id: id of the application to delete
    :return:             200 on successful delete, 404 if not found
    """
    with db_session() as dbs:
        # Does the application to delete exist?
        existing_application = (
            dbs.query(Application).filter(Application.id == oid).one_or_none()
        )

        # if found?
        if existing_application is not None:

            # Validate the business unit
            business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
            if business_unit_ids:
                activator = (
                    dbs.query(Activator)
                        .filter(Activator.id == existing_application.activatorId)
                        .one_or_none()
                )
                business_unit = activator.businessUnitId
                if business_unit and business_unit not in business_unit_ids:
                    abort(
                        400,
                        f"Unauthorized to delete applications for business unit {business_unit}",
                    )
            else:
                # initially will let this pass, but in future we could abort if user is
                # not a member of any business units
                pass

            existing_application.isActive = False
            dbs.merge(existing_application)
            dbs.commit()

            return make_response(f"Application id {oid} successfully deleted", 200)

        # Otherwise, nope, application to delete not found
        else:
            abort(404, f"Application id {oid} not found")
