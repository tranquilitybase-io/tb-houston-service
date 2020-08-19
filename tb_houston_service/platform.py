"""
This is the deployments module and supports all the ReST actions for the
platform collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import Platform, PlatformSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/platform
    with the complete lists of Platforms 

    :return:        json string of list of Platforms 
    """

    # Create the list of Platforms from our data
    platform = db.session.query(Platform).order_by(Platform.id).all()
    app.logger.debug(pformat(platform))
    # Serialize the data for the response
    platform_schema = PlatformSchema(many=True)
    data = platform_schema.dump(platform)
    return data


def read_one(id):
    """
    This function responds to a request for /platform/{id}
    with one matching platform from Platforms

    :param application:   id of platform to find
    :return:              platform matching id
    """

    platform = db.session.query(Platform).filter(Platform.id == id).one_or_none()

    if platform is not None:
        # Serialize the data for the response
        platform_schema = PlatformSchema()
        data = platform_schema.dump(platform)
        return data
    else:
        abort(404, "Platform with id {id} not found".format(id=id))

def read_keyValues():
    """
    This function responds to a request for /keyValues/platform
    with the complete lists of Platforms 

    :return:        json string of list of Platforms 
    """

    # Create the list of Platforms from our data
    platform = db.session.query(Platform).order_by(Platform.id).all()
    app.logger.debug(pformat(platform))
    # Serialize the data for the response
    platform_schema = PlatformSchema(many=True)
    data = platform_schema.dump(platform)
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = d.get("id")
        keyValuePair["value"] = d.get("value")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues



def create(platformDetails):
    """
    This function creates a new platform in the platform list
    based on the passed in platform data

    :param platform: platform to create in platform structure
    :return:        201 on success, 406 on platform exists
    """
    # Remove id as it's created automatically
    if 'id' in platformDetails:
        del platformDetails['id']
    # Does the platform exist already?
    existing_platform = db.session.query(Platform).filter(Platform.value == platformDetails["value"]).one_or_none()

    if existing_platform is None:
        schema = PlatformSchema()
        new_platform = schema.load(platformDetails, session=db.session)
        db.session.add(new_platform)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_platform)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"Platform already exists")


def update(id, platformDetails):
    """
    This function updates an existing platform in the platform list

    :param id:    id of the platform to update in the platform list
    :param platform:   platform to update
    :return:       updated platform
    """

    app.logger.debug(pformat(platformDetails))

    if platformDetails["id"] != id:
        abort(400, f"Key mismatch in path and body")

    # Does the platform exist in platform list?
    existing_platform = db.session.query(Platform).filter(Platform.id == id).one_or_none()

    # Does platform exist?

    if existing_platform is not None:
        schema = PlatformSchema()
        update_platform = schema.load(platformDetails, session=db.session)
        update_platform.id = platformDetails["id"]

        db.session.merge(update_platform)
        db.session.commit()

        # return the updted platform in the response
        data = schema.dump(update_platform)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Platform not found")


def delete(id):
    """
    This function deletes a Platform from the Platform list

    :param id: id of the Platform to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the platform to delete exist?
    existing_platform = db.session.query(Platform).filter(Platform.id == id).one_or_none()

    # if found?
    if existing_platform is not None:
        db.session.delete(existing_platform)
        db.session.commit()

        return make_response(f"Platform {id} successfully deleted", 200)

    # Otherwise, nope, platform to delete not found
    else:
        abort(404, f"Platform {id} not found")
