import logging 
from tb_houston_service.models import Team, TeamMember, Role
from tb_houston_service import team_member_extension
from config import db

logger = logging.getLogger("tb_houston_service.teammember")

def expand_user(a_user):
    if a_user:                
        team_count = db.session.query(TeamMember).filter(TeamMember.userId == a_user.id, TeamMember.isActive).count()
        a_user.teamCount = team_count
    return a_user


def expand_team_member(a_team_member):
    # This function is similar to the one in team_member_extension.py but without the user object,
    # it's not required when we expand a user with the teams he's a member of: expand_user_with_teams.
    logger.debug("expand_team_member: %s", a_team_member)

    if a_team_member == None:
        return None

    role = db.session.query(Role).filter(Role.id == a_team_member.roleId).one_or_none()

    if role:
        a_team_member.role = role

    tm = db.session.query(Team).filter(Team.id == a_team_member.teamId).one_or_none()
    a_team_member.team = team_member_extension.expand_team(tm)

    return a_team_member


def expand_user_with_teams(a_user):
    logger.debug("expand_user_with_teams: %s", a_user)
    if a_user:         
        a_user.teamMembers = db.session.query(TeamMember).filter(TeamMember.userId == a_user.id, TeamMember.isActive).all()
        for tm in a_user.teamMembers:
            expand_team_member(tm)
            print(tm)
    return a_user