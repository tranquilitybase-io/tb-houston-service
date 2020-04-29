"""
This is the solution resource module and supports all the ReST actions for the
solution resource collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import SolutionResource, SolutionResourceSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/solutionresources
    with the complete lists of solutionresources

    :return:        json string of list of solutionresources
    """

    # Create the list of solutionresources from our data
    solutionresource = SolutionResource.query.order_by(SolutionResource.key).all()
    app.logger.debug(pformat(solutionresource))
    # Serialize the data for the response
    solutionresource_schema = SolutionResourceSchema(many=True)
    data = solutionresource_schema.dump(solutionresource)
    return data, 200


def read_one(oid):
    """
    This function responds to a request for /api/solutionresource/{oid}
    with one matching solutionresource from solutionresources

    :param application:   id of solutionresource to find
    :return:              solutionresource matching key
    """

    solutionresource = (SolutionResource.query.filter(SolutionResource.id == oid).one_or_none())

    if solutionresource is not None:
        # Serialize the data for the response
        solutionresource_schema = SolutionResourceSchema()
        data = solutionresource_schema.dump(solutionresource)
        return data, 200
    else:
        abort(404, f"SolutionResource with id {oid} not found")


def create(solutionResourceDetails):
    """
    This function creates a new solutionresource in the solutionresource list
    based on the passed in solutionresource data

    :param solutionresource:  solutionresource to create in solutionresource structure
    :return:        201 on success, 406 on solutionresource exists
    """

    # Remove id as it's created automatically
    if 'id' in solutionResourceDetails:
        del solutionResourceDetails['id']

    schema = SolutionResourceSchema()
    new_solutionresource = schema.load(solutionResourceDetails, session=db.session)
    db.session.add(new_solutionresource)
    db.session.commit()

    # Serialize and return the newly created solution resource
    # in the response
    data = schema.dump(new_solutionresource)
    return data, 201


def update(oid, solutionResourceDetails):
    """
    This function updates an existing solutionresource in the solution resource list

    :param key:    key of the solutionresource to update in the solution resource list
    :param solutionresource:   solutionresource to update
    :return:       updated solutionresource
    """

    app.logger.debug(pformat(solutionResourceDetails))

    if solutionResourceDetails.get("id", oid) != oid:
           abort(400, f"Key mismatch in path and body")

    # Does the solutionresource exist in solutionresource list?
    existing_solutionresource = SolutionResource.query.filter(
            SolutionResource.id == oid
    ).one_or_none()

    # Does the solution resource exist?

    if existing_solutionresource is not None:
        SolutionResource.query.filter(SolutionResource.id == oid).update(solutionResourceDetails)
        db.session.commit()

        # return the updated the solution resource in the response
        schema = SolutionResourceSchema()
        data = schema.dump(existing_solutionresource)
        return data, 200
    else:
        abort(404, f"SolutionResource {oid} not found")


def delete(oid):
    """
    Deletes a solutionresource from the solutionresources list.

    :param key: key of the solutionresource to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solutionresource to delete exist?
    existing_solutionresource = SolutionResource.query.filter(SolutionResource.id == oid).one_or_none()

    # if found?
    if existing_solutionresource is not None:
        db.session.delete(existing_solutionresource)
        db.session.commit()

        return make_response(f"SolutionResource {oid} successfully deleted", 200)

    # Otherwise, nope, solutionresource to delete not found
    else:
        abort(404, f"SolutionResource {oid} not found")


