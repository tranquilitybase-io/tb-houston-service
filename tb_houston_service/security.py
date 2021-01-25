import logging
import os

import connexion
from google.auth.transport import requests
from google.oauth2 import id_token
from werkzeug.exceptions import Unauthorized

from models import BusinessUnit, Team, TeamMember, User

CLIENT_ID = os.environ.get("CLIENT_ID")

logger = logging.getLogger("tb_houston_service.security")


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
            raise ValueError("CLIENT_ID is not set.")

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
        logger.error("decode_token failed: %s", e)
        raise Unauthorized from e


def get_valid_user_from_token(dbsession):
    """
    Get currently logged in user id.
    :return:        user id
    :return:        None if no valid user id
    """
    authorization = connexion.request.headers.get("Authorization")
    if not authorization:
        return None

    token = authorization.split(" ")[1]

    logger.debug("Authorization: %s", token)
    claims = decode_token(token)
    logger.debug("Claims: %s", claims)

    user = (
        dbsession.query(User)
        .filter(User.email == claims.get("email"), User.isActive)
        .one_or_none()
    )
    return user


def get_business_units_for_user(dbsession):
    business_units = None
    user = get_valid_user_from_token(dbsession)
    logger.debug("user: %s", user)
    if user:
        business_units = (
            dbsession.query(BusinessUnit)
            .filter(
                BusinessUnit.id == Team.businessUnitId,
                TeamMember.teamId == Team.id,
                TeamMember.userId == user.id,
                Team.isActive,
                TeamMember.isActive,
                BusinessUnit.isActive,
            )
            .all()
        )
    logger.debug("business_units: %s", business_units)
    return business_units


def get_business_units_ids_for_user(dbsession):
    business_units = get_business_units_for_user(dbsession)
    business_unit_ids = None
    if business_units:
        business_unit_ids = [bu.id for bu in business_units]
    return business_unit_ids
