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
from tb_houston_service.key_utils import _KEY, encrypt, decrypt

K = _KEY.VAL


def read_one(oid):
    """
    Responds to a request for /api/settings/{oid}.
    with one matching settings from system settings

    :param application:   oid of system settings to find
    :return:              system settings matching oid
    """
    s = db.session.query(Systemsettings).filter(Systemsettings.id == oid).one_or_none()
    if s is not None:
        # Serialize the data for the response decrypt token
        if s.token is not None:
            t = bytes(s.token, 'ascii')
            s.token = decrypt(t, K).decode('ascii')
        else:
            raise RuntimeError('Unable to decrypt git access token')
        settings_schema = ExtendedSystemsettingsSchema()
        data = settings_schema.dump(s)
        return data, 200
    return abort(404, f"System settings with id {oid} not found")


def create(settingsDetails):
    """
    Creates a new settings in the system settings list.
    based on the passed in settings details

    :param systemsettings:  details to create in system settings structure
    :return:        201 on success, 406 on settings exists
    """
    # Remove id as it's created automatically
    if "id" in settingsDetails:
        del settingsDetails["id"]

    # Does the settings entry exists for given git username?
    s = (
        db.session.query(Systemsettings).filter(Systemsettings.username == settingsDetails["username"]).one_or_none()
    )

    if s is None:
        schema = SystemsettingsSchema()
        new_entry = schema.load(settingsDetails, session=db.session)
        t = bytes(new_entry.token, 'ascii')
        new_entry.token = encrypt(t, K).decode('ascii')
        db.session.add(new_entry)
        db.session.commit()

        return make_response(f"Created system settings for {new_entry.username}", 200)

    # Otherwise, it already exists, that's an error
    return abort(406, "System settings already exists")


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

    # Fetch entry from db?
    s = db.session.query(Systemsettings).filter(Systemsettings.id == oid).one_or_none()

    if s is not None:
        settingsDetails['id'] = oid
        schema = SystemsettingsSchema()
        update_settings = schema.load(settingsDetails, session=db.session)
        # Encrypt token
        t = bytes(update_settings.token, 'ascii')
        update_settings.token = encrypt(t, K).decode('ascii')
        db.session.merge(update_settings)
        db.session.commit()

        # return the updated settings in the response
        data = schema.dump(update_settings)
        return make_response(f"{oid} - system settings updated successfully deleted", 200)

    # otherwise, nope, deployment doesn't exist, so that's an error
    return abort(404, f"System settings {oid} not found")


def delete(oid):
    """
    Deletes a system settings from list.

    :param id: oid of the system settings to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does entry exist?
    settings_to_del = db.session.query(Systemsettings).filter(Systemsettings.id == oid).one_or_none()

    print(delete_text(oid))

    if settings_to_del is not None:
        db.session.merge(settings_to_del)
        db.session.commit()

        return make_response(f"System settings {oid} successfully deleted", 200)

    # Otherwise, nope, not found
    return abort(404, f"System settings {oid} not found")


def delete_text(oid):
    return db.session.execute(
        text("DElETE FROM systemsettings WHERE id=:param"),
        {"param": oid}
    )
