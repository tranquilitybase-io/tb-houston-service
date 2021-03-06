"""
This is the deployments module and supports all the ReST actions for the
businessunit collection
"""
from pprint import pformat

from flask import abort, make_response

from config import app, db
from models import BusinessUnit, BusinessUnitSchema


def read_all():
    """
    Responds to a request for /api/businessunit
    with the complete lists of BusinessUnits

    :return:        json string of list of BusinessUnits
    """
    # Create the list of BusinessUnits from our data
    businessUnit = db.session.query(BusinessUnit).order_by(BusinessUnit.id).all()
    app.logger.debug(pformat(businessUnit))
    # Serialize the data for the response
    businessUnit_schema = BusinessUnitSchema(many=True)
    data = businessUnit_schema.dump(businessUnit)
    app.logger.debug(data)
    return data, 200


def read_keyvalues():
    """
    Responds to a request for /api/keyValues/businessUnit
    with the complete lists of BusinessUnits
    :return:        json string of list of key value pairs
    """
    # Create the list of BusinessUnits from our data
    businessUnit = db.session.query(BusinessUnit).order_by(BusinessUnit.id).all()
    app.logger.debug(pformat(businessUnit))
    # Serialize the data for the response
    businessUnit_schema = BusinessUnitSchema(many=True)
    data = businessUnit_schema.dump(businessUnit)
    app.logger.debug(data)
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = str(d.get("name"))
        keyValuePair["value"] = d.get("name")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues


def read_keyValues():
    """
    Responds to a request for /api/keyValues/businessUnit
    with the complete lists of BusinessUnits
    :return:        json string of list of key value pairs
    """
    # Create the list of BusinessUnits from our data
    businessUnit = db.session.query(BusinessUnit).order_by(BusinessUnit.id).all()
    app.logger.debug(pformat(businessUnit))
    # Serialize the data for the response
    businessUnit_schema = BusinessUnitSchema(many=True)
    data = businessUnit_schema.dump(businessUnit)
    app.logger.debug(data)
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = d.get("id")
        keyValuePair["value"] = d.get("name")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues


def read_one(oid):
    """
    Responds to a request for /api/businessunit/{id}
    with one matching businessUnit from BusinessUnits

    :param application:   id of businessUnit to find
    :return:              businessUnit matching id
    """
    businessUnit = (
        db.session.query(BusinessUnit).filter(BusinessUnit.id == oid).one_or_none()
    )

    if businessUnit is not None:
        # Serialize the data for the response
        businessUnit_schema = BusinessUnitSchema()
        data = businessUnit_schema.dump(businessUnit)
        app.logger.debug(data)
        return data, 200
    else:
        abort(404, f"BusinessUnit with id {oid} not found")


def create(businessUnitDetails):
    """
    Creates a new businessUnit in the businessUnit list
    based on the passed in businessUnit data

    :param businessUnit: businessUnit to create in businessUnit structure
    :return:        201 on success, 406 on businessUnit exists
    """
    # Remove id as it's created automatically
    if "id" in businessUnitDetails:
        del businessUnitDetails["id"]

    # Does the cd exist already?
    existing_businessUnit = (
        db.session.query(BusinessUnit)
        .filter(BusinessUnit.name == businessUnitDetails["name"])
        .one_or_none()
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
        abort(
            406, f"BusinessUnit with name {businessUnitDetails['name']} already exists"
        )


def update(oid, businessUnitDetails):
    """
    Updates an existing businessUnit in the businessUnit list

    :param key:    id of the businessUnit to update in the businessUnit list
    :param businessUnit:   businessUnit to update
    :return:       updated businessUnit.
    """
    if businessUnitDetails["id"] != oid:
        abort(400, "id mismatch in path and body")

    # Does the businessUnit exist in businessUnit list?
    existing_businessUnit = (
        db.session.query(BusinessUnit).filter(BusinessUnit.id == oid).one_or_none()
    )

    # Does businessUnit exist?

    if existing_businessUnit is not None:

        schema = BusinessUnitSchema()
        update_businessUnit = schema.load(businessUnitDetails, session=db.session)
        update_businessUnit.id = existing_businessUnit.id

        db.session.merge(update_businessUnit)
        db.session.commit()

        # return the updted deployment in the response
        data = schema.dump(update_businessUnit)
        app.logger.debug(data)
        return data, 200

    # otherwise, nope, businessUnit doesn't exist, so that's an error
    else:
        abort(404, f"BusinessUnit with id {oid} not found")


def delete(oid):
    """
    Deletes a BusinessUnit from the BusinessUnit list.

    :param id: id of the BusinessUnit to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the businessUnit to delete exist?
    existing_businessUnit = (
        db.session.query(BusinessUnit).filter(BusinessUnit.id == oid).one_or_none()
    )

    # if found?
    if existing_businessUnit is not None:
        db.session.delete(existing_businessUnit)
        db.session.commit()

        return make_response(f"BusinessUnit {oid} successfully deleted", 200)

    # Otherwise, nope, businessUnit to delete not found
    else:
        abort(404, f"BusinessUnit with id {oid} not found")
