"""
deployments module
supports all the ReST actions for the
system settings collection
"""
import logging
from tb_houston_service.tools import ModelTools
from models.system_settings import SystemSettingsResultSchema
from tb_houston_service import security

from flask import abort

from config import db
from models import SystemSettings, SystemSettingsSchema

logger = logging.getLogger("tb_houston_service.systemsettings")

def read_one():
    """
    Responds to a request for /api/settings/.
    with one matching settings from system settings

    :return:              system settings matching user id
    """
    user = security.get_valid_user_from_token(dbsession=db.session)
    logger.debug(f"Logged in user {user}")
    if not (user and user.isAdmin):
        return abort(401, "JWT not valid or user is not an Admin")

    s:SystemSettings = db.session.query(SystemSettings).filter(SystemSettings.userId == user.id).one_or_none()
    if s is not None:
        resultSchema = SystemSettingsResultSchema()
        data = resultSchema.dump(s)

        return data, 200

    return abort(404, "System settings not found")


def create(settingsDetails):
    """
    Creates a new settings in the system settings list.
    based on the passed in settings details

    :param systemsettings:  details to create in system settings structure
    :return:        201 on success, 406 on settings exists
    """
    user = security.get_valid_user_from_token(dbsession=db.session)
    logger.debug(f"Logged in user {user}")
    if not (user and user.isAdmin):
        return abort(401, "JWT not valid or user is not an Admin")

    s:SystemSettings = db.session.query(SystemSettings).filter(SystemSettings.userId == user.id).one_or_none()
    if s is None:
        schema = SystemSettingsSchema()
        new_entry = schema.load(settingsDetails, session=db.session)
        new_entry.userId = user.id

        db.session.add(new_entry)
        db.session.commit()

        resultSchema = SystemSettingsResultSchema()
        data = resultSchema.dump(new_entry)

        return data, 201

    return abort(409, "System settings already exists")


def update(settingsDetails):
    """
    Updates an existing settings entry in the system settings.

    :param settingsDetails:     details to update
    :return:       updated settings
    """
    user = security.get_valid_user_from_token(dbsession=db.session)
    logger.debug(f"Logged in user {user}")
    if not (user and user.isAdmin):
        return abort(401, "JWT not valid or user is not an Admin")

    s:SystemSettings = db.session.query(SystemSettings).filter(SystemSettings.userId == user.id).one_or_none()
    if s is not None:
        s.username = settingsDetails['username']
        s.token = settingsDetails['token']
        s.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(s)
        db.session.commit()

        resultSchema = SystemSettingsResultSchema()
        data = resultSchema.dump(s)

        return data, 200

    return abort(404, "System settings not found")


def delete():
    """
    Deletes a system settings from list.

    :return:    200 on successful delete, 404 if not found
    """
    user = security.get_valid_user_from_token(dbsession=db.session)
    logger.debug(f"Logged in user {user}")
    if not (user and user.isAdmin):
        return abort(401, "JWT not valid or user is not an Admin")

    s:SystemSettings = db.session.query(SystemSettings).filter(SystemSettings.userId == user.id).one_or_none()
    if s is not None:
        db.session.delete(s)
        db.session.commit()

        return '', 204

    return abort(404, "System settings not found")

def get_github_credentials(userId):
    s = db.session.query(SystemSettings).filter(SystemSettings.userId == userId).one_or_none()
    if s is None:
        s = SystemSettings()
        s.username = ''
        s.token = ''
    return s
