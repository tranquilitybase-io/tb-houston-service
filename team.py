"""
deployments module
supports all the ReST actions for the
team collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import Team, TeamSchema
from pprint import pformat


def read_all():
    """
    Responds to a request for /api/team
    with the complete lists of teams

    :return:        json string of list of teams.
    """

    # Create the list of teams from our data
    team = Team.query.order_by(Team.id).all()
    app.logger.debug(pformat(team))
    # Serialize the data for the response
    team_schema = TeamSchema(many=True)
    data = team_schema.dump(team)
    return data


def read_one(id):
    """
    Responds to a request for /api/team/{key}
    with one matching team from teams

    :param application:   key of team to find
    :return:              team matching key
    """

    team = (Team.query.filter(Team.id == id).one_or_none())


    if team is not None:
        # Serialize the data for the response
        team_schema = TeamSchema()
        data = team_schema.dump(team)
        return data
    else:
        abort(
            404, "Team with id {id} not found".format(id=id)
        )

def read_keyvalues():
    """
    Responds to a request for /api/keyValues/team
    with the complete lists of teams
    :return:        json string of list of teams
    """

    # Create the list of teams from our data
    team = Team.query.order_by(Team.id).all()
    app.logger.debug(pformat(team))
    # Serialize the data for the response
    team_schema = TeamSchema(many=True)
    data = team_schema.dump(team)
    app.logger.debug(data)
    # Convert the data to keyvalue pairs of id and name column
    keyValues = []
    for d in data:
        keyValuePair={}
        keyValuePair['key']= str(d.get('name'))
        keyValuePair['value']= d.get('name')
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues

def create(teamDetails):
    """
    Creates a new team in the team list
    based on the passed in team data

    :param team:  team to create in team structure
    :return:        201 on success, 406 on team exists.
    """
    # Remove id as it's created automatically
    if 'id' in teamDetails:
        del teamDetails['id']
    # Does the team exist already?
    existing_team = (
        Team.query.filter(Team.name == teamDetails['name']).one_or_none()
    )

    if existing_team is None:
        schema = TeamSchema()
        new_team = schema.load(teamDetails, session=db.session)
        db.session.add(new_team)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_team)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"Team already exists")


def update(id, teamDetails):
    """
    Updates an existing team in the team list

    :param id:    id of the team to update in the team list
    :param team:   team to update
    :return:       updated team.
    """

    app.logger.debug(pformat(teamDetails))

    if teamDetails["id"] != int(id):
           abort(400, f"Id mismatch in path and body")

    # Does the team exist in team list?
    existing_team = Team.query.filter(
            Team.id == id
    ).one_or_none()

    # Does team exist?

    if existing_team is not None:
        schema = TeamSchema()
        update_team = schema.load(teamDetails, session=db.session)
        update_team.id = teamDetails['id']

        db.session.merge(update_team)
        db.session.commit()

        # return the updted team in the response
        data = schema.dump(update_team)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Team not found")


def delete(id):
    """
    Deletes a team from the teams list

    :param id: id of the team to delete
    :return:    200 on successful delete, 404 if not found.
    """
    # Does the team to delete exist?
    existing_team = Team.query.filter(Team.id == id).one_or_none()

    # if found?
    if existing_team is not None:
        db.session.delete(existing_team)
        db.session.commit()

        return make_response(f"Team {id} successfully deleted", 200)

    # Otherwise, nope, team to delete not found
    else:
        abort(404, f"Team {id} not found")


