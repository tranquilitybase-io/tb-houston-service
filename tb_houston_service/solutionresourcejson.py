"""
This is the solution resource JSON module and supports all the ReST actions for the
solution resource JSON collection
"""
import json
from pprint import pformat

from flask import abort, make_response

from config import app, db
from models import SolutionResourceJSON, SolutionResourceJSONSchema
from tb_houston_service import solutionresource


def read_all():
    """
    This function responds to a request for /api/solutionresourcejsons
    with the complete lists of solutionresourcejsons

    :return:        json string of list of solutionresourcejsons
    """
    # Create the list of solutionresourcejsons from our data
    solutionresourcejson = (
        db.session.query(SolutionResourceJSON)
        .order_by(SolutionResourceJSON.solutionId)
        .all()
    )
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
    solutionresourcejson = (
        db.session.query(SolutionResourceJSON)
        .filter(SolutionResourceJSON.solutionId == solutionId)
        .one_or_none()
    )

    if solutionresourcejson is not None:
        # Serialize the data for the response
        solutionresourcejson_schema = SolutionResourceJSONSchema()
        data = solutionresourcejson_schema.dump(solutionresourcejson)
        return data, 200
    else:
        abort(404, f"SolutionResourceJSON with solution id {solutionId} not found")


def create_solution_resources(resources_dict):
    app.logger.debug("resources_dict")
    app.logger.debug(pformat(resources_dict))
    solutionId = resources_dict.get("solutionId")
    resources = json.loads(resources_dict.get("json"))
    value = resources.get("environment_projects").get("value")
    for v in value:
        sr = {}
        env = v.get("labels").get("environment")
        sr["solutionId"] = solutionId
        sr["value"] = v.get("project_id")
        sr["key"] = f"project-id-{env}"
        solutionresource.create(sr)

    # workspace
    ws_proj = resources.get("workspace_project")
    if ws_proj:
        ws_value = ws_proj.get("value")
        wc_project_id_value = ws_value.get("project_id")
        ws = {
            "solutionId": solutionId,
            "key": "project-id-workspace",
            "value": wc_project_id_value,
        }
        solutionresource.create(ws)


def create(solutionResourceJSONDetails):
    """
    This function updates an existing or creates a
    solutionresource json in the solution resource json list

    :param key:    solutionId and key of the solutionresource json
                   to update in the solution resource json  list
    :param solutionresourcejson:   solutionresourcejson to update
    :return:       updated solutionresourcejson
    """
    app.logger.debug(pformat(solutionResourceJSONDetails))

    solutionId = solutionResourceJSONDetails["solutionId"]

    app.logger.debug(f"update_or_create {solutionId}")

    # Does the solutionresource exist in solutionresource list?
    solutionresourcejson_filter = db.session.query(SolutionResourceJSON).filter(
        SolutionResourceJSON.solutionId == solutionId
    )
    solutionresourcejson = solutionresourcejson_filter.one_or_none()

    schema = SolutionResourceJSONSchema()
    # Does the solution resource json exist?
    if solutionresourcejson is not None:
        app.logger.debug(f"Update: {solutionresourcejson.solutionId}")
        solutionresourcejson_filter.update(solutionResourceJSONDetails)
        db.session.commit()
    else:
        solutionresourcejson = schema.load(
            solutionResourceJSONDetails, session=db.session
        )
        db.session.add(solutionresourcejson)
        db.session.commit()

    # return the updated/created object in the response
    data = schema.dump(solutionresourcejson)
    app.logger.debug(pformat(data))
    create_solution_resources(data)
    return data, 201


def delete(solutionId):
    """
    Deletes a solutionresourcejson from the solutionresourcejsons list.
    :param solutionId: solutionId of the solutionresourcejson to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solutionresourcejson to delete exist?
    existing_solutionresourcejson = (
        db.session.query(SolutionResourceJSON)
        .filter(SolutionResourceJSON.solutionId == solutionId)
        .one_or_none()
    )

    # if found?
    if existing_solutionresourcejson is not None:
        db.session.delete(existing_solutionresourcejson)
        db.session.commit()

        return make_response(
            f"SolutionResourceJSON {solutionId} successfully deleted", 200
        )

    # Otherwise, nope, solutionresourcejson to delete not found
    else:
        abort(404, f"SolutionResourceJSON {solutionId} not found")
