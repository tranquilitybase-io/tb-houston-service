"""
This is the solution resource JSON module and supports all the ReST actions for the
solution resource JSON collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import SolutionResourceJSON, SolutionResourceJSONSchema
import solutionresource
import json
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/solutionresourcejsons
    with the complete lists of solutionresourcejsons

    :return:        json string of list of solutionresourcejsons
    """

    # Create the list of solutionresourcejsons from our data
    solutionresourcejson = SolutionResourceJSON.query.order_by(SolutionResourceJSON.solutionId).all()
    app.logger.debug(pformat(solutionresourcejson))
    # Serialize the data for the response
    solutionresourcejson_schema = SolutionResourceJSONSchema(many=True)
    data = solutionresourcejson_schema.dump(solutionresourcejson)
    return data, 200


def read_one(solutionId):
    """
    This function responds to a request for /api/solutionresourcejson/{oid}
    with one matching solutionresourcejson from solutionresourcejsons

    :param application:   id of solutionresourcejson to find
    :return:              solutionresourcejson matching id
    """

    solutionresourcejson = (SolutionResourceJSON.query.filter(SolutionResourceJSON.solutionId == solutionId).one_or_none())

    if solutionresourcejson is not None:
        # Serialize the data for the response
        solutionresourcejson_schema = SolutionResourceJSONSchema()
        data = solutionresourcejson_schema.dump(solutionresourcejson)
        return data, 200
    else:
        abort(404, f"SolutionResourceJSON with solution id {solutionId} not found")


def create_solution_resources(resources_dict):
    print("resources_dict")
    print(pformat(resources_dict))
    solutionId = resources_dict['solutionId']
    resources_json = json.loads(resources_dict['json'])
    if 'resources' in resources_json:
        for resource in resources_json['resources']:
            if 'instances' in resource:
                for instance in resource['instances']:
                    if 'attributes' in instance:
                        attributes = instance['attributes']
                        if 'project_id' in attributes:
                            project_id = attributes['project_id']
                            proj_parts = project_id.split('-')
                            if len(proj_parts) > 1:
                              env = proj_parts[1]
                              key = "project_id_" + env
                              value = project_id
                              sr = {
                                      'solutionId': solutionId,
                                      'key': key,
                                      'value': value 
                                      }
                              solutionresource.create(sr)


def create(solutionResourceJSONDetails):
    """
    This function updates an existing or creates a solutionresource json in the solution resource json list

    :param key:    solutionId and key of the solutionresource json to update in the solution resource json  list
    :param solutionresourcejson:   solutionresourcejson to update
    :return:       updated solutionresourcejson
    """

    app.logger.debug(pformat(solutionResourceJSONDetails))

    solutionId = solutionResourceJSONDetails['solutionId']

    print(f"update_or_create {solutionId}")

    # Does the solutionresource exist in solutionresource list?
    solutionresourcejson_filter = SolutionResourceJSON.query.filter(SolutionResourceJSON.solutionId == solutionId)
    solutionresourcejson = solutionresourcejson_filter.one_or_none()

    schema = SolutionResourceJSONSchema()
    # Does the solution resource json exist?
    if solutionresourcejson is not None:
        print(f"Update: {solutionresourcejson.solutionId}")
        solutionresourcejson_filter.update(solutionResourceJSONDetails)
        db.session.commit()
    else:
        solutionresourcejson = schema.load(solutionResourceJSONDetails, session=db.session)
        db.session.add(solutionresourcejson)
        db.session.commit()

    # return the updated/created object in the response
    data = schema.dump(solutionresourcejson)
    print(pformat(data))
    create_solution_resources(data)
    return data, 201


def delete(solutionId):
    """Deletes a solutionresourcejson from the solutionresourcejsons list.
    :param solutionId: solutionId of the solutionresourcejson to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solutionresourcejson to delete exist?
    existing_solutionresourcejson = SolutionResourceJSON.query.filter(SolutionResourceJSON.solutionId == solutionId).one_or_none()

    # if found?
    if existing_solutionresourcejson is not None:
        db.session.delete(existing_solutionresourcejson)
        db.session.commit()

        return make_response(f"SolutionResourceJSON {solutionId} successfully deleted", 200)

    # Otherwise, nope, solutionresourcejson to delete not found
    else:
        abort(404, f"SolutionResourceJSON {solutionId} not found")


