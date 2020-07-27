import logging 
from tb_houston_service.models import User, CloudRole
from config import db

logger = logging.getLogger("tb_houston_service.userCloudRole_extension")

def expand_user_cloud_role(a_user_cloud_role):
    logger.debug("a_user_cloud_role: %s", a_user_cloud_role)

    if a_user_cloud_role == None:
        return None

    user = db.session.query(User).filter(User.id == a_user_cloud_role.userId).one_or_none()
    a_user_cloud_role.user = user

    cloudRole = db.session.query(CloudRole).filter(CloudRole.id == a_user_cloud_role.cloudRoleId).one_or_none()
    a_user_cloud_role.cloudRole = cloudRole

    return a_user_cloud_role
