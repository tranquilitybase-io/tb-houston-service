"""
This is the deployments module and supports all the ReST actions for the
businessunit collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import BusinessUnit, BusinessUnitSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/businessunit
    with the complete lists of BusinessUnits 

    :return:        json string of list of BusinessUnits 
    """

    # Create the list of BusinessUnits from our data
    businessUnit = BusinessUnit.query.order_by(BusinessUnit.key).all()
    app.logger.debug(pformat(businessUnit))
    # Serialize the data for the response
    businessUnit_schema = BusinessUnitSchema(many=True)
    data = businessUnit_schema.dump(businessUnit)
    app.logger.debug(data)
    return data


def read_one(key):
    """
    This function responds to a request for /api/businessunit/{key}
    with one matching businessUnit from BusinessUnits 

    :param application:   key of businessUnit to find
    :return:              businessUnit matching key
    """

    businessUnit = (BusinessUnit.query.filter(BusinessUnit.key == key).one_or_none())

    if businessUnit is not None:
        # Serialize the data for the response
        businessUnit_schema = BusinessUnitSchema()
        data = businessUnit_schema.dump(businessUnit)
        app.logger.debug(data)
        return data
    else:
        abort(
            404, "BusinessUnit with key {key} not found".format(key=key)
        )


def create(businessUnitDetails):
    """
    This function creates a new businessUnit in the businessUnit list
    based on the passed in businessUnit data

    :param businessUnit: businessUnit to create in businessUnit structure
    :return:        201 on success, 406 on businessUnit exists
    """
    key = businessUnitDetails.get("key", None)
    value = businessUnitDetails.get("value", None)

    # Does the cd exist already?
    existing_businessUnit = (
        BusinessUnit.query.filter(BusinessUnit.key == key).one_or_none()
    )

    if existing_businessUnit is None:
        schema = BusinessUnitSchema()
        new_businessUnit = schema.load(businessUnitDetails, session=db.session)
        db.session.add(new_businessUnit)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_businessUnit)
        app.logger.debug(data)
        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"BusinessUnit already exists")


def update(key, businessUnitDetails):
    """
    This function updates an existing businessUnit in the businessUnit list

    :param key:    key of the businessUnit to update in the businessUnit list
    :param businessUnit:   businessUnit to update
    :return:       updated businessUnit
    """

    if businessUnitDetails["key"] != key:
           abort(400, f"Key mismatch in path and body")

    # Does the businessUnit exist in businessUnit list?
    existing_businessUnit = BusinessUnit.query.filter(
            BusinessUnit.key == key
    ).one_or_none()

    # Does businessUnit exist?

    if existing_businessUnit is not None:

        schema = BusinessUnitSchema()
        update_businessUnit = schema.load(businessUnitDetails, session=db.session)
        update_businessUnit.key = existing_businessUnit.key

        db.session.merge(update_businessUnit)
        db.session.commit()

        # return the updted deployment in the response
        data = schema.dump(update_businessUnit)
        app.logger.debug(data)
        return data, 200

    # otherwise, nope, businessUnit doesn't exist, so that's an error
    else:
        abort(404, f"BusinessUnit not found")


def delete(key):
    """
    Deletes a BusinessUnit from the BusinessUnit list.

    :param key: key of the BusinessUnit to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the businessUnit to delete exist?
    existing_businessUnit = BusinessUnit.query.filter(BusinessUnit.key == key).one_or_none()

    # if found?
    if existing_businessUnit is not None:
        db.session.delete(existing_businessUnit)
        db.session.commit()

        return make_response(f"BusinessUnit {key} successfully deleted", 200)

    # Otherwise, nope, businessUnit to delete not found
    else:
        abort(404, f"BusinessUnit {key} not found")


