"""
Login module - supports all the ReST actions login.
"""

# 3rd party modules
import os
from flask import abort
from config import db, app
from pprint import pformat
from http import HTTPStatus
from tb_houston_service.models import User
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedLoginSchema
from tb_houston_service import team
from config.db_lib import db_session


pw_backup = "eaglehaslanded"

def check_credentials(login_details):
    """
    Responds to a request for /api/login.
    :return:        json string of user details
    """

    app.logger.info(
        "Login Details: {}".format(pformat(ModelTools.redact_dict(login_details)))
    )

    username = login_details["username"]
    password = login_details["password"]

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
            app.logger.debug("LOGIN accepted!")
            teams_resp = team.read_list_by_user_id(user.id)
            if teams_resp[1] == HTTPStatus.OK:
                user.teams = teams_resp[0]
            else:
                app.logger.info("No teams found for user {user.id}")
            data = schema.dump(user)
            return data, 200

    app.logger.warning("LOGIN FAILED!")
    abort(401, "Unauthorised! {}".format(ModelTools.redact_dict(login_details)))
