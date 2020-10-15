"""
Login module - supports all the ReST actions login.
"""
import os
import logging
from pprint import pformat
from http import HTTPStatus
import connexion
from flask import abort

from config import db
from config.db_lib import db_session
from models import User, UserSchema
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedLoginSchema
from tb_houston_service import team
from tb_houston_service import security

logger = logging.getLogger("login")

pw_backup = "eaglehaslanded"

def check_credentials(login_details):
    """
    Responds to a request for /api/login.
    :return:        json string of user details
    """
    authorization = connexion.request.headers.get('Authorization')

    if authorization:
        logger.debug("Authorization: %s", authorization)
        token = authorization.split(' ')[1]
        claims = security.decode_token(token)
        logger.debug("Claims: %s", claims)      

        existing_user = (
            db.session.query(User)
            .filter(User.email == claims.get("email"))
            .one_or_none()
        )
        if not existing_user:
            userDetails = {

                "email": claims.get("email"),
                "firstName": claims.get("given_name"),
                "lastName": claims.get("family_name")
            }

            with db_session() as dbs:
                schema = UserSchema()
                new_user = schema.load(userDetails, session=dbs)
                dbs.add(new_user)                
        login_details['username'] = claims.get("email")
        login_details['password'] = os.environ.get("EC_PASSWORD", pw_backup)


    logger.info(
        "Login Details: {}".format(pformat(ModelTools.redact_dict(login_details)))
    )

    username = login_details.get("username")
    password = login_details.get("password")

    is_active_user = False
    with db_session() as dbs:
        user = dbs.query(User).filter(User.email == username, User.isActive).one_or_none()
        if user:
            is_active_user = True

        is_valid_password = False
        if os.environ.get("EC_PASSWORD", pw_backup) == password:
            is_valid_password = True

        schema = ExtendedLoginSchema(many=False)
        if is_active_user and is_valid_password:
            logger.debug("LOGIN accepted!")
            teams_resp = team.read_list_by_user_id(user.id)
            if teams_resp[1] == HTTPStatus.OK:
                user.teams = teams_resp[0]
            else:
                logger.info("No teams found for user {user.id}")
            data = schema.dump(user)
            return data, 200

    logger.warning("LOGIN FAILED!")
    abort(401, "Unauthorised! {}".format(ModelTools.redact_dict(login_details)))
