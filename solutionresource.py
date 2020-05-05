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
    solutionresource = SolutionResource.query.order_by(SolutionResource.solutionId).all()
    app.logger.debug(pformat(solutionresource))
    # Serialize the data for the response
    solutionresource_schema = SolutionResourceSchema(many=True)
    data = solutionresource_schema.dump(solutionresource)
    return data, 200


def read_one(solutionId, key):
    """
    This function responds to a request for /api/solutionresource/{solutionId}/{key}
    with one matching solutionresource from solutionresources

    :param solutionId, key:   composite key of solutionresource to find
    :return:              solutionresource matching key
    """

    solutionresource = SolutionResource.query.filter(SolutionResource.key == key, SolutionResource.solutionId == solutionId).one_or_none()

    if solutionresource is not None:
        # Serialize the data for the response
        solutionresource_schema = SolutionResourceSchema()
        data = solutionresource_schema.dump(solutionresource)
        return data, 200
    else:
        abort(404, f"SolutionResource with solutionId {solutionId}, key {key} not found")


def create(solutionResourceDetails):
    """
    This function updates an existing or creates a solutionresource in the solution resource list

    :param solutionresource:   solutionresource to create or update
    :return:       updated solutionresource
    """

    app.logger.debug(pformat(solutionResourceDetails))

    solutionId = solutionResourceDetails['solutionId']
    key = solutionResourceDetails['key']

    print("solutionresource:create")
    print(pformat(solutionResourceDetails))

    print(f"solutionId: {solutionId} key: {key}")
    
    # Does the solutionresource exist in solutionresource list?
    solutionresource = SolutionResource.query.filter(SolutionResource.solutionId == solutionId, SolutionResource.key == key).one_or_none()

    schema = SolutionResourceSchema()
    # Does the solution resource exist?
    if solutionresource is not None:
        SolutionResource.query.filter(SolutionResource.key == key, SolutionResource.solutionId == solutionId).update(solutionResourceDetails)
        db.session.commit()
    else:
        solutionresource = schema.load(solutionResourceDetails, session=db.session)
        db.session.add(solutionresource)
        db.session.commit()

    # return the updated/created object in the response
    data = schema.dump(solutionresource)
    print("solutionresource")
    print(pformat(data))
    return data, 201


def delete(solutionId, key):
    """
    Deletes a solutionresource from the solutionresources list.

    :param solutionId, key: composite key of the solutionresource to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solutionresource to delete exist?
    solutionresource = SolutionResource.query.filter(SolutionResource.solutionId == solutionId, SolutionResource.key == key).one_or_none()

    # if found?
    if solutionresource is not None:
        db.session.delete(solutionresource)
        db.session.commit()

        return make_response(f"SolutionResource solutionId: {solutionId} key: {key} successfully deleted", 200)

    # Otherwise, nope, solutionresource to delete not found
    else:
        abort(404, f"SolutionResource solutionId: {solutionId} key: {key} not found")
