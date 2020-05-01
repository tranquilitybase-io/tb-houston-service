"""
This is the solution resource JSON module and supports all the ReST actions for the
solution resource JSON collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import SolutionResourceJSON, SolutionResourceJSONSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/solutionresourcejsons
    with the complete lists of solutionresourcejsons

    :return:        json string of list of solutionresourcejsons
    """

    # Create the list of solutionresourcejsons from our data
    solutionresourcejson = SolutionResourceJSON.query.order_by(SolutionResourceJSON.key).all()
    app.logger.debug(pformat(solutionresourcejson))
    # Serialize the data for the response
    solutionresourcejson_schema = SolutionResourceJSONSchema(many=True)
    data = solutionresourcejson_schema.dump(solutionresourcejson)
    return data, 200


def read_one(oid):
    """
    This function responds to a request for /api/solutionresourcejson/{oid}
    with one matching solutionresourcejson from solutionresourcejsons

    :param application:   id of solutionresourcejson to find
    :return:              solutionresourcejson matching key
    """

    solutionresourcejson = (SolutionResourceJSON.query.filter(SolutionResourceJSON.id == oid).one_or_none())

    if solutionresourcejson is not None:
        # Serialize the data for the response
        solutionresourcejson_schema = SolutionResourceJSONSchema()
        data = solutionresourcejson_schema.dump(solutionresourcejson)
        return data, 200
    else:
        abort(404, f"SolutionResourceJSON with id {oid} not found")


def create(solutionResourceJSONDetails):
    """
    This function creates a new solutionresourcejson in the solutionresourcejson list
    based on the passed in solutionresourcejson data

    :param solutionresourcejson:  solutionresourcejson to create in solutionresourcejson structure
    :return:        201 on success, 406 on solutionresourcejson exists
    """

    # Remove id as it's created automatically
    if 'id' in solutionResourceJSONDetails:
        del solutionResourceJSONDetails['id']

    schema = SolutionResourceJSONSchema()
    new_solutionresourcejson = schema.load(solutionResourceJSONDetails, session=db.session)
    db.session.add(new_solutionresourcejson)
    db.session.commit()

    # Serialize and return the newly created solution resource JSON
    # in the response
    data = schema.dump(new_solutionresourcejson)
    return data, 201


def update(oid, solutionResourceJSONDetails):
    """
    This function updates an existing solutionresourcejson in the solution resource JSON list

    :param key:    key of the solutionresourcejson to update in the solution resource JSON list
    :param solutionresourcejson:   solutionresourcejson to update
    :return:       updated solutionresourcejson
    """

    app.logger.debug(pformat(solutionResourceJSONDetails))

    if solutionResourceJSONDetails.get("id", oid) != oid:
           abort(400, f"Key mismatch in path and body")

    # Does the solutionresourcejson exist in solutionresourcejson list?
    existing_solutionresourcejson = SolutionResourceJSON.query.filter(
            SolutionResourceJSON.id == oid
    ).one_or_none()

    # Does the solution resource JSON exist?

    if existing_solutionresourcejson is not None:
        SolutionResourceJSON.query.filter(SolutionResourceJSON.id == oid).update(solutionResourceJSONDetails)
        db.session.commit()

        # return the updated the solution resource JSON in the response
        schema = SolutionResourceJSONSchema()
        data = schema.dump(existing_solutionresourcejson)
        return data, 200
    else:
        abort(404, f"SolutionResourceJSON {oid} not found")


def delete(oid):
    """
    Deletes a solutionresourcejson from the solutionresourcejsons list.

    :param key: key of the solutionresourcejson to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solutionresourcejson to delete exist?
    existing_solutionresourcejson = SolutionResourceJSON.query.filter(SolutionResourceJSON.id == oid).one_or_none()

    # if found?
    if existing_solutionresourcejson is not None:
        db.session.delete(existing_solutionresourcejson)
        db.session.commit()

        return make_response(f"SolutionResourceJSON {oid} successfully deleted", 200)

    # Otherwise, nope, solutionresourcejson to delete not found
    else:
        abort(404, f"SolutionResourceJSON {oid} not found")
