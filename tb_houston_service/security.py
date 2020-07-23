import logging
import os
import six
import connexion
from werkzeug.exceptions import Unauthorized
from google.oauth2 import id_token
from google.auth.transport import requests
from tb_houston_service.models import User
from config.db_lib import db_session
from flask import make_response


CLIENT_ID = os.environ.get("CLIENT_ID")

logger = logging.getLogger("security")

def decode_token(token):
    """
    Args:
        token ([string]): [Authorisation Bearer token]

    Raises:
        ValueError: [Unauthorized]

    Returns:
        [dict]: [oauth claims]
    """

    logger.debug("decode_token: %s", token)
    logger.debug("CLIENT_ID: %s", CLIENT_ID)    
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if not CLIENT_ID:
            raise ValueError('CLIENT_ID is not set.')

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        logger.debug("payload sub: %s", idinfo)
        return idinfo
    except ValueError as e:
        six.raise_from(Unauthorized, e)


def is_active_user(username, dbsession = None):
    dbs = dbsession or db_session()
    user = dbs.query(User).filter(User.email == username, User.isActive).one_or_none()
    return user != None


def get_user_id_from_token(dbsession = None):
    """
    Get currently logged in user id.
    :return:        user id
    :return:        None if no valid user id
    """
    authorization = connexion.request.headers.get('Authorization')
    if authorization:
        logger.debug("Authorization: %s", authorization)
        token = authorization.split(' ')[1]
        claims = decode_token(token)
        logger.debug("Claims: %s", claims)  

        dbs = dbsession or db_session()
        user = dbs.query(User).filter(User.email == claims.get("username"), User.isActive).one_or_none()
        if user:
            return user.id
    return None


def is_valid_token():
    """
    Validate the Authorisation Bearer token, and check user is a valid user.
    :return:        json string of user details
    """
    authorization = connexion.request.headers.get('Authorization')
    if authorization:
        logger.debug("Authorization: %s", authorization)
        token = authorization.split(' ')[1]
        claims = decode_token(token)
        logger.debug("Claims: %s", claims)  

        if is_active_user(claims.get("email")):
            return True
    return False


def validate_token():
    """
    For use when all endpoints require an authorisation bearer token.
    For use by endpoints, except the login endpoint.

    Returns:
        [400]: [Either the token is invalid or the user is inactive.]
    """

    if not is_valid_token():
        return make_response(400, "Access denied")