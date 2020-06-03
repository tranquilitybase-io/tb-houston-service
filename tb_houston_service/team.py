"""
deployments module
supports all the ReST actions for the
team collection
"""

# 3rd party modules
from pprint import pformat
import json
from http import HTTPStatus
from flask import make_response, abort

from config import db, app
from tb_houston_service.models import Team, TeamMember, TeamSchema
from marshmallow import Schema, fields
from tb_houston_service.extendedSchemas import KeyValueSchema


def read_all():
    """
    Responds to a request for /api/team
    with the complete lists of teams

    :return:        json string of list of teams.
    """

    # Create the list of teams from our data
    teams = db.session.query(Team).order_by(Team.id).all()
    app.logger.debug(pformat(teams))
    # Serialize the data for the response
    team_schema = TeamSchema(many=True)
    data = team_schema.dump(teams)
    return data, 200


def read_one(oid):
    """
    Responds to a request for /api/team/{key}
    with one matching team from teams

    :param application:   key of team to find
    :return:              team matching key
    """

    team = db.session.query(Team).filter(Team.id == oid).one_or_none()

    if team is not None:
        # Serialize the data for the response
        team_schema = TeamSchema()
        data = team_schema.dump(team)
        return data
    return abort(404, f"Team with id {oid} not found")


def create(teamDetails):
    """
    Creates a new team in the team list
    based on the passed in team data

    :param team:  team to create in team structure
    :return:        201 on success, 406 on team exists.
    """
    # Remove id as it's created automatically
    if "id" in teamDetails:
        del teamDetails["id"]
    # Does the team exist already?
    existing_team = (
        db.session.query(Team).filter(Team.name == teamDetails["name"]).one_or_none()
    )

    if existing_team is None:
        schema = TeamSchema(many=False)
        new_team = schema.load(teamDetails, session=db.session)
        app.logger.debug(f"new_team: {new_team} type: {type(new_team)}")
        db.session.add(new_team)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_team)

        return data, 201

    # Otherwise, it already exists, that's an error
    abort(406, "Team already exists")


def update(oid, teamDetails):
    """
    Updates an existing team in the team list

    :param id:    id of the team to update in the team list
    :param team:   team to update
    :return:       updated team.
    """

    app.logger.debug(pformat(teamDetails))

    if teamDetails.get("id") and teamDetails.get("id") != int(oid):
        abort(400, f"Id mismatch in path and body")

    # Does the team exist in team list?
    existing_team = db.session.query(Team).filter(Team.id == oid).one_or_none()

    # Does team exist?

    if existing_team is not None:
        schema = TeamSchema()
        update_team = schema.load(teamDetails, session=db.session)
        update_team.name = teamDetails.get('name', existing_team.name)
        update_team.description = teamDetails.get('description', existing_team.description)
        update_team.businessUnitId = teamDetails.get('businessUnitId', existing_team.businessUnitId)
        update_team.isActive = teamDetails.get('isActive', existing_team.isActive)

        db.session.merge(update_team)
        db.session.commit()

        # return the updted team in the response
        data = schema.dump(update_team)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    abort(404, f"Team not found")


def delete(oid):
    """
    Deletes a team from the teams list

    :param id: id of the team to delete
    :return:    200 on successful delete, 404 if not found.
    """
    # Does the team to delete exist?
    existing_team = db.session.query(Team).filter(Team.id == oid).one_or_none()

    # if found?
    if existing_team is not None:
        existing_team.isActive = False
        db.session.merge(existing_team)
        db.session.commit()

        return make_response(f"Team {oid} successfully deleted", 200)

    # Otherwise, nope, team to delete not found
    abort(404, f"Team {oid} not found")


# Other queries
def read_keyvalues():
    """
    Responds to a request for /api/keyValues/team
    with the complete lists of teams
    :return:        json string of list of teams
    """

    # Create the list of teams from our data
    team = db.session.query(Team).order_by(Team.id).all()
    app.logger.debug(pformat(team))
    # Serialize the data for the response
    team_schema = TeamSchema(many=True)
    data = team_schema.dump(team)
    app.logger.debug(data)
    # Convert the data to keyvalue pairs of id and name column
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = str(d.get("name"))
        keyValuePair["value"] = d.get("name")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues


def read_all_by_user_id(userId):
    teams = (
        db.session.query(Team)
        .filter(
            TeamMember.teamId == Team.id,
            TeamMember.userId == userId,
            Team.isActive,
            TeamMember.isActive,
        )
        .all()
    )

    schema = TeamSchema(many=True)

    # Convert to JSON (Serialization)
    data = schema.dump(teams)
    app.logger.debug(f"{data} type: {type(data)}")
    return data, 200


def read_key_values_by_user_id(userId):
    teams_resp = read_all_by_user_id(userId)
    if teams_resp[1] == HTTPStatus.OK:
        teams_key_values = []
        teams = teams_resp[0]
        for team in teams:
            kv = {}
            kv["key"] = team.get('id')
            kv["value"] = team.get('name')
            teams_key_values.append(kv)

        schema = KeyValueSchema(many=True)

        # Convert to JSON (Serialization)
        data = schema.dump(teams_key_values)
        app.logger.debug(f"{data} type: {type(data)}")
        return data, 200
    else:
        return abort(teams_resp[0], "Error reading key / values by user id.")


def read_list_by_user_id(userId):
    teams_resp = read_all_by_user_id(userId)
    if teams_resp[1] == HTTPStatus.OK:
        teams = teams_resp[0]
        team_list = []
        for team in teams:
            team_list.append(team.get('name'))
        data = team_list
        app.logger.debug(f"{data} type: {type(data)}")
        return data, 200
    else:
        return abort(teams_resp[0], "Error reading key / values by user id.")
