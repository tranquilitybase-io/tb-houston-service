"""
deployments module
supports all the ReST actions for the
system settings collection
"""
from pprint import pformat

from flask import make_response, abort
from sqlalchemy import text

from config import db, app
from models import Systemsettings, SystemsettingsSchema
from tb_houston_service.extendedSchemas import ExtendedSystemsettingsSchema

def read_one(oid):
    """
    Responds to a request for /api/settings/{oid}.
    with one matching settings from system settings

    :param application:   oid of system settings to find
    :return:              system settings matching oid
    """
    s = db.session.query(Systemsettings).filter(Systemsettings.id == oid).one_or_none()
    if s is not None:
        schema = SystemsettingsSchema()
        data = schema.dump(s)
        return data, 200
    return abort(404, f"System settings with id {oid} not found")


def create(settingsDetails):
    """
    Creates a new settings in the system settings list.
    based on the passed in settings details

    :param systemsettings:  details to create in system settings structure
    :return:        201 on success, 406 on settings exists
    """
    if "id" in settingsDetails:
        del settingsDetails["id"]

    s = db.session.query(Systemsettings).filter(Systemsettings.username == settingsDetails["username"]).one_or_none()

    if s is None:
        schema = SystemsettingsSchema()
        new_entry = schema.load(settingsDetails, session=db.session)

        db.session.add(new_entry)
        db.session.commit()

        data = schema.dump(new_entry)

        return data, 201

    return abort(409, "System settings already exists")


def update(oid, settingsDetails):
    """
    Updates an existing settings entry in the system settings.

    :param id:    oid of the settings to update
    :param settingsDetails:     details to update
    :return:       updated settings
    """
    app.logger.debug(pformat(settingsDetails))
    if settingsDetails.get("id") and settingsDetails.get("id") != oid:
        abort(400, f"Id {oid} mismatch in path and body")

    s = db.session.query(Systemsettings).filter(Systemsettings.id == oid).one_or_none()

    if s is not None:
        settingsDetails['id'] = oid
        schema = SystemsettingsSchema()
        update_settings = schema.load(settingsDetails, session=db.session)

        db.session.merge(update_settings)
        db.session.commit()

        data = schema.dump(update_settings)

        return data, 200

    return abort(404, f"System settings {oid} not found")


def delete(oid):
    """
    Deletes a system settings from list.

    :param id: oid of the system settings to delete
    :return:    200 on successful delete, 404 if not found
    """
    settings_to_del = db.session.query(Systemsettings).filter(Systemsettings.id == oid).one_or_none()

    print(delete_text(oid))

    if settings_to_del is not None:
        db.session.merge(settings_to_del)
        db.session.commit()

        return '', 204

    return abort(404, f"System settings {oid} not found")


def delete_text(oid):
    return db.session.execute(
        text("DELETE FROM systemsettings WHERE id=:param"),
        {"param": oid}
    )


def get_github_credentials(oid):
    settings_schema = ExtendedSystemsettingsSchema()
    s = db.session.query(Systemsettings).filter(Systemsettings.userId == oid).one_or_none()
    if s is None:
        s = {
            "username": "",
            "token": ""
        }
    data = settings_schema.dump(s)
    return data
