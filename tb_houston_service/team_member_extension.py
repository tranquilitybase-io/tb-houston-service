import logging

from config import db
from models import Team, User
from tb_houston_service.team_extension import expand_team

logger = logging.getLogger("tb_houston_service.teammember")


def expand_team_member(a_team_member):
    logger.debug("team_member: %s", a_team_member)

    if a_team_member == None:
        return None

    tm = db.session.query(Team).filter(Team.id == a_team_member.teamId).one_or_none()
    a_team_member.team = expand_team(tm)

    ur = db.session.query(User).filter(User.id == a_team_member.userId).one_or_none()
    a_team_member.user = ur

    return a_team_member
