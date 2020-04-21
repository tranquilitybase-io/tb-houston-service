"""
Login module - supports all the ReST actions login.
"""

# 3rd party modules
from flask import  abort
from config import app
from pprint import pformat
from models import ModelTools
from models import User
from extendedSchemas import ExtendedUserSchema


def check_credentials(login_details):
    """
    Responds to a request for /api/login.
    :return:        json string of user details
    """

    app.logger.info("Login Details: {}".format(pformat(ModelTools.redact_dict(login_details))))

    username = login_details['username']
    password = login_details['password']

    if (username == 'admin@your.company' and password == 'pass1'):
      user = User.query.filter(User.email == username).one_or_none()
      schema = ExtendedUserSchema(many=False)
      if user is not None:
        app.logger.debug('LOGIN accepted!');
        schema = ExtendedUserSchema(many=False)
        data = schema.dump(user)
        return data, 200

    if (username == 'dev@your.company' and password == 'pass2'):
      user = User.query.filter(User.email == username).one_or_none()
      if user is not None:
        app.logger.debug('LOGIN accepted!');
        schema = ExtendedUserSchema(many=False)
        data = schema.dump(user)
        return data, 200

    app.logger.warning('LOGIN FAILED!');
    abort(
      401, "Unauthorised! {}".format(ModelTools.redact_dict(login_details))
    )
