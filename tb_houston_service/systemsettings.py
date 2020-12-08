"""
deployments module
supports all the ReST actions for the
system settings collection
"""
from pprint import pformat
from typing import Final

from cryptography.fernet import Fernet
from flask import make_response, abort

from config import db, app
from models import Systemsettings, SystemsettingsSchema
from tb_houston_service.extendedSchemas import ExtendedSystemsettingsSchema

# db hash key
K: Final[bytes] = Fernet.generate_key()


def read_all():
    """
    Gets the complete lists of system settings
    :return:        json string of list of system settings
    """
    # Create the list of system settings from our data
    settings = db.session.query(Systemsettings).order_by(Systemsettings.id).all()
    app.logger.debug(pformat(settings))
    # Serialize the data for the response
    settings_schema = ExtendedSystemsettingsSchema(many=True)
    data = settings_schema.dump(settings)
    return data, 200


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
        s['token'] = decrypt(s['token'], K) if s['token'] is not None else s['token']
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
        db.session.query(Systemsettings)
            .filter(Systemsettings.username == settingsDetails["username"])
            .one_or_none()
    )

    if s is None:
        schema = SystemsettingsSchema()
        new_entry = schema.load(settingsDetails, session=db.session)
        new_entry['token'] = encrypt(new_entry['token'], K) if new_entry['token'] is not None else new_entry['token']
        db.session.add(new_entry)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_entry)

        return data, 201

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
        update_settings['token'] = encrypt(update_settings['token'], K) if update_settings['token'] is not None else \
            update_settings['token']
        db.session.merge(update_settings)
        db.session.commit()

        # return the updated settings in the response
        data = schema.dump(update_settings)
        return data, 200

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

    if settings_to_del is not None:
        db.session.merge(settings_to_del)
        db.session.commit()

        return make_response(f"System settings {oid} successfully deleted", 200)

    # Otherwise, nope, not found
    return abort(404, f"System settings {oid} not found")


def encrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(token)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)
