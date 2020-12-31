"""
deployments module
supports all the ReST actions for the
team collection
"""
from pprint import pformat

from flask import abort, make_response
from sqlalchemy import literal_column

from config import app, db
from models import TeamMember, TeamMemberSchema
from tb_houston_service.extendedSchemas import ExtendedTeamMemberFullSchema
from tb_houston_service.team_member_extension import expand_team_member


def read_all(
    userId=None, teamId=None, active=None, page=None, page_size=None, sort=None
):
    """
    Gets the complete lists of team members
    Responds to a request for /api/teammember

    :return:        json string of list of team members
    """
    # Create the list of team members from our data
    # pre-process sort instructions
    if sort is None:
        teammember_query = db.session.query(TeamMember).order_by(TeamMember.id)

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
            teammember_query = db.session.query(TeamMember).order_by(
                literal_column(", ".join(orderby_arr))
            )
        except Exception as e:
            print(e)
            teammember_query = db.session.query(TeamMember).order_by(TeamMember.id)

    teammember_query = teammember_query.filter(
        (userId is None or TeamMember.userId == userId),
        (teamId is None or TeamMember.teamId == teamId),
        (active is None or TeamMember.isActive == active),
    )

    if page is None or page_size is None:
        teammembers = teammember_query.all()
    else:
        teammembers = teammember_query.limit(page_size).offset(page * page_size).all()

    # Serialize the data for the response
    teammember_schema = TeamMemberSchema(many=True)
    data = teammember_schema.dump(teammembers)
    app.logger.debug("team members data:")
    app.logger.debug(pformat(data))
    return data


def read_all_full_details(
    userId=None, teamId=None, active=None, page=None, page_size=None, sort=None
):
    """
    Gets the complete lists of team members
    Responds to a request for /api/teammember

    :return:        json string of list of team members
    """
    # Create the list of team members from our data
    # pre-process sort instructions
    if sort is None:
        teammember_query = db.session.query(TeamMember).order_by(TeamMember.id)

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
            teammember_query = db.session.query(TeamMember).order_by(
                literal_column(", ".join(orderby_arr))
            )
        except Exception as e:
            print(e)
            teammember_query = db.session.query(TeamMember).order_by(TeamMember.id)

    teammember_query = teammember_query.filter(
        (userId is None or TeamMember.userId == userId),
        (teamId is None or TeamMember.teamId == teamId),
        (active is None or TeamMember.isActive == active),
    )

    if page is None or page_size is None:
        teammembers = teammember_query.all()
    else:
        teammembers = teammember_query.limit(page_size).offset(page * page_size).all()

    # Serialize the data for the response
    for tm in teammembers:
        expand_team_member(tm)
    teammember_schema = ExtendedTeamMemberFullSchema(many=True)
    data = teammember_schema.dump(teammembers)
    app.logger.debug("team members data:")
    app.logger.debug(pformat(data))
    return data


def read_one(oid):
    """
    Responds to a request for /api/teammember/{oid}
    with one matching team from teams

    :param application:   key of team to find
    :return:              team matching key.
    """
    teammember = db.session.query(TeamMember).filter(TeamMember.id == oid).one_or_none()
    if teammember is not None:
        # Serialize the data for the response
        expand_team_member(teammember)
        teammember_schema = ExtendedTeamMemberFullSchema(many=False)
        data = teammember_schema.dump(teammember)
        return data
    else:
        abort(404, f"Team Member with id {oid} not found")


def create(teamMemberDetails):
    """
    Creates a new team in the team list
    based on the passed in team data

    :param team:  team to create in team structure
    :return:        201 on success, 406 on team exists.
    """
    # Remove id as it's created automatically
    if "id" in teamMemberDetails:
        del teamMemberDetails["id"]

    # Does the team member exist already?
    existing_team_member = (
        db.session.query(TeamMember)
        .filter(TeamMember.userId == teamMemberDetails["userId"])
        .filter(TeamMember.teamId == teamMemberDetails["teamId"])
        .one_or_none()
    )

    if existing_team_member is None:
        schema = TeamMemberSchema()
        new_team_member = schema.load(teamMemberDetails, session=db.session)
        db.session.add(new_team_member)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_team_member)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, "Team member already exists")


def update(oid, teamMemberDetails):
    """
    Updates an existing team member in the team list

    :param id:    id of the team to update in the team list
    :param team:   team to update
    :return:       updated team.
    """
    app.logger.debug(pformat(teamMemberDetails))
    if teamMemberDetails["id"] != int(oid):
        abort(400, "Id mismatch in path and body")

    # Does the teammembr exist in teammembers list?
    existing_team_member = (
        db.session.query(TeamMember).filter(TeamMember.id == oid).one_or_none()
    )

    # Does team exist?

    if existing_team_member is not None:
        schema = TeamMemberSchema()
        update_team_member = schema.load(teamMemberDetails, session=db.session)
        update_team_member.id = teamMemberDetails["id"]

        db.session.merge(update_team_member)
        db.session.commit()

        # return the updted team member in the response
        data = schema.dump(update_team_member)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, "Team Member not found")


def delete(oid):
    """
    Logical deletes a team member from the team members list

    :param id: id of the team member to delete
    :return:    200 on successful delete, 404 if not found.
    """
    # Does the team member to delete exist?
    existing_team_member = (
        db.session.query(TeamMember).filter(TeamMember.id == oid).one_or_none()
    )

    # if found?
    if existing_team_member is not None:
        existing_team_member.isActive = False
        db.session.merge(existing_team_member)
        db.session.commit()

        return make_response(f"Team Member {oid} successfully deleted", 200)

    # Otherwise, nope, team member to delete not found
    else:
        abort(404, f"Team Member {oid} not found")
