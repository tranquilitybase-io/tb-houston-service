"""
This is the application settings module to enable dev user to change application settings
"""
import logging
from pprint import pformat

from flask import abort

from config import db
from models.application_settings import ApplicationSettings, ApplicationSettingsSchema

logger = logging.getLogger("tb_houston_service.application_settings")


def create_default_settings(dbs, application_id, variables, isOptional):
    schema = ApplicationSettingsSchema()
    for variable in variables or ():
        var_details = {
            "applicationId": application_id,
            "name": variable["name"],
            "type": variable["type"],
        }
    if "value" in variable:
        var_details["value"] = variable["value"]
    else:
        var_details["value"] = ""

    var_details["isOptional"] = isOptional
    app_settings = schema.load(var_details, session=dbs)
    dbs.add(app_settings)
    dbs.flush()
    return False


def create_application_settings(appSettings):
    if appSettings is not None:
        schema = ApplicationSettingsSchema()
        new_entry = {
            "applicationId": appSettings["application_id"],
            "name": appSettings["name"],
            "type": appSettings["type"],
            "value": appSettings["value"],
            "isOptional": 0,
        }
        new_application_settings = schema.load(new_entry, session=db.session)
        db.session.add(new_application_settings)
        db.session.commit()
        data = schema.dump(new_application_settings)
        return data, 201

    return abort(409, "System settings already exists")


def update_application_settings(applicatioSettings):
    """
    Updates an existing settings entry in the system settings.

    :param: ApplicationSettings object to update current/default settings
    :return:       updated settings
    """
    a: ApplicationSettings = (
        db.session.query(ApplicationSettings)
        .filter(ApplicationSettings.applicaitonId == applicatioSettings.applicationId)
        .one_or_none()
    )
    if a is not None:
        a.name = applicatioSettings.name
        a.type = applicatioSettings.type
        a.value = applicatioSettings.value
        db.session.merge(a)
        db.session.commit()
        # Serialize the data for the response
        rs = ApplicationSettingsSchema()
        data = rs.dump(a)
        return data, 200
    return abort(404, "Application settings not found")


def delete_application_settings(applicationId):
    """
    Deletes a Application Settings from list.

    :return:    200 on successful delete, 404 if not found
    """
    a: ApplicationSettings = (
        db.session.query(ApplicationSettings)
        .filter(ApplicationSettings.applicaitonId == applicationId)
        .one_or_none()
    )
    if a is not None:
        db.session.delete()
        db.session.commit()

        return "", 204

    return abort(404, "Application settings not found.")


def read_all_application_settings():
    """
    Return all Application Settings
    :return: List of App Settings
    """
    a = db.session.query(ApplicationSettings).order_by(ApplicationSettings.id).all()
    logger.debug(pformat(a))
    # Serialize the data for the response
    app_schema = ApplicationSettingsSchema()
    data = app_schema.dump(ApplicationSettings)
    logger.debug(data)
    return data, 200


def read_one_application_settings(applicationId):
    """
    Return application settings for appId = 'applicationId'
    :return: ApplicationSettings -> applicationId
    """
    a: ApplicationSettings = (
        db.session.query(ApplicationSettings)
        .filter(ApplicationSettings.applicaitonId == applicationId)
        .one_or_none()
    )
    if a is not None:
        rs = ApplicationSettingsSchema()
        data = rs.dump(a)

        return data, 200

    return abort(404, "Application settings not found!")
