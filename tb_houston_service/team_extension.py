import logging
from config import db
from tb_houston_service.models import BusinessUnit, TeamMember, User, Role

logger = logging.getLogger("tb_houston_service.solution")


def expand_team(a_team):
    logger.debug("team: %s", a_team)

    if a_team == None:
        return None

    bu = (
        db.session.query(BusinessUnit)
        .filter(BusinessUnit.id == a_team.businessUnitId and BusinessUnit.isActive)
        .one_or_none()
    )

    if bu:
        a_team.businessUnit = bu

    user_count = (
        db.session.query(User)
        .filter(
            TeamMember.teamId == a_team.id,
            TeamMember.userId == User.id,
            a_team.isActive,
            TeamMember.isActive,
            User.isActive,
        )
        .count()
    )
    a_team.userCount = user_count
    return a_team


def expand_team_with_users(a_team):
    bu = (
        db.session.query(BusinessUnit)
        .filter(BusinessUnit.id == a_team.businessUnitId and BusinessUnit.isActive)
        .one_or_none()
    )

    if bu:
        a_team.businessUnit = bu

    users = db.session.query(User).filter(User.isActive).all()
    user_dict = {}
    for u in users:
        user_dict[u.id] = u
    users = db.session.query(User).filter(User.isActive).all()
    user_dict = {}
    for u in users:
        user_dict[u.id] = u

    team_members = (
        db.session.query(TeamMember)
        .filter(
            TeamMember.teamId == a_team.id,
            TeamMember.userId == User.id,
            TeamMember.isActive,
            User.isActive,
        )
        .all()
    )
    for tm in team_members:
        tm.user = user_dict.get(tm.userId)
        role = db.session.query(Role).filter(Role.id == tm.roleId).one_or_none()
        tm.role = role
    a_team.teamMembers = team_members
    return a_team
